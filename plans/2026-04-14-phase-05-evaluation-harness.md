# Phase 05: Evaluation Harness

## Goal

Define and build the first honest regression harness for the six-skill system so
skill changes can be compared against baselines and real-repo behavior instead
of judged only by intuition.

## Scope

- Turn the roadmap’s evaluation design into tracked eval definitions and a real
  artifact contract.
- Use the canonical eval runtime for gating while keeping it configurable later.
- Use pinned `cryptoli` as the first official real-repo fixture.
- Make the remaining evaluation-governance rules explicit in the implementation:
  train/validation splits, repeated trials, pass/fail thresholds, grading
  protocol, must-run regression surface, and regression artifact review.

## Non-Goals

- Final maintenance-interface polish.
- Broad CI rollout before the local loop is usable.
- Rewriting the skills themselves unless an eval surfaces a concrete gap.

## Owned TODO Sections

- `7. Add Full Evaluation Coverage`

## Deliverables

- Per-skill `<skill>/evals/` tracked definitions, with `evals/evals.json` as
  the default tracked entrypoint for each skill
- Shared tracked harness metadata under repo-root `evals/`, anchored by
  `evals/README.md` for the artifact contract and review procedure,
  `evals/runtime.json` for the canonical runtime profile and configuration
  surface, `evals/fixtures/cryptoli.json` for the tracked real-repo fixture
  pin, and `evals/scripts/` only for any thin cross-skill runner surface
  needed before Phase 06
- Initial eval artifact contract and storage conventions, including a dedicated
  generated-output root outside tracked source
- Pinned `cryptoli` fixture manifest for real-repo evals
- Repeatable local eval runners or the first thin scaffolding required to run
  them
- Documented baseline comparison policy, pass/fail thresholds, and regression
  review procedure

## Dependencies

- Delivered contracts for all six skills through Phase 04
- Existing `AGENTS.md`, `README.md`, and `TODO.md`
- Access to `scripness/cryptoli` for deliberate pinning during Milestone 4;
  the tracked pin created here is an output of this phase, not a prerequisite

## Repo Context

- Task source: `TODO.md` section `7. Add Full Evaluation Coverage`, plus the
  `AGENTS.md` command-table requirement to document exact commands when a phase
  introduces executable helpers or eval runners
- Owning code paths: tracked eval definitions belong with the skills they
  validate under `consult/evals/`, `execute/evals/`, `plan/evals/`,
  `specs/evals/`, `tests/evals/`, and `verify/evals/`; each skill should own
  its own `evals/evals.json` plus any tracked skill-local fixture prompts,
  grading notes, or rubric files that are specific to that skill
- Shared harness paths: `evals/README.md` owns the cross-skill artifact
  contract and regression-review procedure; `evals/runtime.json` owns the
  canonical runtime profile and future configuration surface;
  `evals/fixtures/cryptoli.json` owns the tracked `cryptoli` pin manifest; and
  `evals/scripts/` owns only the thinnest shared runner surface needed before
  Phase 06. Broader operator polish still belongs to Phase 06
- Generated artifact paths: generated outputs, temp workspaces, and cloned
  fixture repos must stay outside tracked source under a dedicated ignored root
  such as `.tmp/evals/`; the slice that introduces that root must also add the
  ignore coverage rather than relying on convention alone
- Owning spec paths: `AGENTS.md` is the authoritative workflow contract,
  including the Commands section that must name exact local runner commands
  once they exist; `README.md` is the shipped usage and maintenance surface;
  `TODO.md` remains roadmap truth and should only be updated here if shipped
  behavior would otherwise make its wording false or misleading
- Owning test paths: there is still no formal automated suite in this repo, so
  the applicable follow-through for this phase is definition validation,
  fixture-pin sanity checks, and smoke execution of any runner surface
  introduced; if Milestone 5 adds executable scripts, validators, or comparison
  helpers, add the smallest credible automated sanity layer and document its
  command before claiming completion
- Related docs or references:
  `plans/2026-04-14-phase-04-specs-and-tests-refresh.md`, `PROMPT_verify.md`,
  and the evaluation-governance bullets in `TODO.md` section `7`

## Sync Expectations

- `specs`: expected as part of this phase rather than optional after the fact.
  Milestones 1, 2, and 5 change durable repo truth about eval layout,
  acceptance policy, artifact review, and maintenance workflow, so sync
  `AGENTS.md` first, keep `README.md` aligned, and update any repo-truth docs
  that name runner commands or regression-review requirements before calling
  the phase complete.
- `tests`: required when Milestone 5 introduces executable runners, validators,
  or comparison helpers. The minimum acceptable follow-through is repeatable
  sanity coverage for runner entrypoints plus validation of tracked eval
  definitions and fixture-pin metadata; if a fuller automated layer is still
  deferred, record that blocker explicitly in the plan instead of silently
  treating ad hoc checks as enough.

## Milestones

1. Define the tracked eval layout, baseline comparison policy, artifact
   contract, runtime configuration surface, and generated-output root.
2. Define the governance layer explicitly:
   train/validation splits, repeated-run policy, grading protocol, pass/fail
   thresholds, must-run regression surface, and regression artifact review.
3. Add the first trigger and workflow eval definitions for the six-skill
   workflow under the owning `<skill>/evals/` paths.
4. Add the tracked pinned `cryptoli` real-repo fixture manifest at
   `evals/fixtures/cryptoli.json` and the first must-run regression cases.
5. Add the first repeatable local runner surface under `evals/scripts/`,
   document the exact commands in `AGENTS.md`, and document how regression
   results are reviewed in `evals/README.md`.

## Verification

- Confirm eval definitions live with the skills they validate.
- Confirm artifact outputs include enough detail to inspect regressions rather
  than only summarize them.
- Confirm generated outputs and temporary fixture workspaces stay outside
  tracked source under the dedicated ignored root.
- Confirm `cryptoli` is pinned for repeatability.
- Confirm the harness compares against previous-skill-version baselines and uses
  no-skill comparisons only where they add signal.
- Confirm train/validation splits, repeated trials, grading protocol, pass/fail
  thresholds, and the must-run regression surface are explicit rather than only
  implied.
- Confirm regression artifact review is required before accepting a skill
  change.
- Confirm the exact local eval-runner commands are documented in `AGENTS.md`
  once the runner surface exists.
- [2026-04-16] Re-read `AGENTS.md`, `README.md`, `TODO.md`, and this plan after
  the Milestone 1 edits and confirmed they now align on the tracked eval
  layout, baseline comparison policy, canonical runtime profile, and ignored
  `.tmp/evals/` generated-output root without claiming that runners or
  governance policy already ship.
- [2026-04-16] Ran
  `jq empty evals/runtime.json consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and it passed.
- [2026-04-16] Ran
  `rg -n 'Evaluation Harness|\\.tmp/evals|previous committed version|evals/runtime.json|<skill>/evals/evals.json' AGENTS.md README.md evals/README.md`
  and confirmed the repo-truth docs and shared harness contract describe the
  same Milestone 1 layout and baseline policy.
- [2026-04-16] Ran
  `find consult/evals execute/evals plan/evals specs/evals tests/evals verify/evals evals -maxdepth 2 -type f | sort`
  and confirmed the new tracked eval skeleton exists only at the intended
  Milestone 1 paths.
- [2026-04-16] Ran `git diff --check` after the Milestone 1 edits; it passed
  with no whitespace or patch-format issues.
- [2026-04-16] Re-read `AGENTS.md`, `README.md`, `TODO.md`, `evals/README.md`,
  `evals/runtime.json`, and this plan after the Milestone 2 edits and
  confirmed they now align on the shipped governance contract without claiming
  that concrete eval cases, pinned fixtures, or runner helpers already exist.
- [2026-04-16] Ran
  `jq empty evals/runtime.json consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and it passed after the Milestone 2 governance updates.
- [2026-04-16] Ran
  `rg -n 'Milestones 1 and 2|train splits|validation split|artifact review|governance|must-run' AGENTS.md README.md evals/README.md evals/runtime.json`
  and confirmed the repo-truth docs and machine-readable runtime metadata all
  describe the same Milestone 2 governance rules.
- [2026-04-16] Ran `git diff --check` after the Milestone 2 edits; it passed
  with no whitespace or patch-format issues.
- [2026-04-16] Re-read `README.md`, `evals/README.md`, the six
  `<skill>/evals/evals.json` files, and this plan after the Milestone 3 edits
  and confirmed they now align on the first concrete skill-local trigger and
  workflow definitions while still deferring pinned fixtures, must-run surface
  selection, and runner helpers to Milestones 4 and 5.
- [2026-04-16] Ran
  `jq empty consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json evals/runtime.json`
  and it passed after the Milestone 3 eval-definition edits.
- [2026-04-16] Ran
  `jq '{skill, status, trigger_packs: (.trigger_evals | length), workflow_cases: (.workflow_evals | length)}' consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and confirmed all six skills now carry two trigger packs and two workflow
  cases with `milestone_3_seeded` status.
- [2026-04-16] Ran
  `rg -n "Milestones 1 through 3|must-run surface|skill-local trigger and workflow|placeholder" README.md evals/README.md consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and confirmed the shared docs now describe Milestone 3 honestly and no
  shipped skill-local eval file still advertises placeholder-only state.
- [2026-04-16] Ran `git diff --check` after the Milestone 3 edits; it passed
  with no whitespace or patch-format issues.
- [2026-04-16] Repaired one follow-up Milestone 3 policy gap by re-reading
  `README.md`, `evals/README.md`, this plan, and the six
  `<skill>/evals/evals.json` files, then converting workflow comparison
  metadata from an unconditional flat list into required-vs-optional baselines
  so the default previous-version comparison stays explicit and no-skill
  baselines stay conditional.
- [2026-04-16] Ran
  `jq empty consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json evals/runtime.json`
  and it passed after the comparison-metadata repair.
- [2026-04-16] Ran
  `jq '.workflow_evals[] | {id, comparison_targets}' consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and confirmed every workflow eval now records `previous_committed_skill_version`
  as the required target while treating `no_skill_when_it_adds_signal` as an
  optional target with an explicit reason.
- [2026-04-16] Ran
  `rg -n 'optional_secondary_baseline|"required":|"optional":|materially clarifies' evals/README.md consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and confirmed the shared artifact-contract wording now matches the repaired
  skill-local metadata.
- [2026-04-16] Ran `git diff --check` after the comparison-metadata repair; it
  passed with no whitespace or patch-format issues.
- [2026-04-17] Queried
  `gh api repos/scripness/cryptoli/commits/main --jq '{sha: .sha, date: .commit.committer.date, message: .commit.message}'`
  and pinned the first official real-repo fixture to commit
  `5c634bd5018eba27b5d6881116d5328e287c03c3` from `2026-04-16T08:44:06Z`
  with commit message `Feat/seo optimization (#12)`.
- [2026-04-17] Queried `gh api repos/scripness/cryptoli/contents?ref=5c634bd5018eba27b5d6881116d5328e287c03c3`,
  `gh api repos/scripness/cryptoli/contents/pnpm-workspace.yaml?ref=5c634bd5018eba27b5d6881116d5328e287c03c3`,
  `gh api repos/scripness/cryptoli/contents/package.json?ref=5c634bd5018eba27b5d6881116d5328e287c03c3`,
  and `gh api repos/scripness/cryptoli/git/trees/5c634bd5018eba27b5d6881116d5328e287c03c3?recursive=1`
  and confirmed the pinned fixture is a three-app pnpm workspace with
  `apps/backend`, `apps/frontend`, `apps/admin`, root repo-truth docs,
  backend integration/e2e layers, and frontend/admin Vitest entrypoints.
- [2026-04-17] Ran
  `jq empty evals/runtime.json evals/fixtures/cryptoli.json consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and it passed after the Milestone 4 fixture and must-run edits.
- [2026-04-17] Ran
  `for f in consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json; do jq '{skill, validation_trigger_must_run: (.trigger_evals[] | select(.id | endswith("validation-boundary-pack")).must_run), cryptoli_case: (.workflow_evals[] | select(.id | contains("cryptoli")) | {id, must_run, fixture: .fixture.id})}' "$f"; done`
  and confirmed each shipped skill now marks its validation boundary trigger
  pack and one pinned `cryptoli` workflow case as `must_run: true`.
- [2026-04-17] Ran
  `rg -n 'Milestones 1 through 4|evals/fixtures/cryptoli.json|must-run surface|cryptoli-backed|validation boundary trigger pack' AGENTS.md README.md evals/README.md evals/runtime.json consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`
  and confirmed the repo-truth docs, shared harness contract, machine-readable
  runtime metadata, and skill-local eval definitions all describe the same
  shipped Milestone 4 state.
- [2026-04-17] Ran `git diff --check` after the Milestone 4 edits; it passed
  with no whitespace or patch-format issues.
- [2026-04-17] Followed up on fresh-session verification feedback that the new
  pinned fixture manifest was still untracked in the worktree, added
  `evals/fixtures/cryptoli.json` to Git, and re-ran
  `git ls-files --error-unmatch evals/fixtures/cryptoli.json` to confirm the
  Milestone 4 fixture now exists as tracked source instead of only as a local
  file.
- [2026-04-17] Re-read `AGENTS.md`, `README.md`, `evals/README.md`, and this
  plan after the Milestone 5 edits and confirmed they now align on the shipped
  thin runner surface: tracked-harness validation, repeatable run scaffolding
  under `.tmp/evals/<run-id>/`, exact local commands in `AGENTS.md`, and
  review starting from a generated `review-template.md`.
- [2026-04-17] Ran `python3 -m py_compile evals/scripts/harness.py` and it
  passed.
- [2026-04-17] Ran `python3 evals/scripts/harness.py validate` and it passed,
  reporting 6 shipped skills, 12 trigger packs, 18 workflow cases, and 1
  pinned fixture manifest after checking runtime, skill-local eval, must-run,
  and ignore-coverage invariants.
- [2026-04-17] Ran
  `python3 evals/scripts/harness.py init-run --run-id milestone-5-smoke --selection must-run`,
  `git check-ignore -v .tmp/evals/milestone-5-smoke/run.json`, and
  `jq '{run_id, profile, selected_cases: (.selected_cases | length), fixtures}' .tmp/evals/milestone-5-smoke/run.json`;
  they confirmed the smoke workspace is ignored, the scaffolded run manifest
  selects the 12 current must-run cases, and the pinned `cryptoli` fixture is
  projected into `.tmp/evals/milestone-5-smoke/fixtures/cryptoli`.
- [2026-04-17] Ran
  `rg -n 'harness.py|init-run --run-id|Milestones 1 through 5|review-template.md|Validate tracked eval definitions' AGENTS.md README.md evals/README.md`
  and confirmed the repo-truth docs now describe the same Milestone 5 helper
  surface and review flow.
- [2026-04-17] Ran `git diff --check` after the Milestone 5 edits; it passed
  with no whitespace or patch-format issues.

## Risks

- Building a harness that looks rigorous but still leaves too much room for
  unreviewed drift.
- Making the initial harness too heavy before the six-skill system stabilizes.
- Mixing runtime/provider changes into skill comparisons and corrupting the
  signal.

## Open Questions

- None currently.

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3
- [x] Milestone 4
- [x] Milestone 5

Milestone 1 note:

- Added the shared harness skeleton at repo root with `evals/README.md`,
  `evals/runtime.json`, and the ignored `.tmp/evals/` generated-output root.
- Added placeholder `evals/evals.json` entrypoints under each shipped skill so
  the tracked layout is defined without pulling real eval cases forward from
  Milestone 3.
- Synced `AGENTS.md` and `README.md` so repo truth now describes the eval
  layout, artifact contract, and default baseline policy honestly.

Milestone 2 note:

- Expanded `evals/README.md` from a layout-only contract into the explicit
  governance source of truth for split policy, repeated trials, grading modes,
  pass/fail thresholds, must-run surface rules, and regression artifact review.
- Extended `evals/runtime.json` with matching machine-readable governance
  defaults so later runner work can enforce the same policy without inventing a
  second source of truth.
- Synced `AGENTS.md` and `README.md` so repo-facing docs now describe the
  shipped governance contract honestly while still deferring concrete eval
  cases, pinned fixtures, and runner helpers to later milestones.

Milestone 3 note:

- Replaced the six placeholder `<skill>/evals/evals.json` entrypoints with the
  first concrete trigger and workflow definitions, using paired train and
  validation trigger packs plus two workflow cases per shipped skill.
- Encoded boundary-focused trigger near-misses and workflow comparison targets
  directly in the tracked definitions so later runner work does not need to
  guess baseline-vs-with-skill intent or the intended skill boundaries.
- After follow-up verification found the no-skill baseline policy was still too
  implicit, refined the workflow comparison metadata so previous-version
  baselines are required while no-skill baselines remain explicitly optional
  and justified per case.
- Kept every Milestone 3 case non-must-run so Milestone 4 still owns the first
  pinned-fixture and must-run surface decisions.
- Synced `README.md` and `evals/README.md` so repo-facing docs now describe
  the shipped first-case state honestly while still deferring pinned fixtures
  and runner helpers to later milestones.

Milestone 4 note:

- Added `evals/fixtures/cryptoli.json` as the first tracked real-repo fixture
  manifest, pinning `scripness/cryptoli` to commit
  `5c634bd5018eba27b5d6881116d5328e287c03c3` and recording its three-app pnpm
  workspace shape plus sanity-check paths.
- Promoted the validation boundary trigger pack for each shipped skill into the
  initial must-run trigger surface and added one pinned `cryptoli`
  validation workflow case per skill as the initial must-run real-repo surface.
- Synced `AGENTS.md`, `README.md`, `evals/README.md`, and `evals/runtime.json`
  so repo-facing docs and machine-readable defaults now describe the pinned
  fixture and the selected must-run surface honestly while still deferring the
  runnable helper surface to Milestone 5.
- Closed the follow-up repo-state gap from verification by adding
  `evals/fixtures/cryptoli.json` to tracked source, so the pinned fixture
  manifest now ships with the rest of the Milestone 4 harness changes.

Milestone 5 note:

- Added `evals/scripts/harness.py` as the first shared runner entrypoint with
  two thin commands: `validate` for tracked-harness invariants and `init-run`
  for repeatable local run scaffolding under `.tmp/evals/<run-id>/`.
- Made the scaffolded run workspace explicit with `run.json`,
  `review-template.md`, `outputs/`, `transcripts/`, and `fixtures/` so future
  manual or automated runs have one predictable generated layout.
- Synced `AGENTS.md`, `README.md`, and `evals/README.md` so repo truth now
  documents the exact local commands, the thin-helper scope boundary, and the
  regression-review flow honestly.

## Decision Log

- [2026-04-14] Use `codex` + `gpt-5.4` + `xhigh` as the initial canonical eval
  runtime, but keep it intentionally configurable later.
- [2026-04-16] Define the per-skill eval layout in Milestone 1 with placeholder
  `<skill>/evals/evals.json` entrypoints instead of real cases so the repo can
  ship the storage contract now without collapsing Milestones 1 and 3.
- [2026-04-16] Keep the baseline comparison policy and generated-output root in
  repo-facing docs now, but defer split policy, repeated runs, thresholds, and
  must-run governance to Milestone 2 as planned.
- [2026-04-16] Encode the Milestone 2 governance contract in both
  `evals/README.md` and `evals/runtime.json` so human review and future runner
  defaults stay aligned.
- [2026-04-16] Apply the initial repeated-run policy to every must-run
  validation case, not only a hand-picked subset, so the first gating surface
  stays simple and honest.
- [2026-04-16] Define the must-run surface contract in Milestone 2 even before
  Milestones 3 and 4 populate the concrete cases, so later slices inherit an
  explicit governance target instead of inventing one ad hoc.
- [2026-04-16] Seed every shipped skill with the same initial Milestone 3
  shape: one train trigger pack, one validation trigger pack, one train
  workflow case, and one validation workflow case, so split policy and
  boundary coverage are explicit before runner tooling exists.
- [2026-04-16] Leave every Milestone 3 eval with `must_run: false` even on the
  validation split so Milestone 4 can make the first deliberate must-run
  surface decision alongside the pinned `cryptoli` fixture.
- [2026-04-16] Record workflow `comparison_targets` in the skill-local
  definitions now, including optional `no_skill_when_it_adds_signal`, so later
  runner work inherits the baseline-vs-with-skill intent instead of inferring
  it ad hoc.
- [2026-04-16] Distinguish required comparison targets from optional ones in
  the skill-local eval definitions so future runner work can honor the default
  previous-version baseline while adding no-skill baselines only when the case
  explicitly says they add signal.
- [2026-04-17] Pin the first official real-repo fixture to the current
  `scripness/cryptoli` `main` commit instead of an older historical snapshot so
  the harness captures the monorepo shape actually used during the Phase 04
  design work while remaining repeatable from one explicit commit.
- [2026-04-17] Select the initial must-run surface as the validation boundary
  trigger pack for each shipped skill plus one pinned `cryptoli` validation
  workflow case per skill, leaving the older generic validation workflow cases
  available as non-must-run comparison fixtures.
- [2026-04-17] Reference `evals/fixtures/cryptoli.json` from the skill-local
  real-repo workflow cases and mirror the selected case ids in
  `evals/runtime.json` so future runner work can reuse one shared fixture
  manifest instead of duplicating repo metadata per skill.
- [2026-04-17] Keep the first runner surface as one
  `evals/scripts/harness.py` entrypoint with `validate` and `init-run`
  subcommands so the phase ships repeatable local validation and run
  scaffolding without pretending model execution or grading is already
  automated.
- [2026-04-17] Generate `review-template.md` alongside each scaffolded
  `run.json` so artifact review stays explicit and repeatable without
  inventing a new tracked review system before broader tooling exists.

## Discoveries

- [2026-04-14] Without concrete eval artifacts and pinned fixtures, skill drift
  is too easy to miss or misattribute to provider/runtime changes.
- [2026-04-16] This repo had no existing ignore coverage, so introducing the
  generated eval root required adding repo-level `.gitignore` coverage in the
  same slice rather than relying on convention alone.
- [2026-04-16] The governance layer needed a durable place for review
  dispositions before tooling exists; allowing the plan, PR, or equivalent
  change record keeps the review requirement honest without inventing a new
  tracked artifact prematurely.
- [2026-04-16] Once concrete eval cases existed, the shared eval docs needed a
  small repo-truth sync even though the main Milestone 3 deliverable lived in
  skill-local JSON; otherwise the repo would keep implying that all concrete
  cases were still future work.
- [2026-04-16] A simple shared seed shape across all six skill-local
  `evals/evals.json` files is enough to express split policy, boundary
  coverage, and baseline intent without introducing runner-specific metadata
  early.
- [2026-04-16] A flat `comparison_targets` list was not enough to preserve the
  conditional no-skill-baseline policy; the tracked definitions needed to
  distinguish required and optional baselines explicitly to avoid pushing that
  decision back onto future runner code.
- [2026-04-17] Real-repo eval definitions need to separate pinned fixture facts
  from harness-injected task context such as temporary plan files, stale-doc
  branches, or candidate diffs; a shared fixture manifest plus skill-local
  scenario state is enough to express that boundary before runner tooling
  exists.
- [2026-04-17] `cryptoli` already exposes enough durable repo truth and layered
  test topology at one pinned commit to stress repo-truth, test-truth, and
  plan/execute/verify workflows from a single monorepo fixture.
- [2026-04-17] A generated `run.json` plus `review-template.md` is enough to
  bridge tracked eval intent and ignored run artifacts in Phase 05; the repo
  can now stage repeatable regression work without needing a full executor yet.

## Blockers

- None currently.

## Outcomes / Retrospective

- Milestones 1 through 5 completed by defining the tracked eval layout, the
  shared artifact-storage contract, the canonical runtime profile, the ignored
  generated-output root, the explicit governance and regression-review
  contract, the first concrete skill-local trigger and workflow cases, the
  first pinned real-repo fixture, the initial must-run surface, and the first
  thin local runner helpers with documented commands and repeatable run
  scaffolding.

## Follow-up verification repair

- [2026-04-16] Fresh verification found one remaining Milestone 1 repo-truth
  sync gap: `evals/README.md` described the tracked eval layout but did not
  explicitly say that each `<skill>/evals/evals.json` is hand-authored tracked
  input rather than generated output.
- [2026-04-16] Added that missing contract rule to `evals/README.md` so the
  shipped artifact contract now matches `TODO.md`'s Milestone 1 intent and the
  plan's completion claim.
- [2026-04-16] Re-ran
  `jq empty evals/runtime.json consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`,
  `git check-ignore -v .tmp/evals/example-run/artifact.json`,
  `git diff --check`, and
  `rg -n "author each <skill>/evals/evals.json|Evaluation Harness|\\.tmp/evals|previous committed version|evals/runtime.json|<skill>/evals/evals.json" AGENTS.md README.md evals/README.md TODO.md plans/2026-04-14-phase-05-evaluation-harness.md`;
  they passed or confirmed the repaired contract wording.
- [2026-04-16] Fresh verification then found one remaining Milestone 3 policy
  gap: every workflow eval still listed `no_skill_when_it_adds_signal`
  alongside the default previous-version baseline in one flat
  `comparison_targets` list, which left future runner work to guess whether the
  extra baseline was actually required.
- [2026-04-16] Reworked the six skill-local eval definitions so workflow
  comparison metadata now distinguishes required and optional baselines, keeps
  `previous_committed_skill_version` as the required default, and records a
  short per-case reason whenever `no_skill_when_it_adds_signal` is available as
  an optional comparison.
- [2026-04-16] Added the matching artifact-contract rule to `evals/README.md`
  and re-ran `jq empty`, `jq '.workflow_evals[] | {id, comparison_targets}'`,
  `rg -n 'optional_secondary_baseline|"required":|"optional":|materially clarifies' evals/README.md consult/evals/evals.json execute/evals/evals.json plan/evals/evals.json specs/evals/evals.json tests/evals/evals.json verify/evals/evals.json`,
  and `git diff --check`; they passed and confirmed the repaired baseline
  policy is now explicit in tracked repo truth.
- [2026-04-17] Fresh verification found two remaining Milestone 5 gaps: the
  new validator did not yet enforce the shipped rule that all pinned real-repo
  fixture workflow cases join the must-run surface by default, and the
  `python3 -m py_compile evals/scripts/harness.py` smoke check left generated
  `__pycache__` bytecode outside the intended `.tmp/evals/` artifact root.
- [2026-04-17] Updated `evals/scripts/harness.py` so any workflow eval that
  references a pinned fixture manifest must set `must_run: true`, added
  repo-level ignore coverage for local `__pycache__/`, and removed the
  generated bytecode created during verification.
- [2026-04-17] Re-ran
  `python3 evals/scripts/harness.py validate`,
  `python3 evals/scripts/harness.py init-run --run-id milestone-5-repair-smoke --selection must-run`,
  `git check-ignore -v .tmp/evals/milestone-5-repair-smoke/run.json`,
  `python3 evals/scripts/harness.py init-run --run-id milestone-5-repair-verify --selection validation --skill verify`,
  `find evals/scripts -maxdepth 2 -type f | sort`, and
  `git diff --check`; they passed and confirmed the repaired Milestone 5
  validator contract, helper surface, and repo hygiene.
