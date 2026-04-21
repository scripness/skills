# Continuous Plan Loop

Use this file as the living plan for the continuous execute/verify loop
follow-up. The goal is one opt-in helper run that can carry plan-driven work
through bounded execution slices, verification after each slice, repairable
verification failures, and a strict final completion review.

## Goal

Extend the optional `src/execute/scripts/plan_loop.py` helper and the owning
skill contracts so one explicit plan-driven run can continue safely until the
plan is truly complete: each slice is executed and verified, repairable verify
failures are fed back into the same plan for another bounded execute pass, and
the loop only exits successfully after a strict final whole-plan verification
pass.

## Scope

- Define the continuous-loop contract across `execute`, `verify`, and the
  helper.
- Implement opt-in continue-after-fail behavior in `plan_loop.py` while
  keeping the helper dumb and file-backed.
- Add strict final review semantics that require a final whole-plan `verify`
  pass before the helper can succeed.
- Define how repairable and blocking verify failures affect `Progress`,
  `Blockers`, and final follow-up milestones in the plan file.
- Sync repo-truth docs and tracked eval metadata to the implemented behavior.
- Verify the helper with bounded repo checks and targeted synthetic smoke runs.

## Non-Goals

- Making continuous fail-recovery the default helper behavior.
- Teaching the helper to parse model prose or infer fixes outside plan state and
  exit codes.
- Replacing the six-skill split with provider-specific orchestration.
- Building a general-purpose automated test framework for helper scripts beyond
  what this repo already ships.

## Deliverables

- An updated `src/execute/scripts/plan_loop.py` with opt-in continuous repair
  flow and strict final review.
- Updated `src/execute/SKILL.md`, `src/verify/SKILL.md`, and any plan-template
  wording needed to keep plan semantics truthful.
- Synced repo-truth docs and eval metadata for the new helper behavior.
- Verification notes in this plan covering command-based checks and synthetic
  runner smoke evidence.

## Repo Context

- Task source: user request on branch `refine-01` to make the helper
  continuous so one run can carry execution plus verification through full
  plan completion.
- Owning code paths: `src/execute/scripts/plan_loop.py`,
  `src/execute/SKILL.md`, `src/verify/SKILL.md`,
  `src/plan/assets/plan-template.md`, `src/*/agents/openai.yaml`,
  `src/*/evals/evals.json`
- Owning spec paths: `AGENTS.md`, `README.md`,
  `specs/workflow-contract.md`, `specs/repo-surface.md`, `REFINE.md`
- Owning test paths: no dedicated automated helper-test tree exists today; use
  bounded command checks and synthetic non-interactive runner smoke scenarios
  for this slice.
- Related docs and commands: `make validate`,
  `python3 src/execute/scripts/plan_loop.py --help`,
  `python3 -m py_compile src/execute/scripts/plan_loop.py`,
  `python3 src/execute/scripts/plan_loop.py --dry-run ...`

## Dependencies

- The current plan-driven `execute` contract that reads prior plan context
  before choosing a slice.
- The current plan-driven `verify` contract that writes review truth back into
  the same explicit plan file.
- The helper's existing file-backed state model based on `## Progress` and
  `## Blockers`.
- The absence of a shipped automated unit-test layer for helper scripts, which
  makes command-driven verification the smallest meaningful existing test
  surface.

## Sync Expectations

- `specs`: Required. Changing helper behavior and plan-driven workflow
  semantics requires syncing the owning repo-truth docs under `AGENTS.md`,
  `README.md`, `specs/workflow-contract.md`, `specs/repo-surface.md`, and
  `REFINE.md` as needed.
- `tests`: No `tests` skill follow-through is currently required because the
  repo does not ship an existing automated test layer for this helper. Use the
  smallest meaningful command-driven verification instead: repo validation,
  helper CLI smoke checks, Python compile checks, and synthetic non-interactive
  runner scenarios. If implementation complexity forces a tracked executable
  test surface, stop and reassess before inventing one casually.

## Milestones

1. Define the continuous-loop contract: finalize the helper rules for opt-in
   continue-after-fail behavior, strict final review, repairable versus
   blocking verify failures, milestone reopening, appended follow-up
   milestones for cross-cutting final-review failures, and the final helper
   outcome model.
2. Implement the helper flow in `src/execute/scripts/plan_loop.py`: add the
   new opt-in control flags and loop logic, keep the helper dumb and
   file-backed, require verify plan write-back, and emit machine-readable final
   outcome data without parsing prose.
3. Sync the owning docs and skill surfaces: update `execute`, `verify`, the
   plan template, top-level repo-truth docs, and tracked eval assertions so the
   shipped surface matches the helper behavior exactly.
4. Run bounded verification and follow-up: validate repo metadata, compile and
   inspect the helper, and exercise targeted synthetic runner scenarios that
   prove repairable fail recovery, strict final review, and appended follow-up
   milestone behavior.

## Verification

- [2026-04-21] Adversarial plan review against the current helper and skill
  contracts found no material scope, sequencing, or ownership problems.
- [2026-04-21] `rg -n "strict final|pass with risks|continue-after-fail|append.*milestone|final whole-plan|final_outcome|blocked|Progress|Blockers" plans/2026-04-21-continuous-plan-loop.md src/execute/scripts/plan_loop.py src/execute/SKILL.md src/verify/SKILL.md src/plan/assets/plan-template.md REFINE.md AGENTS.md README.md specs/workflow-contract.md specs/repo-surface.md`
  confirmed the plan is anchored to the current shipped surfaces and the open
  helper gap in `REFINE.md`.
- Run `make validate`.
- Run `python3 -m py_compile src/execute/scripts/plan_loop.py`.
- Run `python3 src/execute/scripts/plan_loop.py --help`.
- Run at least one `--dry-run` invocation against this plan or a small synthetic
  plan to confirm the CLI remains coherent.
- Run targeted synthetic non-interactive runner scenarios that prove:
  - repairable `verify fail` can continue when opt-in mode is enabled and the
    plan is not blocked
  - the helper stops on blocking verify failures
  - strict final review requires a final whole-plan `verify pass`
  - a final cross-cutting verify failure can append a new bounded follow-up
    milestone without losing the original context
- Run `git diff --check`.

## Risks

- The helper can livelock or stop incorrectly if the plan-state expectations
  for repairable versus blocking failures are not precise enough.
- Appending follow-up milestones after a final review could accidentally erase
  provenance unless `Verification` and `Decision Log` carry the original
  failure context clearly.
- Strict final review could conflict with existing `Progress` semantics if the
  helper or verifier fails to reopen work accurately after a disproven
  completion claim.
- Without a shipped automated test layer, the synthetic smoke scenarios need to
  be thorough enough to catch control-flow mistakes in the helper.

## Open Questions

- None currently. The current design decisions are settled enough to implement:
  strict final review is required, cross-cutting final failures may append one
  new bounded follow-up milestone, and richer completion semantics should live
  in helper events rather than in extra shell exit codes.

## Blockers

- None currently.

## Progress

- [x] Milestone 1: define the continuous-loop contract
- [ ] Milestone 2: implement the helper flow in `src/execute/scripts/plan_loop.py`
- [ ] Milestone 3: sync the owning docs and skill surfaces
- [ ] Milestone 4: run bounded verification and follow-up

## Decision Log

- [2026-04-21] Make the final helper review strict: the helper should only
  exit successfully after a final whole-plan `verify` pass.
- [2026-04-21] Treat `pass with risks` as insufficient for strict final
  completion even if it remains acceptable for mid-loop continuation.
- [2026-04-21] Reopen an existing milestone only when the verify finding
  clearly disproves that milestone's own done condition.
- [2026-04-21] Allow verify to append one new bounded follow-up milestone when
  a final cross-cutting failure does not map cleanly to any existing milestone.
- [2026-04-21] Keep the helper's shell exit codes simple and put richer final
  status in structured helper events.

## Discoveries

- [2026-04-21] The current helper already enforces execute and verify plan
  write-back, but it still stops on any unacceptable verify verdict or blocked
  plan state.
- [2026-04-21] `execute` already reads prior plan intelligence before choosing
  the next slice, so the main remaining gap is helper orchestration rather than
  missing task-local state.
- [2026-04-21] This repo does not currently ship a dedicated automated test
  layer for helper scripts, so command-based verification and synthetic runner
  scenarios are the smallest meaningful existing test surface.

## Outcomes / Retrospective

- [2026-04-21] Completed Milestone 1 by writing the explicit implementation
  plan, settling the strict final-review and follow-up-milestone rules, and
  verifying that the plan aligns with the current helper and skill contracts.
