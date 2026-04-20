# REFINE

This file tracks only the remaining refinement questions after the repo-truth
cleanup work completed.

## Current Status

- Live operational truth now lives in `AGENTS.md`, `README.md`,
  `MAINTENANCE.md`, `SOURCES.md`, top-level `specs/`, `src/`, and `evals/`.
- Secondary historical framing has been removed from the active harness docs
  and helper text.
- Skill-local evals now use neutral tracked fixtures instead of depending on
  the completed 2026-04-14 build-plan files.
- The completed 2026-04-14 build records remain in `plans/` as historical
  background.

## Remaining / Needs Clarification

- No mandatory repo-truth cleanup is currently open.
- If helper follow-up is revisited later, decide whether extending
  `src/execute/scripts/plan_loop.py` is worth the added complexity.

## Optional Helper Follow-Up

If helper work is revisited later, keep it optional, file-backed,
explicit-plan-path only, non-interactive by default, and bounded.

Possible follow-up:

1. Persist failed `verify` outputs as durable plan-scoped artifacts.
2. Start a fresh remediation `execute` run after `verify=fail`.
3. Pass the latest failed verify artifact into that remediation run without
   guessing paths or state.
4. Re-run fresh `verify` after remediation and stop on repeated or conflicting
   failures.
5. Keep `verify` as a verifier only; do not let it patch code directly.
