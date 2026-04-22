---
Status: Shipped
Last verified: 2026-04-21
---

# Workflow Contract

> Source of truth: `AGENTS.md`, `README.md`, `docs/maintenance.md`,
> `docs/sources.md`, and `src/*/SKILL.md`
> Non-owning trees to ignore unless explicitly in scope: `.git/`, `.tmp/evals/`
> If this spec contradicts the code, the code is correct — update this spec.

<!-- Review when AGENTS.md changes -->
<!-- Review when README.md changes -->
<!-- Review when src/*/SKILL.md changes -->

## Overview

This repo ships a provider-agnostic six-skill workflow plus the docs, eval
metadata, and thin helpers needed to maintain it. It is the upstream source
repo for the portable skill payloads that get copied into `.agents/skills/` in
target repos.

## Non-Goals

- defining provider-specific plan modes, plugins, auto-memory, or other client
  features as required workflow primitives
- acting as an application repo or product-code monorepo
- replacing task-local `plans/*.md` files with generic topic docs

## Key Patterns

- keep durable workflow truth in checked-in files rather than chat memory
- keep `consult`, `plan`, `execute`, and `verify` as distinct steps with sharp
  trigger boundaries
- keep the shipped `src/*/SKILL.md` files as the workflow source of truth;
  keep `src/*/README.md` as human-facing companion overviews only; helpers may
  standardize invocation, transport, and presentation only
- allow a local `.agents/skills -> ../src` symlink mirror in this source repo
  for copied-layout ergonomics without creating a second owning skill tree
- prefer structured `consult -> plan` carry-forward so concrete facts,
  decisions, risks, blockers, owning paths, and durable discoveries survive
  into the explicit plan file instead of staying trapped in chat
- keep the next unfinished plan slice decision-complete so later `execute`
  work does not need to guess the core change, stop condition, or slice-level
  `specs` / `tests` exit criteria
- use `specs` for repo-truth sync and `tests` for test-truth sync
- use one explicit `plans/YYYY-MM-DD-short-task-slug.md` path when work becomes
  plan-driven
- keep that explicit plan file as the canonical task record for plan-driven
  work
- keep helper automation optional and file-backed, including opt-in continuous
  helper flows that still rely on plan state rather than chat memory
- when provider support exists, let `consult` and `verify` prefer one
  independent pass, but keep the main session responsible for applying the
  skill and comparing or synthesizing results rather than blindly trusting
  either side alone
- treat `src/<skill>/` as the full upstream source payload and downstream
  `.agents/skills/<skill>/` as a filtered installed payload rather than a
  byte-for-byte mirror
- use `make sync`, backed by `scripts/sync_downstream.py`, as the required
  downstream install and refresh workflow

## Truth Layers

- `AGENTS.md` owns repo-wide operational truth.
- `specs/` owns durable topic truth for this repo.
- `README.md` owns the high-level shipped-system overview.
- `docs/maintenance.md` owns the operator loop for updates and eval refresh.
- `docs/sources.md` owns durable external grounding.
- `plans/*.md` own task-local plans for new work and also contain a small
  number of tracked plan-shaped eval fixtures plus completed historical build
  records.
- `src/`, `scripts/`, and `evals/` are the shipped implementation surface
  behind those docs.
- `.agents/skills/` may exist locally as a symlink mirror to `src/` for
  copied-layout checks, but it is not a separate truth layer.

## Six-Skill Contract

- `consult` owns clarification, option comparison, and recommendation when the
  next move is not yet clear enough to execute or plan, and it should leave
  copy-ready carry-forward when the safest next move is `plan`.
- `plan` owns one explicit plan file when durable task state is needed across
  sessions, milestones, or review loops, and it should leave the next
  unfinished slice decision-complete enough for later `execute` work to act
  without guessing.
- `execute` owns one bounded implementation slice plus the smallest meaningful
  checks, required `specs` or `tests` follow-through, and truthful plan
  updates for the current execution slice. If the next unfinished plan slice
  is under-specified, it should stop or bounce back to `plan` instead of
  guessing.
- `verify` owns adversarial review of a concrete plan, implementation slice,
  diff, or claim, and in plan-driven work writes its findings back into the
  same explicit plan file, reopening or appending one bounded follow-up slice
  when repairable review failures disprove completion. For plan review, weak
  next-slice contracts and missing required slice-level `specs` / `tests`
  exit criteria are failures, not soft risks.
- `specs` owns repo-truth bootstrap and sync in `AGENTS.md`, `CLAUDE.md`, and
  `specs/`.
- `tests` owns test-truth bootstrap and sync when coverage is missing, stale,
  or too weak for safe work.

## Distribution And Refresh

- Use `make sync TARGET=/abs/path/to/repo [SKILL="consult execute"]` as the
  required downstream install and refresh path.
- The sync helper copies filtered skill payloads from `src/` into the target
  repo's `.agents/skills/`, excluding upstream-only `evals/`,
  `__pycache__/`, and `*.py[cod]`.
- The sync helper also creates or fully replaces the target `README.md`
  `## Agentic Workflow` section with the managed human-facing workflow
  overview, including the currently installed shipped skills.
- In this source repo, `.agents/skills` may exist as a tracked symlink mirror
  to `src/` for local copied-layout checks; it does not replace `src/` as the
  authoritative source.
- Keep helper scripts, wrapper commands, and provider-specific integrations
  optional and replaceable.
- Keep the workflow file-backed so a fresh session can recover truth from the
  repo alone.

## Plans And Historical Records

- For new task work, `plan` and `execute` must use one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` path.
- In plan-driven work, that explicit plan file remains the canonical task
  record across `plan`, `execute`, and `verify`.
- The next unfinished slice in that file should be decision-complete enough
  that a fresh `execute` session knows what to change, when to stop, and which
  slice-level `specs` / `tests` follow-through is part of done.
- Durable discoveries from `consult` or `verify` that matter to later work
  should be promoted into that explicit plan file instead of being left only in
  chat or helper output.
- `src/execute/scripts/loop.py` may optionally continue after repairable
  verify failures and run one strict final whole-plan verify pass, but it
  remains a thin helper rather than workflow truth.
- Optional provider-specific accelerators may also exist under
  `src/execute/scripts/providers/`, but they must remain replaceable wrappers
  or dashboards over the generic helper rather than redefining the workflow
  contract.
- Helper scripts may add machine-readable events, exit-code transport, default
  provider commands, or terminal presentation, but they must not become a
  competing source of workflow semantics against `src/*/SKILL.md`.
- If the generic loop grows additive machine-readable events for local
  dashboards, those events must remain backward-compatible and must not move
  canonical task state out of the plan file.
- Never guess the latest plan file.
- Completed historical plan records under `plans/` are available as background
  source material but are not the default operational reading chain.
- Tracked evals that need a real plan-shaped input now use neutral fixture
  files instead of depending on the completed historical build plans.

## Verification

- Inspect `AGENTS.md`, `README.md`, and `src/*/SKILL.md` together when judging
  whether the workflow contract is still aligned.
- Run `rg -n "plans/YYYY-MM-DD-short-task-slug.md|Never guess the latest plan file|never guess the latest plan file" src/plan/SKILL.md src/execute/SKILL.md AGENTS.md` to confirm the explicit-plan contract still appears in the shipped surface.
- Run `rg -n "provider-specific|auto-memory|plan modes|plugins" AGENTS.md README.md specs` when checking that the repo still stays provider-agnostic.
- Run `rg -n "decision-complete|under-specified|slice-level" src/plan/SKILL.md src/plan/assets/plan-template.md src/execute/SKILL.md src/verify/SKILL.md specs/workflow-contract.md` when checking the tightened plan and execute handoff contract.
