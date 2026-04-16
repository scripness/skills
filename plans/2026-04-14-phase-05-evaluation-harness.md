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

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4
- [ ] Milestone 5

## Decision Log

- [2026-04-14] Use `codex` + `gpt-5.4` + `xhigh` as the initial canonical eval
  runtime, but keep it intentionally configurable later.

## Discoveries

- [2026-04-14] Without concrete eval artifacts and pinned fixtures, skill drift
  is too easy to miss or misattribute to provider/runtime changes.

## Outcomes / Retrospective

- Pending.
