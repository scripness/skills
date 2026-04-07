---
name: tests
description: Keep the test suite aligned with current code behavior and repo testing policy across all applicable existing layers.
argument-hint: [task, feature, branch, or changed area]
---

Use this skill after implementation or when you suspect test coverage has
drifted from reality.

This skill is the testing analogue of `specs`:

- `specs` keeps repo docs and intent aligned with reality
- `tests` keeps repo tests and verification layers aligned with reality

## Inputs

- the task, feature, branch, or changed area
- `AGENTS.md`
- relevant `specs/*`, especially testing-related specs
- current code and test tree

## Process

1. Determine scope.
   - Prefer the changed files, changed behavior, and owning specs.
   - If no explicit scope is given, infer it from recent changes or the current
     task context.

2. Audit the current test truth layer.
   - Read the testing rules in `AGENTS.md`.
   - Read any testing spec in `specs/`.
   - Inspect the actual test tree to confirm what layers already exist.
   - Identify:
     - changed behavior that should be covered
     - existing coverage that is stale, thin, or absent
     - applicable test tiers for this work
     - useful existing helpers and patterns to reuse
     - other repo-specific layers such as smoke, contract, browser, visual, or
       performance tests if they already exist

3. Consult before broad or uncertain test work.
   - If it is unclear which layers matter most, or the affected system is
     complex, perform a short internal consultation.
   - Cover at least:
     - behavior that truly changed
     - best test layers for that behavior
     - edge cases and regressions worth locking down
   - If the provider supports independent passes, use them. Otherwise do this
     in one session.

4. Verify the intended test updates before and after writing.
   - Check that the chosen tests actually map to repo policy and changed
     behavior.
   - After writing tests, adversarially check for important uncovered paths or
     false confidence.
   - If unrelated failures already exist, separate that baseline from problems
     introduced by the current work.

5. Sync the suite with reality.
   - Add or update tests at every applicable existing layer.
   - Match changed behavior to the layers the repo already expects; do not stop
     at unit tests when integration, e2e, browser, or contract coverage is
     clearly required.
   - Reuse existing helpers, fixtures, factories, and patterns.
   - Do not invent new testing infrastructure unless the repo clearly needs it
     and the user asked for it.

6. Run the mechanical checks required by the repo.
   - Use the exact commands from `AGENTS.md`.
   - Prefer targeted test commands during iteration, then the required broader
     checks for final confirmation.

## Output

Return a short summary with:

- which test layers were applicable
- which tests were added or updated
- which commands were run and whether they passed
- any remaining risk or uncovered area

## Rules

- The internal shape of this skill is: audit -> consult -> verify -> apply.
- Match the repo's existing test style before adding new tests.
- Treat missing required test layers as a real gap.
- Prefer behavior-oriented tests over implementation-detail tests.
- Prefer proportional fixes. Unrelated legacy test debt should be surfaced, but
  should only be absorbed into the current work when it blocks safe
  verification.
- If the testing policy in `AGENTS.md` or `specs/` is stale, recommend running
  the `specs` skill after the test work is complete.
