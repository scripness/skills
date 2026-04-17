---
name: tests
description: Bootstrap, extend, or sync test truth by discovering the repo's actual test topology and covering the right layers for safe execution and verification.
argument-hint: [task, feature, branch, or changed area]
---

Use this skill in three user-facing situations:

1. bootstrap test truth when a repo has little or no reliable automated
   coverage yet
2. sync existing tests after behavior changes or when coverage has drifted from
   reality
3. close concrete coverage gaps that are blocking safe execution or
   verification

This skill may also be auto-invoked during implementation when changed
behavior or repo policy makes the current test truth clearly insufficient.

This skill is the testing analogue of `specs`:

- `specs` keeps repo docs and intent aligned with reality
- `tests` keeps repo tests and verification layers aligned with reality

Treat test-topology discovery as part of bootstrap, sync, and gap-close work.
Before writing tests, determine what the repo actually owns, where suites live,
which commands drive them, and which paths are real test surfaces versus
generated or vendor noise.

## Inputs

- the task, feature, branch, or changed area
- `AGENTS.md`
- relevant `specs/*`, especially testing-related specs
- current code and test tree

## Process

1. Determine scope.
   - `bootstrap`: test truth is missing or clearly too weak for the repo
   - `sync`: existing tests need to catch up with changed behavior or current
     repo policy
   - `gap-close`: the suite exists, but a concrete coverage hole is blocking
     safe execution or verification
   - Prefer the changed files, changed behavior, and owning specs.
   - If no explicit scope is given, infer it from recent changes or the current
     task context.

2. Audit the current test truth layer and repo shape.
   - Read the testing rules in `AGENTS.md`.
   - Read any testing spec in `specs/`.
   - Inspect the current codebase, test tree, runner configs, and CI hooks
     before deciding what to change.
   - Map the actual test topology:
     - monorepo vs single package
     - per-app, per-package, per-service, or shared suites
     - colocated tests vs top-level `src/tests/`, `e2e/`, or other suite roots
     - runner and command roots that define how each suite is executed
     - existing layers such as unit, integration, e2e, smoke, browser,
       contract, visual, security, or performance tests
   - Separate owning test surfaces from non-owning trees. Ignore vendor,
     generated, cache, and copied noise by default unless the task explicitly
     targets it:
     - `node_modules/`
     - package-manager stores and framework caches
     - build outputs such as `dist/`, `build/`, `.next/`, or coverage reports
     - vendored dependencies and copied artifacts
   - Identify:
     - changed behavior that should be covered
     - existing coverage that is stale, thin, or absent
     - applicable test tiers for this work
     - useful existing helpers and patterns to reuse
     - which layers are required by repo policy or boundary risk versus merely
       nice to have
     - whether a weak repo needs minimal bootstrap coverage before deeper sync
     - other repo-specific layers such as smoke, contract, browser, visual, or
       performance tests if they already exist

3. Consult before broad or uncertain test work.
   - If it is unclear which layers matter most, or the affected system is
     complex, perform a short internal consultation.
   - Cover at least:
     - behavior that truly changed
     - best test layers for that behavior
     - whether this slice needs bootstrap, sync, or explicit gap reporting
     - edge cases and regressions worth locking down
   - If the provider supports independent passes, use them. Otherwise do this
     in one session.

4. Verify the intended test updates before and after writing.
   - Check that the chosen tests actually map to repo policy, changed
     behavior, and the repo's real test topology.
   - After writing tests, adversarially check for important uncovered paths,
     cross-boundary regressions, or false confidence.
   - If an applicable layer cannot be updated safely in this slice, report that
     as an uncovered gap instead of implying coverage is complete.
   - If unrelated failures already exist, separate that baseline from problems
     introduced by the current work.

5. Sync the suite with reality.
   - Start from the smallest credible layer that matches repo reality and the
     user task.
   - On weak repos, bootstrap the minimum durable automated coverage needed to
     anchor current behavior and future verification before suggesting broader
     expansion.
   - Add or update tests at every applicable existing layer.
   - Match changed behavior to the layers the repo already expects; do not stop
     at unit tests when integration, e2e, browser, or contract coverage is
     clearly required.
   - Place tests in the owning package, app, service, or shared suite that the
     repo already uses; do not assume one stack or one default location.
   - Reuse existing helpers, fixtures, factories, and patterns.
   - Do not invent broad new testing infrastructure when a proportional update
     or minimal bootstrap will do.

6. Run the mechanical checks required by the repo.
   - Use the exact commands from `AGENTS.md` or the relevant `specs/*` when
     they exist.
   - Otherwise run the smallest meaningful commands for the owning suite,
     package, app, or service you changed.
   - Prefer targeted test commands during iteration, then the required broader
     checks for final confirmation.
   - If a needed layer has no runnable command or harness yet, say so
     explicitly.

## Output

Return a short summary with:

- which test topology and layers were applicable
- which tests were added or updated
- which commands were run and whether they passed
- any remaining risk, blocked check, or uncovered area

## Rules

- Start by discovering the repo's actual test topology, not by assuming one
  stack, one suite location, or one layer.
- The internal shape of this skill is: audit -> consult -> verify -> apply.
- Match the repo's existing test style before adding new tests.
- Ignore vendor, generated, cache, and copied-artifact noise by default unless
  the task explicitly targets it.
- Treat missing required test layers as a real gap.
- Prefer behavior-oriented tests over implementation-detail tests.
- Prefer proportional fixes. Unrelated legacy test debt should be surfaced, but
  should only be absorbed into the current work when it blocks safe
  verification.
- On weak repos, prefer the smallest credible automated layer over a
  speculative testing overhaul.
- Be explicit about coverage gaps, blocked layers, and false-confidence risks
  when this slice cannot close them safely.
- User-facing role: bootstrap, sync, or close concrete coverage gaps. Treat
  task-scoped test follow-through as part of this same skill.
- Do not turn one repo's concrete layout into a portable default. The guidance
  should survive monorepos, flat trees, mixed stacks, and repos without a
  single shared test root.
- If the testing policy in `AGENTS.md` or `specs/` is stale, recommend running
  the `specs` skill after the test work is complete.
