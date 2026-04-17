# Phase 06: Tooling And Final Docs

## Goal

Add the thin maintenance tooling and final doc polish needed to operate the
six-skill system cleanly once the skills and eval harness exist.

## Scope

- Add the repo-level validation and eval-refresh operator surface.
- Add any thin optional helper scripts that merely save keystrokes without
  becoming workflow truth.
- Finish the remaining README and maintenance documentation cleanup.

## Non-Goals

- Re-architecting the skill system again.
- Building heavy orchestration that becomes required for correctness.
- Provider-specific lock-in.

## Owned TODO Sections

- `8. Add Repo-Level Maintenance Tooling`
- `9. Add Core Repo Docs`
- Any remaining cross-cutting cleanup from `6. Ground The Skills In Official
  Sources`

## Deliverables

- Repo-root `Makefile` exposing the Phase 06 maintenance command surface while
  delegating unique harness logic to `evals/scripts/harness.py`
- Optional thin helper scripts under `execute/scripts/` only if they earn their
  place after the repo-level operator surface exists
- Repo-root `MAINTENANCE.md` plus final `README.md`, `AGENTS.md`, and
  `evals/README.md` polish

## Repo Context

- Task source: `TODO.md` sections `8. Add Repo-Level Maintenance Tooling` and
  `9. Add Core Repo Docs`, plus the 2026-04-17 verification finding that this
  plan needed explicit owning paths, blockers, and milestone acceptance
  criteria before Phase 06 execution could start safely
- Existing operator surface: Phase 05 already ships
  `python3 evals/scripts/harness.py validate` and
  `python3 evals/scripts/harness.py init-run --run-id <run-id> --selection <selection>`
  as the first thin local runner helpers; Phase 06 must add repo-level
  maintenance entrypoints and any broader validation without re-implementing
  unique harness logic in wrappers
- Owning code paths: repo-root `Makefile` for the maintenance entrypoint;
  `evals/scripts/harness.py` for shared eval validation and run scaffolding;
  `execute/scripts/` for any justified plan-driven convenience helper;
  generated run artifacts remain outside tracked source under `.tmp/evals/`
- Owning spec paths: `AGENTS.md` for the authoritative workflow contract and
  command table, `README.md` for the shipped usage surface, `evals/README.md`
  for eval artifact and review procedure details, and repo-root
  `MAINTENANCE.md` for operator guidance on updating skills, running evals, and
  upstreaming improvements from downstream repos; update `TODO.md` only if
  shipped behavior would otherwise make the roadmap wording false
- Owning test paths: there is still no formal automated suite in this repo, so
  the minimum acceptable follow-through is smoke execution of each new
  repo-level command or helper entrypoint plus the existing eval-harness
  validation commands that prove the new surface stays aligned with tracked
  truth
- Related docs or references:
  `plans/2026-04-14-phase-05-evaluation-harness.md`, `PROMPT_verify.md`,
  `README.md`, `AGENTS.md`, and `TODO.md` sections `8` and `9`

## Dependencies

- Delivered six-skill system
- Delivered initial eval harness, including the current
  `evals/scripts/harness.py` validate-plus-init-run surface
- Existing `README.md`, `AGENTS.md`, `evals/README.md`, and `TODO.md`

## Sync Expectations

- `specs`: required as part of this phase rather than optional after the fact.
  Milestones 1 and 3 change durable repo truth about the maintenance command
  surface, validation coverage, eval refresh workflow, and operator guidance,
  so keep `AGENTS.md`, `README.md`, `evals/README.md`, and `MAINTENANCE.md`
  aligned before calling any milestone complete.
- `tests`: required for any new executable surface in this phase. The minimum
  acceptable follow-through is smoke execution of each new `make` target or
  helper entrypoint, `--help` coverage for any script interface, and
  re-running `python3 evals/scripts/harness.py validate`; if stronger
  automation is still deferred, record that blocker explicitly in this plan
  instead of implying coverage exists.

## Milestones

1. Add the repo-level operator surface with an explicit Phase 05 delta: ship a
   repo-root `Makefile` as the thin maintenance entrypoint, wire validation and
   eval-refresh commands through the existing `evals/scripts/harness.py`
   helpers, extend validation to cover skill structure, frontmatter, and local
   asset integrity as needed, and document every shipped command in the owning
   docs.
2. Add only justified helper scripts with an explicit agent-safe contract: if a
   plan-driven convenience gap remains after Milestone 1, add at most thin
   helpers under `execute/scripts/` that take an explicit provider command and
   explicit plan path, never guess state, expose `--help`, separate
   machine-readable stdout from stderr diagnostics, document meaningful exit
   codes, and support `--dry-run` or explicit confirmation for any stateful
   action; otherwise close the milestone by recording that no helper earned
   inclusion.
3. Finish final docs and maintenance guidance so shipped truth matches the
   implemented system: add repo-root `MAINTENANCE.md`, sync `README.md`,
   `AGENTS.md`, and `evals/README.md`, and close any remaining wording drift
   about the durable-state model, maintenance loop, and upstreaming guidance.

## Verification

- Confirm the repo-level operator commands stay thin and do not hide unique
  workflow logic that should live in tracked Python or markdown instead.
- Confirm the chosen validation surface covers skill structure, frontmatter, and
  local asset integrity in addition to the existing eval-contract checks.
- Confirm any helper scripts remain convenience wrappers only, are
  non-interactive, expose `--help`, separate machine-readable stdout from
  stderr diagnostics, report meaningful exit codes, and implement `--dry-run`
  or explicit confirmation when stateful behavior exists.
- Confirm `AGENTS.md`, `README.md`, `evals/README.md`, and `MAINTENANCE.md`
  describe the same command surface, maintenance loop, and durable-state model.
- Smoke-run each shipped command surface and record the exact commands and
  results in this plan before closing milestones.

## Risks

- Adding wrappers that quietly become required for normal workflow use.
- Final docs drifting into aspirational claims instead of shipped truth.
- Polishing tooling before the eval harness and skill contracts are stable
  enough.

## Open Questions

- Should the repo-root `Makefile` also carry a discoverable `help` target, or
  is explicit command documentation in `README.md` and `MAINTENANCE.md`
  sufficient for the initial shipped surface?
- After the `Makefile` exists, does any plan-driven helper still earn inclusion,
  or should Milestone 2 close by explicitly recording that no helper is needed?

## Blockers

- None currently.
- Current repo state is still Phase 05-only: `evals/scripts/harness.py` exists
  and is documented, but there is no repo-root `Makefile`, no `execute/scripts/`
  helper surface, and no separate `MAINTENANCE.md` yet.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Decision Log

- [2026-04-14] Tooling should remain thin and optional; the workflow must stay
  skill-native first.
- [2026-04-17] Use a repo-root `Makefile` as the first Phase 06 maintenance
  surface so operator commands stay thin, reviewable, and additive above the
  existing `evals/scripts/harness.py` helpers.
- [2026-04-17] If a plan-driven convenience wrapper is justified, it belongs
  under `execute/scripts/` because it composes `execute` and `verify`; if no
  real gap remains after Milestone 1, close Milestone 2 explicitly without
  adding a helper just to satisfy the plan.
- [2026-04-17] Use repo-root `MAINTENANCE.md` as the durable home for skill
  update guidance, eval-running guidance, and upstreaming notes from downstream
  repo work.

## Discoveries

- [2026-04-14] The right time to add wrappers is after the skills and eval
  contracts exist, not before.
- [2026-04-17] The current repo already ships the Phase 05 harness entrypoints
  in `evals/scripts/harness.py`, so Phase 06 must layer operator polish and
  broader validation on top of that surface rather than replace it.
- [2026-04-17] Before this repair, the Phase 06 plan lacked `Repo Context`,
  `Blockers`, and milestone-level acceptance criteria, which made fresh-session
  execution riskier than the shipped `plan` contract allows.

## Outcomes / Retrospective

- Pending.
