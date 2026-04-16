# Evaluation Harness

This directory holds the tracked eval metadata for the six-skill workflow.
Milestone 1 defines the layout, artifact contract, baseline policy, and
canonical runtime profile. Later milestones add governance rules, pinned
fixtures, and runnable helpers without changing the tracked-versus-generated
split below.

## Tracked Source

- `<skill>/evals/evals.json` is the default tracked entrypoint for each
  skill's trigger and workflow eval definitions.
- Author each `<skill>/evals/evals.json` by hand as tracked eval intent; do
  not treat these files as generated run artifacts.
- `evals/runtime.json` pins the canonical runtime profile used for default
  regression gating while leaving room for deliberate future profile changes.
- Future shared fixture manifests belong under `evals/fixtures/`.
- Future thin shared runner helpers belong under `evals/scripts/`.

## Baseline Policy

- Compare a candidate skill change against the previous committed version of
  that same skill by default.
- Add a no-skill baseline only when it materially clarifies whether the skill
  itself is helping.
- Keep runtime changes explicit in `evals/runtime.json` so skill comparisons do
  not silently absorb runtime or model drift.

## Generated Outputs

Generated outputs do not belong in tracked source. Store them under
`.tmp/evals/<run-id>/` so runs can be refreshed cleanly without polluting the
repo.

Each run should retain, at minimum:

- `outputs/`
- `timing.json`
- `grading.json`
- `benchmark.json`
- `feedback.json`
- execution transcripts or equivalent logs
- temporary cloned fixture repos or other repro workspaces needed for reruns

## Scope Note

This Milestone 1 contract defines layout and storage only. Train/validation
splits, repeated-run policy, grading protocol, pass/fail thresholds, must-run
regression surfaces, and regression-review gates land in the next milestones.
