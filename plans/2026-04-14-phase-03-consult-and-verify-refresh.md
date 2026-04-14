# Phase 03: Consult And Verify Refresh

## Goal

Refresh `consult` and `verify` so they fit the six-skill workflow cleanly,
especially around explicit plan files, phase-based execution, and findings-first
review.

## Scope

- Tighten the trigger boundaries and outputs for `consult`.
- Tighten the verification targets, verdict rules, and evidence requirements for
  `verify`.
- Align both skills with the new `plan` and `execute` contracts.

## Non-Goals

- Reworking `specs` or `tests`.
- Building eval runners or helper scripts.
- Large repo-doc rewrites beyond minimal truth sync.

## Owned TODO Sections

- The `consult` and `verify` parts of `5. Improve The Six Core Skills`
- The relevant cross-cutting source-grounding work from `6. Ground The Skills In
  Official Sources`

## Deliverables

- Updated `consult/SKILL.md`
- Updated `verify/SKILL.md`
- Minimal updates to docs if shipped behavior changes current truth

## Dependencies

- Completed Phase 01 and Phase 02 or equivalent delivered contracts for `plan`
  and `execute`
- Existing `README.md` and `TODO.md`

## Sync Expectations

- `specs`: required only if the refreshed skill contracts change durable repo
  truth about how consultation or verification should operate.
- `tests`: not expected unless this phase adds executable validators or eval
  helpers that should be covered immediately.

## Milestones

1. Refresh `consult` so it stays evidence-backed, bounded, and explicit about
   what should be carried into a durable plan.
2. Refresh `verify` so it treats plans, implementations, and claims as distinct
   targets with findings-first output and honest blocked-check reporting.
3. Align both skills with the new workflow boundaries and minimal doc truth.

## Verification

- Confirm `consult` does not drift into owning long-lived task state.
- Confirm `verify` remains a verifier, not an implementer.
- Confirm `verify` explicitly treats missing required `specs` or `tests` sync as
  `fail` when the obligation is clear.
- Confirm both skills point to code/spec references rather than opinion-only
  guidance.

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Decision Log

- [2026-04-14] Keep `consult` and `verify` separate from planning and execution
  instead of collapsing them into broader meta-skills.

## Discoveries

- [2026-04-14] `consult` and `verify` are the decision/review pair in the
  workflow and deserve their own refresh phase rather than being spread across
  unrelated work.

