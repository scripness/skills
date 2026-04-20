#!/usr/bin/env python3
"""Optional thin helper for plan-driven execute/verify loops.

This script stays intentionally dumb:

- the plan file remains the durable state
- the external runner stays explicit and non-interactive
- the helper never guesses the latest plan or parses model prose for verdicts

The external runner contract is:

    <runner> execute <plan-path>
    <runner> verify <plan-path>

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
    command: list[str]
    exit_code: int
    stdout_log: str
    stderr_log: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a thin, file-backed execute/verify loop against one explicit "
            "plan path using an explicit external runner."
        ),
        epilog=(
            "Example:\n"
            "  python3 src/execute/scripts/plan_loop.py --dry-run \\\n"
            "      --plan plans/YYYY-MM-DD-short-task-slug.md \\\n"
            "      --provider-command \"./bin/run-skill\"\n\n"
            "The external runner must be non-interactive and accept:\n"
            "  ./bin/run-skill execute <plan>\n"
            "  ./bin/run-skill verify <plan>\n\n"
            "Expected helper exit codes:\n"
            "  0 = clean stop or completed plan\n"
            "  1 = blocked plan, invalid plan state, unacceptable verify verdict, or missing plan update\n"
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
        "--allow-pass-with-risks",
        action="store_true",
        help="Continue the loop when verify returns pass-with-risks.",
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


def diag(message: str) -> None:
    print(f"[plan-loop] {message}", file=sys.stderr, flush=True)


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
            f"{plan_path} must have at least one '- [ ]' or '- [x]' item in ## Progress"
        )

    blockers_section = read_section(text, "Blockers")
    blockers: list[str] = []
    for raw_line in blockers_section:
        stripped = raw_line.strip()
        if not stripped:
            continue
        if normalize_none_marker(stripped) in {"none", "none currently", "n/a"}:
            continue
        blockers.append(stripped)

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
) -> RunnerResult:
    command = [*base_command, mode, str(plan_path)]
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

    stdout_log = log_root / f"{iteration:02d}-{mode}.stdout.log"
    stderr_log = log_root / f"{iteration:02d}-{mode}.stderr.log"
    stdout_log.write_text(completed.stdout, encoding="utf-8")
    stderr_log.write_text(completed.stderr, encoding="utf-8")

    return RunnerResult(
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
        "event": "stop",
        "reason": reason,
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
    emit(event)
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

    log_root = Path(tempfile.mkdtemp(prefix="plan-loop-"))
    start_event["dry_run"] = False
    start_event["log_root"] = str(log_root)
    emit(start_event)

    if initial_state.blocked:
        emit(
            {
                "event": "stop",
                "reason": "plan_blocked_before_loop",
                "state": initial_state.__dict__,
            }
        )
        return 1

    if initial_state.remaining_milestones == 0:
        emit(
            {
                "event": "stop",
                "reason": "plan_already_complete",
                "state": initial_state.__dict__,
            }
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
            emit(
                {
                    "event": "stop",
                    "reason": "plan_blocked_before_execute",
                    "iteration": iteration,
                    "state": state_before.__dict__,
                }
            )
            return 1

        if state_before.remaining_milestones == 0:
            emit(
                {
                    "event": "stop",
                    "reason": "plan_completed_before_execute",
                    "iteration": iteration,
                    "state": state_before.__dict__,
                }
            )
            return 0

        try:
            execute_result = run_runner(base_command, "execute", plan_path, log_root, iteration)
        except RuntimeError as exc:
            emit(
                {
                    "event": "stop",
                    "reason": "execute_runner_failed_to_start",
                    "iteration": iteration,
                    "error": str(exc),
                }
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
            return 3

        try:
            verify_result = run_runner(base_command, "verify", plan_path, log_root, iteration)
        except RuntimeError as exc:
            emit(
                {
                    "event": "stop",
                    "reason": "verify_runner_failed_to_start",
                    "iteration": iteration,
                    "error": str(exc),
                    "execute": execute_result.__dict__,
                }
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
        verdict = verify_verdict(
            verify_result.exit_code,
            args.pass_with_risks_code,
            args.fail_code,
        )
        acceptable = verdict == "pass" or (
            verdict == "pass_with_risks" and args.allow_pass_with_risks
        )

        emit(
            {
                "event": "iteration",
                "iteration": iteration,
                "status": "continue" if acceptable else "stop",
                "plan_changed": plan_changed,
                "verification_verdict": verdict,
                "state_before": state_before.__dict__,
                "state_after_execute": state_after_execute.__dict__,
                "state_after_verify": state_after_verify.__dict__,
                "execute": execute_result.__dict__,
                "verify": verify_result.__dict__,
            }
        )

        if verdict == "runner_error":
            return 3
        if not plan_changed:
            return 1
        if state_after_verify.blocked:
            return 1
        if not acceptable:
            return 1
        if state_after_verify.remaining_milestones == 0:
            return 0

    try:
        final_state = read_plan_state(plan_path)
    except ValueError as exc:
        return stop_for_invalid_plan_state(
            reason="invalid_plan_after_max_iterations",
            plan_path=plan_path,
            error=exc,
        )
    emit(
        {
            "event": "stop",
            "reason": "max_iterations_reached",
            "state": final_state.__dict__,
            "max_iterations": args.max_iterations,
        }
    )
    return 4


if __name__ == "__main__":
    sys.exit(main())
