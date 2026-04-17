# Evaluation Harness

This directory holds the tracked eval metadata for the six-skill workflow.
Milestones 1 through 4 define the layout, artifact contract, governance rules,
canonical runtime profile, the first skill-local trigger and workflow cases,
the first pinned real-repo fixture, and the initial must-run surface. Later
milestones add runnable helpers without changing the tracked-versus-generated
split below.

## Tracked Source

- `<skill>/evals/evals.json` is the default tracked entrypoint for each
  skill's trigger and workflow eval definitions.
- Author each `<skill>/evals/evals.json` by hand as tracked eval intent; do
  not treat these files as generated run artifacts.
- `evals/runtime.json` pins the canonical runtime profile used for default
  regression gating while leaving room for deliberate future profile changes.
- `evals/runtime.json` also carries the machine-readable default governance
  settings that future runners should enforce.
- Shared real-repo fixture manifests belong under `evals/fixtures/`;
  `evals/fixtures/cryptoli.json` is the first pinned fixture manifest.
- Real-repo workflow cases should reference the owning manifest instead of
  inlining floating repo metadata in each skill-local definition.
- Future thin shared runner helpers belong under `evals/scripts/`.

## Baseline Policy

- Compare a candidate skill change against the previous committed version of
  that same skill by default.
- Add a no-skill baseline only when it materially clarifies whether the skill
  itself is helping.
- In skill-local eval definitions, record default baselines as required
  comparison targets and record no-skill baselines as optional comparison
  targets with a short reason, so later runner work does not guess when the
  extra comparison is warranted.
- Keep runtime changes explicit in `evals/runtime.json` so skill comparisons do
  not silently absorb runtime or model drift.

## Governance

Milestone 2 defines the evaluation-governance contract now so manual review and
future runners use the same rules.

### Split Policy

- Use `train` cases for fixture design, skill-description tuning, and other
  development-time iteration.
- Use `validation` cases for regression gating against the chosen baseline.
- Mark must-run cases on the `validation` split only.
- Do not rewrite or retire validation cases just to rescue a candidate; land
  harness changes as their own reviewed updates.

### Repeated Trials

- Default to one trial for `train` cases.
- Default to one trial for non-must-run `validation` cases when doing
  exploratory checks.
- Run every must-run validation case three times for both the candidate and the
  comparison baseline.
- Keep the runtime profile and trial count identical across compared runs.
- Aggregate repeated trials by majority outcome for binary checks and median
  score for rubric or hybrid checks.

### Grading Protocol

- Every concrete eval added in Milestone 3 or later should declare one grading
  mode: `assertion`, `rubric`, or `hybrid`.
- Use `assertion` grading when deterministic pass/fail checks are credible.
- Use `rubric` grading when human judgment is required; retain reviewer notes
  in the run artifacts rather than collapsing them into an unexplained score.
- Use `hybrid` grading when both deterministic checks and reviewer judgment are
  needed.
- Treat severe findings as correctness, safety, or workflow-boundary failures
  that would block trusting the candidate output in real repo work.

### Pass/Fail Thresholds

- Compare against the previous committed version of the same skill by default.
- Add a no-skill baseline only when it materially improves the signal.
- A candidate fails the default gate if required artifacts are missing,
  required repeated trials were not run, or unresolved severe findings increase
  on the must-run real-repo surface.
- A candidate also fails if the must-run validation surface regresses against
  baseline and that regression is not explicitly explained and accepted during
  artifact review.
- Trigger quality should not drop on the must-run validation trigger surface;
  treat worse aggregate trigger outcomes than baseline as a gating regression.

### Must-Run Regression Surface

- The must-run surface is a subset of the `validation` split used for everyday
  regression checks and release-gating decisions.
- The initial shipped must-run surface is the validation boundary trigger pack
  for each skill plus one pinned `cryptoli`-backed validation workflow case
  per skill.
- Skill-local `must_run: true` flags are the tracked source of truth for that
  surface, and `evals/runtime.json` mirrors the selected case ids for future
  runner defaults.
- All pinned real-repo fixture cases join the must-run surface by default.

### Regression Artifact Review

- Do not accept a skill change on summary numbers alone.
- Review changed `outputs/`, `timing.json`, `grading.json`, `benchmark.json`,
  `feedback.json`, and execution transcripts or equivalent logs before
  accepting the change.
- Record whether observed regressions are real, expected, or blocked on harness
  follow-up in the plan, PR, or other durable change record.

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

Milestones 1 through 4 define layout, storage, baseline policy, governance,
review gates, the first concrete skill-local cases, the first pinned fixture,
and the initial must-run surface. Milestone 5 still owns the runnable helper
surface.
