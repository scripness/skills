# Phase 01: Plan Skill And Contract

## Goal

Establish the provider-agnostic contract for this repo, lock the six-skill
workflow shape, and add the missing `plan` skill so later phases can execute
against explicit living plan files instead of only against `plans/2026-04-14-phase-00-design-doc.md`, while
keeping `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md` aligned with the shipped
contract.

## Scope

- Define and ship the first version of the `plan` skill.
- Make the repo contract and six-skill workflow explicit in the shipped docs.
- Keep the implementation grounded in the current roadmap and source guidance.
- Decide and document the target-repo refresh workflow for distributing these
  skills into other repos.

## Non-Goals

- Adding the `execute` skill.
- Refreshing the existing four shipped skills beyond minimal contract alignment.
- Building the eval harness or helper scripts.

## Owned TODO Sections

- `1. Define Repo Contract`
- `2. Define The Six-Skill Workflow`
- `3. Add The Plan Skill`
- Minimal doc sync needed to keep `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md`
  truthful after shipping `plan`

## Deliverables

- `src/plan/SKILL.md`
- `src/plan/agents/openai.yaml`
- `src/plan/assets/plan-template.md`
- Minimal updates to `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md` needed to keep the
  shipped contract and refresh workflow truth aligned with the delivered
  `plan` skill

## Dependencies

- Existing `AGENTS.md`
- Existing `README.md`
- Existing `plans/2026-04-14-phase-00-design-doc.md`
- Existing shipped skills for boundary alignment:
  `consult`, `specs`, `tests`, and `verify`

## Sync Expectations

- `specs`: required in this phase because shipping `plan` changes durable repo
  truth about the canonical workflow, skill boundaries, and task-state model;
  in this repo that means updating `AGENTS.md` first as the authoritative
  contract, then keeping `README.md` and `plans/2026-04-14-phase-00-design-doc.md` aligned with the delivered
  `plan` skill and the chosen refresh workflow.
- `tests`: not expected in this phase unless the implementation introduces
  executable helpers, validators, or other behavior that should be covered now.

## Milestones

1. Finalize the contract that `plan` owns:
   trigger conditions, boundaries versus `consult` and `execute`, default file
   naming, and resumption requirements.
2. Decide and document the target-repo refresh workflow:
   manual copy, install script, subtree, plugin, or another sync mechanism.
3. Tighten the trigger description and invocation guidance for the future
   `plan` skill so activation is explicit and reliable.
4. Add the `src/plan/` skill scaffold and write `src/plan/SKILL.md` with a narrow,
   provider-agnostic scope.
5. Add `src/plan/assets/plan-template.md` with the full self-contained living-plan
   structure required by the roadmap.
6. Sync repo docs minimally so `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md` stay
   truthful, while keeping the bootstrap asymmetry explicit until `execute`
   exists.

## Verification

- Read the shipped `plan` skill against `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md`
  and confirm the boundaries are consistent.
- Confirm the plan template includes goal, scope, non-goals, milestones,
  verification, risks, open questions, progress, decision log, discoveries, and
  outcomes/retrospective.
- Confirm the skill requires explicit sync expectations for `specs` and `tests`
  inside each task plan.
- Confirm the target-repo refresh workflow decision is captured explicitly in
  shipped docs, with the owning doc location named rather than left implied.
- Confirm the docs say `plan` is shipped, `execute` is not, and that the
  pre-`execute` bootstrap loop is captured accurately for this phase.

## Risks

- Over-designing the refresh workflow before there is real distribution usage.
- Writing a `plan` skill that overlaps too much with `consult` or anticipates
  `execute` details too aggressively.
- Updating docs in a way that implies the full six-skill system is already
  shipped.

## Open Questions

- Should the first shipped `plan` skill include examples beyond the core plan
  template, or stay minimal?

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3
- [x] Milestone 4
- [x] Milestone 5
- [x] Milestone 6

Milestone 6 note:

- Minimal `AGENTS.md` and `README.md` truth sync was completed as required
  follow-through for shipping Milestone 4.
- Milestone 5 did not require new doc edits because the shipped template
  matches the existing `AGENTS.md`, `README.md`, `plans/2026-04-14-phase-00-design-doc.md`, and `src/plan/SKILL.md`
  contract rather than changing it.
- Milestone 6 closed after the final phase-wide doc pass confirmed the shipped
  docs remained truthful and the reusable template no longer contained the raw
  angle-bracket placeholders called out during verification.

## Decision Log

- [2026-04-14] Use one phase plan per coherent workstream rather than one giant
  master implementation plan.
- [2026-04-14] `plan` promotion is based on durable task-state need across
  sessions, milestones, review loops, or restarts, not on abstract task size.
- [2026-04-14] `plan` owns task-local files under `plans/`; `consult` owns
  clarification and recommendation, and `execute` owns implementation from an
  explicit plan path.
- [2026-04-14] The default plan filename contract is
  `plans/YYYY-MM-DD-short-task-slug.md`.
- [2026-04-14] Every `plan` artifact must be resumable from repo truth plus the
  plan file alone.
- [2026-04-14] Use manual copy into `.agents/skills/` as the initial
  target-repo refresh workflow, and keep install helpers, subtree wiring, and
  provider-specific plugins optional future accelerators only.
- [2026-04-14] Milestone 3 is a doc-contract slice only: tighten positive
  triggers, anti-triggers, and explicit plan-path handoff guidance in shipped
  docs before adding the actual `src/plan/` scaffold in Milestone 4.
- [2026-04-14] Ship Milestone 4 with only `src/plan/SKILL.md`,
  `src/plan/agents/openai.yaml`, and the minimum shipped-truth doc edits needed to
  avoid leaving `AGENTS.md` and `README.md` stale; defer the reusable plan
  template asset to Milestone 5.
- [2026-04-14] Ship the reusable `plan` template as plain Markdown that matches
  the existing living-plan house style, rather than introducing frontmatter or
  provider-specific metadata requirements.

## Discoveries

- [2026-04-14] `plans/2026-04-14-phase-00-design-doc.md` is the roadmap, not the execution artifact; later
  phases should execute from explicit `plans/*.md` files.
- [2026-04-14] The existing `consult` skill already forbids owning long-lived
  task state, so the `consult` -> `plan` boundary could be locked with
  proportional doc edits rather than a broader skill rewrite.
- [2026-04-14] `README.md` already named `.agents/skills/` as the canonical
  target-repo path, but the repo had not yet named an authoritative refresh
  method or owning doc for that contract.
- [2026-04-14] The repo already had the positive `plan` trigger, but it lacked
  equally explicit anti-triggers and an explicit "hand off the exact
  `plans/*.md` path" rule, which left invocation guidance looser than the
  planned execution flow needed.
- [2026-04-14] The existing skill house style is lightweight but consistent:
  frontmatter plus `Inputs`, `Process`, `Output`, and rule/quality sections,
  so the new `plan` skill could be added proportionally without inventing a
  different scaffold shape.
- [2026-04-14] Shipping `src/plan/` immediately made the old "plan is still
  planned" wording in `AGENTS.md` and `README.md` false, while `plans/2026-04-14-phase-00-design-doc.md`
  remained valid because it is the roadmap rather than the shipped-state index.
- [2026-04-14] The existing phase plans already provided a stable reusable
  shape for the template: goal, scope, non-goals, sync expectations,
  milestones, verification, blockers, progress, decision log, discoveries, and
  outcomes/retrospective, with only repo-specific sections needing
  generalization.
- [2026-04-14] The reusable template can make `specs` and `tests`
  follow-through more explicit without changing shipped repo truth, because the
  current docs and `plan` skill already require those obligations.
- [2026-04-14] Raw angle-bracket placeholders render poorly in Markdown
  previews, so the reusable template should use plain bracketed placeholder
  text instead of HTML-like markers.
- [2026-04-14] The final Phase 01 doc pass found that the template and plan log
  had drifted slightly after Milestone 5: the template still used raw angle-
  bracket placeholders and the Milestone 6 note still described pre-template
  state.

## Verification

- [2026-04-14] Verified `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md` all capture the
  same Milestone 1 contract: `plan` triggers on durable-state need, starts
  after `consult` has clarified the next move, owns only task-local plan files,
  hands implementation off to `execute` via an explicit plan path, uses
  `plans/YYYY-MM-DD-short-task-slug.md`, and must support fresh-session
  resumption from repo truth plus the plan file.
- [2026-04-14] Verified Milestone 2 doc sync: `AGENTS.md` now names itself as
  the authoritative refresh-workflow contract, and `AGENTS.md`, `README.md`,
  and `plans/2026-04-14-phase-00-design-doc.md` all say the initial default is manual copy into
  `.agents/skills/`, with install helpers, subtree wiring, and
  provider-specific plugins remaining optional.
- [2026-04-14] Re-ran Milestone 2 verification after adding the missing
  `plans/2026-04-14-phase-00-design-doc.md` pointer: `README.md` and `plans/2026-04-14-phase-00-design-doc.md` both now explicitly name
  `AGENTS.md` as the owning refresh-workflow contract, so the owner location is
  captured in shipped docs rather than implied.
- [2026-04-14] Deferred milestone-specific verification that depends on the
  shipped `plan` skill, template, and refresh workflow to later milestones in
  this phase.
- [2026-04-14] Verified Milestone 3 trigger tightening by re-reading
  `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md`: all now say `plan` is for durable
  task-state need, not abstract size; they explicitly name anti-triggers for
  short clarification or locally clear bounded work; and they require an
  explicit `plans/*.md` path for handoff to `execute` and `verify`.
- [2026-04-14] Ran `git diff --check` after the doc edits; it passed with no
  whitespace or patch-format issues.
- [2026-04-14] Re-read `src/plan/SKILL.md`, `AGENTS.md`, and `README.md` after the
  Milestone 4 edits and confirmed they align on `plan` owning task-local plan
  files only, durable-state-based promotion, the `consult` -> `plan` ->
  `execute`/`verify` boundary, the default
  `plans/YYYY-MM-DD-short-task-slug.md` path, and explicit `specs`/`tests`
  sync expectations inside each plan.
- [2026-04-14] Ran `find src/plan -maxdepth 3 -type f | sort` and confirmed the
  Milestone 4 scaffold is intentionally narrow: `src/plan/SKILL.md` and
  `src/plan/agents/openai.yaml` only. `src/plan/assets/plan-template.md` remains
  deferred to Milestone 5.
- [2026-04-14] Re-ran `git diff --check` after adding the `src/plan/` scaffold and
  doc truth-sync edits; it passed with no whitespace or patch-format issues.
- [2026-04-14] Re-read `AGENTS.md`, `README.md`, and `src/plan/SKILL.md` after the
  follow-up doc fix and confirmed the shipped contract now stays aligned on two
  previously drifting points: plans must record explicit `specs`/`tests`
  follow-through, and plans must preserve material blockers for fresh-session
  resumption.
- [2026-04-14] Re-read `src/plan/assets/plan-template.md`, `src/plan/SKILL.md`,
  `AGENTS.md`, `README.md`, and `plans/2026-04-14-phase-00-design-doc.md` after adding the template and
  confirmed the reusable plan skeleton includes goal, scope, non-goals,
  deliverables, repo context, dependencies, explicit `specs`/`tests` sync
  expectations, milestones, verification, risks, open questions, blockers,
  progress, decision log, discoveries, and outcomes/retrospective.
- [2026-04-14] Confirmed the template explicitly tells future execution work to
  keep repo truth and test truth aligned, including naming when `specs` or
  `tests` sync is required and when either is not currently required.
- [2026-04-14] Ran `git diff --check` after adding `src/plan/assets/plan-template.md`
  and updating this phase plan; it passed with no whitespace or patch-format
  issues.
- [2026-04-14] Re-ran `git diff --check` after replacing raw angle-bracket
  placeholders in `src/plan/assets/plan-template.md` with plain bracketed text; it
  passed with no whitespace or patch-format issues.
- [2026-04-14] Re-read `AGENTS.md`, `README.md`, `plans/2026-04-14-phase-00-design-doc.md`, `src/plan/SKILL.md`,
  and `src/plan/assets/plan-template.md` during the final Phase 01 verification
  pass and confirmed the shipped contract still aligns on `plan` being shipped,
  `execute` remaining unshipped, manual copy into `.agents/skills/` as the
  default refresh workflow, explicit `specs`/`tests` sync expectations inside
  each plan, and bootstrap prompt usage until `execute` lands.
- [2026-04-14] Ran `rg -n '<[^>]+>' src/plan/assets/plan-template.md` during the
  final Phase 01 verification pass; it returned no matches after the placeholder
  cleanup.
- [2026-04-14] Re-ran `git diff --check` after closing the Phase 01 plan drift;
  it passed with no whitespace or patch-format issues.

## Outcomes / Retrospective

- Milestone 1 completed with minimal doc sync only; later milestones still own
  refresh-workflow decisions, trigger phrasing inside the shipped skill, and
  the actual `src/plan/` scaffold.
- Milestone 2 completed with proportional doc-only changes; the refresh
  workflow is now explicit without introducing required automation before there
  is real distribution pressure.
- Milestone 3 completed with proportional doc-only changes; invocation guidance
  is now explicit enough to support a narrow `plan` skill without prematurely
  shipping the scaffold itself.
- Milestone 4 completed with a narrow shipped `plan` scaffold that matches the
  existing skill house style, keeps the contract provider-agnostic, and avoids
  spilling into Milestone 5's reusable template work.
- Milestone 5 completed with a reusable `src/plan/assets/plan-template.md` that
  packages the repo's living-plan contract into a portable template without
  expanding scope into final phase-wide doc cleanup.
- Milestone 6 completed with a final truth pass that closed the remaining plan
  drift, confirmed the shipped docs still matched the delivered `plan` skill
  and template, and kept the bootstrap asymmetry explicit until `execute`
  exists.
