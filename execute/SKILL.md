---
name: execute
description: Implement one bounded task directly or execute the next bounded slice from an explicit plan file, then run mechanical checks and hand off to verify.
argument-hint: [bounded task or explicit plan path]
---

Use this skill when the user wants implementation now.

Valid entry modes:

- `direct`: the work is still locally clear, bounded, and does not need durable
  task state
- `plan-driven`: there is already one explicit `plans/*.md` path to execute

Do not use this skill when:

- the next move is still unclear and needs `consult`
- the work now needs durable task state but no explicit plan file exists yet;
  use `plan`
- the request is adversarial review, final judgment, or fact-checking; use
  `verify`

## Inputs

- the user task
- `AGENTS.md`
- relevant `specs/*`
- relevant tests, testing policy, or existing test patterns
- current codebase
- the explicit plan file, when the work is plan-driven

## Process

1. Determine entry mode.
   - Use `direct` only when the implementation is still locally clear and
     bounded.
   - Use `plan-driven` only when there is one explicit `plans/*.md` path.
   - Never guess the latest plan file.
   - If direct-mode work stops being locally clear or starts needing durable
     task state, stop and hand off to `plan`.

2. Read repo truth before editing.
   - Read `AGENTS.md`, the relevant `specs/*`, the affected code and tests, and
     the explicit plan file when present.
   - In plan-driven mode, identify the next unfinished milestone or other
     bounded slice.
   - Identify any required `specs` or `tests` follow-through from repo truth,
     the plan, and the changed paths.

3. Choose one bounded slice.
   - In direct mode, choose the smallest implementation slice that can be
     completed safely in the current session.
   - In plan-driven mode, implement only one milestone or other bounded slice.
   - Do not continue into the next milestone even if more work is obvious.

4. Implement the slice.
   - Make only the code and file changes needed for that one slice.
   - Keep notes on discoveries, decisions, blockers, and unexpected corrections
     that matter for resumption.
   - If repeated corrections, dead ends, or context clutter push the session
     out of the smart working zone, stop early, preserve the truth, and
     recommend a fresh session.

5. Run bounded mechanical checks.
   - Use the smallest meaningful commands that test the changed slice.
   - Follow the repo command guidance in `AGENTS.md`.
   - Separate unrelated baseline failures from failures introduced by the
     current work.

6. Complete required follow-through.
   - If the slice changed durable repo truth, sync the relevant `specs`
     follow-through before claiming completion.
   - If the slice changed behavior that now needs added or updated coverage at
     the applicable existing test layers, sync the relevant `tests`
     follow-through before claiming completion.
   - If required `specs` or `tests` follow-through is blocked, stop and report
     that blocker instead of claiming the slice is done.

7. Update the plan when plan-driven.
   - Update the explicit plan file in place.
   - Record `Progress`, `Decision Log`, `Discoveries`, `Verification`, and any
     new blockers or scope corrections.
   - Mark the milestone accurately: complete, partial, or blocked.

8. Hand off to `verify`.
   - Return the bounded slice that was completed, the mechanical results, any
     follow-through done, and the exact next `verify` handoff target.
   - Do not absorb adversarial review into `execute`.

## Output

Return:

1. `Completed work`
2. `Mechanical results`
3. `Plan updates`
   - If direct mode was used, say that no plan file was involved
4. `Follow-through`
   - `specs` or `tests` sync done, not needed, or blocked
5. `Next step`

## Rules

- `execute` owns implementation and bounded mechanical checks only.
- Do not create or reshape durable task state when `plan` is required.
- Never guess the active or latest plan file.
- Keep provider features such as plan modes, subagents, or worktrees optional
  only.
- Prefer fresh sessions for serious plan-driven work.
- Stop when blocked, noisy, or correction-heavy rather than pretending the
  session is still sharp.

## Quality Bar

- Entry mode was chosen correctly and any anti-trigger was respected.
- Repo truth was read before editing.
- Only one bounded slice was implemented.
- Mechanical checks are specific, relevant, and honest about baseline noise.
- Required `specs`/`tests` follow-through was completed or surfaced as
  blocking.
- Plan-driven work leaves the explicit plan file resumable for the next fresh
  session.
- The handoff to `verify` is explicit.
