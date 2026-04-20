---
Status: Shipped
Last verified: 2026-04-20
---

# Repo Surface

> Source of truth: `src/`, `plans/`, `Makefile`,
> `src/execute/scripts/plan_loop.py`, and the top-level docs
> Non-owning trees to ignore unless explicitly in scope: `.git/`, `.tmp/evals/`
> If this spec contradicts the code, the code is correct — update this spec.

<!-- Review when top-level layout changes -->
<!-- Review when src/*/agents/openai.yaml changes -->
<!-- Review when src/execute/scripts/plan_loop.py changes -->

## Overview

This spec maps the actual shipped repo layout and what each top-level area
owns. It exists so a fresh agent can find the real workflow surface quickly
without treating generated artifacts or historical build records as the active
system.

## Non-Goals

- describing target-repo application architecture
- documenting generated eval workspace contents as tracked repo structure
- duplicating every detail from skill-local eval definitions

## Key Patterns

- top-level docs are the live truth layer around the shipped source skills
- each `src/<skill>/` directory is a copyable source skill payload
- shared eval metadata lives under `evals/`, while generated run artifacts live
  under `.tmp/evals/`
- `CLAUDE.md` is a thin mirror of `AGENTS.md`, not a separate contract

## Top-Level Layout

- `AGENTS.md`: repo-wide operational truth
- `README.md`: shipped-system overview
- `MAINTENANCE.md`: operator loop for maintenance and eval refresh
- `SOURCES.md`: durable external grounding
- `REFINE.md`: current post-merge cleanup context
- `specs/`: durable topic truth for this repo
- `src/`: source-of-truth skill payloads
- `evals/`: shared harness metadata, fixture manifests, and harness helper
- `Makefile`: thin wrapper over `evals/scripts/harness.py`
- `plans/`: explicit task plans for current work, a small number of tracked
  plan-shaped eval fixtures, plus completed historical build records

## Skill Directory Contract

Every shipped skill directory contains:

- `SKILL.md` for the portable workflow contract
- `agents/openai.yaml` for the local agent shim metadata
- `evals/evals.json` for tracked trigger and workflow eval intent

Additional shipped local assets:

- `src/plan/assets/plan-template.md`
- `src/specs/assets/AGENTS.md`
- `src/specs/assets/specs/README.md`
- `src/specs/assets/specs/spec-template.md`
- `src/execute/scripts/plan_loop.py`

## Plans Directory Semantics

- New plan-driven work should create or update one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` file.
- `execute` and `verify` must use the exact named plan path in plan-driven
  work.
- A small number of tracked plan-shaped eval fixtures may also live under
  `plans/` when a skill eval needs a real explicit `plans/*.md` input.
- Completed historical plan records under `plans/` are still available in the
  repo but should not be treated as the default live reading chain.

## Documentation Surface

- Keep `AGENTS.md` compact and operational.
- Put durable topic truth in `specs/`, not in task plans.
- Keep `README.md` focused on the shipped system rather than historical build
  narration.
- Use `MAINTENANCE.md` for operator commands and loops, and `SOURCES.md` for
  external grounding instead of repeating them everywhere.

## Verification

- Run `rg --files src evals specs` to confirm the shipped surface and live
  spec tree are present.
- Run `test -L CLAUDE.md` to confirm `CLAUDE.md` remains a symlink mirror to
  `AGENTS.md`.
- Run `find . -maxdepth 2 \\( -path './.git' -o -path './.tmp' \\) -prune -o -maxdepth 2 -type d | sort` to confirm the top-level layout described here still matches the repo.
