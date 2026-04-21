# [Task Title]

Use this file as a living task plan. Keep it updated in place. A fresh session
should be able to resume from repo truth plus this file alone.

Update `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
`Blockers` after each bounded slice or plan-driven verification pass. Hand off
later `execute` and `verify` sessions with this exact file path.

## Goal

[Describe the end state, why it matters, and what "done" means.]

## Scope

- [In-scope work]
- [In-scope work]

## Non-Goals

- [Explicitly out of scope]
- [Explicitly out of scope]

## Deliverables

- [File, behavior, or artifact to ship]
- [Doc, spec, or follow-through needed to keep truth aligned]

## Repo Context

- Task source: [issue, ticket, prompt, or request]
- Owning code paths: [path] or `N/A`
- Owning spec paths: [path] or `N/A`
- Owning test paths: [path] or `N/A`
- Related docs, commands, or external dependencies: [details]

## Dependencies

- [Required prerequisite, prior phase, or upstream input]
- [Say "None" when there are no meaningful dependencies]

## Sync Expectations

State the repo-truth and test-truth follow-through explicitly. If
implementation changes durable behavior, boundaries, operating guidance, or
coverage expectations, follow through with `specs` and `tests` rather than
leaving drift behind.

- `specs`: [Name the owning specs or missing specs to create/update. State when
  `specs` sync is required. If not currently required, say that explicitly.]
- `tests`: [Name the applicable test layers and expected coverage
  follow-through. State when `tests` sync is required. If not currently
  required, say that explicitly.]

## Milestones

1. [Milestone name]: [bounded slice and done condition].
2. [Milestone name]: [bounded slice and done condition].
3. [Milestone name]: [bounded slice and done condition].

## Verification

Keep planned proof points here, then append dated execution and verification
results, findings, verdicts, and remaining gaps so later sessions can resume
from this file alone.

If a strict final review finds cross-cutting work that does not fit an
existing milestone cleanly, append one new bounded follow-up milestone and
record the provenance here plus in `Decision Log`.

- [Command, inspection pass, or evidence that should prove the slice worked]
- [Command, inspection pass, or evidence that should prove docs, specs, and
  tests stayed aligned]

## Risks

- [Meaningful risk]
- [Meaningful risk]

## Open Questions

- [Question to resolve before or during execution]
- [Question to resolve before or during execution]

## Blockers

Use this section for anything that blocks the next safe execute slice,
including unresolved verification failures.

Do not treat every repairable verify failure as a blocker. If the next safe
move is another bounded execute slice, reopen or append that work in
`Progress` instead.

- None currently.

## Progress

Reflect the current task state for each milestone. If later verification proves
that an earlier completion claim was too optimistic, correct it here.

When a strict final review uncovers a cross-cutting failure that does not map
cleanly to an existing milestone, append one new bounded follow-up milestone
instead of overwriting unrelated historical progress.

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Decision Log

- [YYYY-MM-DD] [Decision and rationale]

## Discoveries

- [YYYY-MM-DD] [Important surprise, constraint, or repo fact learned during the
  work]

## Outcomes / Retrospective

- Pending.
