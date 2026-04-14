# Phase 04: Specs And Tests Refresh

## Goal

Refresh `specs` and `tests` so they prepare real-world repos for reliable
agentic work across different topologies, including monorepos and mixed stacks,
without hardcoded layout assumptions.

## Scope

- Strengthen `specs` around codebase organization quality, topology discovery,
  and durable repo-truth ownership.
- Strengthen `tests` around test-topology discovery, honest coverage
  expectations, and sync/bootstrap behavior.
- Use `cryptoli` as a real-world reference shape for the design, without turning
  this phase into the full eval harness.

## Non-Goals

- Building the formal eval harness or local runners.
- Building the helper loop scripts.
- Reworking `consult` or `verify` except where minor alignment is required.

## Owned TODO Sections

- The `specs` and `tests` parts of `5. Improve The Six Core Skills`
- The relevant cross-cutting source-grounding work from `6. Ground The Skills In
  Official Sources`

## Deliverables

- Updated `specs/SKILL.md`
- Updated `tests/SKILL.md`
- Updated `specs/assets/*` if the repo-truth bootstrap templates need to match
  the refreshed contract
- Minimal doc sync if the shipped behavior changes current truth

## Dependencies

- Delivered contracts for `plan` and `execute`
- Existing `README.md`, `TODO.md`, and `specs/assets/*`
- Real-world reference understanding from `scripness/cryptoli`

## Sync Expectations

- `specs`: this phase directly changes repo-truth guidance and bootstrap assets,
  so minimal truth sync is expected as part of the deliverable.
- `tests`: this phase directly changes test-truth guidance; if templates,
  examples, or executable validation surfaces are introduced, sync them before
  considering the phase complete.

## Milestones

1. Refresh `specs` for repo-topology discovery, agentic-readiness evaluation,
   and proportional organization guidance.
2. Refresh `tests` for test-topology discovery, layered coverage expectations,
   and honest gap reporting across repo shapes.
3. Update any shipped bootstrap assets that now drift from the refreshed skill
   behavior.
4. Sync docs minimally so the shipped truth matches the refreshed behavior.

## Verification

- Confirm `specs` does not assume a single-app `src/` layout.
- Confirm `tests` does not assume one stack, one suite location, or one layer.
- Confirm both skills ignore vendor/generated noise by default.
- Confirm the refreshed guidance still keeps code as the ultimate source of
  truth and uses docs/tests as synchronized truth layers.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4

## Decision Log

- [2026-04-14] Treat `cryptoli` as the primary real-world monorepo reference for
  shaping `specs` and `tests`.

## Discoveries

- [2026-04-14] The biggest practical risk for `specs` and `tests` is naive path
  discovery that gets polluted by `node_modules`, build outputs, and copied
  artifacts.

