# Phase 02: Execute Skill

## Goal

Ship the `execute` skill so plan-driven implementation can happen in fresh
sessions with a clear stop/update/restart contract instead of relying on
improvised prompts.

## Scope

- Define and ship the first version of the `execute` skill.
- Support both direct bounded execution and explicit plan-driven execution.
- Encode the `specs` and `tests` sync gates and the explicit handoff to
  `verify`.

## Non-Goals

- Building the helper loop scripts.
- Building the full eval harness.
- Refreshing `consult`, `specs`, `tests`, or `verify` beyond minimal boundary
  alignment needed for `execute`.

## Owned TODO Sections

- `4. Add The Execute Skill`
- Minimal doc sync needed to keep `README.md` and `TODO.md` truthful after
  shipping `execute`

## Deliverables

- `execute/SKILL.md`
- `execute/agents/openai.yaml`
- Minimal updates to docs if the shipped behavior differs from the current
  roadmap wording

## Dependencies

- Completed Phase 01 or equivalent delivered `plan` skill contract
- Existing `consult`, `specs`, `tests`, and `verify` skill boundaries
- Existing `README.md` and `TODO.md`

## Sync Expectations

- `specs`: required if shipping `execute` changes durable repo truth about
  implementation flow, stop/restart behavior, or truth-sync responsibilities.
- `tests`: not expected in this phase unless executable helpers or validators
  are introduced during implementation.

## Milestones

1. Finalize the `execute` boundary:
   direct mode versus plan-driven mode, explicit plan-path requirements, and
   handoff rules to `verify`.
2. Write `execute/SKILL.md` with one-bounded-slice execution, required
   mechanical checks, and mandatory plan updates for plan-driven work.
3. Encode the sync gates for `specs` and `tests`, including direct-mode
   inference from repo truth when no plan file exists.
4. Sync docs minimally so the shipped skill contract stays truthful.

## Verification

- Confirm `execute` never guesses the latest plan file.
- Confirm `execute` stops after one bounded slice and updates the plan before
  stopping in plan-driven mode.
- Confirm `execute` does not self-invoke adversarial `verify`.
- Confirm `execute` treats missing required `specs` or `tests` sync as blocking
  follow-through, not optional polish.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4

## Decision Log

- [2026-04-14] `execute` should support both direct bounded execution and
  explicit plan-driven execution instead of splitting into two skills.

## Discoveries

- [2026-04-14] A clean `execute` skill is the missing primitive that turns the
  roadmap into a reliable fresh-session implementation loop.

