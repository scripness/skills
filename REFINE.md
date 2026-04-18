# REFINE

This file tracks post-merge refinement work for the repo.

## Current Refinement Plan

Rebuild live repo truth first, then remove or replace the remaining references
to historical build plans.

Recommended sequence:

1. Rebuild live repo truth with `specs`.
   - Rewrite `AGENTS.md` from current shipped reality.
   - Create `specs/` from scratch as durable topic truth.
   - Rewrite `README.md` so it describes the shipped system, not the build
     history.
   - Use the historical phase plans only as background source material, not as
     current truth.
2. Demote historical Phase 00-06 files out of the live surface.
   - Remove top-level doc references that make the completed phase plans look
     like required reading.
   - Keep generic `plans/*.md` workflow references only where they are still
     part of the shipped `plan` and `execute` contracts.
3. Replace eval coupling to historical phase plans.
   - Inventory eval cases that currently use Phase 00-06 files as fixtures.
   - Replace those inputs with neutral fixture plan files where plan artifacts
     are still needed for testing.
   - Delete historical-plan eval references that are no longer serving a real
     test purpose.
4. Decide archive policy for the completed build plans.
   - Either keep them in `plans/` as clearly historical records, move them to
     an archive location later, or trim them once they are no longer needed.

Success criteria for this refinement:

- `AGENTS.md`, `README.md`, and `specs/` are sufficient to understand and use
  the repo safely.
- Historical Phase 00-06 files are no longer part of the default operational
  reading chain.
- Evals do not depend on historical build-plan files unless that dependency is
  explicitly intentional and justified as fixture data.

## Helper Loop Note

The remainder of this file is only about a **future optional helper script**
for plan-driven execution.

The intended future home is something like:

- `src/execute/scripts/run-plan.sh`
- or `src/execute/scripts/loop.sh`

That script does not exist yet.

This file does **not** describe:

- a prompt-based workflow
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

## Reference Grounding

Future refinement work should keep essential references in this repo so both
users and fresh agents can recover the best-practice context from repo truth
alone.

That means:

- store the canonical source list in a stable in-repo location rather than only
  in plans, prompts, or chat
- make it obvious where to look for the repo's guiding best practices
- summarize which best practices materially shaped the current `skills` repo,
  not just the raw URLs
- let future plans and helper-loop work point to that shared reference note and
  record only task-specific application or deltas
- avoid leaving critical source grounding implied, scattered, or dependent on
  session memory

The exact file can be chosen later, but it should be a durable repo-level note
such as `SOURCES.md` or a similar shared reference document.

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
