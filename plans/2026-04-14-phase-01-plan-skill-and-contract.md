# Phase 01: Plan Skill And Contract

## Goal

Establish the provider-agnostic contract for this repo, lock the six-skill
workflow shape, and add the missing `plan` skill so later phases can execute
against explicit living plan files instead of only against `TODO.md`, while
keeping `AGENTS.md`, `README.md`, and `TODO.md` aligned with the shipped
contract.

## Scope

- Define and ship the first version of the `plan` skill.
- Make the repo contract and six-skill workflow explicit in the shipped docs.
- Keep the implementation grounded in the current roadmap and source guidance.
- Decide and document the target-repo refresh workflow for distributing these
  skills into other repos.

## Non-Goals

- Adding the `execute` skill.
- Refreshing the existing four shipped skills beyond minimal contract alignment.
- Building the eval harness or helper scripts.

## Owned TODO Sections

- `1. Define Repo Contract`
- `2. Define The Six-Skill Workflow`
- `3. Add The Plan Skill`
- Minimal doc sync needed to keep `AGENTS.md`, `README.md`, and `TODO.md`
  truthful after shipping `plan`

## Deliverables

- `plan/SKILL.md`
- `plan/agents/openai.yaml`
- `plan/assets/plan-template.md`
- Minimal updates to `AGENTS.md`, `README.md`, and `TODO.md` needed to keep the
  shipped contract and refresh workflow truth aligned with the delivered
  `plan` skill

## Dependencies

- Existing `AGENTS.md`
- Existing `README.md`
- Existing `TODO.md`
- Existing shipped skills for boundary alignment:
  `consult`, `specs`, `tests`, and `verify`

## Sync Expectations

- `specs`: required in this phase because shipping `plan` changes durable repo
  truth about the canonical workflow, skill boundaries, and task-state model;
  in this repo that means updating `AGENTS.md` first as the authoritative
  contract, then keeping `README.md` and `TODO.md` aligned with the delivered
  `plan` skill and the chosen refresh workflow.
- `tests`: not expected in this phase unless the implementation introduces
  executable helpers, validators, or other behavior that should be covered now.

## Milestones

1. Finalize the contract that `plan` owns:
   trigger conditions, boundaries versus `consult` and `execute`, default file
   naming, and resumption requirements.
2. Decide and document the target-repo refresh workflow:
   manual copy, install script, subtree, plugin, or another sync mechanism.
3. Tighten the trigger description and invocation guidance for the future
   `plan` skill so activation is explicit and reliable.
4. Add the `plan/` skill scaffold and write `plan/SKILL.md` with a narrow,
   provider-agnostic scope.
5. Add `plan/assets/plan-template.md` with the full self-contained living-plan
   structure required by the roadmap.
6. Sync repo docs minimally so `AGENTS.md`, `README.md`, and `TODO.md` stay
   truthful, while keeping the bootstrap asymmetry explicit until `execute`
   exists.

## Verification

- Read the shipped `plan` skill against `AGENTS.md`, `README.md`, and `TODO.md`
  and confirm the boundaries are consistent.
- Confirm the plan template includes goal, scope, non-goals, milestones,
  verification, risks, open questions, progress, decision log, discoveries, and
  outcomes/retrospective.
- Confirm the skill requires explicit sync expectations for `specs` and `tests`
  inside each task plan.
- Confirm the target-repo refresh workflow decision is captured explicitly in
  shipped docs, with the owning doc location named rather than left implied.
- Confirm the docs say `plan` is shipped, `execute` is not, and this repo still
  uses temporary bootstrap prompts for the plan-driven execution step until
  `execute` is delivered here.

## Risks

- Over-designing the refresh workflow before there is real distribution usage.
- Writing a `plan` skill that overlaps too much with `consult` or anticipates
  `execute` details too aggressively.
- Updating docs in a way that implies the full six-skill system is already
  shipped.

## Open Questions

- Which refresh workflow should be the initial default: manual copy, install
  helper, subtree, or another sync mechanism?
- Should the first shipped `plan` skill include examples beyond the core plan
  template, or stay minimal?

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4
- [ ] Milestone 5
- [ ] Milestone 6

## Decision Log

- [2026-04-14] Use one phase plan per coherent workstream rather than one giant
  master implementation plan.

## Discoveries

- [2026-04-14] `TODO.md` is the roadmap, not the execution artifact; later
  phases should execute from explicit `plans/*.md` files.

## Outcomes / Retrospective

- Pending.
