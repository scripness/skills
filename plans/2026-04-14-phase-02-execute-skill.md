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
- [ ] Milestone 2
- [ ] Milestone 3
- [ ] Milestone 4
- [ ] Milestone 5

Milestone 1 note:

- Completed as a doc-contract slice in `AGENTS.md` and `README.md`.
- Left the `execute/` scaffold and broader sync-gate behavior to later
  milestones so the repo does not imply that `execute` is already shipped.

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

## Outcomes / Retrospective

- Milestone 1 completed with doc-only contract sync; repo truth now makes the
  future `execute` boundary explicit without shipping the `execute/` scaffold
  early.
- Remaining milestones still own trigger tightening, the actual `execute`
  scaffold, sync-gate encoding, and final shipped-doc alignment.
