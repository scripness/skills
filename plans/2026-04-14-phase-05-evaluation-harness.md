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

## Non-Goals

- Final maintenance-interface polish.
- Broad CI rollout before the local loop is usable.
- Rewriting the skills themselves unless an eval surfaces a concrete gap.

## Owned TODO Sections

- `7. Add Full Evaluation Coverage`

## Deliverables

- Per-skill `<skill>/evals/` tracked definitions
- Initial eval artifact contract and storage conventions
- Pinned `cryptoli` fixture reference for real-repo evals
- Repeatable local eval runners or the first thin scaffolding required to run
  them

## Dependencies

- Delivered or mostly stable versions of all six skills
- Existing `README.md` and `TODO.md`
- Pinned reference to `scripness/cryptoli`

## Sync Expectations

- `specs`: required if the eval harness changes durable repo truth about how
  skills are maintained or accepted.
- `tests`: required if the harness introduces executable behavior, validators, or
  comparison scripts that should themselves be covered or sanity-checked.

## Milestones

1. Define the tracked eval layout, baseline comparison policy, artifact
   contract, and runtime configuration surface.
2. Add the first trigger and workflow eval definitions for the six-skill
   workflow.
3. Add the pinned `cryptoli` real-repo fixture handling and must-run regression
   cases.
4. Add the first repeatable local runner surface and document how regression
   results are reviewed.

## Verification

- Confirm eval definitions live with the skills they validate.
- Confirm artifact outputs include enough detail to inspect regressions rather
  than only summarize them.
- Confirm `cryptoli` is pinned for repeatability.
- Confirm the harness compares against previous-skill-version baselines and uses
  no-skill comparisons only where they add signal.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4

## Decision Log

- [2026-04-14] Use `codex` + `gpt-5.4` + `xhigh` as the initial canonical eval
  runtime, but keep it intentionally configurable later.

## Discoveries

- [2026-04-14] Without concrete eval artifacts and pinned fixtures, skill drift
  is too easy to miss or misattribute to provider/runtime changes.

