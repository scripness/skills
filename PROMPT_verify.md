# PROMPT: Verify One Plan Or Latest Plan Slice

Use this prompt with a **fresh Codex session** and an **explicit plan file**.

Replace `<PLAN_FILE>` with the exact file you want to verify.

## Inputs

- `README.md`
- `TODO.md`
- `<PLAN_FILE>`
- any files referenced by the plan
- the current repo state

## Task

Read `README.md`, `TODO.md`, and `<PLAN_FILE>`, then verify the plan against the
current repo state.

If implementation has already happened for the most recently updated milestone,
verify that implementation slice too. If no implementation has happened yet,
verify the plan itself.

## Rules

1. Do not guess the latest plan file. Use only `<PLAN_FILE>`.
2. Treat `<PLAN_FILE>` as the task source of truth for this verification.
3. Read relevant repo truth before judging:
   the plan, the changed files, and any referenced docs or skill files.
4. Verify adversarially. Try to disprove correctness, sequencing, and sync
   claims rather than defend them.
5. Check whether required repo-truth sync was done.
6. Check whether required test or eval follow-through was done.
7. Run the smallest meaningful mechanical checks if they are needed to ground a
   finding; if checks are blocked or too expensive, say so clearly.
8. Do not implement fixes. Report findings only.

## Output

Return findings first.

1. `Findings`
   - ordered by severity
   - grounded in file references or command evidence
2. `Mechanical results`
   - commands run and whether they passed
3. `Verdict`
   - `pass`, `pass with risks`, or `fail`
4. `Remaining gaps`
   - what still needs fixing, syncing, or checking before the next execution
     slice

If there are no findings, say that explicitly and still note any residual risk.
