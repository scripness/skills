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

## Risks

- Building a harness that looks rigorous but still leaves too much room for
  unreviewed drift.
- Making the initial harness too heavy before the six-skill system stabilizes.
- Mixing runtime/provider changes into skill comparisons and corrupting the
  signal.

## Open Questions

- How much of the grading should be automated assertions versus reviewer rubric
  in the first version?
- Should the initial repeated-run policy apply to every must-run case or only to
  the highest-signal cases first?

## Progress

- [x] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4
- [ ] Milestone 5

Milestone 1 note:

- Added the shared harness skeleton at repo root with `evals/README.md`,
  `evals/runtime.json`, and the ignored `.tmp/evals/` generated-output root.
- Added placeholder `evals/evals.json` entrypoints under each shipped skill so
  the tracked layout is defined without pulling real eval cases forward from
  Milestone 3.
- Synced `AGENTS.md` and `README.md` so repo truth now describes the eval
  layout, artifact contract, and default baseline policy honestly.

## Decision Log

- [2026-04-14] Use `codex` + `gpt-5.4` + `xhigh` as the initial canonical eval
  runtime, but keep it intentionally configurable later.
- [2026-04-16] Define the per-skill eval layout in Milestone 1 with placeholder
  `<skill>/evals/evals.json` entrypoints instead of real cases so the repo can
  ship the storage contract now without collapsing Milestones 1 and 3.
- [2026-04-16] Keep the baseline comparison policy and generated-output root in
  repo-facing docs now, but defer split policy, repeated runs, thresholds, and
  must-run governance to Milestone 2 as planned.

## Discoveries

- [2026-04-14] Without concrete eval artifacts and pinned fixtures, skill drift
  is too easy to miss or misattribute to provider/runtime changes.
- [2026-04-16] This repo had no existing ignore coverage, so introducing the
  generated eval root required adding repo-level `.gitignore` coverage in the
  same slice rather than relying on convention alone.

## Blockers

- None currently.

## Outcomes / Retrospective

- Milestone 1 completed by defining the tracked eval layout, the shared
  artifact-storage contract, the canonical runtime profile, and the ignored
  generated-output root. Milestones 2 through 5 remain pending.

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
