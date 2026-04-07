---
name: verify
description: Adversarially verify a plan, implementation, or set of claims against repo truth and mechanical checks.
argument-hint: [what to verify]
---

Use this skill after implementation, on a proposed plan, or to fact-check a
technical claim.

## Inputs

- the thing being verified
- `AGENTS.md`
- relevant `specs/*`
- current code and test state

## Process

1. Determine verification target.
   - `plan`: verify the plan matches repo reality and intended scope
   - `implementation`: verify changed code, tests, and behavior
   - `claims`: verify specific conclusions against code and specs

2. Audit the target against repo truth.
   - Identify the concrete claims being verified.
   - Use `AGENTS.md`, `specs/*`, and code to determine what should be true.

3. Run mechanical checks when code changed.
   - Use the exact commands from `AGENTS.md`.
   - Run the smallest set that still proves correctness.
   - If required checks are too expensive or blocked, say so clearly.
   - If the repo already has unrelated failing checks, separate that baseline
     from failures introduced or exposed by the current work.

4. Verify against source of truth.
   - code for reality
   - `specs/*` for intended behavior
   - `AGENTS.md` for repo rules and required test tiers

5. Check testing honestly.
   - Were tests added or updated at every applicable tier?
   - Do the tests prove the intended behavior rather than internal details?
   - Are important edge cases still uncovered?

6. Apply adversarial reasoning.
   - Try to disprove the target, not to defend it.
   - If the provider supports subagents or isolated passes, use separate angles
     such as:
     - core correctness
     - regressions and edge cases
     - test coverage and blind spots
     - security or authorization when relevant
   - If it does not, still perform those angles explicitly in one review.

## Output

For implementations and plans, return findings first.

Format:

1. `Findings`
   - Ordered by severity
   - Include file references or command evidence
   - Focus on bugs, regressions, missing tests, stale assumptions
2. `Mechanical results`
   - Commands run and whether they passed
3. `Verdict`
   - `pass`, `pass with risks`, or `fail`
4. `Remaining gaps`
   - What still needs testing, spec updates, or follow-up

If there are no findings, say that explicitly and still note residual risk.

## Rules

- Do not invent failures. Ground each claim in code, specs, or command output.
- Prefer concrete reproduction paths over vague concern language.
- Missing or weak tests are real findings when the repo's testing policy
  requires them.
- If docs drifted during the work, recommend running the `specs` skill.
- If test truth drifted during the work, recommend running the `tests` skill.
- This skill is a verifier, not an implementer. It can suggest fixes, but its
  main job is to judge the target honestly.

## Verdict Rubric

- `pass`: no material findings; required checks passed or baseline issues were
  clearly unrelated
- `pass with risks`: no blocking defect, but there are meaningful residual
  risks, weak coverage, or blocked checks
- `fail`: concrete correctness, regression, or policy-compliance issues remain
