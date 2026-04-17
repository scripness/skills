#!/usr/bin/env python3
"""Thin local runner helpers for the six-skill evaluation harness.

This intentionally does two bounded things for Milestone 5:

1. Validate the tracked eval contract and cross-file invariants.
2. Scaffold a repeatable local run workspace under .tmp/evals/<run-id>/.

It does not execute model calls or grade runs automatically.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
EVALS_ROOT = REPO_ROOT / "evals"
SKILLS = ("consult", "execute", "plan", "specs", "tests", "verify")
ALLOWED_TRIGGER_OUTCOMES = {"trigger", "no_trigger"}
REQUIRED_RUN_DIRECTORIES = ("outputs", "transcripts", "fixtures")
REQUIRED_RUN_FILES = ("timing.json", "grading.json", "benchmark.json", "feedback.json")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path.relative_to(REPO_ROOT)} is not valid JSON: {exc}") from exc


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def full_eval_id(skill: str, eval_id: str) -> str:
    return f"{skill}:{eval_id}"


def compare_target_map(entry: dict[str, Any]) -> tuple[list[str], list[dict[str, str]]]:
    targets = entry.get("comparison_targets")
    if not isinstance(targets, dict):
        raise ValueError("comparison_targets must be an object")

    required = targets.get("required")
    if not isinstance(required, list) or not required:
        raise ValueError("comparison_targets.required must be a non-empty list")

    optional = targets.get("optional", [])
    if optional is None:
        optional = []
    if not isinstance(optional, list):
        raise ValueError("comparison_targets.optional must be a list when present")

    normalized_optional: list[dict[str, str]] = []
    for item in optional:
        if not isinstance(item, dict):
            raise ValueError("comparison_targets.optional items must be objects")
        target = item.get("target")
        why = item.get("why")
        if not isinstance(target, str) or not target:
            raise ValueError("comparison_targets.optional items must include a target string")
        if not isinstance(why, str) or not why.strip():
            raise ValueError("comparison_targets.optional items must include a non-empty why string")
        normalized_optional.append({"target": target, "why": why})

    return required, normalized_optional


def validate_fixture_manifest(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = load_json(path)
    except ValueError as exc:
        errors.append(str(exc))
        return None

    rel = path.relative_to(REPO_ROOT)
    fixture_id = data.get("fixture_id")
    if not isinstance(fixture_id, str) or not fixture_id:
        errors.append(f"{rel}: fixture_id must be a non-empty string")
        return None

    if data.get("status") != "pinned":
        errors.append(f"{rel}: status must be 'pinned'")

    pinned_commit = (
        data.get("repository", {})
        .get("pinned_commit", {})
    )
    pinned_sha = pinned_commit.get("sha")
    if not isinstance(pinned_sha, str) or not pinned_sha:
        errors.append(f"{rel}: repository.pinned_commit.sha must be a non-empty string")

    generated_workspace_root = data.get("checkout", {}).get("generated_workspace_root")
    expected_workspace_root = f".tmp/evals/<run-id>/fixtures/{fixture_id}"
    if generated_workspace_root != expected_workspace_root:
        errors.append(
            f"{rel}: checkout.generated_workspace_root must be {expected_workspace_root!r}"
        )

    checkout_command = data.get("checkout", {}).get("checkout_command", "")
    if isinstance(pinned_sha, str) and pinned_sha and pinned_sha not in checkout_command:
        errors.append(f"{rel}: checkout.checkout_command must pin the recorded commit SHA")

    return data


def validate_skill_eval(
    skill: str,
    path: Path,
    runtime: dict[str, Any],
    fixture_manifests: dict[str, dict[str, Any]],
    errors: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    try:
        data = load_json(path)
    except ValueError as exc:
        errors.append(str(exc))
        return [], []

    rel = path.relative_to(REPO_ROOT)
    if data.get("skill") != skill:
        errors.append(f"{rel}: skill must be {skill!r}")
    if data.get("version") != 1:
        errors.append(f"{rel}: version must be 1")

    default_baseline = runtime["governance"]["gating"]["default_baseline"]
    optional_baseline = runtime["governance"]["gating"]["optional_secondary_baseline"]
    allowed_splits = set(runtime["governance"]["split_policy"]["allowed_splits"])
    allowed_modes = set(runtime["governance"]["grading"]["allowed_modes"])

    if data.get("default_baseline") != default_baseline:
        errors.append(f"{rel}: default_baseline must match evals/runtime.json")
    if data.get("optional_secondary_baseline") != optional_baseline:
        errors.append(f"{rel}: optional_secondary_baseline must match evals/runtime.json")

    trigger_entries = data.get("trigger_evals")
    workflow_entries = data.get("workflow_evals")
    if not isinstance(trigger_entries, list) or not trigger_entries:
        errors.append(f"{rel}: trigger_evals must be a non-empty list")
        trigger_entries = []
    if not isinstance(workflow_entries, list) or not workflow_entries:
        errors.append(f"{rel}: workflow_evals must be a non-empty list")
        workflow_entries = []

    seen_ids: set[str] = set()

    def validate_entry(kind: str, entry: dict[str, Any]) -> dict[str, Any] | None:
        entry_id = entry.get("id")
        label = f"{rel}:{entry_id or '<missing id>'}"
        if not isinstance(entry_id, str) or not entry_id:
            errors.append(f"{label}: id must be a non-empty string")
            return None
        if entry_id in seen_ids:
            errors.append(f"{label}: duplicate eval id within {rel}")
            return None
        seen_ids.add(entry_id)
        if not entry_id.startswith(f"{skill}-"):
            errors.append(f"{label}: id must start with {skill}-")

        split = entry.get("split")
        if split not in allowed_splits:
            errors.append(f"{label}: split must be one of {sorted(allowed_splits)}")

        grading = entry.get("grading")
        if grading not in allowed_modes:
            errors.append(f"{label}: grading must be one of {sorted(allowed_modes)}")

        must_run = entry.get("must_run")
        if not isinstance(must_run, bool):
            errors.append(f"{label}: must_run must be a boolean")
        elif must_run and split != "validation":
            errors.append(f"{label}: must-run evals must live on the validation split")

        try:
            required_targets, optional_targets = compare_target_map(entry)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            required_targets = []
            optional_targets = []

        if default_baseline not in required_targets:
            errors.append(f"{label}: comparison_targets.required must include {default_baseline}")
        if optional_baseline in required_targets:
            errors.append(
                f"{label}: comparison_targets.required must not include the optional baseline"
            )
        for optional_target in optional_targets:
            if optional_target["target"] != optional_baseline:
                errors.append(
                    f"{label}: optional comparison target must be {optional_baseline!r} when present"
                )

        fixture = entry.get("fixture")
        fixture_id: str | None = None
        if fixture is not None:
            if not isinstance(fixture, dict):
                errors.append(f"{label}: fixture must be an object when present")
            else:
                fixture_id = fixture.get("id")
                manifest_path = fixture.get("manifest_path")
                if not isinstance(fixture_id, str) or not fixture_id:
                    errors.append(f"{label}: fixture.id must be a non-empty string")
                if not isinstance(manifest_path, str) or not manifest_path:
                    errors.append(f"{label}: fixture.manifest_path must be a non-empty string")
                else:
                    manifest_abs = REPO_ROOT / manifest_path
                    manifest = fixture_manifests.get(manifest_path)
                    if manifest is None:
                        errors.append(f"{label}: fixture manifest {manifest_path} is missing or invalid")
                    elif manifest_abs.exists() and manifest.get("fixture_id") != fixture_id:
                        errors.append(
                            f"{label}: fixture.id must match {manifest_path}'s fixture_id"
                        )

        summary = {
            "kind": kind,
            "skill": skill,
            "id": entry_id,
            "full_id": full_eval_id(skill, entry_id),
            "split": split,
            "must_run": bool(must_run),
            "grading": grading,
            "goal": entry.get("goal", ""),
            "fixture_id": fixture_id,
            "comparison_required": required_targets,
            "comparison_optional": optional_targets,
        }

        if kind == "trigger":
            cases = entry.get("cases")
            if not isinstance(cases, list) or not cases:
                errors.append(f"{label}: trigger_evals must include a non-empty cases list")
                summary["case_count"] = 0
                return summary

            case_ids: set[str] = set()
            for case in cases:
                case_id = case.get("id")
                if not isinstance(case_id, str) or not case_id:
                    errors.append(f"{label}: each trigger case must have a non-empty id")
                    continue
                if case_id in case_ids:
                    errors.append(f"{label}: duplicate trigger case id {case_id!r}")
                case_ids.add(case_id)
                if case.get("expected_outcome") not in ALLOWED_TRIGGER_OUTCOMES:
                    errors.append(
                        f"{label}: trigger case {case_id!r} expected_outcome must be one of "
                        f"{sorted(ALLOWED_TRIGGER_OUTCOMES)}"
                    )
                if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                    errors.append(f"{label}: trigger case {case_id!r} must include a non-empty prompt")
                if not isinstance(case.get("why"), str) or not case["why"].strip():
                    errors.append(f"{label}: trigger case {case_id!r} must include a non-empty why")

            summary["case_count"] = len(cases)
            return summary

        scenario = entry.get("scenario")
        if not isinstance(scenario, dict):
            errors.append(f"{label}: workflow_evals must include a scenario object")
            summary["required_inputs"] = []
        else:
            required_inputs = scenario.get("required_inputs")
            if not isinstance(required_inputs, list) or not required_inputs:
                errors.append(f"{label}: scenario.required_inputs must be a non-empty list")
                required_inputs = []
            summary["required_inputs"] = required_inputs

        assertions = entry.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{label}: workflow_evals must include a non-empty assertions list")

        return summary

    validated_triggers = [
        summary
        for entry in trigger_entries
        if isinstance(entry, dict)
        for summary in [validate_entry("trigger", entry)]
        if summary is not None
    ]
    validated_workflows = [
        summary
        for entry in workflow_entries
        if isinstance(entry, dict)
        for summary in [validate_entry("workflow", entry)]
        if summary is not None
    ]
    return validated_triggers, validated_workflows


def validate_repo() -> dict[str, Any]:
    errors: list[str] = []

    runtime_path = EVALS_ROOT / "runtime.json"
    try:
        runtime = load_json(runtime_path)
    except ValueError as exc:
        raise SystemExit(str(exc))

    if runtime.get("version") != 1:
        errors.append("evals/runtime.json: version must be 1")

    default_profile = runtime.get("default_profile")
    profiles = runtime.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        errors.append("evals/runtime.json: profiles must be a non-empty object")
        profiles = {}
    if default_profile not in profiles:
        errors.append("evals/runtime.json: default_profile must exist in profiles")

    fixture_dir = EVALS_ROOT / "fixtures"
    fixture_manifests: dict[str, dict[str, Any]] = {}
    for manifest_path in sorted(fixture_dir.glob("*.json")):
        manifest = validate_fixture_manifest(manifest_path, errors)
        if manifest is not None:
            fixture_manifests[str(manifest_path.relative_to(REPO_ROOT))] = manifest

    all_trigger_summaries: list[dict[str, Any]] = []
    all_workflow_summaries: list[dict[str, Any]] = []
    for skill in SKILLS:
        skill_path = REPO_ROOT / skill / "evals" / "evals.json"
        triggers, workflows = validate_skill_eval(skill, skill_path, runtime, fixture_manifests, errors)
        all_trigger_summaries.extend(triggers)
        all_workflow_summaries.extend(workflows)

    pinned_fixture_ids = {
        manifest.get("fixture_id")
        for manifest in fixture_manifests.values()
        if isinstance(manifest.get("fixture_id"), str) and manifest.get("fixture_id")
    }
    for summary in all_workflow_summaries:
        fixture_id = summary.get("fixture_id")
        if fixture_id in pinned_fixture_ids and not summary["must_run"]:
            errors.append(
                f"{summary['skill']}/evals/evals.json:{summary['id']}: "
                "workflow evals for pinned fixtures must set must_run: true"
            )

    selected_trigger_ids = {
        summary["full_id"] for summary in all_trigger_summaries if summary["must_run"]
    }
    selected_workflow_ids = {
        summary["full_id"] for summary in all_workflow_summaries if summary["must_run"]
    }
    runtime_selected = runtime.get("governance", {}).get("must_run_surface", {}).get("selected_cases", {})
    runtime_trigger_ids = set(runtime_selected.get("trigger_packs", []))
    runtime_workflow_ids = set(runtime_selected.get("workflow_cases", []))

    if selected_trigger_ids != runtime_trigger_ids:
        errors.append(
            "evals/runtime.json: selected trigger_packs must exactly match skill-local must_run trigger packs"
        )
    if selected_workflow_ids != runtime_workflow_ids:
        errors.append(
            "evals/runtime.json: selected workflow_cases must exactly match skill-local must_run workflow cases"
        )

    real_repo_fixtures = set(runtime.get("governance", {}).get("must_run_surface", {}).get("real_repo_fixtures", []))
    expected_real_repo_fixtures = set()
    for manifest in fixture_manifests.values():
        fixture_id = manifest.get("fixture_id")
        pinned_sha = manifest.get("repository", {}).get("pinned_commit", {}).get("sha")
        if fixture_id and pinned_sha:
            expected_real_repo_fixtures.add(f"{fixture_id}@{pinned_sha}")
    if real_repo_fixtures != expected_real_repo_fixtures:
        errors.append(
            "evals/runtime.json: real_repo_fixtures must mirror the pinned fixture manifests"
        )

    gitignore_path = REPO_ROOT / ".gitignore"
    if not gitignore_path.exists():
        errors.append(".gitignore is missing; .tmp/evals/ ignore coverage is required")
    else:
        gitignore_text = gitignore_path.read_text(encoding="utf-8")
        if ".tmp/evals/" not in gitignore_text:
            errors.append(".gitignore must ignore .tmp/evals/")

    if errors:
        raise SystemExit("Eval harness validation failed:\n- " + "\n- ".join(errors))

    return {
        "runtime": runtime,
        "fixtures": fixture_manifests,
        "trigger_summaries": all_trigger_summaries,
        "workflow_summaries": all_workflow_summaries,
    }


def build_case_selection(
    context: dict[str, Any],
    selection: str,
    skills: set[str] | None,
) -> list[dict[str, Any]]:
    all_cases = context["trigger_summaries"] + context["workflow_summaries"]

    def include(summary: dict[str, Any]) -> bool:
        if skills is not None and summary["skill"] not in skills:
            return False
        if selection == "must-run":
            return summary["must_run"]
        if selection == "validation":
            return summary["split"] == "validation"
        if selection == "all":
            return True
        raise ValueError(f"Unsupported selection mode: {selection}")

    return [summary for summary in all_cases if include(summary)]


def write_run_template(run_dir: Path, manifest: dict[str, Any]) -> None:
    selected_case_lines = "\n".join(f"- `{case['full_id']}`" for case in manifest["selected_cases"])
    review_template = f"""# Eval Run Review

Run id: `{manifest["run_id"]}`
Profile: `{manifest["profile"]}`
Selection: `{manifest["selection"]["mode"]}`
Created at: `{manifest["created_at"]}`

## Candidate

- commit or branch:
- changed skill paths:

## Baseline

- required baseline: `previous_committed_skill_version`
- optional no-skill baseline used:
- optional baseline rationale:

## Artifact Checklist

- [ ] `outputs/`
- [ ] `timing.json`
- [ ] `grading.json`
- [ ] `benchmark.json`
- [ ] `feedback.json`
- [ ] `transcripts/` or equivalent logs

## Selected Cases

{selected_case_lines}

## Review Notes

- regressions judged real / expected / blocked:
- unresolved severe findings:
- follow-up actions:
"""
    (run_dir / "review-template.md").write_text(review_template, encoding="utf-8")


def init_run(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.run_id):
        raise SystemExit("run-id must match [A-Za-z0-9._-]+")

    context = validate_repo()
    runtime = context["runtime"]
    profile_name = args.profile or runtime["default_profile"]
    profiles = runtime["profiles"]
    if profile_name not in profiles:
        raise SystemExit(f"Unknown profile {profile_name!r}; choose one of {sorted(profiles)}")

    skills = set(args.skill) if args.skill else None
    selected_cases = build_case_selection(context, args.selection, skills)
    if not selected_cases:
        raise SystemExit("No eval cases matched the requested selection")

    run_dir = REPO_ROOT / ".tmp" / "evals" / args.run_id
    if run_dir.exists():
        raise SystemExit(f"{run_dir.relative_to(REPO_ROOT)} already exists; choose a new run-id")

    for directory in REQUIRED_RUN_DIRECTORIES:
        (run_dir / directory).mkdir(parents=True, exist_ok=True)

    selected_fixture_ids = sorted(
        {case["fixture_id"] for case in selected_cases if case.get("fixture_id")}
    )
    fixtures: list[dict[str, Any]] = []
    for fixture_manifest_path, fixture in sorted(context["fixtures"].items()):
        fixture_id = fixture["fixture_id"]
        if fixture_id not in selected_fixture_ids:
            continue
        generated_workspace_root = str(
            Path(".tmp") / "evals" / args.run_id / "fixtures" / fixture_id
        )
        (run_dir / "fixtures" / fixture_id).mkdir(parents=True, exist_ok=True)
        fixtures.append(
            {
                "id": fixture_id,
                "manifest_path": fixture_manifest_path,
                "pinned_commit": fixture["repository"]["pinned_commit"]["sha"],
                "generated_workspace_root": generated_workspace_root,
            }
        )

    manifest = {
        "version": 1,
        "run_id": args.run_id,
        "created_at": utc_now(),
        "profile": profile_name,
        "profile_settings": profiles[profile_name],
        "selection": {
            "mode": args.selection,
            "skills": sorted(skills) if skills is not None else list(SKILLS),
        },
        "required_artifacts": {
            "directories": list(REQUIRED_RUN_DIRECTORIES),
            "files": list(REQUIRED_RUN_FILES),
            "notes": [
                "Populate the required files before review.",
                "Record regression decisions in review-template.md or another durable change record.",
            ],
        },
        "selected_cases": selected_cases,
        "fixtures": fixtures,
    }

    (run_dir / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_run_template(run_dir, manifest)

    print(f"Initialized {run_dir.relative_to(REPO_ROOT)}")
    print(f"- profile: {profile_name}")
    print(f"- selection: {args.selection}")
    print(f"- cases: {len(selected_cases)}")
    if fixtures:
        print(f"- fixtures: {', '.join(fixture['id'] for fixture in fixtures)}")
    else:
        print("- fixtures: none")
    return 0


def validate_command(_: argparse.Namespace) -> int:
    context = validate_repo()
    trigger_count = len(context["trigger_summaries"])
    workflow_count = len(context["workflow_summaries"])
    fixture_count = len(context["fixtures"])
    print("Eval harness validation passed")
    print(f"- skills: {len(SKILLS)}")
    print(f"- trigger packs: {trigger_count}")
    print(f"- workflow cases: {workflow_count}")
    print(f"- fixture manifests: {fixture_count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Thin local runner helpers for the six-skill evaluation harness."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate tracked eval definitions, fixture manifests, runtime metadata, and must-run invariants.",
    )
    validate_parser.set_defaults(func=validate_command)

    init_run_parser = subparsers.add_parser(
        "init-run",
        help="Create a repeatable local run workspace under .tmp/evals/<run-id>/.",
    )
    init_run_parser.add_argument("--run-id", required=True, help="Unique run identifier.")
    init_run_parser.add_argument(
        "--profile",
        help="Runtime profile from evals/runtime.json. Defaults to the repo's default_profile.",
    )
    init_run_parser.add_argument(
        "--selection",
        choices=("must-run", "validation", "all"),
        default="must-run",
        help="Which tracked eval cases to include in the run manifest.",
    )
    init_run_parser.add_argument(
        "--skill",
        action="append",
        choices=SKILLS,
        help="Limit the run manifest to one or more skills. Repeat the flag to select more than one.",
    )
    init_run_parser.set_defaults(func=init_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
