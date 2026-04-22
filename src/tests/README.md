# tests

Bootstrap, extend, or sync test truth by discovering the repo's actual test
topology and covering the right layers for safe execution and verification.

## What It Owns

`tests` owns test-truth sync. It audits the real test topology, decides which
layers are applicable, adds or updates the right tests, and runs the required
mechanical checks for the changed behavior.

## Use It When

- changed behavior is not clearly covered by the current test suite
- the repo's test topology or coverage is stale or too weak
- safe execution or verification is blocked by a concrete coverage gap

## Do Not Use It When

- the task is only clarification or planning
- the repo already has adequate coverage for the current slice
- the issue is stale repo docs rather than stale test truth

## Workflow Position

`tests` is a support skill that comes in when behavior changes need coverage
follow-through:

`execute -> tests -> verify`

or, when a repo is weak on both repo truth and test truth:

`specs -> consult -> plan -> execute -> tests -> verify`

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

- `../execute/README.md`: use before test sync when implementation changes are still pending
- `../verify/README.md`: use after test follow-through for adversarial review
- `../specs/README.md`: use when repo-truth docs also need to be corrected
