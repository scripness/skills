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

## Risks

- Overfitting `specs` and `tests` to `cryptoli` and accidentally narrowing
  portability.
- Making topology discovery too abstract to be actionable for agents.
- Letting repo-bootstrap concerns crowd out sync behavior on mature repos.

## Open Questions

- How much real-repo shape detail from `cryptoli` should become generic skill
  guidance versus remain only an eval/reference input?
- Should `specs/assets/*` evolve now for the refreshed contract or wait for the
  later eval phase to validate the changes first?

## Progress

- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4
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

## Discoveries

- [2026-04-14] The biggest practical risk for `specs` and `tests` is naive path
  discovery that gets polluted by `node_modules`, build outputs, and copied
  artifacts.
- [2026-04-15] This repo still has no formal automated suite, so Phase 04 must
  make its bounded mechanical verification layer explicit or later
  `execute`/`verify` sessions can disagree about completion requirements.

## Outcomes / Retrospective

- Pending.
