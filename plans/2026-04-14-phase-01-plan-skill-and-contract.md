# Phase 01: Plan Skill And Contract

## Goal

Establish the provider-agnostic contract for this repo, lock the six-skill
workflow shape, and add the missing `plan` skill so later phases can execute
against explicit living plan files instead of only against `TODO.md`.

## Scope

- Define and ship the first version of the `plan` skill.
- Make the repo contract and six-skill workflow explicit in the shipped docs.
- Keep the implementation grounded in the current roadmap and source guidance.

## Non-Goals

- Adding the `execute` skill.
- Refreshing the existing four shipped skills beyond minimal contract alignment.
- Building the eval harness or helper scripts.

## Owned TODO Sections

- `1. Define Repo Contract`
- `2. Define The Six-Skill Workflow`
- `3. Add The Plan Skill`
- Minimal doc sync needed to keep `README.md` truthful after shipping `plan`

## Deliverables

- `plan/SKILL.md`
- `plan/agents/openai.yaml`
- `plan/assets/plan-template.md`
- Minimal updates to `README.md` and `TODO.md` only if the shipped `plan` skill
  changes the documented truth

## Dependencies

- Existing `README.md`
- Existing `TODO.md`
- Existing shipped skills for boundary alignment:
  `consult`, `specs`, `tests`, and `verify`

## Sync Expectations

- `specs`: required only if shipping `plan` changes durable repo truth about the
  canonical workflow, skill boundaries, or task-state model; in this repo that
  means keeping `README.md` and `TODO.md` aligned with the delivered `plan`
  skill.
- `tests`: not expected in this phase unless the implementation introduces
  executable helpers, validators, or other behavior that should be covered now.

## Milestones

1. Finalize the contract that `plan` owns:
   trigger conditions, boundaries versus `consult` and `execute`, default file
   naming, and resumption requirements.
2. Add the `plan/` skill scaffold and write `plan/SKILL.md` with a narrow,
   provider-agnostic scope.
3. Add `plan/assets/plan-template.md` with the full self-contained living-plan
   structure required by the roadmap.
4. Sync repo docs minimally so the shipped skill set and workflow contract stay
   truthful.

## Verification

- Read the shipped `plan` skill against `README.md` and `TODO.md` and confirm
  the boundaries are consistent.
- Confirm the plan template includes goal, scope, non-goals, milestones,
  verification, risks, open questions, progress, decision log, discoveries, and
  outcomes/retrospective.
- Confirm the skill requires explicit sync expectations for `specs` and `tests`
  inside each task plan.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4

## Decision Log

- [2026-04-14] Use one phase plan per coherent workstream rather than one giant
  master implementation plan.

## Discoveries

- [2026-04-14] `TODO.md` is the roadmap, not the execution artifact; later
  phases should execute from explicit `plans/*.md` files.

