# Eval Harness Follow-Up Roadmap Fixture

This file is a neutral tracked fixture used by skill evals that need a real
roadmap-style input without depending on the completed 2026-04-14 build plans.

## Goal

Carry the shipped evaluation harness forward through a few bounded follow-up
slices without changing the baseline six-skill workflow.

## Current State

- The repo already ships tracked skill-local eval definitions.
- The repo already ships `evals/runtime.json`, `evals/fixtures/cryptoli.json`,
  `evals/scripts/harness.py`, and the thin repo-root `Makefile`.
- The remaining work is cleanup and follow-up, not inventing the first harness.

## Remaining Follow-Up Slices

1. Keep the live repo-truth layer aligned with the shipped harness surface.
2. Remove historical framing from secondary docs and helper text where that
   wording still reads like current workflow truth.
3. Replace skill-eval dependence on completed build-plan files with neutral
   tracked fixtures where plan-shaped inputs still help.

## Constraints

- Keep the repo provider-agnostic.
- Keep helper automation optional and thin.
- Keep completed historical build records available for background reference.
- Use explicit plan files when work becomes multi-session or review-driven.
