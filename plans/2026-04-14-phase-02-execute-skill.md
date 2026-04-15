# Phase 02: Execute Skill

## Goal

Ship the `execute` skill so plan-driven implementation can happen in fresh
sessions with a clear stop/update/restart contract instead of relying on
improvised prompts.

## Scope

- Define and ship the first version of the `execute` skill.
- Support both direct bounded execution and explicit plan-driven execution.
- Encode the `specs` and `tests` sync gates and the explicit handoff to
  `verify`.
- Tighten the trigger description and invocation guidance for the future
  `execute` skill.

## Non-Goals

- Building the helper loop scripts.
- Building the full eval harness.
- Refreshing `consult`, `specs`, `tests`, or `verify` beyond minimal boundary
  alignment needed for `execute`.

## Owned TODO Sections

- `4. Add The Execute Skill`
- The `execute` parts of `5. Improve The Six Core Skills`
- Minimal doc sync needed to keep `AGENTS.md`, `README.md`, and `TODO.md`
  truthful after shipping `execute`

## Deliverables

- `execute/SKILL.md`
- `execute/agents/openai.yaml`
- Minimal updates to `AGENTS.md` and `README.md` needed to keep the shipped
  `execute` contract truthful
- Minimal updates to `TODO.md` if the delivered `execute` behavior changes the
  current roadmap wording or assumptions for later phases

## Repo Context

- Task source: `TODO.md` section `4. Add The Execute Skill`, plus the
  `execute`-specific trigger and boundary work in section
  `5. Improve The Six Core Skills`
- Owning code paths: `execute/`, with boundary-alignment touchpoints in
  `plan/SKILL.md`, `consult/SKILL.md`, `verify/SKILL.md`, and any prompt or
  doc files that still describe the pre-`execute` bootstrap loop
- Owning spec paths: `AGENTS.md` as the authoritative workflow contract and
  `README.md` as shipped usage guidance; `TODO.md` remains the roadmap and must
  stay consistent where shipped behavior would otherwise make its wording false
- Owning test paths: no formal automated suite exists yet in this repo; use the
  repo command guidance in `AGENTS.md` plus bounded mechanical checks for the
  shipped skill and doc sync
- Related docs, commands, or external dependencies:
  `PROMPT_execute.md`, `PROMPT_verify.md`, `rg --files .`, `rg "execute" .`,
  `git status --short`, and `git diff --check`

## Dependencies

- Completed Phase 01 or equivalent delivered `plan` skill contract
- Existing `consult`, `specs`, `tests`, and `verify` skill boundaries
- Existing `AGENTS.md`, `README.md`, and `TODO.md`
- Existing bootstrap prompts: `PROMPT_execute.md` and `PROMPT_verify.md`

## Sync Expectations

- `specs`: required in this phase because shipping `execute` changes durable
  repo truth about the canonical implementation flow, stop/update/restart
  behavior, plan-path handoff, and `specs`/`tests` sync responsibilities; in
  this repo that means updating `AGENTS.md` first as the authoritative
  contract, then keeping `README.md` aligned with the shipped `execute` skill,
  and updating `TODO.md` only where the roadmap wording would otherwise become
  false or misleading after the ship.
- `tests`: no dedicated automated test layer is expected in this phase unless
  the implementation introduces executable helpers, validators, or eval
  scaffolding earlier than planned; until then, the required follow-through is
  bounded mechanical verification of the shipped skill and doc sync, including
  file-presence checks, contract re-reads against `AGENTS.md` and `README.md`,
  and `git diff --check`

## Milestones

1. Finalize the `execute` boundary:
   direct mode versus plan-driven mode, explicit plan-path requirements, and
   handoff rules to `verify`.
2. Tighten the trigger description and invocation guidance for `execute` so it
   is clearly distinguishable from `consult`, `plan`, and `verify`.
3. Write `execute/SKILL.md` with one-bounded-slice execution, required
   mechanical checks, and mandatory plan updates for plan-driven work.
4. Encode the sync gates for `specs` and `tests`, including direct-mode
   inference from repo truth when no plan file exists.
5. Sync docs minimally so the shipped skill contract stays truthful.

## Verification

- Confirm the Phase 02 deliverables exist with the intended narrow scaffold:
  `execute/SKILL.md` and `execute/agents/openai.yaml`.
- Re-read `execute/SKILL.md`, `AGENTS.md`, `README.md`, and `TODO.md` together
  after each contract-changing slice and confirm they stay aligned on shipped
  versus planned workflow.
- Confirm `execute` never guesses the latest plan file.
- Confirm `execute` stops after one bounded slice and updates the plan before
  stopping in plan-driven mode.
- Confirm `execute` does not self-invoke adversarial `verify`.
- Confirm `execute` treats missing required `specs` or `tests` sync as blocking
  follow-through, not optional polish.
- Confirm the `execute` trigger description is explicit enough that direct and
  plan-driven modes are both discoverable without overlapping other skills.
- Run `git diff --check` after each edit set that changes the shipped skill or
  doc contract.
- [2026-04-14] Re-read `AGENTS.md`, `README.md`, and `TODO.md` after the
  Milestone 1 edits and confirmed they now align on `execute` supporting
  direct bounded execution and explicit plan-driven execution, forbidding
  latest-plan guessing, and handing adversarial review to `verify`.
- [2026-04-14] Ran
  `rg -n 'latest plan file|adversarial review|hand off explicitly|hand adversarial review back' AGENTS.md README.md TODO.md`
  and confirmed the tightened boundary language is present in repo truth and
  the roadmap.
- [2026-04-14] Ran `git diff --check` after the Milestone 1 doc edits; it
  passed with no whitespace or patch-format issues.
- [2026-04-14] Re-read `AGENTS.md`, `README.md`, and `TODO.md` after the
  Milestone 2 edits and confirmed they now align on the positive `execute`
  trigger ("implementation now"), the anti-triggers that hand unclear work
  back to `consult`, durable-state setup back to `plan`, and adversarial
  judgment back to `verify`, while keeping `execute` clearly marked as planned
  rather than shipped.
- [2026-04-14] Ran
  `rg -n 'invoke \`execute\` when the user wants implementation now|do not invoke \`execute\`|trigger when the user wants implementation now|do not use when the next move still needs clarification|Execute directly:|improvising a hidden plan in chat' AGENTS.md README.md`
  and confirmed the tightened trigger language and direct-mode promotion rule
  are present in repo truth.
- [2026-04-14] Ran `git diff --check` after the Milestone 2 doc edits; it
  passed with no whitespace or patch-format issues.
- [2026-04-15] Re-read `execute/SKILL.md`, `AGENTS.md`, `README.md`, and
  `TODO.md` after shipping the `execute/` scaffold and confirmed they align on
  direct versus plan-driven entry modes, the explicit-plan-path requirement,
  one-bounded-slice execution, required `specs`/`tests` follow-through, and
  explicit handoff to `verify`.
- [2026-04-15] Ran `find execute -maxdepth 3 -type f | sort` and confirmed the
  shipped scaffold is intentionally narrow:
  `execute/SKILL.md` and `execute/agents/openai.yaml`.
- [2026-04-15] Ran
  `rg -n 'planned next skill|Until \`execute\` ships|Planned \`execute\` contract|### \`execute\` \(planned\)|while \`execute\` is still not shipped here|target workflow after \`execute\` ships' AGENTS.md README.md`
  and confirmed those stale pre-ship phrases no longer appear in shipped docs.
- [2026-04-15] Ran
  `rg -n 'never guess the latest plan file|implement only one milestone or other bounded slice|specs\` or \`tests\` follow-through' execute/SKILL.md AGENTS.md README.md`
  and confirmed the core execute contract is present in the shipped skill and
  synced docs.
- [2026-04-15] Ran
  `rg -n 'hand off.*\`verify\`|Do not absorb adversarial review into \`execute\`|hand adversarial review back to \`verify\`' execute/SKILL.md AGENTS.md README.md`
  and confirmed the shipped contract keeps adversarial review in `verify`.
- [2026-04-15] Ran `git diff --check` after shipping `execute/` and syncing the
  docs; it passed with no whitespace or patch-format issues.
- [2026-04-15] Repaired the `execute/agents/openai.yaml` default prompt so it
  no longer implies that direct mode always updates a plan file; the wording
  now makes plan updates conditional on plan-driven work, matching
  `execute/SKILL.md`.
- [2026-04-15] Re-ran `git diff --check`, `find execute -maxdepth 3 -type f |
  sort`, and the contract `rg` checks after that repair and confirmed the
  shipped `execute` scaffold still matches the Phase 02 contract.

## Risks

- Letting `execute` silently absorb review behavior that should stay in
  `verify`.
- Making direct mode too broad and encouraging plan-skipping on work that
  really needs durable state.
- Encoding sync gates too vaguely, which would leave `specs` or `tests`
  follow-through inconsistent.

## Open Questions

- Should the first shipped `execute` skill include explicit examples for direct
  mode and plan-driven mode in the skill body?
- How much mechanical-check guidance should live in the generic skill versus be
  deferred to per-repo `AGENTS.md`?

## Blockers

- None currently.

## Progress

- [x] Milestone 1
- [x] Milestone 2
- [x] Milestone 3
- [x] Milestone 4
- [x] Milestone 5

Milestone 1 note:

- Completed as a doc-contract slice in `AGENTS.md` and `README.md`.
- Left the `execute/` scaffold and broader sync-gate behavior to later
  milestones so the repo does not imply that `execute` is already shipped.

Milestone 2 note:

- Completed as a doc-contract slice in `AGENTS.md` and `README.md`.
- Locked positive triggers, anti-triggers, direct-to-`plan` promotion rules,
  and clearer direct versus plan-driven invocation examples without shipping
  the `execute/` scaffold yet.

Milestone 3 note:

- Shipped the narrow `execute/` scaffold in `execute/SKILL.md` and
  `execute/agents/openai.yaml`.
- Completed the minimum `AGENTS.md` and `README.md` truth sync in the same
  slice so the repo no longer claims `execute` is still only planned.

Milestone 4 note:

- Encoded `specs` and `tests` follow-through gates directly in the first
  shipped `execute` skill.
- The shipped skill now makes repo-truth inference explicit before editing and
  treats blocked required sync as a stop condition rather than optional polish.

Milestone 5 note:

- Kept doc sync proportional: flipped `execute` from planned to shipped,
  updated the roadmap working loop to use the real `execute` and `verify`
  skills, and marked the old bootstrap prompt files as legacy reference
  artifacts.
- No `TODO.md` edit was required because the roadmap wording remained truthful
  after the shipped `execute` contract landed.

## Decision Log

- [2026-04-14] `execute` should support both direct bounded execution and
  explicit plan-driven execution instead of splitting into two skills.
- [2026-04-14] Phase 02 must treat `AGENTS.md` as required truth-sync follow-
  through when `execute` ships, because `AGENTS.md` is this repo's highest-
  priority workflow contract and cannot remain in the pre-`execute` state.
- [2026-04-14] Treat Milestone 1 as doc-contract tightening only: align
  `AGENTS.md` and `README.md` with the existing `TODO.md` boundary before
  creating any `execute/` files, so the repo does not imply that `execute` is
  already shipped.
- [2026-04-14] Treat Milestone 2 as a second doc-contract slice before
  creating `execute/`: make the trigger explicit in repo truth, name the
  anti-triggers versus `consult`, `plan`, and `verify`, and add direct and
  plan-driven invocation examples in `README.md`.
- [2026-04-15] Ship the first `execute` scaffold as one bounded slice that
  includes the narrow skill files plus the minimum shipped-truth doc edits;
  leaving `AGENTS.md` and `README.md` in the pre-ship state would have made
  repo truth immediately false.
- [2026-04-15] Encode the `specs` and `tests` follow-through gate in the first
  shipped `execute` skill rather than deferring it to a later rewrite, because
  the direct-mode and plan-driven contracts are not safe without an explicit
  stop condition when required sync is missing.
- [2026-04-15] Keep `PROMPT_execute.md` and `PROMPT_verify.md` in the repo as
  legacy reference artifacts rather than baseline workflow requirements now
  that `execute` is shipped.
- [2026-04-15] The OpenAI agent scaffold must preserve the same direct versus
  plan-driven distinction as `execute/SKILL.md`; helper-facing prompts are part
  of the shipped contract, not just packaging.

## Discoveries

- [2026-04-14] A clean `execute` skill is the missing primitive that turns the
  roadmap into a reliable fresh-session implementation loop.
- [2026-04-14] The Phase 02 plan itself needed explicit repo context,
  blockers, and named `specs` ownership to satisfy the shipped `plan`
  resumability contract before implementation starts.
- [2026-04-14] `TODO.md` already captured the intended `execute` boundary more
  precisely than `AGENTS.md` and `README.md`, so Milestone 1 only needed truth
  sync rather than roadmap edits.
- [2026-04-14] The missing contract details were the explicit split between
  direct and plan-driven modes, the "never guess the latest plan file" rule,
  and the explicit `execute` -> `verify` handoff.
- [2026-04-14] Even after Milestone 1, `execute` was still less discoverable
  than the shipped skills because repo truth lacked an explicit
  "implementation now" trigger and explicit anti-triggers.
- [2026-04-14] The strongest missing invocation cue was a direct-mode example;
  the repo already had a plan-driven example, but not a matching direct
  bounded-execution example.
- [2026-04-15] Most of the `execute` boundary was already captured in
  `AGENTS.md`, `README.md`, and `TODO.md`; shipping the skill mainly required
  turning that planned contract into a concrete skill scaffold and removing the
  stale "not shipped yet" wording.
- [2026-04-15] The `specs`/`tests` sync gate could be expressed proportionally
  inside the first `execute` skill without broadening the repo or adding new
  tooling.
- [2026-04-15] `TODO.md` remained valid as roadmap truth after the ship, so the
  required doc sync for this slice was limited to `AGENTS.md` and `README.md`.
- [2026-04-15] The narrowest remaining risk after shipping was not in the main
  skill body but in the connector-facing default prompt, which also needed to
  avoid implying that every `execute` run has a plan file.

## Outcomes / Retrospective

- Phase 02 is now complete: the repo ships `execute/SKILL.md` and
  `execute/agents/openai.yaml`, `AGENTS.md` and `README.md` now describe
  `execute` as shipped rather than planned, and the working loop now uses the
  real `execute`/`verify` skills instead of the bootstrap prompts.
- The legacy prompt files remain checked in only as reference artifacts from
  the pre-ship execution loop; the baseline workflow is now the six shipped
  skills plus explicit `plans/*.md` files when durable task state is needed.
- The post-ship verification gap in `execute/agents/openai.yaml` is now closed;
  the packaged OpenAI prompt matches the same direct-mode versus plan-driven
  behavior required by the shipped `execute` skill.
