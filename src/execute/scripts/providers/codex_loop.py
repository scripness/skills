#!/usr/bin/env python3
"""Optional Codex convenience wrapper around the generic plan loop helper.

This script has two modes:

- user mode: a short daily command that invokes the generic `loop.py` helper
  with Codex-oriented defaults
- runner mode: a low-level `execute <plan>` / `verify <plan>` adapter that the
  generic helper can call non-interactively

The generic `loop.py` contract remains the provider-agnostic source of truth.
This file is an optional accelerator for working on the current repo with the
local Codex CLI. The shipped skill contracts remain the workflow source of
truth; this wrapper only changes how those skills are invoked and how verify
verdicts are transported back to the generic helper.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


DEFAULT_CODEX_COMMAND = "codex exec --yolo --color never --ephemeral"
DEFAULT_PASS_WITH_RISKS_CODE = 10
DEFAULT_FAIL_CODE = 20


def script_path() -> Path:
    path = Path(__file__)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def current_skill_root() -> Path:
    skill_root = script_path().parents[2]
    if skill_root.name != "execute":
        raise RuntimeError(
            "codex_loop.py must live under an execute skill directory"
        )
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
        "codex_loop.py must live under src/execute/ or .agents/skills/execute/"
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


def skill_path(skill_name: str, *parts: str) -> Path:
    path = skills_root() / skill_name
    for part in parts:
        path /= part
    return path


def generic_loop_path() -> Path:
    return current_skill_root() / "scripts" / "loop.py"


def this_script_path() -> Path:
    return script_path()


def parse_command(command_text: str) -> list[str]:
    command = shlex.split(command_text)
    if not command:
        raise ValueError("command text must expand to at least one argv token")
    return command


def codex_base_command(codex_command_text: str) -> list[str]:
    command = parse_command(codex_command_text)
    if "-C" in command or "--cd" in command:
        return command
    return [*command, "-C", str(repo_root())]


def execute_prompt(plan_path: Path) -> str:
    execute_skill = repo_relative_path(skill_path("execute", "SKILL.md"))
    return textwrap.dedent(
        f"""\
        Follow `{execute_skill}` as the workflow source of truth.

        This runner is only providing invocation context for one plan-driven
        execute call. If this prompt and the skill contract ever disagree, the
        skill contract wins.

        Invocation-specific constraints:
        - explicit plan path: `{plan_path}`
        - plan-driven mode
        - execute exactly one bounded slice
        - update that same plan file in place
        - stop after that one slice

        Read `AGENTS.md`, the relevant `specs/*`, `{execute_skill}`,
        and the explicit plan at `{plan_path}`. Read code, docs, and tests as
        required by that skill contract. Do not turn this execute invocation
        into adversarial verification.
        """
    )


def verify_prompt(plan_path: Path) -> str:
    verify_skill = repo_relative_path(skill_path("verify", "SKILL.md"))
    execute_skill = repo_relative_path(skill_path("execute", "SKILL.md"))
    plan_template = repo_relative_path(
        skill_path("plan", "assets", "plan-template.md")
    )
    return textwrap.dedent(
        f"""\
        Follow `{verify_skill}` as the workflow source of truth.

        This runner is only providing invocation context and transport
        constraints for one plan-driven verify call. If this prompt and the
        skill contract ever disagree, the skill contract wins.

        Invocation-specific constraints:
        - explicit plan path: `{plan_path}`
        - keep that same plan file as the canonical task record
        - return JSON only matching the provided schema

        Read `AGENTS.md`, the relevant `specs/*`, `{verify_skill}`,
        `{execute_skill}`, `{plan_template}`, and the
        explicit plan at `{plan_path}`.
        """
    )


def run_codex_execute(plan_path: Path, codex_command_text: str) -> int:
    command = codex_base_command(codex_command_text)
    completed = subprocess.run(
        [*command, "-"],
        input=execute_prompt(plan_path),
        text=True,
    )
    return completed.returncode


def run_codex_verify(
    plan_path: Path,
    codex_command_text: str,
    *,
    pass_with_risks_code: int,
    fail_code: int,
) -> int:
    command = codex_base_command(codex_command_text)
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "verdict": {
                "type": "string",
                "enum": ["pass", "pass_with_risks", "fail"],
            },
            "summary": {"type": "string"},
        },
        "required": ["verdict", "summary"],
    }

    with tempfile.TemporaryDirectory(prefix="codex-loop-verify-") as tmpdir:
        schema_path = Path(tmpdir) / "verify_schema.json"
        output_path = Path(tmpdir) / "verify.json"
        schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")

        completed = subprocess.run(
            [
                *command,
                "--output-schema",
                str(schema_path),
                "-o",
                str(output_path),
                "-",
            ],
            input=verify_prompt(plan_path),
            text=True,
        )
        if completed.returncode != 0:
            return completed.returncode

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        verdict = payload["verdict"]
        if verdict == "pass":
            return 0
        if verdict == "pass_with_risks":
            return pass_with_risks_code
        return fail_code


def build_user_parser() -> argparse.ArgumentParser:
    display_script = repo_relative_path(this_script_path())
    display_loop = repo_relative_path(generic_loop_path())
    parser = argparse.ArgumentParser(
        description=(
            "Run the generic plan loop helper with local Codex defaults."
        ),
        epilog=(
            "Examples:\n"
            f"  python3 {display_script} \\\n"
            "      --plan plans/YYYY-MM-DD-short-task-slug.md\n\n"
            f"  python3 {display_script} \\\n"
            "      --dry-run \\\n"
            "      --plan plans/YYYY-MM-DD-short-task-slug.md\n\n"
            "Defaults in user mode:\n"
            "  - real runs imply `--yes`\n"
            "  - continuous repair mode is on unless `--no-continue-after-fail`\n"
            "  - provider command points back to this file in hidden `--runner` mode\n"
            "  - internal Codex calls default to:\n"
            f"      {DEFAULT_CODEX_COMMAND}\n\n"
            "Here `--yolo` is shorthand for dangerously bypassing approvals and\n"
            "sandboxing in the local Codex CLI. Override `--codex-command` if\n"
            "you want a different Codex invocation."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--plan",
        required=True,
        help="Explicit plan file to run through the generic loop helper.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the resolved generic loop command without stateful work.",
    )
    parser.add_argument(
        "--no-continue-after-fail",
        action="store_true",
        help="Disable the default continuous repair mode.",
    )
    parser.add_argument(
        "--allow-pass-with-risks",
        action="store_true",
        help="Allow slice-level `verify=pass_with_risks` in the generic helper.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        help="Override the generic helper's max-iterations value.",
    )
    parser.add_argument(
        "--pass-with-risks-code",
        type=int,
        default=DEFAULT_PASS_WITH_RISKS_CODE,
        help=(
            "Exit code that the internal runner uses for `verify=pass_with_risks`. "
            f"Default: {DEFAULT_PASS_WITH_RISKS_CODE}."
        ),
    )
    parser.add_argument(
        "--fail-code",
        type=int,
        default=DEFAULT_FAIL_CODE,
        help=(
            "Exit code that the internal runner uses for `verify=fail`. "
            f"Default: {DEFAULT_FAIL_CODE}."
        ),
    )
    parser.add_argument(
        "--provider-command",
        help=(
            "Override the default internal runner command. By default this file "
            "runs itself in hidden `--runner` mode."
        ),
    )
    parser.add_argument(
        "--codex-command",
        default=DEFAULT_CODEX_COMMAND,
        help=(
            "Quoted Codex command prefix used by the hidden internal runner. "
            f"Default: {DEFAULT_CODEX_COMMAND!r}."
        ),
    )
    parser.add_argument(
        "--loop-command",
        help=(
            "Override the generic loop helper command prefix. By default this "
            f"uses the local `{display_loop}`."
        ),
    )
    return parser


def build_runner_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--runner", action="store_true")
    parser.add_argument(
        "--codex-command",
        default=DEFAULT_CODEX_COMMAND,
    )
    parser.add_argument(
        "--pass-with-risks-code",
        type=int,
        default=DEFAULT_PASS_WITH_RISKS_CODE,
    )
    parser.add_argument(
        "--fail-code",
        type=int,
        default=DEFAULT_FAIL_CODE,
    )
    parser.add_argument("mode", choices=["execute", "verify"])
    parser.add_argument("plan")
    return parser


def wrapper_main(argv: list[str]) -> int:
    parser = build_user_parser()
    args = parser.parse_args(argv)

    loop_command = args.loop_command or shlex.join(
        [sys.executable, str(generic_loop_path())]
    )
    provider_command = args.provider_command or shlex.join(
        [
            sys.executable,
            str(this_script_path()),
            "--runner",
            "--codex-command",
            args.codex_command,
            "--pass-with-risks-code",
            str(args.pass_with_risks_code),
            "--fail-code",
            str(args.fail_code),
        ]
    )

    command = [*parse_command(loop_command), "--plan", args.plan]
    if args.dry_run:
        command.append("--dry-run")
    else:
        command.append("--yes")
    if not args.no_continue_after_fail:
        command.append("--continue-after-fail")
    if args.allow_pass_with_risks:
        command.append("--allow-pass-with-risks")
    if args.max_iterations is not None:
        command.extend(["--max-iterations", str(args.max_iterations)])
    if args.pass_with_risks_code != DEFAULT_PASS_WITH_RISKS_CODE:
        command.extend(["--pass-with-risks-code", str(args.pass_with_risks_code)])
    if args.fail_code != DEFAULT_FAIL_CODE:
        command.extend(["--fail-code", str(args.fail_code)])
    command.extend(["--provider-command", provider_command])

    completed = subprocess.run(command)
    return completed.returncode


def runner_main(argv: list[str]) -> int:
    parser = build_runner_parser()
    args = parser.parse_args(argv)
    plan_path = Path(args.plan).resolve()
    if args.mode == "execute":
        return run_codex_execute(plan_path, args.codex_command)
    return run_codex_verify(
        plan_path,
        args.codex_command,
        pass_with_risks_code=args.pass_with_risks_code,
        fail_code=args.fail_code,
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--runner" in argv:
        return runner_main(argv)
    return wrapper_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
