# Phase 03: Consult And Verify Refresh

## Goal

Refresh `consult` and `verify` so they fit the six-skill workflow cleanly,
especially around explicit plan files, phase-based execution, and findings-first
review.

## Scope

- Tighten the trigger boundaries and outputs for `consult`.
- Tighten the verification targets, verdict rules, and evidence requirements for
  `verify`.
- Align both skills with the new `plan` and `execute` contracts.
- Make the trigger-description refinement for both skills explicit rather than
  implied.

## Non-Goals

- Reworking `specs` or `tests`.
- Building eval runners or helper scripts.
- Large repo-doc rewrites beyond minimal truth sync.

## Owned TODO Sections

- The `consult` and `verify` parts of `5. Improve The Six Core Skills`
- The relevant cross-cutting source-grounding work from `6. Ground The Skills In
  Official Sources`

## Deliverables

- Updated `consult/SKILL.md`
- Updated `consult/agents/openai.yaml` if the refreshed `consult` trigger or
  default prompt changes shipped behavior
- Updated `verify/SKILL.md`
- Updated `verify/agents/openai.yaml` if the refreshed `verify` trigger or
  default prompt changes shipped behavior
- Minimal updates to `AGENTS.md` and `README.md` if shipped behavior changes
  current truth

## Dependencies

- Completed Phase 01 and Phase 02 or equivalent delivered contracts for `plan`
  and `execute`
- Existing `README.md` and `TODO.md`

## Repo Context

- Task source: the `consult` and `verify` entries in `TODO.md` section
  `5. Improve The Six Core Skills`, plus the relevant source-grounding work in
  section `6. Ground The Skills In Official Sources`
- Owning code paths: `consult/` and `verify/`, including both `SKILL.md` and
  `agents/openai.yaml` because the agent wrapper prompts are part of the
  shipped surface
- Owning spec paths: `AGENTS.md` as the authoritative workflow contract and
  `README.md` as shipped usage guidance; `TODO.md` remains roadmap truth and
  should stay aligned where shipped behavior would otherwise make its wording
  false or misleading
- Owning test paths: there is still no formal automated suite in this repo, so
  Phase 03 verification should use bounded mechanical checks such as contract
  re-reads, targeted `rg` checks, file-presence checks, and `git diff --check`
- Related docs or references: `PROMPT_verify.md`,
  `plans/2026-04-14-phase-02-execute-skill.md`, and the specific official
  sources that shaped the refreshed `consult` and `verify` contracts:
  `https://developers.openai.com/codex/skills`,
  `https://developers.openai.com/cookbook/articles/codex_exec_plans`,
  `https://agentskills.io/specification`,
  `https://agentskills.io/skill-creation/best-practices`, and
  `https://agentskills.io/skill-creation/optimizing-descriptions`

## Sync Expectations

- `specs`: required if the refreshed `consult` or `verify` contracts change
  durable repo truth about workflow boundaries, trigger guidance, verification
  verdict rules, or the shipped invocation flow; in this repo that means
  updating `AGENTS.md` first as the authoritative contract, then keeping
  `README.md` aligned with the shipped skill and wrapper behavior
- `tests`: no dedicated automated test layer is expected in this phase unless
  the work adds executable validators or eval helpers earlier than planned;
  until then, required follow-through is bounded mechanical verification of the
  shipped skills, wrappers, and any truth-sync edits

## Relevant Official-Source Grounding

- `https://developers.openai.com/codex/skills` reinforced keeping skills
  narrow, explicit about trigger boundaries, and grounded in concrete repo
  inputs rather than vague role descriptions. Phase 03 applied that guidance by
  tightening `consult` and `verify` triggers and anti-triggers in both
  `SKILL.md` files and the shipped OpenAI wrappers.
- `https://developers.openai.com/cookbook/articles/codex_exec_plans`
  reinforced durable task state in files, fresh-session resumability, and
  explicit handoff between planning, execution, and review. Phase 03 applied
  that guidance by making `consult` emit plan carry-forward facts instead of
  hidden plans in chat, and by making `verify` judge explicit plan,
  implementation, and claim targets.
- `https://agentskills.io/specification` reinforced concise skill contracts with
  clear invocation semantics, required inputs, and bounded outputs. Phase 03
  applied that guidance by spelling out the required inputs, findings-first
  output, and explicit failure conditions for `verify`, plus the bounded
  recommendation output for `consult`.
- `https://agentskills.io/skill-creation/best-practices` and
  `https://agentskills.io/skill-creation/optimizing-descriptions` reinforced
  strong trigger descriptions, progressive disclosure, and avoiding overlapping
  skill ownership. Phase 03 applied that guidance by sharpening the wrapper
  descriptions, surfacing anti-trigger routing to `plan`/`execute`/`verify`,
  and keeping minimal repo-truth sync proportional to shipped behavior.

## Milestones

1. Refresh `consult` so it stays evidence-backed, bounded, and explicit about
   what should be carried into a durable plan.
2. Tighten the trigger descriptions and invocation guidance for `consult` and
   `verify` so activation stays clear and reliable.
3. Refresh `verify` so it treats plans, implementations, and claims as distinct
   targets with findings-first output and honest blocked-check reporting.
4. Align both skills with the new workflow boundaries and minimal doc truth.

## Verification

- Confirm `consult` does not drift into owning long-lived task state.
- Confirm `verify` remains a verifier, not an implementer.
- Confirm `verify` explicitly treats missing required `specs` or `tests` sync as
  `fail` when the obligation is clear.
- Confirm both skills point to code/spec references rather than opinion-only
  guidance.
- Confirm the trigger descriptions are explicit enough to reduce overlap with
  `plan`, `execute`, `specs`, and `tests`.
- Confirm `consult/agents/openai.yaml` and `verify/agents/openai.yaml` stay
  aligned with the shipped `SKILL.md` contracts when their prompts or wrapper
  descriptions are touched.
- Run bounded mechanical checks after each contract-changing slice:
  contract re-reads, targeted `rg` checks, file-presence checks, and
  `git diff --check`.
- [2026-04-15] Re-read `consult/SKILL.md` and `consult/agents/openai.yaml`
  after the Milestone 1 edits and confirmed they now align on evidence-backed
  consultation, current-behavior grounding, bounded research, and explicit
  plan carry-forward guidance without turning `consult` into `plan` or
  `execute`.
- [2026-04-15] Ran `find consult -maxdepth 3 -type f | sort` and confirmed the
  shipped `consult/` surface remains intentionally narrow:
  `consult/SKILL.md` and `consult/agents/openai.yaml`.
- [2026-04-15] Ran
  `rg -n 'current behavior|durable task state|research theater|Plan carry-forward|recommend .*plan|recommend .*execute|start from exploration|safest next move' consult/SKILL.md consult/agents/openai.yaml README.md AGENTS.md`
  and confirmed the refreshed `consult` contract is present in the shipped
  skill and wrapper, but this check alone was not sufficient to prove the full
  `README.md` invocation flow still matched the refreshed trigger guidance.
- [2026-04-15] Ran `git diff --check` after the Milestone 1 contract edits; it
  passed with no whitespace or patch-format issues.
- [2026-04-15] Re-read the shipped workflow in `README.md` and found one
  invocation-flow mismatch: step 4 incorrectly said to start every task with
  `consult`, which conflicted with the refreshed `consult` trigger that now
  routes already-clear bounded work to `execute` and already-clear durable work
  to `plan`.
- [2026-04-15] Updated `README.md` so the shipped flow now invokes `consult`
  only when the next move is not yet clear, then re-ran the contract re-reads,
  targeted `rg` checks, file-presence check, and `git diff --check`.
- [2026-04-15] Re-read `AGENTS.md`, `README.md`, `consult/SKILL.md`,
  `consult/agents/openai.yaml`, `verify/SKILL.md`, and
  `verify/agents/openai.yaml` after the Milestone 2 edits and confirmed they
  now align on `consult` only for unclear next moves, `verify` only for
  concrete targets to judge, and explicit anti-triggers that hand plan-file
  work back to `plan`, implementation back to `execute`, and clarification
  back to `consult`.
- [2026-04-15] Ran
  `rg -n 'safest next move is not yet clear enough|concrete target to judge|do not use when the next move is still unclear|do not use for simple lookups|do not use to implement fixes|already a concrete plan, implementation slice, diff, or claim' AGENTS.md README.md consult/SKILL.md consult/agents/openai.yaml verify/SKILL.md verify/agents/openai.yaml`
  and confirmed the tightened trigger language and anti-trigger guidance are
  present across the shipped skill contracts, wrappers, and repo-truth docs.
- [2026-04-15] Ran `git diff --check` after the Milestone 2 trigger and
  invocation edits; it passed with no whitespace or patch-format issues.
- [2026-04-15] A follow-up verification pass found the Milestone 2 wrapper
  prompts still lagged behind the shipped skill anti-triggers: the `consult`
  wrapper did not yet defer concrete judgment work to `verify`, and the
  `verify` wrapper did not yet defer durable-state creation to `plan` or fix
  requests to `execute`.
- [2026-04-15] Updated `consult/agents/openai.yaml` and
  `verify/agents/openai.yaml` so the shipped wrapper prompts now explicitly
  match the Milestone 2 anti-trigger boundaries in the corresponding
  `SKILL.md` files, then re-ran the bounded contract checks and verification.
- [2026-04-15] Re-read `AGENTS.md`, `README.md`, `verify/SKILL.md`, and
  `verify/agents/openai.yaml` after the Milestone 3 edits and confirmed they
  now align on distinct `plan`, `implementation`, and `claims` review
  targets, findings-first output, honest blocked-check reporting, and explicit
  `fail` handling when required `specs` or `tests` sync is missing.
- [2026-04-15] Ran `find verify -maxdepth 3 -type f | sort` and confirmed the
  shipped `verify/` surface remains intentionally narrow:
  `verify/SKILL.md` and `verify/agents/openai.yaml`.
- [2026-04-15] Ran
  `rg -n 'distinct verification targets|findings first|blocked checks|required \`specs\` or \`tests\` sync is a failure|required \`specs\` or \`tests\` sync is \`fail\`|material claim unproven|plan, implementation, or claim review' AGENTS.md README.md verify/SKILL.md verify/agents/openai.yaml`
  and confirmed the refreshed `verify` evidence and verdict contract is
  present across the shipped skill, wrapper, and repo-truth docs.
- [2026-04-15] Ran `git diff --check` after the Milestone 3 contract edits; it
  passed with no whitespace or patch-format issues.
- [2026-04-15] A follow-up verification pass found one remaining repo-truth
  gap: `AGENTS.md` still described `verify` too generically and did not yet
  name distinct plan, implementation, and claim review targets even though the
  refreshed `README.md` and shipped `verify` surfaces did.
- [2026-04-15] Updated `AGENTS.md` so the authoritative one-line `verify`
  summary now matches the shipped target distinction, then re-ran the bounded
  Phase 03 checks and verification.
- [2026-04-15] Re-ran `git diff --check` after the `AGENTS.md` sync; it passed
  with no whitespace or patch-format issues.
- [2026-04-15] Re-ran
  `rg -n 'treat plan review|implementation review, and claim review as distinct targets|identify whether the target is a plan, implementation, or claim review|return findings first|blocked checks|missing required \`specs\` or \`tests\` sync' AGENTS.md README.md verify/SKILL.md verify/agents/openai.yaml`
  and confirmed the authoritative contract, shipped usage guidance, skill, and
  wrapper now all expose the tightened `verify` target distinction and
  findings-first evidence contract.
- [2026-04-15] Re-read `AGENTS.md`, `README.md`, `consult/SKILL.md`,
  `consult/agents/openai.yaml`, `verify/SKILL.md`,
  `verify/agents/openai.yaml`, and `PROMPT_verify.md` for the Milestone 4
  close-out pass and confirmed the refreshed `consult` and `verify` contracts
  already align with the new workflow boundaries and the minimal repo-truth
  docs; no additional shipped contract edits were required in this slice.
- [2026-04-15] Ran `find consult verify -maxdepth 3 -type f | sort`, then ran
  `rg -n 'safest next move is not yet clear enough|do not use it to judge a concrete plan, implementation, diff, or claim|there is already a concrete plan, implementation slice, diff, or claim to judge|findings first|blocked checks|durable task state|create or maintain durable task state|implementation or claim|plan, implementation, or claim' AGENTS.md README.md consult/SKILL.md consult/agents/openai.yaml verify/SKILL.md verify/agents/openai.yaml PROMPT_verify.md`,
  and confirmed the Phase 03 shipped surface remains narrow and the tightened
  boundary language is still present across the skill contracts, wrappers, and
  minimal repo-truth docs.
- [2026-04-15] A follow-up verification pass found the plan still pointed at
  unspecified official-source notes, which made the owned source-grounding
  slice harder to audit from repo truth plus the plan alone.
- [2026-04-15] Replaced that dangling source-note reference with explicit
  official-source links and an in-file `Relevant Official-Source Grounding`
  summary, then re-ran `git diff --check`, the targeted boundary-language
  `rg` scan, and a targeted source-link `rg` scan to confirm the plan is now
  self-contained enough for fresh-session verification.

## Risks

- Making `consult` too verbose or too research-heavy for bounded tasks.
- Making `verify` too broad and turning it into a fixer instead of a reviewer.
- Tightening triggers in a way that weakens proactive use when it is genuinely
  helpful.

## Open Questions

- Should `consult` include a stronger rule for when it must surface “this
  belongs in a plan file”?

## Blockers

- None currently. If Phase 03 truth sync widens beyond `consult`, `verify`,
  `AGENTS.md`, and `README.md`, stop and ask before expanding scope.

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3
- [x] Milestone 4

Milestone 1 note:

- Refreshed `consult/SKILL.md` so it explicitly grounds consultation in current
  repo truth, keeps the work bounded, and surfaces concrete plan carry-forward
  data when durable task state is warranted.
- Synced `consult/agents/openai.yaml` so the shipped wrapper prompt matches the
  refreshed skill contract.
- Updated `README.md` so the shipped invocation flow no longer requires
  `consult` for already-clear tasks; `AGENTS.md` remained accurate without
  changes in this slice.

Milestone 2 note:

- Tightened the shipped `consult` trigger and anti-trigger language in
  `consult/SKILL.md` and `consult/agents/openai.yaml` so it now activates only
  when the safest next move is still unclear and explicitly defers concrete
  judgment work to `verify`.
- Tightened the shipped `verify` trigger and invocation guidance in
  `verify/SKILL.md` and `verify/agents/openai.yaml` so it now activates only
  when there is already a concrete target to judge and explicitly defers
  clarification, planning, and implementation back to `consult`, `plan`, and
  `execute`.
- Synced the minimal durable repo truth in `AGENTS.md` and `README.md` so the
  authoritative workflow contract and usage guidance both reflect the sharper
  activation boundaries without pulling Milestone 3 verdict or evidence work
  forward.
- Repaired the wrapper-level anti-trigger drift that a verification pass found
  after the initial Milestone 2 edit set, so the shipped OpenAI wrappers now
  explicitly redirect concrete judgment to `verify`, durable-state creation to
  `plan`, and implementation requests to `execute` in the same places as the
  refreshed skill contracts.

Milestone 3 note:

- Refreshed `verify/SKILL.md` so plan review, implementation review, and claim
  checks are now distinct targets with target-specific obligations, findings-
  first output, honest blocked-check reporting, and explicit `fail` handling
  for missing required `specs` or `tests` sync.
- Synced `verify/agents/openai.yaml` so the shipped wrapper prompt now matches
  the refreshed skill contract on target selection, findings-first output,
  blocked-check reporting, and missing-sync failure handling.
- Updated the minimal durable repo truth in `AGENTS.md` and `README.md` so the
  authoritative workflow summary and shipped usage guidance both reflect the
  stricter `verify` verdict and evidence contract without pulling Milestone 4
  boundary work forward.
- Re-synced `AGENTS.md` after a follow-up verification pass found its one-line
  `verify` summary still lagged behind the shipped target distinction, then
  re-ran the bounded Phase 03 verification checks.

Milestone 4 note:

- Completed as a bounded close-out verification slice across `consult/`,
  `verify/`, `AGENTS.md`, `README.md`, and the legacy `PROMPT_verify.md`
  reference prompt.
- Confirmed the earlier milestone edits already left the refreshed `consult`
  and `verify` contracts aligned with the new workflow boundaries and the
  minimum required repo-truth docs, so no additional shipped contract edits
  were needed in this slice.
- Left `PROMPT_verify.md` unchanged because it remains a compatible legacy
  helper prompt for explicit plan-path review and widening Phase 03 truth sync
  beyond the phase-owned shipped surfaces was unnecessary.

## Decision Log

- [2026-04-14] Keep `consult` and `verify` separate from planning and execution
  instead of collapsing them into broader meta-skills.
- [2026-04-15] Keep Milestone 1 scoped to `consult/` and its wrapper only;
  leave broader trigger-tightening and `verify` contract work to later
  milestones unless repo-truth docs become false.
- [2026-04-15] Make `consult` emit explicit `Plan carry-forward` guidance
  instead of creating or updating plan files directly, so the boundary with
  `plan` stays sharp while still preserving high-signal handoff material.
- [2026-04-15] Keep Milestone 2 scoped to activation language, anti-triggers,
  and invocation examples across the shipped skill surfaces and minimal
  repo-truth docs; defer deeper `verify` verdict and evidence-contract changes
  to Milestone 3.
- [2026-04-15] Update `AGENTS.md` in this slice because tightened trigger
  guidance is durable workflow contract, not just wrapper copy; leaving
  `AGENTS.md` broad while the shipped skill surfaces became narrower would have
  left the repo's top-priority source of truth underspecified.
- [2026-04-15] Treat `plan`, `implementation`, and `claims` as first-class
  `verify` targets in the shipped contract instead of leaving that distinction
  implicit in examples, so the review obligations and findings-first output
  stay unambiguous.
- [2026-04-15] Treat missing required `specs` or `tests` sync as `fail` when
  the obligation is clear, because `verify` is the workflow gate that enforces
  explicit follow-through from `plan` and `execute`, not a place to downgrade
  those misses into optional risk notes.
- [2026-04-15] Treat Milestone 4 as a close-out verification slice instead of
  forcing another contract edit; once `consult/`, `verify/`, `AGENTS.md`, and
  `README.md` were all aligned, extra truth-sync churn would not improve the
  shipped Phase 03 surface.
- [2026-04-15] Inline the relevant official-source grounding in this plan
  instead of leaving a dangling external-note reference, so the Phase 03
  source-grounding slice remains auditable from repo truth plus the plan file.

## Discoveries

- [2026-04-14] `consult` and `verify` are the decision/review pair in the
  workflow and deserve their own refresh phase rather than being spread across
  unrelated work.
- [2026-04-15] `consult/agents/openai.yaml` and `verify/agents/openai.yaml`
  are part of the shipped skill surface, so Phase 03 should verify wrapper
  prompts stay aligned whenever trigger descriptions or default prompts change.
- [2026-04-15] The pre-refresh `consult` skill already had the right high-level
  role, so Milestone 1 mainly needed sharper execution guidance around current
  behavior, bounded research, and explicit plan handoff content rather than a
  broader repo-truth rewrite.
- [2026-04-15] `AGENTS.md` already described `consult` closely enough for
  Milestone 1, but `README.md` still needed one invocation-flow fix once the
  refreshed trigger boundary made the old "start every task with consult"
  wording false.
- [2026-04-15] `verify` already had the right adversarial-review posture, but
  it still lacked explicit anti-triggers; adding those at the skill and wrapper
  layer reduced overlap with `consult`, `plan`, and `execute` without changing
  the deeper review contract yet.
- [2026-04-15] Once both `consult` and `verify` triggers became more explicit,
  `AGENTS.md` needed a small sync after all because its one-line role summaries
  are the authoritative cross-client contract for this repo.
- [2026-04-15] The wrapper prompts need explicit anti-trigger routing, not
  just tightened positive trigger language; otherwise the shipped surface still
  leaves overlap ambiguity even when the underlying `SKILL.md` contracts are
  correct.
- [2026-04-15] The shipped `verify` skill already had the right adversarial
  posture, but its output and verdict contract was still too generic to make
  blocked evidence and missing required sync reliably actionable.
- [2026-04-15] `AGENTS.md` and the `README.md` verify summary both needed a
  small Milestone 3 sync as well; otherwise the wrapper and `SKILL.md` would
  claim stricter findings-first and fail-on-missing-sync behavior than the
  authoritative repo truth.
- [2026-04-15] The one-line `AGENTS.md` skill summaries need the same level of
  target-shape specificity as the shipped `README.md` and `SKILL.md` files;
  otherwise a later verification pass can correctly reject the slice even when
  the deeper `verify` contract is already aligned.
- [2026-04-15] After the Milestone 3 sync, the remaining Phase 03 work was
  plan closure rather than another shipped-surface rewrite; the minimal
  repo-truth docs were already aligned with the refreshed skills.
- [2026-04-15] Even when the shipped skill surfaces are aligned, the phase plan
  still needs to carry its own durable source-grounding summary if that work is
  in scope; otherwise the close-out claim is harder to verify fresh.

## Outcomes / Retrospective

- Phase 03 is complete: `consult` and `verify` now have refreshed shipped
  contracts, aligned OpenAI wrappers, and matching minimal repo truth in
  `AGENTS.md` and `README.md`.
- The phase stayed proportional by tightening the skill surfaces and only
  touching repo-truth docs when the shipped behavior would otherwise have been
  false or underspecified.
