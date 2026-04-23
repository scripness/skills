# plan

Create or maintain one explicit `plans/*.md` file when work needs durable task
state across sessions, milestones, or review loops.

## What It Owns

`plan` owns task-local planning. It reads repo truth, chooses one explicit plan
path, and writes a living plan that is resumable from repo files plus that plan
alone. It should make the next unfinished slice decision-complete so later
`execute` work does not need to guess.

## Use It When

- the direction is clear enough to structure
- the work needs durable state across sessions or milestones
- discoveries, blockers, or review history need to survive fresh context

## Do Not Use It When

- the next move is still unclear and needs `consult`
- the task is small and still locally clear enough for one bounded execute pass
- the task is implementation now with no durable-state need

## Workflow Position

`plan` is the durable state layer of the full workflow:

`consult -> plan -> execute -> verify`

In plan-driven work, later `execute` and `verify` runs should keep using the
same exact plan file path.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `assets/plan-template.md`: local plan template
- `evals/`: upstream-only eval metadata in this source repo; not included in normal downstream installs

## Related Scripts

No scripts ship directly with this skill.

Optional plan-driven execute helpers ship with the `execute` skill. If
`execute` is installed locally, open its README for `loop.py` and the optional
Codex wrappers.

## Related Skills

- `consult`: use before planning when the direction is not settled
- `execute`: use to implement one bounded slice from the plan
- `verify`: use to review the plan and later implementation slices
