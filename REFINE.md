# REFINE

This file tracks post-merge refinement work for the repo.

## Current State

This branch is a post-merge cleanup branch. The initial six-skill system is
already shipped.

Current shipped repo surface:

- six skills under `src/`: `consult`, `execute`, `plan`, `specs`, `tests`,
  `verify`
- live top-level docs: `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `SOURCES.md`
- repo support surface: `Makefile`, `evals/`, and the shared harness helper at
  `evals/scripts/harness.py`
- optional execute/verify loop helper:
  `src/execute/scripts/plan_loop.py`
- historical build records under `plans/`:
  - `plans/2026-04-14-phase-00-design-doc.md`
  - `plans/2026-04-14-phase-01-plan-skill-and-contract.md`
  - `plans/2026-04-14-phase-02-execute-skill.md`
  - `plans/2026-04-14-phase-03-consult-and-verify-refresh.md`
  - `plans/2026-04-14-phase-04-specs-and-tests-refresh.md`
  - `plans/2026-04-14-phase-05-evaluation-harness.md`
  - `plans/2026-04-14-phase-06-tooling-and-final-docs.md`

Current refinement problem:

- the build is complete, but some top-level docs still surface the historical
  Phase 00-06 files too prominently
- durable repo-truth docs under top-level `specs/` do not exist yet and need
  to be created from shipped reality
- some eval cases still use the historical phase files as convenient fixture
  inputs
- this file previously mixed that cleanup work with stale notes that treated
  the optional helper loop as not yet shipped

Intended steady state after refinement:

- live operational truth: `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `SOURCES.md`, top-level `specs/`, `src/`, and `evals/`
- future task-local state: explicit `plans/*.md` files created for new work
- completed Phase 00-06 files: historical background only, not default
  required reading
- helper notes, if kept here, describe the shipped helper truth and any real
  remaining gaps instead of describing a missing script

## Current Refinement Plan

Rebuild live repo truth first, then remove or replace the remaining references
to historical build plans.

Recommended sequence:

1. Rebuild live repo truth with `specs`.
   - Rewrite `AGENTS.md` from current shipped reality.
   - Create `specs/` from scratch as durable topic truth.
   - Rewrite `README.md` so it describes the shipped system, not the build
     history.
   - Use the historical phase plans only as background source material, not as
     current truth.
2. Demote historical Phase 00-06 files out of the live surface.
   - Remove top-level doc references that make the completed phase plans look
     like required reading.
   - Keep generic `plans/*.md` workflow references only where they are still
     part of the shipped `plan` and `execute` contracts.
3. Replace eval coupling to historical phase plans.
   - Inventory eval cases that currently use Phase 00-06 files as fixtures.
   - Replace those inputs with neutral fixture plan files where plan artifacts
     are still needed for testing.
   - Delete historical-plan eval references that are no longer serving a real
     test purpose.
4. Decide archive policy for the completed build plans.
   - Either keep them in `plans/` as clearly historical records, move them to
     an archive location later, or trim them once they are no longer needed.
5. Only after repo-truth cleanup, decide whether any helper follow-up is worth
   doing.
   - Treat `src/execute/scripts/plan_loop.py` as the current shipped helper
     surface.
   - Any later helper work should extend that script or replace it
     deliberately, not pretend the helper surface does not exist yet.

Success criteria for this refinement:

- `AGENTS.md`, `README.md`, and `specs/` are sufficient to understand and use
  the repo safely.
- Historical Phase 00-06 files are no longer part of the default operational
  reading chain.
- Evals do not depend on historical build-plan files unless that dependency is
  explicitly intentional and justified as fixture data.
- This file no longer claims the helper loop is missing when the repo already
  ships `src/execute/scripts/plan_loop.py`.

## Shipped Helper Reality

The repo already ships `src/execute/scripts/plan_loop.py` as an optional thin
wrapper for plan-driven work. It is already part of the documented maintenance
surface in `AGENTS.md`, `README.md`, `MAINTENANCE.md`, and `make help`.

Current helper contract:

- take one explicit `plans/*.md` path
- take one explicit non-interactive external runner command
- support `--dry-run`, `--yes`, `--max-iterations`, and optional continue on
  `pass_with_risks`
- run `execute -> verify` loops while the plan stays valid and the verify
  verdict remains acceptable
- stop on blocked or invalid plan state, unacceptable verify verdict, missing
  plan update, runner failure, or max iterations

Current baseline workflow still remains:

- manual or prompt-driven fresh sessions
- `execute`
- `verify`
- human decides the next step

## Real Remaining Helper Gap

If helper work is revisited later, the missing piece is not "create the first
helper." The real remaining delta is:

1. Persist failed `verify` outputs as durable plan-scoped artifacts.
2. Start a fresh remediation `execute` run automatically after `verify=fail`.
3. Pass the latest failed verify artifact into that remediation run without
   guessing paths or state.
4. Re-run fresh `verify` after remediation and stop on repeated or conflicting
   failures.
5. Keep `verify` as a verifier only; do not let it patch code directly.

Guardrails for any future helper follow-up:

- optional
- file-backed
- explicit-plan-path only
- non-interactive by default
- honest about failure and stop conditions
- bounded so scope does not widen beyond the current milestone

## Reference Grounding

Future refinement work should keep essential references in this repo so both
users and fresh agents can recover the best-practice context from repo truth
alone.

That means:

- store the canonical source list in a stable in-repo location rather than
  only in plans, prompts, or chat
- make it obvious where to look for the repo's guiding best practices
