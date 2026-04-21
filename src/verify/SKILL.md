---
name: verify
description: Adversarially judge one concrete plan, implementation slice, diff, or technical claim against repo truth, required sync, and bounded mechanical checks.
argument-hint: [plan path, implementation slice, diff, or claim]
---

Use this skill only when there is already a concrete target to judge: a plan,
an implementation slice, a diff or PR, or a specific technical claim.

Examples:

- does this plan match repo reality and intended scope?
- did this implementation slice actually do what it claims?
- does this diff miss required specs/tests sync?
- is claim X true in the current repo?

Do not use this skill when:

- the next move is still unclear and you need clarification or option analysis;
  use `consult`
- the task is to create or maintain durable task state; use `plan`
- the user asked for implementation or fixes now; use `execute`
- there is no concrete target yet to judge

## Inputs

- the thing being verified
- `AGENTS.md`
- relevant `specs/*`
- the explicit plan file, when the target comes from plan-driven work
- the changed files, diff, or command claims being judged
- current code and test state

## Process

1. Determine verification target and obligations.
   - `plan`: verify scope, sequencing, owning paths, blockers, and explicit
     `specs` or `tests` follow-through against repo reality
   - `implementation`: verify changed code, docs, tests, and behavior against
     the plan or claimed outcome
   - `claims`: verify each concrete technical statement against code, specs,
     and command evidence
   - If multiple target types are mixed together, say which one is primary and
     judge the rest only as supporting evidence.

2. Audit the target against repo truth.
   - Identify the concrete claims, obligations, and success conditions being
     verified.
   - Use `AGENTS.md`, relevant `specs/*`, the plan file when present, and code
     to determine what should be true.
   - If repo truth is missing, stale, or contradictory, say so explicitly.

3. Run the smallest meaningful mechanical checks.
   - Use the exact commands from `AGENTS.md` when they are needed.
   - For plan-only review, inspection may be enough; do not run noisy commands
     without a reason.
   - For implementation or diff review, run the smallest set that could prove
     or disprove the claimed result.
   - If required checks are too expensive, unavailable, or blocked, say exactly
     what stopped them and how that limits the verdict.
   - If the repo already has unrelated failing checks, separate that baseline
     from failures introduced or exposed by the current work.

4. Attack the target adversarially.
   - `plan`: look for scope mismatch, weak sequencing, missing owning paths,
     hidden blockers, and missing required sync.
   - `implementation`: look for correctness bugs, regressions, stale docs or
     tests, missing required sync, and uncovered edge cases.
   - `claims`: look for unsupported statements, stale assumptions, or omitted
     contrary evidence.
   - Ground every finding in file references or command output.

5. Check testing and spec obligations honestly.
   - Were tests added or updated at every applicable tier?
   - Do the tests prove the intended behavior rather than internal details?
   - Are important edge cases still uncovered?
   - If the plan or repo truth made `specs` or `tests` sync required and it is
     missing, treat that as a finding.
   - Missing required `specs` or `tests` sync is `fail`, not
     `pass with risks`, when the obligation is clear.

6. Apply adversarial reasoning.
   - Try to disprove the target, not to defend it.
   - Cover the angles that matter for the target, such as core correctness,
     regressions, coverage blind spots, and security or authorization when
     relevant.

7. Update the plan when verifying an explicit plan file.
   - Update that exact plan file in place so it remains the canonical task
     record for plan-driven work.
   - Record the dated verdict, findings summary, and supporting command
     evidence in `Verification`.
   - Add or clear `Blockers` to reflect whether follow-up blocks the next safe
     `execute` slice.
   - Record any material repo facts learned during review in `Discoveries`.
   - Correct `Progress` only when review proves the current milestone status in
     the plan is materially inaccurate.
   - Do not implement fixes or broaden into general plan maintenance.

## Output

Return findings first for plans, implementations, and claims.

Format:

1. `Findings`
   - Ordered by severity
   - Open by naming the verification target
   - Include file references or command evidence
   - Focus on bugs, regressions, missing required sync, stale assumptions, and
     blocked evidence that materially limits confidence
2. `Mechanical results`
   - Commands run and whether they passed, failed, or were blocked
3. `Verdict`
   - `pass`, `pass with risks`, or `fail`
4. `Remaining gaps`
   - What still needs testing, spec updates, or follow-up
5. `Plan updates`
   - When an explicit plan file was verified, say what task-local sections were
     updated

If there are no findings, say that explicitly and still note blocked checks or
residual risk.

## Rules

- Do not invent failures. Ground each claim in code, specs, or command output.
- Prefer concrete reproduction paths over vague concern language.
- Missing or weak tests are real findings when the repo's testing policy
  requires them.
- Missing required `specs` or `tests` sync is a `fail` when the obligation was
  explicit in the plan or clearly implied by repo truth.
- Blocked or skipped checks are not silent passes. Say what was not run and why.
- When the verification target is an explicit plan file, update only the
  task-local sections needed to keep that plan truthful; do not broaden into
  creating or reshaping the plan itself.
- If docs drifted during the work, recommend running the `specs` skill.
- If test truth drifted during the work, recommend running the `tests` skill.
- This skill is a verifier, not an implementer. It can suggest fixes, but its
  main job is to judge the target honestly.

## Verdict Rubric

- `pass`: no material findings; required checks passed or baseline issues were
  clearly unrelated
- `pass with risks`: no blocking defect, but there are meaningful residual
  risks, weak coverage, or blocked checks that do not yet justify a fail
- `fail`: concrete correctness, regression, or policy-compliance issues remain,
  required `specs` or `tests` sync is missing, or blocked evidence leaves a
  material claim unproven
