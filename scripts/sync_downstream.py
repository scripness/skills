#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
DOWNSTREAM_SKILLS_RELATIVE = Path(".agents") / "skills"
SECTION_HEADING = "## Agentic Workflow"
MANAGED_SECTION = """## Agentic Workflow

This repo uses a local six-skill workflow under `.agents/skills/`:
`consult`, `plan`, `execute`, `verify`, `specs`, and `tests`.

Use one skill when the task is narrow, or compose them into a full workflow:
`consult` to clarify, `plan` to record durable task state, `execute` to
complete one bounded slice, and `verify` to review the result. Use `specs`
when repo truth is missing or stale, and `tests` when test truth or coverage
needs to be added or synced.

Optional helpers for plan-driven work live under
`.agents/skills/execute/scripts/`:
- `python3 .agents/skills/execute/scripts/loop.py --help`
- `python3 .agents/skills/execute/scripts/providers/codex_loop.py --help`
- `python3 .agents/skills/execute/scripts/providers/codex_loop_dashboard.py --help`

For the longer human-facing description of each skill, open
`.agents/skills/<skill>/README.md`.
"""
IGNORED_DIRECTORY_NAMES = {"evals", "__pycache__"}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo", ".pyd"}
HEADING_RE = re.compile(r"^[ ]{0,3}(# |## )")
FENCE_RE = re.compile(r"^[ ]{0,3}([`~]{3,})")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync filtered skill payloads into a downstream repo's "
            ".agents/skills/ and refresh the managed README.md workflow section."
        )
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Absolute or relative path to the downstream repo root.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help=(
            "Exact skill name to sync. Repeat for multiple skills. "
            "If omitted, all shipped skills are synced."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned changes without writing files.",
    )
    return parser.parse_args(argv)


def discover_skills(src_root: Path) -> list[str]:
    skills = []
    for entry in sorted(src_root.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            skills.append(entry.name)
    if not skills:
        raise RuntimeError(f"no shipped skills found under {src_root}")
    return skills


def select_skills(requested: list[str], available: list[str]) -> list[str]:
    if not requested:
        return available

    deduped = list(dict.fromkeys(requested))
    available_set = set(available)
    invalid = [name for name in deduped if name not in available_set]
    if invalid:
        raise ValueError(
            "unknown skill name(s): "
            + ", ".join(invalid)
            + ". Available skills: "
            + ", ".join(available)
        )
    return deduped


def validate_target_root(target_root: Path) -> None:
    if not target_root.exists():
        raise ValueError(f"target repo does not exist: {target_root}")
    if not target_root.is_dir():
        raise ValueError(f"target path is not a directory: {target_root}")
    if target_root == REPO_ROOT:
        raise ValueError(
            "target repo must be a downstream repo, not this source repo: "
            f"{target_root}"
        )


def validate_target_skills_root(target_skills_root: Path) -> None:
    if target_skills_root.is_symlink():
        raise ValueError(
            "downstream skills path must not be a symlink: "
            f"{target_skills_root}"
        )
    if target_skills_root.exists() and not target_skills_root.is_dir():
        raise ValueError(
            f"downstream skills path is not a directory: {target_skills_root}"
        )


def ensure_skill_contract(skill_root: Path) -> None:
    required_paths = (
        skill_root / "SKILL.md",
        skill_root / "README.md",
        skill_root / "agents" / "openai.yaml",
    )
    missing = [str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()]
    if missing:
        raise RuntimeError(
            f"skill payload is missing required paths for downstream sync: {', '.join(missing)}"
        )


def ignore_downstream_noise(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in IGNORED_DIRECTORY_NAMES:
            ignored.add(name)
            continue
        if Path(name).suffix.lower() in IGNORED_FILE_SUFFIXES:
            ignored.add(name)
    return ignored


def prefix(dry_run: bool) -> str:
    return "[dry-run] " if dry_run else ""


def sync_skill(skill_name: str, target_skills_root: Path, dry_run: bool) -> None:
    source = SRC_ROOT / skill_name
    ensure_skill_contract(source)
    destination = target_skills_root / skill_name

    if destination.exists() or destination.is_symlink():
        print(f"{prefix(dry_run)}replace {destination}")
        if not dry_run:
            if destination.is_symlink() or destination.is_file():
                destination.unlink()
            else:
                shutil.rmtree(destination)
    else:
        print(f"{prefix(dry_run)}create {destination}")

    if not dry_run:
        shutil.copytree(source, destination, ignore=ignore_downstream_noise)


def update_fence_state(
    line: str, fence_state: tuple[str, int] | None
) -> tuple[str, int] | None:
    match = FENCE_RE.match(line)
    if not match:
        return fence_state

    marker = match.group(1)
    marker_char = marker[0]
    marker_length = len(marker)

    if fence_state is None:
        return (marker_char, marker_length)

    if fence_state[0] == marker_char and marker_length >= fence_state[1]:
        return None

    return fence_state


def find_managed_section(lines: list[str]) -> tuple[int, int] | None:
    matches: list[int] = []
    fence_state: tuple[str, int] | None = None
    for index, line in enumerate(lines):
        fence_state = update_fence_state(line, fence_state)
        if fence_state is None and line.strip() == SECTION_HEADING:
            matches.append(index)

    if len(matches) > 1:
        raise ValueError("downstream README.md contains multiple '## Agentic Workflow' headings")

    if not matches:
        return None

    start = matches[0]
    fence_state = None
    for index in range(start + 1, len(lines)):
        fence_state = update_fence_state(lines[index], fence_state)
        if fence_state is None and HEADING_RE.match(lines[index]):
            return start, index

    return start, len(lines)


def render_readme(existing: str) -> str:
    managed = MANAGED_SECTION.rstrip()
    if not existing.strip():
        return managed + "\n"

    lines = existing.splitlines(keepends=True)
    bounds = find_managed_section(lines)
    if bounds is None:
        return existing.rstrip() + "\n\n" + managed + "\n"

    start, end = bounds
    before = "".join(lines[:start]).rstrip()
    after = "".join(lines[end:]).lstrip("\n").rstrip()

    parts = []
    if before:
        parts.append(before)
    parts.append(managed)
    if after:
        parts.append(after)
    return "\n\n".join(parts) + "\n"


def prepare_readme_sync(target_root: Path) -> tuple[Path, str, str]:
    readme_path = target_root / "README.md"
    existing = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    rendered = render_readme(existing)
    return readme_path, existing, rendered


def sync_readme(readme_path: Path, existing: str, rendered: str, dry_run: bool) -> None:
    if existing == rendered:
        print(f"{prefix(dry_run)}leave {readme_path} unchanged")
        return

    action = "update" if readme_path.exists() else "create"
    print(f"{prefix(dry_run)}{action} {readme_path}")
    if not dry_run:
        readme_path.write_text(rendered, encoding="utf-8")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        available_skills = discover_skills(SRC_ROOT)
        selected_skills = select_skills(args.skill, available_skills)
        target_root = Path(args.target).expanduser().resolve()
        validate_target_root(target_root)
        target_skills_root = target_root / DOWNSTREAM_SKILLS_RELATIVE
        validate_target_skills_root(target_skills_root)
    except (RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"target repo: {target_root}")
    print(f"skills: {', '.join(selected_skills)}")

    try:
        readme_path, existing_readme, rendered_readme = prepare_readme_sync(target_root)
        if not target_skills_root.exists():
            print(f"{prefix(args.dry_run)}ensure {target_skills_root}")
        if not target_skills_root.exists() and not args.dry_run:
            target_skills_root.mkdir(parents=True, exist_ok=True)
        for skill_name in selected_skills:
            sync_skill(skill_name, target_skills_root, args.dry_run)
        sync_readme(readme_path, existing_readme, rendered_readme, args.dry_run)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
