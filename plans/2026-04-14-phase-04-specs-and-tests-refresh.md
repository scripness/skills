# Phase 04: Specs And Tests Refresh

## Goal

Refresh `specs` and `tests` so they prepare real-world repos for reliable
agentic work across different topologies, including monorepos and mixed stacks,
without hardcoded layout assumptions.

## Scope

- Strengthen `specs` around codebase organization quality, topology discovery,
  and durable repo-truth ownership.
- Strengthen `tests` around test-topology discovery, honest coverage
  expectations, and sync/bootstrap behavior.
- Use `cryptoli` as a real-world reference shape for the design, without turning
  this phase into the full eval harness.
- Make the trigger-description refinement for `specs` and `tests` explicit.

## Non-Goals

- Building the formal eval harness or local runners.
- Building the helper loop scripts.
- Reworking `consult` or `verify` except where minor alignment is required.

## Owned TODO Sections

- The `specs` and `tests` parts of `5. Improve The Six Core Skills`
- The relevant cross-cutting source-grounding work from `6. Ground The Skills In
  Official Sources`

## Deliverables

- Updated `specs/SKILL.md`
- Updated `specs/agents/openai.yaml` if the refreshed `specs` trigger or
  default prompt changes shipped behavior
- Updated `tests/SKILL.md`
- Updated `tests/agents/openai.yaml` if the refreshed `tests` trigger or
  default prompt changes shipped behavior
- Updated `specs/assets/*` if the repo-truth bootstrap templates need to match
  the refreshed contract
- Durable in-plan summary of the official-source guidance actually used for the
  Phase 04 refresh, so the owned source-grounding slice stays auditable from
  repo truth plus this plan alone
- Minimal doc sync if the shipped behavior changes current truth

## Dependencies

- Delivered contracts for `plan` and `execute`
- Existing `README.md`, `TODO.md`, and `specs/assets/*`
- Real-world monorepo reference shape from `scripness/cryptoli`, but only as
  captured in the repo context below; do not depend on unstated external notes
  or a floating external HEAD

## Repo Context

- Task source: the `specs` and `tests` entries in `TODO.md` section
  `5. Improve The Six Core Skills`, plus the relevant source-grounding work in
  section `6. Ground The Skills In Official Sources`
- Owning code paths: `specs/` and `tests/`, including both `SKILL.md` and
  `agents/openai.yaml` because the agent wrapper prompts are part of the
  shipped surface
- Owning spec paths: `AGENTS.md` as the authoritative workflow contract,
  `README.md` as shipped usage guidance, and `specs/assets/*` because the
  bootstrap assets must stay aligned when the `specs` contract changes
- Owning test paths: there is still no formal automated suite in this repo, so
  Phase 04 verification should use bounded mechanical checks such as contract
  re-reads, targeted `rg` checks, file-presence checks, and `git diff --check`;
  if this phase introduces executable validators, examples, or helpers, update
  this plan and require explicit `tests` follow-through before claiming
  completion
- Real-repo reference guardrails: until Phase 05 pins `cryptoli`, treat it only
  as a reference shape for monorepo-aware behavior already captured in roadmap
  truth: a real pnpm workspace used to stress-test repo-topology discovery,
  codebase-organization assessment, multi-app spec syncing, and multi-layer
  test discovery. Do not depend on unstated `cryptoli` path details during
  Phase 04 execution, and do not turn one repo's concrete layout into a
  required portable default
- Related docs or references: `PROMPT_verify.md`,
  `plans/2026-04-14-phase-03-consult-and-verify-refresh.md`, and the official
  sources listed in `TODO.md` section `6. Ground The Skills In Official
  Sources`

## Sync Expectations

- `specs`: this phase directly changes repo-truth guidance and bootstrap assets,
  so minimal truth sync is expected as part of the deliverable.
- `tests`: this phase directly changes test-truth guidance; if templates,
  examples, or executable validation surfaces are introduced, sync them before
  considering the phase complete.

## Relevant Official-Source Grounding

- From `https://developers.openai.com/codex/learn/best-practices`, keep the
  Phase 04 refresh grounded in actual repo inspection, proportional updates,
  and verification-backed claims rather than generic topology boilerplate.
- From `https://developers.openai.com/codex/skills`, keep `specs` and `tests`
  narrow, explicit about trigger boundaries, and clear about their user-facing
  role in the six-skill workflow.
- From `https://developers.openai.com/cookbook/articles/codex_exec_plans`,
  keep the Phase 04 work resumable from files, explicit about bounded slices,
  and honest about what verification evidence exists in a docs-first repo.
- From `https://agentskills.io/specification`,
  `https://agentskills.io/skill-creation/best-practices`, and
  `https://agentskills.io/skill-creation/optimizing-descriptions`, keep the
  `specs` and `tests` contracts concrete about inputs, outputs, and activation
  semantics across bootstrap, sync, and gap-driven use.
- From `https://agentskills.io/skill-creation/evaluating-skills`,
  `https://agentskills.io/skill-creation/using-scripts`, and
  `https://agentskills.io/client-implementation/adding-skills-support`, borrow
  only durable portability guidance that helps these skills survive different
  repo shapes; do not introduce eval-harness or client-specific requirements in
  Phase 04.

## Milestones

1. Refresh `specs` for repo-topology discovery, agentic-readiness evaluation,
   and proportional organization guidance.
2. Tighten the trigger descriptions and invocation guidance for `specs` and
   `tests` so activation is clear across bootstrap, sync, and gap-driven use.
3. Refresh `tests` for test-topology discovery, layered coverage expectations,
   and honest gap reporting across repo shapes.
4. Update any shipped bootstrap assets that now drift from the refreshed skill
   behavior.
5. Sync docs minimally so the shipped truth matches the refreshed behavior, and
   inline the durable official-source grounding used for this phase so no
   external notes are required for auditability.

## Verification

- Confirm `specs` does not assume a single-app `src/` layout.
- Confirm `tests` does not assume one stack, one suite location, or one layer.
- Confirm both skills ignore vendor/generated noise by default.
- Confirm the refreshed guidance still keeps code as the ultimate source of
  truth and uses docs/tests as synchronized truth layers.
- Confirm the trigger descriptions make it clear when `specs` or `tests` should
  be invoked proactively versus manually.
- Confirm any `cryptoli`-derived guidance is expressed as portable repo-shape
  heuristics rather than unstated repo-specific path assumptions.
- Confirm the plan carries a durable summary of the official-source guidance
  used for the refresh instead of pointing to dangling external notes.
- Confirm `specs/agents/openai.yaml` and `tests/agents/openai.yaml` stay
  aligned with the shipped `SKILL.md` contracts when their prompts or wrapper
  descriptions are touched.
- Run bounded mechanical checks after each contract-changing slice: contract
  re-reads, targeted `rg` checks, file-presence checks, and `git diff --check`.

### 2026-04-15 Milestone 1 results

- Re-read `specs/SKILL.md` and `specs/agents/openai.yaml` after editing to
  confirm the shipped `specs` surface now explicitly covers repo-topology
  discovery, generated/vendor-noise pruning, and proportional organization
  guidance.
- `rg -n "topology|monorepo|generated|vendor|agent reliability|src/"
  specs/SKILL.md specs/agents/openai.yaml` passed and showed the intended
  contract language in the shipped skill surfaces.
- `git diff --check` passed.
- `test -f specs/SKILL.md && test -f specs/agents/openai.yaml && echo present`
  passed.
- `rg -n "Owns repo truth|evaluate codebase organization quality|improve
  boundaries|discoverability|repo truth is weak|AGENTS.md and specs"
  README.md` confirmed the current README still matches the refreshed
  high-level `specs` role closely enough that Milestone 1 did not require
  separate doc edits.

### 2026-04-15 Milestone 2 results

- Re-read `AGENTS.md`, `README.md`, `specs/SKILL.md`,
  `specs/agents/openai.yaml`, `tests/SKILL.md`, and
  `tests/agents/openai.yaml` after editing to confirm the shipped trigger and
  invocation surfaces now cover bootstrap, sync, and gap-driven use for both
  skills.
- `rg -n "trigger when repo truth|trigger when test truth|three user-facing
  situations|gap-close|coverage gaps|safe execution and verification|safe
  planning, execution, or verification" AGENTS.md README.md specs/SKILL.md
  specs/agents/openai.yaml tests/SKILL.md tests/agents/openai.yaml` passed and
  showed the intended activation language across repo-facing docs, skill
  contracts, and wrapper metadata.
- `git diff -- AGENTS.md README.md specs/SKILL.md specs/agents/openai.yaml
  tests/SKILL.md tests/agents/openai.yaml` was reviewed to confirm this slice
  stayed limited to trigger and invocation semantics rather than pulling
  Milestone 3's deeper `tests` contract refresh forward.
- `git diff --check` passed.
- `test -f specs/SKILL.md && test -f specs/agents/openai.yaml && test -f
  tests/SKILL.md && test -f tests/agents/openai.yaml && echo present` passed.

### 2026-04-16 Milestone 3 results

- Re-read `tests/SKILL.md` and `tests/agents/openai.yaml` after editing to
  confirm the shipped `tests` surface now explicitly covers topology-aware
  suite discovery, generated/vendor-noise pruning, layered coverage selection,
  weak-repo bootstrap guidance, and honest uncovered-gap reporting across repo
  shapes.
- `rg -n "topology|monorepo|single package|per-app|per-package|per-service|unit|integration|e2e|smoke|browser|contract|visual|security|performance|vendor|generated|coverage gaps|false-confidence|shared test root" tests/SKILL.md tests/agents/openai.yaml`
  passed and showed the intended contract language in the shipped `tests`
  skill surfaces.
- After follow-up verification flagged provider-facing under-description,
  `tests/agents/openai.yaml` was tightened so the shipped wrapper metadata now
  explicitly covers bootstrap, sync, and concrete coverage-gap closure rather
  than reading as sync-only.
- `git diff -- tests/SKILL.md tests/agents/openai.yaml` was reviewed to
  confirm this slice stayed limited to the `tests` contract and aligned wrapper
  metadata rather than pulling Milestone 4 asset refresh or Milestone 5 doc
  sync forward.
- `git diff --check` passed.
- `test -f tests/SKILL.md && test -f tests/agents/openai.yaml && echo present`
  passed.

### 2026-04-16 Milestone 4 results

- Re-read `specs/assets/AGENTS.md`, `specs/assets/specs/README.md`, and
  `specs/assets/specs/spec-template.md` after editing to confirm the shipped
  bootstrap scaffolding now reflects the six-skill workflow, topology-aware
  ownership guidance, generated/vendor-noise exclusions, and non-assumptive
  test-layer documentation.
- `rg -n "plan/SKILL|execute/SKILL|topology|generated|vendor|copied-artifact|Owning paths|suite root|security|single shared test root|apps, packages, or services" specs/assets`
  passed and showed the intended bootstrap language across the refreshed asset
  templates.
- `git diff -- specs/assets/AGENTS.md specs/assets/specs/README.md
  specs/assets/specs/spec-template.md` was reviewed to confirm this slice
  stayed limited to the shipped bootstrap assets rather than pulling Milestone
  5's broader repo-facing doc sync forward.
- `git diff --check` passed.
- `test -f specs/assets/AGENTS.md && test -f specs/assets/specs/README.md &&
  test -f specs/assets/specs/spec-template.md && echo present` passed.

## Risks

- Overfitting `specs` and `tests` to `cryptoli` and accidentally narrowing
  portability.
- Making topology discovery too abstract to be actionable for agents.
- Letting repo-bootstrap concerns crowd out sync behavior on mature repos.

## Open Questions

- How much real-repo shape detail from `cryptoli` should become generic skill
  guidance versus remain only an eval/reference input?

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3
- [x] Milestone 4
- [ ] Milestone 5

## Decision Log

- [2026-04-14] Treat `cryptoli` as the primary real-world monorepo reference for
  shaping `specs` and `tests`.
- [2026-04-15] Keep Phase 04 self-contained by inlining the official-source
  grounding and the reusable `cryptoli` shape guardrails in this plan instead
  of relying on external notes or a floating repo state.
- [2026-04-15] Until Phase 05 pins `cryptoli`, use it only as a generic
  monorepo stress case for topology and layer discovery, not as a source of
  portable path-level defaults.
- [2026-04-15] Keep Milestone 1 scoped to the shipped `specs` contract and the
  aligned `specs/agents/openai.yaml` wrapper prompt; defer trigger tightening,
  `tests`, asset refresh, and broader doc sync to later milestones.
- [2026-04-15] Leave `README.md` unchanged in Milestone 1 because its current
  `specs` description already remains accurate at a high level; revisit
  minimal doc sync in Milestone 5 if later slices make the gap material.
- [2026-04-15] Keep Milestone 2 limited to activation semantics for `specs`
  and `tests`; do not pull the deeper `tests` topology and coverage-contract
  refresh forward from Milestone 3.
- [2026-04-15] Sync `AGENTS.md`, `README.md`, and both `agents/openai.yaml`
  wrappers in Milestone 2 because trigger wording is part of the shipped
  provider-agnostic and wrapper-facing surface, not just an internal
  `SKILL.md` detail.
- [2026-04-16] Keep Milestone 3 scoped to `tests/SKILL.md` and
  `tests/agents/openai.yaml`; defer asset refresh and broader doc sync to
  Milestones 4 and 5 unless the refreshed `tests` contract exposes material
  shipped-truth drift.
- [2026-04-16] Treat weak-repo bootstrap as establishing the smallest credible
  automated layer plus explicit gap reporting, not as a requirement to build
  broad new testing infrastructure in one pass.
- [2026-04-16] Refresh `specs/assets/*` in Milestone 4 because the shipped
  bootstrap surface had material drift from the refreshed `specs` and `tests`
  contracts; do not defer that drift to the later eval phase.
- [2026-04-16] Keep Milestone 4 limited to bootstrap scaffolding updates under
  `specs/assets/*`; defer repo-facing README sync and any broader shipped-truth
  edits to Milestone 5.

## Discoveries

- [2026-04-14] The biggest practical risk for `specs` and `tests` is naive path
  discovery that gets polluted by `node_modules`, build outputs, and copied
  artifacts.
- [2026-04-15] This repo still has no formal automated suite, so Phase 04 must
  make its bounded mechanical verification layer explicit or later
  `execute`/`verify` sessions can disagree about completion requirements.
- [2026-04-15] The shipped `specs` skill already covered repo-truth ownership
  and proportional updates, but it was still too generic about topology
  discovery and default noise pruning to reliably prepare mixed-stack or
  monorepo repos.
- [2026-04-15] The current README already covers the high-level `specs` role
  closely enough that Milestone 1 could stay bounded to the `specs` skill
  contract and wrapper prompt without leaving obvious shipped-truth drift.
- [2026-04-15] The shipped `tests` surface was still biased toward
  post-implementation sync and needed explicit bootstrap and gap-close entry
  points before the deeper test-topology refresh in Milestone 3.
- [2026-04-15] Trigger wording for `specs` and `tests` is duplicated across
  `AGENTS.md`, `README.md`, `SKILL.md`, and wrapper metadata, so activation
  clarity drifts unless the slice updates the whole shipped surface together.
- [2026-04-16] The deeper `tests` refresh needed separate contract language for
  topology discovery, minimal bootstrap on weak repos, and honest uncovered-gap
  reporting; otherwise the skill still read like a post-change sync helper.
- [2026-04-16] Wrapper metadata also needs the topology and gap-reporting
  language or provider-facing surfaces under-describe the shipped `tests`
  behavior even when `SKILL.md` is accurate.
- [2026-04-16] The shipped bootstrap `specs/assets/AGENTS.md` had material
  contract drift after Milestones 1 through 3: it still omitted `plan` and
  `execute` from the toolbox guidance and nudged fresh repos toward a fixed
  unit/integration/e2e testing table rather than discovered suite topology.
- [2026-04-16] The existing `specs/assets/specs/README.md` and
  `specs/assets/specs/spec-template.md` already had a usable house style, so
  Milestone 4 only needed targeted ownership and exclusion-language refreshes
  instead of a larger asset redesign.

## Outcomes / Retrospective

- Milestone 1 completed by refreshing the shipped `specs` contract for
  topology-aware repo inspection, agentic-readiness evaluation, and
  proportional organization guidance. Remaining Phase 04 milestones are still
  pending.
- Milestone 2 completed by making bootstrap, sync, and gap-driven activation
  explicit for `specs` and `tests` across the skill docs, wrapper prompts, and
  repo-facing workflow docs. Remaining Phase 04 milestones are still pending.
- Milestone 3 completed by refreshing the shipped `tests` contract for
  topology-aware suite discovery, proportional layer selection, weak-repo
  bootstrap guidance, and explicit uncovered-gap reporting across repo shapes.
  Remaining Phase 04 milestones are still pending.
- Milestone 4 completed by refreshing the shipped bootstrap assets in
  `specs/assets/*` so fresh repos inherit the six-skill workflow, topology-
  aware ownership language, and non-assumptive test-layer scaffolding. Only
  Milestone 5 doc sync remains pending for Phase 04.
