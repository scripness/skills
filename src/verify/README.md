# verify

Adversarially judge a concrete plan, implementation slice, diff, or technical
claim against repo truth and required follow-through.

## What It Owns

`verify` owns review and final judgment. It reads repo truth, checks the
concrete target against code, specs, plans, and mechanical evidence, and
returns findings first. In plan-driven work, it writes its review back into the
same plan file so the task record stays canonical.

## Use It When

- there is already a concrete target to judge
- implementation or plan work needs adversarial review
- a technical claim needs to be fact-checked against current repo reality

## Do Not Use It When

- the next move is still unclear and needs `consult`
- the work needs a new or updated plan file
- implementation fixes should happen now

## Workflow Position

`verify` is the review step after planning or implementation:

`execute -> verify`

or, for longer work:

`consult -> plan -> execute -> verify`

In plan-driven work, repeated `verify` passes keep the same explicit plan file
truthful over time.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `evals/`: upstream-only eval metadata in this source repo; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven execute helpers ship with the `execute` skill. If
`execute` is installed locally, open its README for `loop.py` and the optional
Codex wrappers.

## Related Skills

- `execute`: use before verification when implementation is still pending
- `plan`: use when the task-local plan needs to be created or repaired
- `consult`: use when the next move is still ambiguous
