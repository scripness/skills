# REFINE

This file is only about a **future optional helper script** for plan-driven
execution.

The intended future home is something like:

- `execute/scripts/run-plan.sh`
- or `execute/scripts/loop.sh`

That script does not exist yet.

This file does **not** describe:

- the current prompt-based workflow
- `PROMPT_execute.md`
- `PROMPT_verify.md`
- normal manual fresh-session work
- the baseline six-skill workflow itself

It describes only this future automation:

- given one explicit `plans/*.md` file
- run fresh `execute`
- run fresh `verify`
- if `verify` fails, run a fresh remediation `execute`
- run `verify` again
- keep going until the current plan finishes or a stop condition fires

The purpose is to automate the repetitive `execute -> verify -> remediation
execute -> verify` loop for plan-driven work without skipping verification and
without requiring constant manual babysitting.

Current baseline remains:

- manual or prompt-driven fresh sessions
- `execute`
- `verify`
- human decides the next step

## Goal

For the future optional helper loop, keep the core workflow:

- `consult`
- `plan`
- `verify` the plan
- `execute`
- `verify`

But add an optional automation layer for plan-driven work so that a failed
`verify` step can feed a fresh remediation `execute` step automatically and then
continue the plan only after verification passes.

## Core Rule

`verify` must remain a verifier, not an implementer.

So the automation must not turn into:

- `verify` finds issues and fixes them itself

It must remain:

1. fresh `execute` for one bounded slice
2. fresh `verify`
3. if `verify` fails, save the report as a durable artifact
4. fresh `execute` remediation run against the same explicit plan file
5. fresh `verify` again
6. only continue to the next milestone when verification passes

## Proposed Automated Loop

For one explicit `plans/*.md` file:

1. Run fresh `execute` for the next bounded slice.
2. Run fresh `verify` against the same explicit plan path.
3. If `verify` returns `pass`, continue to the next slice if work remains.
4. If `verify` returns `pass with risks`, stop by default and hand control back
   to the operator unless a future policy explicitly allows auto-continue for
   specific low-risk classes.
5. If `verify` returns `fail`:
   - persist the full verify report to disk
   - start a fresh remediation `execute` run
   - tell that run to address only the failed verify findings
   - update the same plan file
   - rerun fresh `verify`
6. Repeat until:
   - verification passes and the plan can continue
   - the plan is complete
   - a stop condition fires

## Required Inputs For Remediation

The remediation `execute` run must receive:

- the same explicit `plans/*.md` path
- the latest failed verify report
- current repo truth:
  - `AGENTS.md`
  - relevant `specs/*`
  - tests and eval surfaces when applicable

The remediation step should not guess the latest plan or latest report.

## Required Durable Artifacts

To automate this safely, failed verification must leave behind a durable review
artifact that the next remediation step can consume.

At minimum, keep:

- explicit plan path
- full verify report
- verify verdict
- timestamp or iteration number

Likely future storage patterns:

- `artifacts/verify/<plan-slug>/<iteration>.md`
- or a similar plan-scoped review artifact layout

The exact path can be decided later, but the artifact must be file-backed and
stable.

## Guardrails

Automation should stay bounded.

The loop should stop and hand control back to a human when:

- the same failure repeats beyond a configured limit
- findings conflict with the plan or with each other
- the plan is stale or contradictory
- required repo truth is missing
- required tests or evals cannot run
- the remediation starts widening scope beyond the current milestone
- the workflow leaves the smart working zone and the plan is no longer enough
  to continue safely

## What This Is Not

This is not:

- removing the `verify` step
- letting `execute` silently mark itself correct
- letting `verify` patch code directly
- replacing the skills with an opaque orchestrator

The automation should remain a thin wrapper around the same skill-native flow:

- fresh `execute`
- fresh `verify`
- fresh remediation `execute` when verification fails
- fresh `verify` again

## Relationship To Helper Scripts

The future helper loop should eventually support two modes:

1. normal progression
   - `execute -> verify -> next slice`
2. remediation progression
   - `execute -> verify(fail) -> remediation execute -> verify -> continue`

The helper should remain:

- optional
- file-backed
- explicit-plan-path only
- non-interactive by default
- honest about failure and stop conditions

## Deferred Until After Current Plans

This refinement is intentionally deferred until after the current roadmap phases
ship the missing core skills and the initial eval/tooling surface.

Use this document only when implementing or refining the future helper-loop
automation for plan-driven execution.

It should be revisited once:

- `plan` exists
- `execute` exists
- `verify` is refreshed
- the evaluation harness exists
- the basic helper-script contract is implemented
