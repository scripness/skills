---
Status: Shipped
Last verified: 2026-04-21
---

# Workflow Contract

> Source of truth: `AGENTS.md`, `README.md`, `MAINTENANCE.md`, `SOURCES.md`,
> `REFINE.md`, and `src/*/SKILL.md`
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
- use `specs` for repo-truth sync and `tests` for test-truth sync
- use one explicit `plans/YYYY-MM-DD-short-task-slug.md` path when work becomes
  plan-driven
- keep that explicit plan file as the canonical task record for plan-driven
  work
- use manual copy as the baseline distribution and refresh workflow

## Truth Layers

- `AGENTS.md` owns repo-wide operational truth.
- `specs/` owns durable topic truth for this repo.
- `README.md` owns the high-level shipped-system overview.
- `MAINTENANCE.md` owns the operator loop for updates and eval refresh.
- `SOURCES.md` owns durable external grounding.
- `REFINE.md` owns current post-merge cleanup context.
- `plans/*.md` own task-local plans for new work and also contain a small
  number of tracked plan-shaped eval fixtures plus completed historical build
  records.
- `src/` and `evals/` are the shipped implementation surface behind those
  docs.

## Six-Skill Contract

- `consult` owns clarification, option comparison, and recommendation when the
  next move is not yet clear enough to execute or plan.
- `plan` owns one explicit plan file when durable task state is needed across
  sessions, milestones, or review loops.
- `execute` owns one bounded implementation slice plus the smallest meaningful
  checks, required `specs` or `tests` follow-through, and truthful plan updates
  for the current execution slice.
- `verify` owns adversarial review of a concrete plan, implementation slice,
  diff, or claim, and in plan-driven work writes its findings back into the
  same explicit plan file.
- `specs` owns repo-truth bootstrap and sync in `AGENTS.md`, `CLAUDE.md`, and
  `specs/`.
- `tests` owns test-truth bootstrap and sync when coverage is missing, stale,
  or too weak for safe work.

## Distribution And Refresh

- Copy the source skill directories from `src/` into `.agents/skills/` in the
  target repo.
- Refresh downstream repos by re-copying only the changed skill directories and
  supporting assets.
- Keep helper scripts, wrapper commands, and provider-specific integrations
  optional and replaceable.
- Keep the workflow file-backed so a fresh session can recover truth from the
  repo alone.

## Plans And Historical Records

- For new task work, `plan` and `execute` must use one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` path.
- In plan-driven work, that explicit plan file remains the canonical task
  record across `plan`, `execute`, and `verify`.
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
