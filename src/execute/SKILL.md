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
   - In plan-driven mode, read the current `Blockers`, `Progress`,
     `Decision Log`, `Discoveries`, `Verification`, and `Open Questions`
     before choosing the slice.
   - In plan-driven mode, identify the next unfinished milestone or other
     bounded slice.
   - In plan-driven mode, check whether the next unfinished slice is
     decision-complete enough to execute safely.
   - Treat a slice as under-specified when it lacks a clear done condition,
     leaves the core approach or owning paths ambiguous, or omits explicit
     slice-level `specs` / `tests` exit criteria that later review would need.
   - Identify any required `specs` or `tests` follow-through from repo truth,
     the plan, and the changed paths.

3. Choose one bounded slice.
   - In direct mode, choose the smallest implementation slice that can be
     completed safely in the current session.
   - In plan-driven mode, implement only one milestone or other bounded slice.
   - If current blockers or prior verification findings make the next
     unfinished milestone unsafe or mislabeled, stop or narrow the slice
     instead of pushing through.
   - If the next unfinished slice is under-specified, do not guess. Stop and
     hand back to `plan`, or narrow the slice only when the narrower contract
     is still truthful to the plan and safe to execute.
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
   - Use any slice-level `specs` / `tests` exit criteria already recorded in
     the plan as part of the completion check for the current slice.
   - If required `specs` or `tests` follow-through is blocked, stop and report
     that blocker instead of claiming the slice is done.

7. Update the plan when plan-driven.
   - Update the explicit plan file in place.
   - Record `Progress`, `Decision Log`, `Discoveries`, `Verification`, and any
     new blockers or scope corrections.
   - Mark the milestone accurately for the execution slice: complete, partial,
     or blocked, and leave enough truth behind for later `verify` to confirm or
     correct it.

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
- In plan-driven work, do not ignore prior blockers, discoveries, decisions, or
  verification findings when choosing the next slice.
- Do not create or reshape durable task state when `plan` is required.
- Never guess the active or latest plan file.
- Keep provider features such as plan modes, subagents, or worktrees optional
  only.
- Prefer fresh sessions for serious plan-driven work.
- Stop when blocked, noisy, or correction-heavy rather than pretending the
  session is still sharp.

## Optional Helper

`scripts/loop.py` is an optional local convenience wrapper for
plan-driven work. It is not workflow truth and it does not replace the skill
contract.

The shipped skill contracts remain the workflow source of truth. Any helper
script in this repo may only add invocation mechanics, machine-readable event
transport, exit-code mapping, or presentation on top of those contracts.

This source repo may also ship provider-specific convenience wrappers above the
generic helper, such as `scripts/providers/codex_loop.py`. Those wrappers are
local accelerators only and must delegate back to the generic `scripts/loop.py`
contract rather than redefining it.

This source repo may also ship provider-specific dashboard wrappers above those
provider wrappers, such as `scripts/providers/codex_loop_dashboard.py`. Those
dashboard layers are presentation only. They may consume the generic helper's
machine-readable event stream, but they must not become the owner of loop
control, verdicts, or plan truth.

When used, pass one explicit plan path and one explicit non-interactive
external runner command. The helper expects that runner to accept
`execute <plan>` and `verify <plan>` invocations, keep durable state in repo
files plus the plan file, persist plan-driven verification findings back into
that same plan file, and map `verify` outcomes to exit codes the helper can
judge: `0` = pass, `10` = pass with risks, `20` = fail.

When `--continue-after-fail` is used, the helper may continue after a
repairable `verify=fail` only when the updated plan is not blocked and still
shows remaining work. In that opt-in mode, the `verify <plan>` pass that runs
against a now-complete plan becomes the strict final review and succeeds only
on `verify=pass`. If the plan is already complete before the next `execute`
pass would start, the helper runs one strict completion review before exiting.

`--allow-pass-with-risks` applies only to slice-level verify passes. Strict
final review still requires `pass`. If final review finds a cross-cutting issue
that does not map cleanly to an existing milestone, `verify` should append one
new bounded follow-up milestone rather than hide the failure inside unrelated
history.

## Quality Bar

- Entry mode was chosen correctly and any anti-trigger was respected.
- Repo truth was read before editing.
- Plan-driven work reads the current plan context before selecting the slice.
- Under-specified plan slices cause `execute` to stop or narrow truthfully
  instead of improvising missing plan detail.
- Only one bounded slice was implemented.
- Mechanical checks are specific, relevant, and honest about baseline noise.
- Required `specs`/`tests` follow-through was completed or surfaced as
  blocking.
- Slice-level `specs` / `tests` exit criteria were honored when the plan named
  them.
- Plan-driven work leaves the explicit plan file resumable for the next fresh
  session.
- In opt-in continuous helper mode, repairable verify failures reopen or append
  bounded work in the plan instead of being lost in chat or helper logs.
- The handoff to `verify` is explicit.
