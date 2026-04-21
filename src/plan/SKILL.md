---
name: plan
description: Create or maintain a self-contained living task plan in plans/ when work needs durable state across sessions, milestones, or review loops.
argument-hint: [task and explicit plan path when known]
---

Use this skill when the direction is already clear enough to structure, but
the work now needs durable task state.

Examples:

- the task will span multiple milestones or review passes
- discoveries, blockers, or handoffs need to survive a fresh session
- the user already knows the direction and wants a resumable plan file
- the implementation will be restarted from fresh context

Do not use this skill when:

- the next move is still unclear and needs `consult`
- the task is a simple lookup or short clarification
- the work is still locally clear enough for one bounded execution pass
- the user asked for implementation now and durable task state is not needed

## Inputs

- the user task
- `AGENTS.md`
- relevant `specs/*`
- relevant tests, testing policy, or existing test patterns
- current codebase
- the existing plan file, if one was provided

## Process

1. Confirm that planning is warranted.
   - Promote based on durable-state need, not abstract task size.
   - If clarification is still missing, hand back to `consult`.
   - If execution is still locally clear and bounded, recommend `execute`
     directly instead of inventing a plan.

2. Read repo truth before writing.
   - Inspect `AGENTS.md`, relevant `specs/*`, and the owning code and test
     paths.
   - Identify the durable repo-truth and test-truth follow-through this task
     may require.

3. Choose one explicit plan path.
   - Use a user-provided plan path when given.
   - Otherwise use `plans/YYYY-MM-DD-short-task-slug.md`.
   - Create `plans/` when it does not exist.
   - Prefer updating the existing plan in place over creating duplicates.

4. Write or update one living plan document.
   - Make it resumable from repo truth plus the plan file alone.
   - Capture:
     - `Goal`
     - `Scope`
     - `Non-Goals`
     - repo context and owning code, spec, and test paths
     - explicit sync expectations for `specs` and `tests`
     - milestones or other bounded slices
     - verification plan plus accumulated execution and verification history
     - risks and open questions
     - blockers
     - progress
     - discoveries
     - decision log
     - outcomes or retrospective
   - Break the work into bounded milestones that a fresh `execute` session can
     take one at a time.

5. Make sync expectations explicit.
   - Name the owning specs or missing specs that will need follow-through.
   - Name the applicable test layers and expected coverage follow-through.
   - Say when `specs` sync is required and when `tests` sync is required.
   - If either sync is not currently required, say that explicitly.

6. Hand off cleanly.
   - Return the exact plan path.
   - Tell later `execute` and `verify` sessions to use that exact path and keep
     task-local truth in that same file.
   - Do not implement code, modify repo truth, or broaden into execution work
     inside `plan`.

## Output

Return:

1. `Plan path`
2. `Why plan`
3. `Plan summary`
4. `Handoff`

## Rules

- `plan` owns task-local plan files only.
- Do not create repo-wide planning docs such as `PLANS.md` as a baseline
  requirement.
- Do not leave the active plan implied in chat; always carry the explicit path
  forward.
- Keep provider features such as plan mode, plugins, or auto-memory optional
  only.
- Keep the plan concrete, update-in-place, and specific to the current task
  rather than turning it into a general backlog.
- Keep the explicit plan file as the canonical task record for plan-driven
  work.
- If the task or scope is too unclear to plan safely, stop and surface the
  ambiguity instead of guessing.

## Quality Bar

- The trigger is evidence-backed: durable task state is actually needed.
- The plan is self-contained enough for a fresh session to resume safely.
- Milestones are bounded, ordered, and verifiable.
- Material blockers are named explicitly rather than left in chat.
- `specs` and `tests` obligations are named explicitly rather than implied.
- The handoff names one exact `plans/*.md` file.
