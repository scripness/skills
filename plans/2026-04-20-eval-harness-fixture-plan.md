# Eval Harness Fixture Plan

This file is a neutral tracked fixture used by skill evals that need a real
`plans/*.md` input. It is not the active plan for current repo work.

## Goal

Carry one explicit follow-up plan for evaluation-harness cleanup and helper
documentation so execute, plan, and verify evals can judge real plan-driven
behavior.

## Scope

- Keep the live repo-truth layer aligned with the shipped harness surface.
- Remove stale historical framing from secondary docs and helper text.
- Keep the harness helper surface thin and documented accurately.

## Non-Goals

- Rebuilding the harness from scratch.
- Rewriting the six shipped skills.
- Replacing the optional helper with required orchestration.

## Deliverables

- Synced repo-truth docs for the harness surface.
- Updated helper-facing docs and commands where needed.
- A plan that remains resumable for a later fresh session.

## Repo Context

- Owning code paths: `evals/`, `Makefile`, `src/execute/scripts/loop.py`
- Owning spec paths: `AGENTS.md`, `README.md`, `specs/evaluation-harness.md`
- Owning test paths: `N/A`; use bounded maintenance checks only

## Dependencies

- `AGENTS.md`
- `README.md`
- `evals/fixtures/eval-harness-roadmap.md`

## Sync Expectations

- `specs`: Required when repo-truth or harness docs change.
- `tests`: Only required if executable helper behavior changes.

## Milestones

1. Confirm the shipped harness surface and sync the owning repo-truth docs.
2. Define or refine the helper-facing maintenance commands and documentation.
3. Replace stale secondary-doc framing and neutralize legacy fixture coupling.
4. Leave a clean verify handoff for the next fresh session.

## Verification

- Run `make validate`.
- Run `git diff --check`.
- Read the changed repo-truth docs against the shipped harness files.

## Blockers

- None currently.

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4

## Decision Log

- [2026-04-20] Keep the helper thin and file-backed.

## Discoveries

- [2026-04-20] The shipped harness already supports validation plus run
  scaffolding; the remaining work is cleanup and follow-through.

## Outcomes / Retrospective

- Pending.
