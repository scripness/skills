# consult

Clarify current behavior, viable options, and the safest next move before
committing to execution or planning.

## What It Owns

`consult` owns clarification. It reads repo truth, inspects the current code
and specs, compares viable approaches, and recommends the safest bounded next
move. When the work should become plan-driven, it should leave durable
carry-forward instead of trapping key facts in chat.

## Use It When

- the next move is not yet clear enough to execute safely
- the work needs architecture or tradeoff analysis
- you need to understand current behavior before choosing a direction

## Do Not Use It When

- the task is already clear and implementation should start now
- the work already has an explicit plan path and needs execution
- the task is adversarial review or final judgment

## Workflow Position

Use `consult` by itself for clarification, or as the front door to a larger
workflow:

`consult -> plan -> execute -> verify`

Bring in `specs` if repo truth is weak or stale. Bring in `tests` later if the
chosen implementation changes behavior that needs coverage follow-through.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `evals/`: upstream-only eval metadata in this source repo; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven helpers for the broader workflow live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../plan/README.md`: use when the direction is clear but the work needs durable task state
- `../execute/README.md`: use when implementation should begin now
- `../verify/README.md`: use when there is already a concrete plan, diff, or claim to judge
