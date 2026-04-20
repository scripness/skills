# Repo Truth Refinement Cleanup

Use this file as the living plan for post-merge repo-truth cleanup. Historical
Phase 00-06 records remain available as background source material, but this
plan owns the current refinement work.

## Goal

Rebuild the live repo-truth surface from the shipped repo state so a fresh
agent can understand and use this repo without treating the completed
2026-04-14 phase plans as default operational truth.

## Scope

- Rewrite `AGENTS.md` from current shipped reality.
- Create top-level `specs/` as durable repo truth for this repo.
- Rewrite `README.md` so it describes the shipped system rather than the
  historical build process.
- Demote historical build-plan references from live surfaces where they still
  read like current workflow truth.
- Replace remaining eval dependencies on historical build-plan files only in a
  later slice.

## Non-Goals

- Changing the shipped skill contracts under `src/` in this slice.
- Rewriting skill-local eval definitions in this slice unless repo-truth
  cleanup proves that strictly necessary.
- Inventing new helpers or changing the optional helper contract in
  `src/execute/scripts/plan_loop.py`.

## Deliverables

- A rewritten `AGENTS.md` that points default reading at shipped repo truth.
- A new top-level `specs/` tree that documents the shipped repo contract.
- A rewritten `README.md` aligned with the shipped system.
- An updated plan recording slice status, discoveries, checks, and the next
  verify handoff target.

## Repo Context

- Task source: user request on branch `refine-01` to rebuild live repo truth
  from shipped reality.
- Owning code paths: `AGENTS.md`, `README.md`, `specs/`, `src/`, `evals/`,
  `Makefile`, `src/execute/scripts/plan_loop.py`
- Owning spec paths: `specs/README.md`, `specs/workflow-contract.md`,
  `specs/repo-surface.md`, `specs/evaluation-harness.md`
- Owning test paths: `N/A` for product tests; use repo maintenance checks only
  for this slice.
- Related docs and commands: `MAINTENANCE.md`, `SOURCES.md`, `REFINE.md`,
  `make validate`

## Dependencies

- The shipped repo surface under `src/`, `evals/`, `Makefile`, and
  `src/execute/scripts/plan_loop.py`
- Historical `plans/2026-04-14-phase-*.md` files only as background source
  material when needed

## Sync Expectations

- `specs`: Required in Milestone 1. Create top-level specs that own repo
  workflow, shipped surface, and evaluation-harness truth.
- `tests`: No test-truth sync is expected in this slice because no product
  behavior or executable harness logic is changing. Run the smallest meaningful
  repo maintenance checks against the edited surface and report limits
  honestly.

## Milestones

1. Rebuild live repo truth: rewrite `AGENTS.md`, create top-level `specs/`,
   and rewrite `README.md` from shipped reality so historical phase plans are
   no longer default required reading.
2. Demote remaining historical references from live docs and helper text where
   they still read like operational truth while keeping valid generic
   `plans/*.md` workflow references intact.
3. Replace eval coupling to historical build-plan files and decide the longer
   archive policy for completed build records.

## Verification

- [2026-04-20] Inspected the rewritten truth layer against shipped files under
  `src/`, `evals/`, `Makefile`, and `src/execute/scripts/plan_loop.py`.
- [2026-04-20] `rg -n "Phase 00|Phase 01|Phase 02|Phase 03|Phase 04|Phase 05|Phase 06|plans/2026-04-14-phase" AGENTS.md README.md specs`
  returned only intentional background-record mentions.
- [2026-04-20] `make validate` passed.
- [2026-04-20] `git diff --check` passed.
- [2026-04-20] `test -L CLAUDE.md && readlink CLAUDE.md` confirmed
  `CLAUDE.md -> AGENTS.md`.

## Risks

- The new top-level specs may drift into repeating `AGENTS.md` and `README.md`
  instead of owning distinct durable topic truth.
- Historical references still embedded in eval definitions may keep leaking
  obsolete framing into later refinement work.
- Over-correcting could flatten genuinely useful generic `plans/*.md`
  workflow references that the shipped `plan` and `execute` contracts still
  require.

## Open Questions

- Should `evals/README.md` and `Makefile` historical wording move in Milestone
  2 or wait until the eval-coupling cleanup slice?
- Should completed 2026-04-14 build records remain under `plans/` long term or
  move to an archive location later?

## Blockers

- None currently.

## Progress

- [x] Milestone 1: rebuild live repo truth
- [ ] Milestone 2: demote remaining historical live-surface references
- [ ] Milestone 3: replace eval coupling and decide archive policy

## Decision Log

- [2026-04-20] Use a new explicit refinement plan file rather than treating
  `REFINE.md` or the completed phase records as the active plan for this work.
- [2026-04-20] Create three top-level specs for the shipped repo surface:
  `workflow-contract.md`, `repo-surface.md`, and `evaluation-harness.md`.

## Discoveries

- [2026-04-20] The shipped repo already includes
  `src/execute/scripts/plan_loop.py`; the current gap is repo-truth cleanup,
  not missing helper invention.
- [2026-04-20] Top-level `specs/` does not exist yet even though the shipped
  workflow expects durable repo truth to live there.
- [2026-04-20] The highest-signal remaining historical references now live in
  `evals/README.md`, `Makefile`, and several skill-local `evals/evals.json`
  files rather than in the main repo-truth docs.

## Outcomes / Retrospective

- [2026-04-20] Completed Milestone 1 by rewriting `AGENTS.md`, creating
  top-level `specs/`, and rewriting `README.md` from shipped repo reality.
- Next verify target: implementation review of `AGENTS.md`, `README.md`,
  `specs/README.md`, `specs/workflow-contract.md`,
  `specs/repo-surface.md`, and `specs/evaluation-harness.md` against
  `plans/2026-04-20-refine-repo-truth-cleanup.md`, `src/`, `evals/`,
  `Makefile`, and `src/execute/scripts/plan_loop.py`.
