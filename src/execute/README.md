# execute

Implement one bounded task directly or execute one bounded slice from one
explicit plan file, then hand off to `verify`.

## What It Owns

`execute` owns implementation work. It reads repo truth first, changes only one
bounded slice, runs the smallest meaningful checks, completes required
`specs` or `tests` follow-through, updates the explicit plan when the work is
plan-driven, and then hands off to `verify`.

## Use It When

- the user wants implementation now
- the task is still locally clear and bounded
- there is already one explicit `plans/*.md` file to execute

## Do Not Use It When

- the next move is still unclear; use `consult`
- the work needs durable task state but no explicit plan file exists yet; use `plan`
- the task is review, final judgment, or fact-checking; use `verify`

## Workflow Position

Use `execute` by itself for a small, locally clear task:

`execute -> verify`

Use it as part of the full plan-driven workflow when the work needs durable
task state:

`consult -> plan -> execute -> verify`

Bring in `specs` when repo truth is weak or stale. Bring in `tests` when test
truth or coverage needs to be added or synced.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `references/optional-helper.md`: helper contract and wrapper notes
- `scripts/loop.py`: optional provider-agnostic execute/verify loop helper
- `scripts/providers/codex_loop.py`: optional local Codex wrapper over `loop.py`
- `scripts/providers/codex_loop_dashboard.py`: optional terminal dashboard over the Codex wrapper
- `evals/`: upstream-only eval metadata in this source repo; not included in normal downstream installs

## Related Scripts

- `scripts/loop.py`: optional helper for plan-driven execute/verify loops
- `scripts/providers/codex_loop.py`: optional local Codex wrapper over `scripts/loop.py`
- `scripts/providers/codex_loop_dashboard.py`: optional dashboard wrapper over the Codex loop flow

When copied into a target repo, these live under:
- `.agents/skills/execute/scripts/loop.py`
- `.agents/skills/execute/scripts/providers/codex_loop.py`
- `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `consult`: use when the next move is still unclear
- `plan`: use when the work needs durable task state
- `verify`: use after implementation for adversarial review
- `specs`: use when repo truth needs syncing
- `tests`: use when test truth or coverage needs syncing
