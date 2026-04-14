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

- Validation/eval-refresh command surface
- Optional thin helper scripts under skill-local `scripts/` where justified
- Final README and maintenance-guide polish

## Dependencies

- Delivered six-skill system
- Delivered initial eval harness
- Existing `README.md` and `TODO.md`

## Sync Expectations

- `specs`: required if the final tooling or docs change durable repo truth about
  workflow operation or maintenance.
- `tests`: required if helper scripts or validators introduce executable
  behavior that should be sanity-checked or covered.

## Milestones

1. Add the validation and eval-refresh operator surface.
2. Add any justified thin helper scripts with the documented agent-safe
   interface contract.
3. Finish README, maintenance guidance, and remaining contract cleanup so the
   shipped repo matches the implemented system.

## Verification

- Confirm helper scripts remain convenience wrappers only and do not hide unique
  workflow logic.
- Confirm helper scripts are non-interactive, documented, structured, and
  reviewable.
- Confirm the docs describe the durable-state model and six-skill workflow
  accurately.

## Risks

- Adding wrappers that quietly become required for normal workflow use.
- Final docs drifting into aspirational claims instead of shipped truth.
- Polishing tooling before the eval harness and skill contracts are stable
  enough.

## Open Questions

- Should the first maintenance surface be a `Makefile`, shell scripts, or a
  different minimal interface?
- Which helper scripts, if any, actually earn their place after the earlier
  phases are complete?

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Decision Log

- [2026-04-14] Tooling should remain thin and optional; the workflow must stay
  skill-native first.

## Discoveries

- [2026-04-14] The right time to add wrappers is after the skills and eval
  contracts exist, not before.

## Outcomes / Retrospective

- Pending.
