---
Status: Shipped
Last verified: 2026-04-22
---

# Evaluation Harness

> Source of truth: `src/*/evals/evals.json`, `evals/runtime.json`,
> `evals/fixtures/cryptoli.json`, `evals/scripts/harness.py`, and `Makefile`
> Non-owning trees to ignore unless explicitly in scope: `.git/`, `.tmp/evals/`
> If this spec contradicts the code, the code is correct — update this spec.

<!-- Review when evals/runtime.json changes -->
<!-- Review when evals/scripts/harness.py changes -->
<!-- Review when src/*/evals/evals.json changes -->

## Overview

The shared evaluation harness keeps tracked eval intent and the thin local
maintenance surface around it. It validates the shipped skill metadata and eval
contract, and it scaffolds repeatable local run workspaces under
`.tmp/evals/<run-id>/`.

## Non-Goals

- executing model calls automatically
- grading runs automatically
- storing generated outputs in tracked source

## Key Patterns

- skill-local eval definitions live with the skill they validate under
  `src/<skill>/evals/evals.json`
- shared runtime metadata, fixture manifests, and the harness helper live under
  repo-root `evals/`
- `Makefile` includes thin repo-root maintenance targets; the eval-related
  targets delegate to the harness script instead of duplicating its logic
- tracked eval truth and generated run artifacts stay in different trees

## Tracked Inputs

- `src/<skill>/evals/evals.json`: trigger and workflow eval definitions for the
  owning skill
- `evals/runtime.json`: default profile and machine-readable governance rules
- `evals/fixtures/cryptoli.json`: pinned real-repo fixture manifest
- `evals/README.md`: human-readable artifact and governance overview
- `evals/scripts/harness.py`: validation and run-scaffolding entrypoint
- `Makefile`: thin repo-root maintenance wrapper whose eval-related targets
  delegate to the harness script

## Generated Outputs

Generated outputs belong under ignored `.tmp/evals/<run-id>/`, not tracked
source.

The shipped harness scaffolds:

- `outputs/`
- `transcripts/`
- `fixtures/`
- `run.json`
- `review-template.md`

The following files are required later for a completed reviewed run, but they
are not created by `init-run`:

- `timing.json`
- `grading.json`
- `benchmark.json`
- `feedback.json`

## Governance Surface

- Use `train` cases for tuning and `validation` cases for regression gating.
- Must-run cases live on the `validation` split only.
- A skill may keep additional non-must-run `validation` cases when they add
  signal; for `tests`, the broader cryptoli layer-selection workflow is the
  must-run case while the narrower backend-only coverage scenario remains
  extra validation coverage.
- Compare against the previous committed version of the same skill by default.
- Add a no-skill baseline only when it adds real signal.
- Run must-run validation cases three times by default.
- Allowed grading modes are `assertion`, `rubric`, and `hybrid`.
- Do not accept a skill change until the generated artifacts have been
  reviewed.

## Maintenance Surface

- `make help` lists the shipped maintenance targets.
- `make validate` runs repo-level validation for skill metadata, local assets,
  runtime metadata, fixture manifests, and eval invariants.
- `make eval-init-run RUN_ID=<run-id> ...` scaffolds a repeatable workspace
  under `.tmp/evals/<run-id>/`.
- `python3 evals/scripts/harness.py --help` exposes the direct harness CLI.
- `python3 evals/scripts/harness.py validate` runs the same validation surface
  without the Makefile wrapper.
- `python3 evals/scripts/harness.py init-run --run-id <run-id> --selection must-run`
  scaffolds a run directly through the harness.

`src/execute/scripts/loop.py` is an adjacent plan-driven helper, not part
of eval grading or the eval governance contract.

## Verification

- Run `make validate` to confirm the tracked harness surface is internally
  consistent.
- Run `python3 evals/scripts/harness.py --help` to confirm the helper still
  exposes the documented CLI.
- Inspect `evals/runtime.json` and one or more `src/<skill>/evals/evals.json`
  files when checking governance or selected-case claims.
