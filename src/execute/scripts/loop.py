#!/usr/bin/env python3
"""Optional thin helper for plan-driven execute/verify loops.

This script stays intentionally dumb:

- the plan file remains the canonical task record
- the external runner stays explicit and non-interactive
- helper logs are supporting evidence only
- the helper never writes canonical task state itself
- the helper never guesses the latest plan or parses model prose for verdicts
- the execute and verify skill contracts remain the workflow source of truth;
  this helper only standardizes loop control, exit-code handling, and
  machine-readable events

The external runner contract is:

    <runner> execute <plan-path>
    <runner> verify <plan-path>

When `verify` runs against the explicit plan path, it must persist the
plan-driven review back into that same plan file.

`verify` must return:

- `0` for pass
- `10` for pass with risks
- `20` for fail

Any other non-zero exit code is treated as runner failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_PASS_WITH_RISKS_CODE = 10
DEFAULT_FAIL_CODE = 20
PROGRESS_PREFIX = "- ["


@dataclass
class PlanState:
    path: str
    total_milestones: int
    completed_milestones: int
    remaining_milestones: int
    next_milestone: str | None
    blocked: bool
    blockers: list[str]
    digest: str


@dataclass
class RunnerResult:
    label: str
    command: list[str]
    exit_code: int
    stdout_log: str
    stderr_log: str


def script_path() -> Path:
    return Path(__file__).resolve()


def current_skill_root() -> Path:
    skill_root = script_path().parents[1]
    if skill_root.name != "execute":
        raise RuntimeError("loop.py must live under an execute skill directory")
    return skill_root


def skills_root() -> Path:
    skill_root = current_skill_root()
    parent = skill_root.parent
    grandparent = parent.parent
    if parent.name == "src":
        return parent
    if parent.name == "skills" and grandparent.name == ".agents":
        return parent
    raise RuntimeError(
        "loop.py must live under src/execute/ or .agents/skills/execute/"
    )


def repo_root() -> Path:
    root = skills_root()
    if root.name == "src":
        return root.parent
    return root.parent.parent


def repo_relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(repo_root()))
    except ValueError:
        return str(path)


def build_parser() -> argparse.ArgumentParser:
    display_script = repo_relative_path(script_path())
    parser = argparse.ArgumentParser(
        description=(
            "Run a thin, file-backed execute/verify loop against one explicit "
            "plan path using an explicit external runner."
        ),
        epilog=(
            "Example:\n"
            f"  python3 {display_script} --dry-run \\\n"
            "      --plan plans/YYYY-MM-DD-short-task-slug.md \\\n"
            "      --provider-command \"./bin/run-skill\"\n\n"
            "The external runner must be non-interactive and accept:\n"
            "  ./bin/run-skill execute <plan>\n"
            "  ./bin/run-skill verify <plan>\n"
            "In plan-driven work, verify must persist its findings back into\n"
            "the same plan file; helper logs are supporting evidence only.\n\n"
            "Expected helper exit codes:\n"
            "  0 = completed plan (strict final review when continuous mode is enabled)\n"
            "  1 = blocked plan, invalid plan state, unacceptable verify verdict, or missing execute/verify plan update\n"
            "  2 = invalid helper usage\n"
            "  3 = external runner failure\n"
            "  4 = max iterations reached"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--plan",
        required=True,
        help="Explicit plan file to drive the loop. The helper never guesses one.",
    )
    parser.add_argument(
        "--provider-command",
        required=True,
        help=(
            "Quoted command string for the external non-interactive runner. "
            "The helper appends `execute <plan>` or `verify <plan>`."
        ),
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=25,
        help="Hard stop after this many execute/verify cycles. Default: 25.",
    )
    parser.add_argument(
        "--continue-after-fail",
        action="store_true",
        help=(
            "Keep looping after a repairable verify=fail by letting execute "
            "consume the updated plan, and require a strict final verify=pass "
            "before success."
        ),
    )
    parser.add_argument(
        "--allow-pass-with-risks",
        action="store_true",
        help=(
            "Continue after slice-level verify returns pass-with-risks. "
            "Strict final review still requires verify=pass."
        ),
    )
    parser.add_argument(
        "--pass-with-risks-code",
        type=int,
        default=DEFAULT_PASS_WITH_RISKS_CODE,
        help=(
            "Exit code that the external runner uses for verify=pass with risks. "
            f"Default: {DEFAULT_PASS_WITH_RISKS_CODE}."
        ),
    )
    parser.add_argument(
        "--fail-code",
        type=int,
        default=DEFAULT_FAIL_CODE,
        help=(
            "Exit code that the external runner uses for verify=fail. "
            f"Default: {DEFAULT_FAIL_CODE}."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the first execute/verify commands and current plan state without running them.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Required for real runs because the helper triggers stateful work.",
    )
    return parser


def emit(event: dict[str, object]) -> None:
    print(json.dumps(event, sort_keys=True), flush=True)


def emit_stop(
    reason: str,
    *,
    final_outcome: str,
    **details: object,
) -> None:
    event: dict[str, object] = {
        "event": "stop",
        "reason": reason,
        "final_outcome": final_outcome,
    }
    event.update(details)
    emit(event)


def emit_phase(
    phase: str,
    *,
    status: str,
    iteration: int,
    command: list[str],
    label: str,
    source: str | None = None,
    state_before: dict[str, object] | None = None,
    state_after: dict[str, object] | None = None,
    result: dict[str, object] | None = None,
    verification_verdict: str | None = None,
) -> None:
    event: dict[str, object] = {
        "event": "phase",
        "phase": phase,
        "status": status,
        "iteration": iteration,
        "label": label,
        "command": command,
    }
    if source is not None:
        event["source"] = source
    if state_before is not None:
        event["state_before"] = state_before
    if state_after is not None:
        event["state_after"] = state_after
    if result is not None:
        event["result"] = result
    if verification_verdict is not None:
        event["verification_verdict"] = verification_verdict
    emit(event)


def diag(message: str) -> None:
    print(f"[loop] {message}", file=sys.stderr, flush=True)


def parse_command(command_text: str) -> list[str]:
    command = shlex.split(command_text)
    if not command:
        raise ValueError("--provider-command must expand to at least one argv token")
    return command


def normalize_none_marker(line: str) -> str:
    return line.lstrip("- ").strip().rstrip(".").lower()


def read_section(text: str, heading: str) -> list[str]:
    target = f"## {heading}"
    lines = text.splitlines()
    in_section = False
    section: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            if line.strip() == target:
                in_section = True
                continue
        if in_section:
            section.append(line)

    if not in_section:
        raise ValueError(f"plan file is missing the {target!r} section")
    return section


def read_plan_state(plan_path: Path) -> PlanState:
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"{plan_path} is not readable: {exc}") from exc

    progress_lines = read_section(text, "Progress")
    milestones: list[tuple[bool, str]] = []
    for raw_line in progress_lines:
        stripped = raw_line.strip()
        if not stripped.startswith(PROGRESS_PREFIX):
            continue
        if not stripped.startswith(("- [ ] ", "- [x] ", "- [X] ")):
            continue
        done = stripped[3].lower() == "x"
        label = stripped[6:].strip()
        milestones.append((done, label))

    if not milestones:
        raise ValueError(
            f"{plan_path} must have at least one '- [ ]' or '- [x]' item in "
            "## Progress; use the shipped plan template and keep milestone "
            "state as checkbox items"
        )

    blockers_section = read_section(text, "Blockers")
    blockers: list[str] = []
    blocker_bullets = 0
    for raw_line in blockers_section:
        stripped = raw_line.strip()
        if not stripped:
            continue
        if not stripped.startswith("- "):
            continue
        blocker_bullets += 1
        if normalize_none_marker(stripped) in {"none", "none currently", "n/a"}:
            continue
        blockers.append(stripped)

    if blocker_bullets == 0:
        raise ValueError(
            f"{plan_path} must have at least one '- ...' item in ## Blockers; "
            "use '- None currently.' when nothing blocks the next safe execute slice"
        )

    total = len(milestones)
    completed = sum(1 for done, _label in milestones if done)
    remaining = total - completed
    next_milestone = next((label for done, label in milestones if not done), None)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return PlanState(
        path=str(plan_path),
        total_milestones=total,
        completed_milestones=completed,
        remaining_milestones=remaining,
        next_milestone=next_milestone,
        blocked=bool(blockers),
        blockers=blockers,
        digest=digest,
    )


def run_runner(
    base_command: list[str],
    mode: str,
    plan_path: Path,
    log_root: Path,
    iteration: int,
    *,
    label: str | None = None,
) -> RunnerResult:
    command = [*base_command, mode, str(plan_path)]
    log_label = label or mode
    diag(f"iteration {iteration}: running {' '.join(shlex.quote(part) for part in command)}")
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"failed to start external runner: {exc}") from exc

    stdout_log = log_root / f"{iteration:02d}-{log_label}.stdout.log"
    stderr_log = log_root / f"{iteration:02d}-{log_label}.stderr.log"
    stdout_log.write_text(completed.stdout, encoding="utf-8")
    stderr_log.write_text(completed.stderr, encoding="utf-8")

    return RunnerResult(
        label=log_label,
        command=command,
        exit_code=completed.returncode,
        stdout_log=str(stdout_log),
        stderr_log=str(stderr_log),
    )


def verify_verdict(exit_code: int, pass_with_risks_code: int, fail_code: int) -> str:
    if exit_code == 0:
        return "pass"
    if exit_code == pass_with_risks_code:
        return "pass_with_risks"
    if exit_code == fail_code:
        return "fail"
    return "runner_error"


def stop_for_invalid_plan_state(
    *,
    reason: str,
    plan_path: Path,
    error: ValueError,
    iteration: int | None = None,
    state_before: PlanState | None = None,
    execute_result: RunnerResult | None = None,
    verify_result: RunnerResult | None = None,
) -> int:
    event: dict[str, object] = {
        "plan": str(plan_path),
        "error": str(error),
    }
    if iteration is not None:
        event["iteration"] = iteration
    if state_before is not None:
        event["state_before"] = state_before.__dict__
    if execute_result is not None:
        event["execute"] = execute_result.__dict__
    if verify_result is not None:
        event["verify"] = verify_result.__dict__
    emit_stop(reason, final_outcome="invalid_plan_state", **event)
    return 1


def maybe_run_final_review(
    *,
    base_command: list[str],
    plan_path: Path,
    log_root: Path,
    iteration: int,
    pass_with_risks_code: int,
    fail_code: int,
    continue_after_fail: bool,
    source: str,
) -> int | None:
    try:
        state_before = read_plan_state(plan_path)
    except ValueError as exc:
        return stop_for_invalid_plan_state(
            reason="invalid_plan_before_final_verify",
            plan_path=plan_path,
            error=exc,
            iteration=iteration,
        )

    try:
        final_verify_command = [*base_command, "verify", str(plan_path)]
        emit_phase(
            "final_verify",
            status="start",
            iteration=iteration,
            command=final_verify_command,
            label="final-verify",
            source=source,
            state_before=state_before.__dict__,
        )
        verify_result = run_runner(
            base_command,
            "verify",
            plan_path,
            log_root,
            iteration,
            label="final-verify",
        )
    except RuntimeError as exc:
        emit_stop(
            "final_verify_runner_failed_to_start",
            final_outcome="runner_error",
            iteration=iteration,
            source=source,
            error=str(exc),
        )
        return 3

    try:
        state_after = read_plan_state(plan_path)
    except ValueError as exc:
        return stop_for_invalid_plan_state(
            reason="invalid_plan_after_final_verify",
            plan_path=plan_path,
            error=exc,
            iteration=iteration,
            state_before=state_before,
            verify_result=verify_result,
        )

    plan_changed = state_before.digest != state_after.digest
    verdict = verify_verdict(
        verify_result.exit_code,
        pass_with_risks_code,
        fail_code,
    )
    emit_phase(
        "final_verify",
        status="end",
        iteration=iteration,
        command=verify_result.command,
        label=verify_result.label,
        source=source,
        state_before=state_before.__dict__,
        state_after=state_after.__dict__,
        result=verify_result.__dict__,
        verification_verdict=verdict,
    )
    strict_completion = verdict == "pass" and state_after.remaining_milestones == 0
    repairable_follow_up = (
        continue_after_fail
        and not state_after.blocked
        and state_after.remaining_milestones > 0
    )
    stop_reasons: list[str] = []
    if verdict == "runner_error":
        stop_reasons.append("final_verify_runner_error")
    if not plan_changed:
        stop_reasons.append("missing_final_verify_plan_update")
    if state_after.blocked:
        stop_reasons.append("plan_blocked_after_final_verify")
    if not strict_completion and not repairable_follow_up:
        if state_after.remaining_milestones == 0 and not state_after.blocked:
            stop_reasons.append("final_review_did_not_reopen_work")
        else:
            stop_reasons.append("strict_final_review_requires_pass")

    status = "completed"
    if repairable_follow_up:
        status = "continue"
    elif stop_reasons:
        status = "stop"

    emit(
        {
            "event": "final_review",
            "iteration": iteration,
            "source": source,
            "status": status,
            "plan_changed": plan_changed,
            "verification_verdict": verdict,
            "stop_reasons": stop_reasons,
            "state_before": state_before.__dict__,
            "state_after": state_after.__dict__,
            "verify": verify_result.__dict__,
        }
    )

    if verdict == "runner_error":
        return 3
    if not plan_changed:
        return 1
    if strict_completion:
        emit_stop(
            "plan_completed_after_final_verify",
            final_outcome="completed_strict",
            iteration=iteration,
            source=source,
            state=state_after.__dict__,
            verify=verify_result.__dict__,
        )
        return 0
    if state_after.blocked:
        emit_stop(
            "plan_blocked_after_final_verify",
            final_outcome="blocked",
            iteration=iteration,
            source=source,
            state=state_after.__dict__,
            verify=verify_result.__dict__,
        )
        return 1
    if repairable_follow_up:
        return None
    emit_stop(
        "strict_final_review_failed",
        final_outcome="incomplete",
        iteration=iteration,
        source=source,
        state=state_after.__dict__,
        verify=verify_result.__dict__,
        verification_verdict=verdict,
    )
    return 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.max_iterations < 1:
        parser.error("--max-iterations must be at least 1")
    if not args.dry_run and not args.yes:
        parser.error("real runs require --yes because they trigger stateful work")

    plan_path = Path(args.plan).expanduser().resolve()
    if not plan_path.is_file():
        parser.error(f"--plan must point to an existing file: {plan_path}")

    try:
        base_command = parse_command(args.provider_command)
        initial_state = read_plan_state(plan_path)
    except ValueError as exc:
        parser.error(str(exc))

    start_event = {
        "event": "start",
        "plan": str(plan_path),
        "provider_command": base_command,
        "initial_state": initial_state.__dict__,
        "max_iterations": args.max_iterations,
        "continue_after_fail": args.continue_after_fail,
        "allow_pass_with_risks": args.allow_pass_with_risks,
    }

    if args.dry_run:
        start_event["dry_run"] = True
        start_event["next_commands"] = {
            "execute": [*base_command, "execute", str(plan_path)],
            "verify": [*base_command, "verify", str(plan_path)],
        }
        emit(start_event)
        return 0 if not initial_state.blocked else 1

    log_root = Path(tempfile.mkdtemp(prefix="loop-"))
    start_event["dry_run"] = False
    start_event["log_root"] = str(log_root)
    emit(start_event)

    if initial_state.blocked:
        emit_stop(
            "plan_blocked_before_loop",
            final_outcome="blocked",
            state=initial_state.__dict__,
        )
        return 1

    if initial_state.remaining_milestones == 0:
        if args.continue_after_fail:
            exit_code = maybe_run_final_review(
                base_command=base_command,
                plan_path=plan_path,
                log_root=log_root,
                iteration=0,
                pass_with_risks_code=args.pass_with_risks_code,
                fail_code=args.fail_code,
                continue_after_fail=args.continue_after_fail,
                source="initial_complete_plan",
            )
            if exit_code is not None:
                return exit_code
        else:
            emit_stop(
                "plan_already_complete",
                final_outcome="completed",
                state=initial_state.__dict__,
            )
            return 0

    for iteration in range(1, args.max_iterations + 1):
        try:
            state_before = read_plan_state(plan_path)
        except ValueError as exc:
            return stop_for_invalid_plan_state(
                reason="invalid_plan_before_execute",
                plan_path=plan_path,
                error=exc,
                iteration=iteration,
            )
        if state_before.blocked:
            emit_stop(
                "plan_blocked_before_execute",
                final_outcome="blocked",
                iteration=iteration,
                state=state_before.__dict__,
            )
            return 1

        if state_before.remaining_milestones == 0:
            if args.continue_after_fail:
                exit_code = maybe_run_final_review(
                    base_command=base_command,
                    plan_path=plan_path,
                    log_root=log_root,
                    iteration=iteration,
                    pass_with_risks_code=args.pass_with_risks_code,
                    fail_code=args.fail_code,
                    continue_after_fail=args.continue_after_fail,
                    source="completed_before_execute",
                )
                if exit_code is not None:
                    return exit_code
                continue
            emit_stop(
                "plan_completed_before_execute",
                final_outcome="completed",
                iteration=iteration,
                state=state_before.__dict__,
            )
            return 0

        try:
            execute_command = [*base_command, "execute", str(plan_path)]
            emit_phase(
                "execute",
                status="start",
                iteration=iteration,
                command=execute_command,
                label="execute",
                state_before=state_before.__dict__,
            )
            execute_result = run_runner(base_command, "execute", plan_path, log_root, iteration)
        except RuntimeError as exc:
            emit_stop(
                "execute_runner_failed_to_start",
                final_outcome="runner_error",
                iteration=iteration,
                error=str(exc),
            )
            return 3

        try:
            state_after_execute = read_plan_state(plan_path)
        except ValueError as exc:
            return stop_for_invalid_plan_state(
                reason="invalid_plan_after_execute",
                plan_path=plan_path,
                error=exc,
                iteration=iteration,
                state_before=state_before,
                execute_result=execute_result,
            )
        plan_changed = state_before.digest != state_after_execute.digest
        emit_phase(
            "execute",
            status="end",
            iteration=iteration,
            command=execute_result.command,
            label=execute_result.label,
            state_before=state_before.__dict__,
            state_after=state_after_execute.__dict__,
            result=execute_result.__dict__,
        )

        if execute_result.exit_code != 0:
            emit(
                {
                    "event": "iteration",
                    "iteration": iteration,
                    "status": "execute_failed",
                    "plan_changed": plan_changed,
                    "state_before": state_before.__dict__,
                    "state_after_execute": state_after_execute.__dict__,
                    "execute": execute_result.__dict__,
                }
            )
            emit_stop(
                "execute_runner_failed",
                final_outcome="runner_error",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                execute=execute_result.__dict__,
            )
            return 3

        try:
            emit_phase(
                "verify",
                status="start",
                iteration=iteration,
                command=[*base_command, "verify", str(plan_path)],
                label="verify",
                state_before=state_after_execute.__dict__,
            )
            verify_result = run_runner(base_command, "verify", plan_path, log_root, iteration)
        except RuntimeError as exc:
            emit_stop(
                "verify_runner_failed_to_start",
                final_outcome="runner_error",
                iteration=iteration,
                error=str(exc),
                execute=execute_result.__dict__,
            )
            return 3

        try:
            state_after_verify = read_plan_state(plan_path)
        except ValueError as exc:
            return stop_for_invalid_plan_state(
                reason="invalid_plan_after_verify",
                plan_path=plan_path,
                error=exc,
                iteration=iteration,
                state_before=state_before,
                execute_result=execute_result,
                verify_result=verify_result,
            )
        verify_plan_changed = state_after_execute.digest != state_after_verify.digest
        verdict = verify_verdict(
            verify_result.exit_code,
            args.pass_with_risks_code,
            args.fail_code,
        )
        emit_phase(
            "verify",
            status="end",
            iteration=iteration,
            command=verify_result.command,
            label=verify_result.label,
            state_before=state_after_execute.__dict__,
            state_after=state_after_verify.__dict__,
            result=verify_result.__dict__,
            verification_verdict=verdict,
        )
        completion_review = (
            args.continue_after_fail and state_after_execute.remaining_milestones == 0
        )
        acceptable = verdict == "pass" or (
            verdict == "pass_with_risks"
            and args.allow_pass_with_risks
            and not completion_review
        )
        repairable_failure = (
            args.continue_after_fail
            and verdict in {"fail", "pass_with_risks"}
            and not state_after_verify.blocked
            and state_after_verify.remaining_milestones > 0
            and (verdict == "fail" or completion_review)
        )
        stop_reasons: list[str] = []
        if verdict == "runner_error":
            stop_reasons.append("verify_runner_error")
        if not plan_changed:
            stop_reasons.append("missing_execute_plan_update")
        if not verify_plan_changed:
            stop_reasons.append("missing_verify_plan_update")
        if state_after_verify.blocked:
            stop_reasons.append("plan_blocked_after_verify")
        if (
            completion_review
            and verdict in {"fail", "pass_with_risks"}
            and not state_after_verify.blocked
            and state_after_verify.remaining_milestones == 0
        ):
            stop_reasons.append("final_review_did_not_reopen_work")
        elif (
            args.continue_after_fail
            and verdict == "fail"
            and not state_after_verify.blocked
            and state_after_verify.remaining_milestones == 0
        ):
            stop_reasons.append("verify_fail_did_not_reopen_work")
        elif not acceptable and not repairable_failure:
            stop_reasons.append("unacceptable_verify_verdict")
        status = "continue"
        if stop_reasons:
            status = "stop"
        elif (
            completion_review
            and verdict == "pass"
            and state_after_verify.remaining_milestones == 0
        ):
            status = "completed"
        elif (
            state_after_verify.remaining_milestones == 0
            and not args.continue_after_fail
        ):
            status = "completed"

        emit(
            {
                "event": "iteration",
                "iteration": iteration,
                "status": status,
                "plan_changed": plan_changed,
                "verify_plan_changed": verify_plan_changed,
                "completion_review": completion_review,
                "verification_verdict": verdict,
                "stop_reasons": stop_reasons,
                "state_before": state_before.__dict__,
                "state_after_execute": state_after_execute.__dict__,
                "state_after_verify": state_after_verify.__dict__,
                "execute": execute_result.__dict__,
                "verify": verify_result.__dict__,
            }
        )

        if verdict == "runner_error":
            emit_stop(
                "verify_runner_error",
                final_outcome="runner_error",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                state_after_verify=state_after_verify.__dict__,
                execute=execute_result.__dict__,
                verify=verify_result.__dict__,
            )
            return 3
        if not plan_changed:
            emit_stop(
                "missing_execute_plan_update",
                final_outcome="incomplete",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                state_after_verify=state_after_verify.__dict__,
                execute=execute_result.__dict__,
                verify=verify_result.__dict__,
            )
            return 1
        if not verify_plan_changed:
            emit_stop(
                "missing_verify_plan_update",
                final_outcome="incomplete",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                state_after_verify=state_after_verify.__dict__,
                execute=execute_result.__dict__,
                verify=verify_result.__dict__,
            )
            return 1
        if state_after_verify.blocked:
            emit_stop(
                "plan_blocked_after_verify",
                final_outcome="blocked",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                state_after_verify=state_after_verify.__dict__,
                execute=execute_result.__dict__,
                verify=verify_result.__dict__,
            )
            return 1
        if repairable_failure:
            continue
        if not acceptable:
            stop_reason = "unacceptable_verify_verdict"
            if stop_reasons:
                stop_reason = stop_reasons[-1]
            emit_stop(
                stop_reason,
                final_outcome="incomplete",
                iteration=iteration,
                state_before=state_before.__dict__,
                state_after_execute=state_after_execute.__dict__,
                state_after_verify=state_after_verify.__dict__,
                execute=execute_result.__dict__,
                verify=verify_result.__dict__,
                verification_verdict=verdict,
            )
            return 1
        if (
            completion_review
            and verdict == "pass"
            and state_after_verify.remaining_milestones == 0
        ):
            emit_stop(
                "plan_completed_after_verify",
                final_outcome="completed_strict",
                iteration=iteration,
                state=state_after_verify.__dict__,
                verify=verify_result.__dict__,
            )
            return 0
        if state_after_verify.remaining_milestones == 0 and not args.continue_after_fail:
            emit_stop(
                "plan_completed_after_verify",
                final_outcome="completed",
                iteration=iteration,
                state=state_after_verify.__dict__,
                verify=verify_result.__dict__,
            )
            return 0

    try:
        final_state = read_plan_state(plan_path)
    except ValueError as exc:
        return stop_for_invalid_plan_state(
            reason="invalid_plan_after_max_iterations",
            plan_path=plan_path,
            error=exc,
        )
    emit_stop(
        "max_iterations_reached",
        final_outcome="max_iterations",
        state=final_state.__dict__,
        max_iterations=args.max_iterations,
    )
    return 4


if __name__ == "__main__":
    sys.exit(main())
