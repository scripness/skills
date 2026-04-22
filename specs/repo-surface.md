---
Status: Shipped
Last verified: 2026-04-21
---

# Repo Surface

> Source of truth: `src/`, `plans/`, `Makefile`,
> `src/execute/scripts/loop.py`, `scripts/sync_downstream.py`, and the repo
> docs
> Non-owning trees to ignore unless explicitly in scope: `.git/`, `.tmp/evals/`
> If this spec contradicts the code, the code is correct — update this spec.

<!-- Review when top-level layout changes -->
<!-- Review when src/*/agents/openai.yaml changes -->
<!-- Review when src/execute/scripts/loop.py changes -->
<!-- Review when scripts/sync_downstream.py changes -->

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

- repo docs are the live truth layer around the shipped source skills
- each `src/<skill>/` directory is a copyable source skill payload
- downstream `.agents/skills/<skill>/` installs are filtered copies produced
  by `scripts/sync_downstream.py`, not byte-for-byte mirrors of `src/`
- `.agents/skills` may exist as a local symlink mirror to `src/` for
  copied-layout checks, but `src/` remains the owning tree
- shared eval metadata lives under `evals/`, while generated run artifacts live
  under `.tmp/evals/`
- `CLAUDE.md` is a thin mirror of `AGENTS.md`, not a separate contract

## Top-Level Layout

- `AGENTS.md`: repo-wide operational truth
- `README.md`: shipped-system overview
- `docs/maintenance.md`: operator loop for maintenance and eval refresh
- `docs/sources.md`: durable external grounding
- `scripts/`: thin repo-level maintenance helpers, including downstream sync
- `.agents/skills`: tracked local symlink mirror to `src/` for copied-layout
  ergonomics in this source repo
- `specs/`: durable topic truth for this repo
- `src/`: source-of-truth skill payloads
- `evals/`: shared harness metadata, fixture manifests, and harness helper
- `Makefile`: thin repo-root maintenance wrapper over the eval harness
  commands plus downstream sync
- `plans/`: explicit task plans for current work, a small number of tracked
  plan-shaped eval fixtures, plus completed historical build records

## Skill Directory Contract

Every shipped skill directory contains:

- `SKILL.md` for the portable workflow contract
- `README.md` for the human-facing overview
- `agents/openai.yaml` for the local agent shim metadata
- `evals/evals.json` for tracked trigger and workflow eval intent

Additional shipped local assets:

- `src/plan/assets/plan-template.md`
- `src/specs/assets/AGENTS.md`
- `src/specs/assets/specs/README.md`
- `src/specs/assets/specs/spec-template.md`
- `src/execute/scripts/loop.py`
- `src/execute/references/optional-helper.md`
- `src/execute/scripts/providers/codex_loop.py`
- `src/execute/scripts/providers/codex_loop_dashboard.py`
- `scripts/sync_downstream.py`

In this source repo, `.agents/skills` is a tracked symlink mirror to `src/`
so copied-layout paths resolve locally without duplicating files. Edit `src/`,
not the mirror.

## Downstream Install Surface

- `make sync TARGET=/abs/path/to/repo [SKILL="consult execute"]` is the
  required downstream install and refresh path.
- `scripts/sync_downstream.py` copies selected skill directories from `src/`
  into a target repo's `.agents/skills/`, filtering out `evals/`,
  `__pycache__/`, and `*.py[cod]`.
- The sync helper replaces only the exact downstream skill paths selected for
  refresh and leaves unrelated custom skills in place.
- The sync helper also creates or fully replaces the target `README.md`
  `## Agentic Workflow` section so the human-facing workflow overview stays in
  sync with upstream wording.

## Plans Directory Semantics

- New plan-driven work should create or update one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` file.
- `execute` and `verify` must use the exact named plan path in plan-driven
  work.
- In plan-driven work, that explicit plan file is the canonical task record;
  helper logs and other generated artifacts are supporting evidence only.
- The optional `src/execute/scripts/loop.py` helper may drive continuous
  plan execution, but it still reads canonical task state from the plan file
  rather than owning its own durable state, and in continuous mode it should
  only succeed after strict final review leaves the plan complete.
- Optional provider-specific wrappers such as
  `src/execute/scripts/providers/codex_loop.py` and
  `src/execute/scripts/providers/codex_loop_dashboard.py` may sit on top of
  that generic helper for local convenience, but they remain non-owning
  accelerators.
- A small number of tracked plan-shaped eval fixtures may also live under
  `plans/` when a skill eval needs a real explicit `plans/*.md` input.
- Completed historical plan records under `plans/` are still available in the
  repo but should not be treated as the default live reading chain.

## Documentation Surface

- Keep `AGENTS.md` compact and operational.
- Put durable topic truth in `specs/`, not in task plans.
- Keep `README.md` focused on the shipped system rather than historical build
  narration.
- Use `docs/maintenance.md` for operator commands and loops, and
  `docs/sources.md` for external grounding instead of repeating them
  everywhere.

## Verification

- Run `rg --files src evals specs scripts` to confirm the shipped surface and live
  spec tree are present.
- Run `test -L CLAUDE.md` to confirm `CLAUDE.md` remains a symlink mirror to
  `AGENTS.md`.
- Run `test -L .agents/skills` to confirm the local copied-layout mirror still
  points at `src/`.
- Run `find . -maxdepth 2 \\( -path './.git' -o -path './.tmp' \\) -prune -o -maxdepth 2 -type d | sort` to confirm the top-level layout described here still matches the repo.
