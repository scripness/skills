# Phase 06: Tooling And Final Docs

## Goal

Add the thin maintenance tooling and final doc polish needed to operate the
six-skill system cleanly once the skills and eval harness exist.

## Scope

- Add the repo-level validation and eval-refresh operator surface.
- Add any thin optional helper scripts that merely save keystrokes without
  becoming workflow truth.
- Finish the remaining README and maintenance documentation cleanup.

## Non-Goals

- Re-architecting the skill system again.
- Building heavy orchestration that becomes required for correctness.
- Provider-specific lock-in.

## Owned TODO Sections

- `8. Add Repo-Level Maintenance Tooling`
- `9. Add Core Repo Docs`
- Any remaining cross-cutting cleanup from `6. Ground The Skills In Official
  Sources`

## Deliverables

- Repo-root `Makefile` exposing the Phase 06 maintenance command surface while
  delegating unique harness logic to `evals/scripts/harness.py`
- Optional thin helper scripts under `execute/scripts/` only if they earn their
  place after the repo-level operator surface exists
- Repo-root `MAINTENANCE.md` plus final `README.md`, `AGENTS.md`, and
  `evals/README.md` polish

## Repo Context

- Task source: `TODO.md` sections `8. Add Repo-Level Maintenance Tooling` and
  `9. Add Core Repo Docs`, plus the 2026-04-17 verification finding that this
  plan needed explicit owning paths, blockers, and milestone acceptance
  criteria before Phase 06 execution could start safely
- Existing operator surface: Phase 05 already ships
  `python3 evals/scripts/harness.py validate` and
  `python3 evals/scripts/harness.py init-run --run-id <run-id> --selection <selection>`
  as the first thin local runner helpers; Phase 06 must add repo-level
  maintenance entrypoints and any broader validation without re-implementing
  unique harness logic in wrappers
- Owning code paths: repo-root `Makefile` for the maintenance entrypoint;
  `evals/scripts/harness.py` for shared eval validation and run scaffolding;
  `execute/scripts/` for any justified plan-driven convenience helper;
  generated run artifacts remain outside tracked source under `.tmp/evals/`
- Owning spec paths: `AGENTS.md` for the authoritative workflow contract and
  command table, `README.md` for the shipped usage surface, `evals/README.md`
  for eval artifact and review procedure details, and repo-root
  `MAINTENANCE.md` for operator guidance on updating skills, running evals, and
  upstreaming improvements from downstream repos; update `TODO.md` only if
  shipped behavior would otherwise make the roadmap wording false
- Owning test paths: there is still no formal automated suite in this repo, so
  the minimum acceptable follow-through is smoke execution of each new
  repo-level command or helper entrypoint plus the existing eval-harness
  validation commands that prove the new surface stays aligned with tracked
  truth
- Related docs or references:
  `plans/2026-04-14-phase-05-evaluation-harness.md`, `PROMPT_verify.md`,
  `README.md`, `AGENTS.md`, and `TODO.md` sections `8` and `9`

## Dependencies

- Delivered six-skill system
- Delivered initial eval harness, including the current
  `evals/scripts/harness.py` validate-plus-init-run surface
- Existing `README.md`, `AGENTS.md`, `evals/README.md`, and `TODO.md`

## Sync Expectations

- `specs`: required as part of this phase rather than optional after the fact.
  Milestone 1 changes durable repo truth about the maintenance command surface,
  validation coverage, and eval refresh workflow, so keep `AGENTS.md`,
  `README.md`, and `evals/README.md` aligned before calling Milestone 1
  complete. Milestone 3 adds operator guidance, so keep those docs plus
  `MAINTENANCE.md` aligned before calling the phase complete.
- `tests`: required for any new executable surface in this phase. The minimum
  acceptable follow-through is smoke execution of each new `make` target or
  helper entrypoint, `--help` coverage for any script interface, and
  re-running `python3 evals/scripts/harness.py validate`; if stronger
  automation is still deferred, record that blocker explicitly in this plan
  instead of implying coverage exists.

## Milestones

1. Add the repo-level operator surface with an explicit Phase 05 delta: ship a
   repo-root `Makefile` as the thin maintenance entrypoint, wire validation and
   eval-refresh commands through the existing `evals/scripts/harness.py`
   helpers, extend validation to cover skill structure, frontmatter, and local
   asset integrity as needed, and document every shipped command in the owning
   docs.
2. Add only justified helper scripts with an explicit agent-safe contract: if a
   plan-driven convenience gap remains after Milestone 1, add at most thin
   helpers under `execute/scripts/` that take an explicit provider command and
   explicit plan path, never guess state, expose `--help`, separate
   machine-readable stdout from stderr diagnostics, document meaningful exit
   codes, and support `--dry-run` or explicit confirmation for any stateful
   action; otherwise close the milestone by recording that no helper earned
   inclusion.
3. Finish final docs and maintenance guidance so shipped truth matches the
   implemented system: add repo-root `MAINTENANCE.md`, sync `README.md`,
   `AGENTS.md`, and `evals/README.md`, and close any remaining wording drift
   about the durable-state model, maintenance loop, and upstreaming guidance.

## Verification

- Confirm the repo-level operator commands stay thin and do not hide unique
  workflow logic that should live in tracked Python or markdown instead.
- Confirm the chosen validation surface covers skill structure, frontmatter, and
  local asset integrity in addition to the existing eval-contract checks.
- Confirm any helper scripts remain convenience wrappers only, are
  non-interactive, expose `--help`, separate machine-readable stdout from
  stderr diagnostics, report meaningful exit codes, and implement `--dry-run`
  or explicit confirmation when stateful behavior exists.
- Confirm `AGENTS.md`, `README.md`, and `evals/README.md` describe the same
  shipped command surface for Milestone 1; include `MAINTENANCE.md` in that
  sync set once Milestone 3 lands.
- Smoke-run each shipped command surface and record the exact commands and
  results in this plan before closing milestones.
- [2026-04-17] Ran `python3 evals/scripts/harness.py --help` and it passed,
  showing the direct `validate` and `init-run` subcommands behind the Makefile
  wrappers.
- [2026-04-17] Ran `python3 evals/scripts/harness.py validate` and it passed,
  reporting 6 skills, 6 skill frontmatter files, 6 agent shims, 4 required
  local assets, 12 trigger packs, 18 workflow cases, and 1 fixture manifest.
- [2026-04-17] Ran
  `python3 evals/scripts/harness.py init-run --run-id phase06-m1-direct-smoke --selection must-run --skill execute`
  and it passed, creating `.tmp/evals/phase06-m1-direct-smoke/` with 2 cases
  and the `cryptoli` fixture.
- [2026-04-17] Ran `make help` and it passed, printing the shipped repo-level
  targets and the direct script help entrypoint.
- [2026-04-17] Ran `make validate` and it passed, delegating to the same
  repo-level validation surface in `evals/scripts/harness.py` with the same
  counts as the direct validation command.
- [2026-04-17] Ran
  `make eval-init-run RUN_ID=phase06-m1-make-smoke SELECTION=validation SKILL="execute verify"`
  and it passed, creating `.tmp/evals/phase06-m1-make-smoke/` with 6 cases and
  the `cryptoli` fixture through the Makefile wrapper.
- [2026-04-17] Ran `git diff --check` and it passed with no whitespace or
  patch-format issues after the Milestone 1 edits.
- [2026-04-17] Ran `python3 evals/scripts/harness.py validate` again after the
  gap-repair slice and it passed, confirming the validator now reads the
  required local assets and checks their structural markers instead of
  existence alone.
- [2026-04-17] Ran `make validate` again after the gap-repair slice and it
  passed through the same repo-level wrapper.
- [2026-04-17] Ran
  `python3 evals/scripts/harness.py init-run --run-id phase06-m1-gap-repair-direct --selection must-run --skill execute`
  and it passed, creating `.tmp/evals/phase06-m1-gap-repair-direct/` with 2
  cases and the `cryptoli` fixture after the validator changes.
- [2026-04-17] Ran
  `make eval-init-run RUN_ID=phase06-m1-gap-repair-make SELECTION=validation SKILL="execute verify"`
  and it passed, creating `.tmp/evals/phase06-m1-gap-repair-make/` with 6
  cases and the `cryptoli` fixture after the validator changes.
- [2026-04-17] Ran `python3 execute/scripts/plan_loop.py --help` and it
  passed, showing the helper contract, required runner shape, and documented
  helper exit codes.
- [2026-04-17] Ran `python3 -m py_compile execute/scripts/plan_loop.py` and it
  passed.
- [2026-04-17] Ran a temp-fixture smoke command that created a temporary plan
  from `plan/assets/plan-template.md`, created a temporary fake external
  runner that accepts `execute <plan>` and `verify <plan>`, then invoked both
  `python3 execute/scripts/plan_loop.py --dry-run ...` and
  `python3 execute/scripts/plan_loop.py --yes --max-iterations 3 ...`; it
  passed with `dry_run_rc = 0`, `real_run_rc = 0`, `last_verdict = "pass"`,
  and all three progress items marked complete in the temporary plan.
- [2026-04-17] Ran `make validate` and it passed after the Milestone 2 helper
  edits, confirming the existing repo-level validation surface still matches
  tracked truth.
- [2026-04-17] Ran `git diff --check` and it passed with no whitespace or
  patch-format issues after the Milestone 2 helper and doc edits.
- [2026-04-17] Re-ran `python3 execute/scripts/plan_loop.py --help` after the
  malformed-plan repair and it passed, now documenting helper exit code `1`
  for invalid plan state as well as blocked or unacceptable runs.
- [2026-04-17] Re-ran a temp-fixture happy-path smoke command that created a
  temporary plan from `plan/assets/plan-template.md`, created a temporary fake
  external runner that marks one `## Progress` item complete per `execute`,
  then invoked `python3 execute/scripts/plan_loop.py --yes --max-iterations 3 ...`;
  it passed with `rc = 0`, `verification_verdict = "pass"` on each loop, and
  all three progress items marked complete in the temporary plan after the
  malformed-plan repair.
- [2026-04-17] Ran a temp-fixture malformed-plan smoke command that created a
  temporary plan from `plan/assets/plan-template.md`, created a temporary fake
  external runner that deletes the `## Blockers` section during `execute`, then
  invoked `python3 execute/scripts/plan_loop.py --yes ...`; it passed by
  failing closed with structured stop event `invalid_plan_after_execute` and
  `rc = 1` instead of surfacing a Python traceback.
- [2026-04-17] Ran `make validate` after the malformed-plan repair and it
  passed, confirming the existing repo-level validation surface still matches
  tracked truth.
- [2026-04-17] Ran
  `make eval-init-run RUN_ID=phase06-m2-execute-eval-refresh SELECTION=validation SKILL="execute"`
  and it passed, creating `.tmp/evals/phase06-m2-execute-eval-refresh/` with
  3 selected execute validation cases and the `cryptoli` fixture, refreshing
  the relevant execute eval workspace for this skill slice.
- [2026-04-17] Re-ran `make help` during the Milestone 3 doc-sync slice and it
  passed, still printing the shipped repo-level maintenance targets described
  in `README.md`, `AGENTS.md`, and the new `MAINTENANCE.md`.
- [2026-04-17] Re-ran `make validate` during the Milestone 3 doc-sync slice
  and it passed, still reporting 6 skills, 6 skill frontmatter files, 6 agent
  shims, 4 required local assets, 12 trigger packs, 18 workflow cases, and 1
  fixture manifest after the final doc edits.
- [2026-04-17] Re-ran `python3 evals/scripts/harness.py --help` during the
  Milestone 3 doc-sync slice and it passed, still showing the direct
  `validate` and `init-run` harness surface behind the Makefile wrappers.
- [2026-04-17] Re-ran `python3 execute/scripts/plan_loop.py --help` during the
  Milestone 3 doc-sync slice and it passed, still documenting the optional
  explicit-plan helper contract, external runner requirement, and exit codes.
- [2026-04-17] Re-ran `git diff --check` during the Milestone 3 doc-sync slice
  and it passed with no whitespace or patch-format issues after adding
  `MAINTENANCE.md` and the final doc links.
- [2026-04-17] Ran `git diff --check` again after the required final plan
  update and it still passed, confirming the final Milestone 3 tree is clean.
- [2026-04-17] Re-ran `make help` after the self-describing-surface repair and
  it passed, now listing the optional `python3 execute/scripts/plan_loop.py`
  `--help` and `--dry-run --plan ... --provider-command ...` commands alongside
  the Makefile-wrapped harness commands so the advertised maintenance surface
  no longer depends on docs-only command names.
- [2026-04-17] Re-ran `make validate` after the self-describing-surface repair
  and it passed, still reporting 6 skills, 6 skill frontmatter files, 6 agent
  shims, 4 required local assets, 12 trigger packs, 18 workflow cases, and 1
  fixture manifest.
- [2026-04-17] Re-ran `python3 evals/scripts/harness.py --help` after the
  self-describing-surface repair and it passed, still showing the direct
  `validate` and `init-run` harness interface behind the Makefile wrappers.
- [2026-04-17] Re-ran `python3 execute/scripts/plan_loop.py --help` after the
  self-describing-surface repair and it passed, still documenting the optional
  explicit-plan helper contract and exit codes.
- [2026-04-17] Re-ran `git diff --check` after the self-describing-surface
  repair and it passed with no whitespace or patch-format issues.

## Risks

- Adding wrappers that quietly become required for normal workflow use.
- Final docs drifting into aspirational claims instead of shipped truth.
- Polishing tooling before the eval harness and skill contracts are stable
  enough.

## Open Questions

- None currently.

## Blockers

- None currently.

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3

## Decision Log

- [2026-04-14] Tooling should remain thin and optional; the workflow must stay
  skill-native first.
- [2026-04-17] Use a repo-root `Makefile` as the first Phase 06 maintenance
  surface so operator commands stay thin, reviewable, and additive above the
  existing `evals/scripts/harness.py` helpers.
- [2026-04-17] Ship a discoverable `make help` target with the Makefile so the
  repo-level maintenance surface is self-describing without adding hidden logic
  or extra docs-only command names.
- [2026-04-17] If a plan-driven convenience wrapper is justified, it belongs
  under `execute/scripts/` because it composes `execute` and `verify`; if no
  real gap remains after Milestone 1, close Milestone 2 explicitly without
  adding a helper just to satisfy the plan.
- [2026-04-17] Use repo-root `MAINTENANCE.md` as the durable home for skill
  update guidance, eval-running guidance, and upstreaming notes from downstream
  repo work.
- [2026-04-17] Keep `MAINTENANCE.md` as a Milestone 3 deliverable rather than
  back-solving the missing file into the Milestone 1 slice; the Milestone 1
  sync gate is the shipped maintenance surface in `AGENTS.md`, `README.md`,
  and `evals/README.md`.
- [2026-04-17] Ship Milestone 2 as one optional helper at
  `execute/scripts/plan_loop.py`; keep it dumb by requiring one explicit plan
  path, one explicit external runner command, file-backed continuation checks,
  and verify verdict exit codes instead of parsing model prose.
- [2026-04-17] Treat malformed plan state after `execute` or `verify` as a
  structured helper stop under exit code `1` rather than an uncaught
  traceback, and include the pre-failure plan state plus runner log paths in
  the emitted event for debugging.
- [2026-04-17] For the current Milestone 5 harness surface, treat "refresh the
  relevant eval reports" for a skill edit as scaffolding a fresh
  `.tmp/evals/<run-id>/` workspace and review template for that skill, because
  the repo still does not ship automated model execution or grading.
- [2026-04-17] Keep `MAINTENANCE.md` as an operator guide that ties together
  skill updates, eval refresh, and downstream-upstream sync without turning it
  into a second workflow contract; `AGENTS.md` remains the authoritative
  refresh and boundary document for the repo.

## Discoveries

- [2026-04-14] The right time to add wrappers is after the skills and eval
  contracts exist, not before.
- [2026-04-17] The current repo already ships the Phase 05 harness entrypoints
  in `evals/scripts/harness.py`, so Phase 06 must layer operator polish and
  broader validation on top of that surface rather than replace it.
- [2026-04-17] Before this repair, the Phase 06 plan lacked `Repo Context`,
  `Blockers`, and milestone-level acceptance criteria, which made fresh-session
  execution riskier than the shipped `plan` contract allows.
- [2026-04-17] The shipped skill surface has one consistent structure today:
  each skill owns `SKILL.md`, `agents/openai.yaml`, and `evals/evals.json`,
  while only `plan/` and `specs/` currently ship required local assets worth
  validating in the Phase 06 maintenance pass.
- [2026-04-17] Re-reading the updated repo-truth docs after Milestone 1 showed
  that `AGENTS.md`, `README.md`, `evals/README.md`, and the new `Makefile`
  now describe the same thin maintenance surface instead of splitting command
  truth across mismatched entrypoints.
- [2026-04-17] The current tracked eval surface is larger than the rough Phase
  06 placeholder implied: repo validation reports 18 workflow cases today, so
  future plan notes should derive counts from the validator output instead of
  carrying stale hardcoded numbers forward.
- [2026-04-17] “Local asset integrity” needed a real implementation rather than
  presence-only file checks; the required asset templates already expose stable
  section markers that can be validated without adding a heavy schema layer.
- [2026-04-17] The shipped `plan` template already provides enough file-backed
  loop state for a thin helper through `## Progress` and `## Blockers`, but
  helper continuation still needs an explicit external runner exit-code
  contract because scraping free-form verify prose would hide workflow logic in
  the wrapper.
- [2026-04-17] The `execute` validation selection currently scaffolds 3 cases
  plus the pinned `cryptoli` fixture, which is enough to refresh the relevant
  eval workspace for this helper-and-skill slice without implying that grading
  artifacts already exist.
- [2026-04-17] By the start of Milestone 3, the remaining Phase 06 gap was no
  longer executable behavior; it was the missing repo-root operator guide that
  linked the already-shipped maintenance commands, eval refresh loop, and
  downstream-upstream sync guidance in one durable place.
- [2026-04-17] For this repo, a "self-describing" `make help` surface needs to
  include optional direct helper entrypoints that the docs treat as shipped,
  not just the Makefile targets themselves.

## Outcomes / Retrospective

- Phase 06 is complete. The repo now ships a thin repo-level maintenance
  surface (`Makefile`, `evals/scripts/harness.py`, and the optional
  `execute/scripts/plan_loop.py`) plus a repo-root `MAINTENANCE.md` that keeps
  `README.md`, `AGENTS.md`, and `evals/README.md` aligned around the same
  provider-agnostic maintenance loop.
