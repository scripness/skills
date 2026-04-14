# PROMPT: Execute One Plan Slice

Use this prompt with a **fresh Codex session** and an **explicit plan file**.

Replace `<PLAN_FILE>` with the exact file you want to execute.

## Inputs

- `README.md`
- `TODO.md`
- `<PLAN_FILE>`
- any files referenced by the plan

## Task

Read `README.md`, `TODO.md`, and `<PLAN_FILE>`, then execute **only the next
unfinished milestone or bounded slice** from that plan.

## Rules

1. Do not guess the latest plan file. Use only `<PLAN_FILE>`.
2. Treat `<PLAN_FILE>` as the task source of truth for this session.
3. Read relevant repo truth before editing:
   `README.md`, `TODO.md`, the plan, and any referenced skill/docs/files.
4. Implement only one milestone or other bounded slice.
5. Do not continue into the next milestone even if more work seems obvious.
6. Run the smallest meaningful mechanical checks for the work you changed.
7. If the work changed durable repo truth, sync the relevant docs within scope.
8. If the work added or changed executable behavior that now needs test or eval
   follow-through, do that follow-through before claiming completion.
9. If the plan is stale, contradictory, or missing needed context, stop and
   report the issue instead of guessing.
10. If the session becomes noisy, correction-heavy, or clearly leaves the smart
    working zone, stop early and preserve the truth in the plan.

## Required Plan Updates Before Stopping

Update `<PLAN_FILE>` in place with:

- `Progress`
- `Decision Log`
- `Discoveries`
- `Verification`
- any new blockers or scope corrections

Mark the milestone accurately:

- complete if it is truly finished
- partial if work started but is not done
- blocked if you cannot proceed safely

## Output

Return:

1. `Completed work`
   - what you changed in this slice
2. `Mechanical results`
   - commands run and whether they passed
3. `Plan updates`
   - what changed in `<PLAN_FILE>`
4. `Next step`
   - usually `run PROMPT_verify.md against <PLAN_FILE>`

