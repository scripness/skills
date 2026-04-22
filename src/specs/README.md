# specs

Bootstrap, sync, or repair repo truth in `AGENTS.md`, `CLAUDE.md`, and
`specs/` when the current guidance is missing, stale, or too weak for safe work.

## What It Owns

`specs` owns repo-truth sync. It audits the real repo topology and current
docs, then updates `AGENTS.md`, `CLAUDE.md`, and `specs/` so future planning,
execution, and verification can rely on durable repo truth instead of
guesswork.

## Use It When

- `AGENTS.md` or `specs/` is missing or stale
- repo topology or operating guidance is weak enough to block safe work
- a task changed durable repo truth and the docs now need follow-through

## Do Not Use It When

- the task is only a short clarification
- the work mainly needs task-local planning rather than repo-wide truth
- the repo truth is already good enough and implementation should start

## Workflow Position

`specs` is a support skill that can be used before or during the rest of the
workflow whenever repo truth is too weak:

`specs -> consult -> plan -> execute -> verify`

or, for a bounded implementation slice with stale docs:

`execute -> specs -> verify`

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `assets/AGENTS.md`: bootstrap template for downstream `AGENTS.md`
- `assets/specs/README.md`: bootstrap template for downstream specs index
- `assets/specs/spec-template.md`: bootstrap template for downstream topic specs
- `evals/`: upstream-only eval metadata in this source repo; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven execute helpers ship with the `execute` skill. If
`execute` is installed locally, open its README for `loop.py` and the optional
Codex wrappers.

## Related Skills

- `consult`: use after repo truth is good enough to choose a direction
- `plan`: use when the task needs durable task-local state
- `tests`: use when test truth also needs syncing
