# REFINE

This file tracks only the remaining follow-up after the repo-truth cleanup
work completed.

## Remaining Follow-Up

- `src/execute/scripts/plan_loop.py`: if a future session revisits an opt-in
  continue-after-`verify`-fail mode, keep the plan file as the canonical task
  record and treat any helper artifacts as supporting evidence only.
