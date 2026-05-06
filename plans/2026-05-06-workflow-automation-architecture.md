# Workflow Automation Architecture

Use this file as the living task plan for replacing `TODO.md` with a
ready-to-execute, file-backed plan for the workflow automation and adjunct
skill work. Keep it updated in place. A fresh session should be able to resume
from repo truth plus this file alone.

Update `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
`Blockers` after each bounded slice or plan-driven verification pass. Hand off
later `execute` and `verify` sessions with this exact file path:
`plans/2026-05-06-workflow-automation-architecture.md`.

## Goal

Replace the broad `TODO.md` backlog with a durable, executable plan that moves
the skills repo toward a stronger provider-agnostic workflow architecture:
clearer repo truth, stricter specs boundaries, leaner six-skill contracts,
optional script-based amplification, planning automation, adjunct skills, and a
controlled downstream cryptoli refresh.

Done means:

- `TODO.md` has been deleted after this plan passes the requested consultation
  and verification review.
- This plan contains all durable decisions and actionable work previously held
  in `TODO.md`.
- The next unfinished milestone is decision-complete enough for a fresh
  `execute` session to take without re-planning.
- Repo validation passes after the conversion.
- Future implementation work can proceed one milestone at a time, with
  verification and commit gates where required.

## Scope

- Preserve the provider-agnostic six-skill workflow as the semantic core:
  `consult`, `plan`, `execute`, `verify`, `specs`, and `tests`.
- Convert the April 22, 2026 Agent Skills comparison and the May 6, 2026 final
  synthesis into this one canonical plan.
- Strengthen `AGENTS.md` and `specs/` so specs explain durable code and system
  truth, never task plans or TODOs.
- Update the `specs` skill and bootstrap assets so downstream repos inherit the
  same hard repo-truth boundary.
- Trim and sharpen the six source skills while preserving direct-chat
  usefulness.
- Add dependency-sensitive external grounding rules.
- Align frontmatter, compatibility metadata, trigger descriptions, and eval
  portability with current Agent Skills guidance where useful.
- Add optional adjunct skill surfaces for `grill` and `caveman`, and decide
  whether `improve` should become a standalone adjunct skill or a `consult`
  mode/reference.
- Define shared script/wrapper conventions for optional skill amplification.
- Ship a planning-only loop under `src/plan/scripts/loop.py`.
- Strengthen execute-loop verification fan-out in the provider wrapper layer
  without changing the generic execute loop contract.
- Define an implemented-plan verification campaign wrapper.
- Add optional operator surface guidance after loop contracts are strong.
- Refresh downstream cryptoli repo truth, installed skills, and fixture pin
  after source-repo decisions land.

## Non-Goals

- Do not implement all workflow changes in one pass.
- Do not make provider-native features such as plan modes, plugins, MCPs,
  hooks, auto-memory, native subagents, or client-specific agent APIs required
  workflow primitives.
- Do not move workflow semantics into scripts, dashboards, provider wrappers,
  or scratch logs.
- Do not replace `AGENTS.md`, `specs/`, and explicit `plans/*.md` with
  `CONTEXT.md`, ADRs, or other external repo-truth layers.
- Do not make `grill`, `caveman`, or `improve` owners of core workflow
  semantics.
- Do not modify cryptoli product code as part of source-repo workflow
  architecture work.
- Do not overwrite dirty cryptoli work during downstream refresh.
- Do not commit generated `.tmp/evals/` artifacts.

## Deliverables

- Delete `TODO.md` after review confirms this plan carries the backlog.
- This plan file, updated in place with execution and verification history.
- Updated source repo docs and specs:
  - `AGENTS.md`
  - `README.md`
  - `docs/maintenance.md`
  - `docs/sources.md`
  - `specs/README.md`
  - `specs/workflow-contract.md`
  - `specs/repo-surface.md`
  - `specs/evaluation-harness.md`
- Updated skill payloads and companion docs:
  - `src/consult/`
  - `src/plan/`
  - `src/execute/`
  - `src/verify/`
  - `src/specs/`
  - `src/tests/`
  - optional `src/grill/`
  - optional `src/caveman/`
  - optional `src/improve/` or `consult` reference material
- Updated bootstrap assets under `src/specs/assets/`.
- Updated shared eval metadata and workflow cases under `src/*/evals/` and
  `evals/`.
- Optional helper and wrapper references/scripts:
  - `src/<skill>/scripts/loop.py` where useful
  - `src/<skill>/scripts/providers/codex_loop.py` where useful
  - `src/<skill>/scripts/providers/codex_loop_dashboard.py` only when operator
    value is real
  - `src/<skill>/references/optional-helper.md`
  - `src/execute/references/verification-campaign.md`
- Refreshed downstream cryptoli install and fixture manifest when source work
  is ready.

## Repo Context

- Task source: user request to convert `TODO.md` into a ready-to-execute plan,
  delete `TODO.md`, and push the result after two consultation and two
  verification agents review both files.
- Owning code paths:
  - `src/*/SKILL.md`
  - `src/*/README.md`
  - `src/*/agents/openai.yaml`
  - `src/*/evals/evals.json`
  - `src/execute/scripts/loop.py`
  - `src/execute/scripts/providers/codex_loop.py`
  - `src/execute/scripts/providers/codex_loop_dashboard.py`
  - `scripts/sync_downstream.py`
  - `evals/scripts/harness.py`
- Owning spec paths:
  - `specs/README.md`
  - `specs/workflow-contract.md`
  - `specs/repo-surface.md`
  - `specs/evaluation-harness.md`
- Owning test/eval paths:
  - `src/*/evals/evals.json`
  - `evals/runtime.json`
  - `evals/fixtures/cryptoli.json`
  - `evals/scripts/harness.py`
  - `Makefile`
- Related docs and assets:
  - `AGENTS.md`
  - `README.md`
  - `docs/maintenance.md`
  - `docs/sources.md`
  - `src/plan/assets/plan-template.md`
  - `src/specs/assets/AGENTS.md`
  - `src/specs/assets/specs/README.md`
  - `src/specs/assets/specs/spec-template.md`
- Downstream repo:
  - `/home/scrip/Code/cryptoli`
  - `evals/fixtures/cryptoli.json`

## Source Grounding

This plan is grounded in a point-in-time review of the official Agent Skills
guidance on April 22, 2026 and local workflow synthesis on May 6, 2026.
Recheck upstream guidance if the Agent Skills spec or this repo's workflow
contract materially changes.

Upstream Agent Skills sources reviewed:

- `https://agentskills.io/home`
- `https://agentskills.io/what-are-skills`
- `https://agentskills.io/specification`
- `https://agentskills.io/skill-creation/best-practices`
- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
- `https://agentskills.io/skill-creation/using-scripts`
- `https://agentskills.io/client-implementation/adding-skills-support`

Additional external skill sources reviewed on May 6, 2026:

- `https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md`
- `https://github.com/mattpocock/skills`
- `https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me`
- `https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs`
- `https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture`
- selected Matt Pocock engineering skills for surrounding patterns:
  `diagnose`, `tdd`, `to-issues`, and `zoom-out`

Local sources reviewed:

- `AGENTS.md`
- `README.md`
- `specs/workflow-contract.md`
- `specs/repo-surface.md`
- `specs/evaluation-harness.md`
- `src/*/SKILL.md`
- `src/execute/scripts/loop.py`
- `src/specs/assets/AGENTS.md`
- `src/specs/assets/specs/README.md`
- `src/specs/assets/specs/spec-template.md`
- local `/home/scrip/Code/cryptoli/AGENTS.md`
- local `/home/scrip/Code/cryptoli/specs/`

Durable source-grounding recheck triggers:

- The published Agent Skills spec changes required or optional frontmatter.
- Upstream trigger guidance moves away from description quality and progressive
  disclosure.
- Upstream script guidance changes away from non-interactive, structured,
  agent-friendly execution.
- Upstream evaluation guidance materially changes repeated runs, validation
  splits, baselines, or human review guidance.
- This repo stops optimizing primarily for coding-agent environments with repo
  access, writable worktrees, and non-interactive shell access.

## Consult Carry-Forward

- Keep the six workflow skills as the semantic core:
  `consult`, `plan`, `execute`, `verify`, `specs`, and `tests`.
- Treat `grill` and `caveman` as workflow-adjacent adjunct skills, not as
  owners of core workflow semantics.
- Use `grill` for alignment and decision-tree clarification before planning or
  before high-risk design choices.
- Use `caveman` for user-facing communication style only.
- Keep Karpathy-style guidance as quality-bar language inside existing skills:
  explicit assumptions, simple scoped changes, surgical edits, and verifiable
  success criteria.
- Treat Matt Pocock's skills as useful pattern input, not as a contract to copy.
  Import the small/composable stance and selected practices; do not import
  provider-native mechanics, mandatory `CONTEXT.md`, or required ADR layers.
- `AGENTS.md` should be stronger, shorter, and more operational.
- `specs/` must explain durable code and system truth only. Specs must not
  contain task plans, task lists, future-work backlogs, milestone status, or
  implementation TODOs.
- Every shipped skill may grow optional scripts, but scripts amplify the skill;
  they do not replace or redefine it.
- Generic helper naming should mirror execute:
  `src/<skill>/scripts/loop.py`,
  `src/<skill>/scripts/providers/codex_loop.py`, and dashboard wrappers only
  when an operator need is real.
- Skill contracts own trigger rules, required evidence, canonical writes,
  output/verdict rules, and `specs` / `tests` obligations.
- Wrappers own worker count, fan-out, retries, logs, dashboards, events,
  provider CLI invocation, pause/resume, locks, and run history.
- Worker or shard outputs are evidence only. Canonical truth stays in
  `AGENTS.md`, `specs/`, explicit `plans/*.md`, and tests.
- Plans should be smaller, with bounded milestones that can be executed and
  verified one at a time.
- A coherent completed milestone should normally become one commit after
  execution, checks, verification, plan evidence updates, and unrelated dirty
  worktree review.
- Base skills should not auto-commit. Commit gates belong in wrapper/operator
  flows and verification-campaign flows.
- Use "6+1 specs agents" as orchestration topology: six read-only specs audit
  angles plus one orchestrator that writes `AGENTS.md` and `specs/`.
- Cryptoli currently has a dirty product worktree; downstream sync should wait
  for that branch to stabilize or be done as an explicitly isolated skill/spec
  refresh with dirty-worktree risk acknowledged.

## Dependencies

- User-requested review gate before deleting `TODO.md`:
  - two consultation agents
  - two verification agents
  - all four agents must compare `TODO.md` with this plan before `TODO.md` is
    deleted and before commit/push
- Existing `TODO.md` remains available until that review gate is complete.
- `make validate` should pass after the plan conversion and after `TODO.md`
  deletion.
- Broad downstream cryptoli refresh depends on either a stable cryptoli branch
  or explicit user approval to refresh skill/spec surfaces on a dirty tree.
- External source rechecks are required before implementation slices that make
  dependency-sensitive or upstream-compatibility claims.

## Sync Expectations

- `specs`: Required for most milestones. Source repo specs and docs must stay
  aligned with any changed shipped behavior, helper surface, eval contract,
  downstream sync behavior, adjunct skill status, or provider-agnostic runtime
  boundary. Specific owning specs are named at each milestone.
- `tests`: Required when a milestone changes harness behavior, helper scripts,
  eval assertions, trigger behavior, or workflow cases. In this repo, "tests"
  primarily means `make validate`, targeted `python3 evals/scripts/harness.py`
  commands, helper dry-runs, and eval metadata updates.

## Milestones

1. Intake conversion and TODO removal: create this plan from `TODO.md`, run the
   requested two consultation and two verification agents against both files,
   incorporate accepted feedback, delete `TODO.md`, run `make validate`, and
   commit/push the plan conversion. Owning paths: `TODO.md`,
   `plans/2026-05-06-workflow-automation-architecture.md`. `specs` exit
   criteria: not required because this slice only moves task-local state from
   `TODO.md` to a plan. `tests` exit criteria: `make validate` passes. Commit:
   one docs commit for plan conversion and TODO deletion.

2. Provider-agnostic runtime boundary and generic worker contract: update
   `AGENTS.md`, `README.md`, `docs/maintenance.md`, `docs/sources.md`,
   `specs/workflow-contract.md`, `specs/repo-surface.md`, and helper
   references so provider-native features are optional adapters only, and
   define a generic worker/session launch contract covering command template,
   working directory, prompt payload, skill invocation, read/write policy,
   timeout, log path, structured output schema, exit-code mapping, installed
   layout path resolution, and file-backed scratch outputs. Done when docs and
   specs consistently distinguish skills from wrappers and use generic terms
   such as worker, shard, session, or provider process unless naming a specific
   provider feature. `specs` exit criteria: `specs/workflow-contract.md` and
   `specs/repo-surface.md` updated. `tests` exit criteria: `make validate` and
   targeted `rg` checks for forbidden required-provider wording. Commit: one
   docs/specs commit.

3. Repo truth and specs hard boundary: improve `AGENTS.md` and `specs/` so
   repo truth is easier for fresh agents to apply without confusing durable
   system truth with task planning. Update `src/specs/SKILL.md`,
   `src/specs/README.md`, `src/specs/assets/AGENTS.md`,
   `src/specs/assets/specs/README.md`,
   `src/specs/assets/specs/spec-template.md`, source repo specs, README, and
   eval cases so specs explain durable code, domain, architecture, operational,
   and testing truth only. Done when specs explicitly reject task plans, task
   lists, future-work backlogs, implementation TODOs, milestone state, active
   blockers, and readiness certifications. `specs` exit criteria:
   `specs/workflow-contract.md`, `specs/repo-surface.md`, and
   `specs/README.md` aligned. `tests` exit criteria: `make validate` plus eval
   cases that fail when `specs` writes planning content. Commit: one
   specs-skill/docs commit.

4. Six-skill lean contract and Karpathy quality bars: trim `consult`, `plan`,
   `execute`, `verify`, `specs`, and `tests` so each remains direct-chat useful
   and wrapper-independent. Move fan-out and helper details into references or
   wrapper docs. Fold Karpathy-style guidance into quality bars: explicit
   assumptions, simple scoped changes, surgical edits, no speculative
   abstractions, and verifiable success criteria. Done when each skill has sharp
   trigger boundaries, canonical write ownership, focused output rules, and no
   required provider-native features. `specs` exit criteria:
   `specs/workflow-contract.md` updated if skill semantics change. `tests` exit
   criteria: `make validate` plus trigger/workflow eval updates for overtrigger,
   wrapper-dependence, skipped canonical writes, broad test/spec mandates, and
   missing quality gates. Commit: one skill-contract commit.

5. Dependency-sensitive external grounding: update `consult`, `plan`,
   `execute`, `verify`, `specs`, `tests`, `src/plan/assets/plan-template.md`,
   specs, docs, and evals so agents must identify exact local dependency
   versions and prefer local shipped artifacts before relying on current docs
   or model memory when freshness matters. Done when plans can record external
   grounding with freshness requirement, local version evidence, official
   source/docs checked, accessed date, decision impact, recheck trigger, and
   unresolved gaps. `specs` exit criteria: workflow contract and docs describe
   grounding obligations. `tests` exit criteria: evals fail
   dependency-sensitive claims without exact-version evidence and source/docs
   comparison. Commit: one grounding commit.

6. Standards alignment, compatibility metadata, trigger ergonomics, and eval
   portability: decide whether `argument-hint` remains a documented local
   extension, moves under metadata, or becomes optional; add `compatibility`
   metadata where useful; tighten descriptions toward user intent; document the
   mapping between this repo's eval governance and upstream eval expectations.
   Done when the harness and docs clearly state what is portable versus
   repo-specific and at least one real-client smoke path is defined or
   recorded. `specs` exit criteria: `specs/evaluation-harness.md`,
   `specs/workflow-contract.md`, README, and maintenance docs aligned.
   `tests` exit criteria: `make validate`, frontmatter validation changes if
   any, and trigger eval updates. Commit: one standards/eval commit.

7. Milestone commit cadence: update `src/plan/SKILL.md`,
   `src/plan/assets/plan-template.md`, `src/execute/SKILL.md`,
   `src/verify/SKILL.md`, helper references, specs, and evals so plans can
   record intended commit boundaries and post-verify commit evidence while base
   skills still avoid direct commit authority. Done when a completed milestone
   has a documented optional gate: execute, checks, required `specs` / `tests`,
   verify, plan evidence update, dirty-worktree review, commit, and commit SHA
   recording. `specs` exit criteria: workflow contract updated. `tests` exit
   criteria: evals fail broad milestones, unrelated-work commits, skipped
   verification before commit, and missing commit evidence when cadence was
   required. Commit: one plan/execute/verify commit.

8. Adjunct skill governance and install-surface decision: decide how adjunct
   skills fit the repo before adding new skill directories. Cover `grill`,
   `caveman`, and possible `improve`; decide default downstream install versus
   optional `SKILL=...`; update the harness/runtime/sync model so
   `evals/scripts/harness.py`, `evals/runtime.json`,
   `scripts/sync_downstream.py`, managed README wording, `AGENTS.md`, and specs
   all agree on which skills are shipped core, shipped adjunct, optional-only,
   or local-only. Done when adding an adjunct directory will not surprise
   validation, sync, or downstream docs. `specs` exit criteria:
   `specs/workflow-contract.md` and `specs/repo-surface.md` record the
   adjunct/core boundary. `tests` exit criteria: `make validate` and any
   harness/sync eval updates required by the decision. Commit: one
   adjunct-governance commit.

9. Grill adjunct skill: add `grill` as a workflow-adjacent alignment skill when
   Milestone 8 says it should ship. It should interview the user one question
   at a time about a plan, design, or high-risk implementation direction;
   provide the recommended answer with each question; inspect repo code and
   specs instead of asking when the repo can answer; preserve copy-ready
   carry-forward for `plan`; use `AGENTS.md` and `specs/` as the durable
   language layer; and treat `CONTEXT.md` or ADRs as optional target-repo
   conventions only. Done when `grill` cannot replace `consult`, cannot create
   implementation plans except by handing off to `plan`, and does not write
   `specs/` directly by default. `specs` exit criteria: core docs and specs
   mention `grill` only as adjunct alignment. `tests` exit criteria: evals
   cover one-question-at-a-time behavior, code/spec lookup before asking,
   copy-ready plan carry-forward, and non-interference with `consult`, `plan`,
   and `specs`. Commit: one `grill` commit.

10. Caveman permanent-citizen adjunct skill: add `caveman` as a permanent
    citizen in this source repo, using
    `https://github.com/mattpocock/skills/blob/main/skills/productivity/caveman/SKILL.md`
    as source reference. Add the source skill payload under `src/caveman/` and
    decide whether it is a shipped workflow-adjacent skill or local optional
    style skill for downstream install purposes, but do not leave it absent
    from this source repo. It affects user-facing chat only and must not
    override workflow skill contracts, repo docs, plan files, tests, code
    comments, error text, commands, safety warnings, findings, required checks,
    or durable repo truth. Done when `src/caveman/` has `SKILL.md`,
    `README.md`, `agents/openai.yaml`, and `evals/evals.json`; `AGENTS.md`,
    README, and `specs/workflow-contract.md` match the chosen shipped/default
    status; downstream sync behavior and managed README wording are updated
    when applicable; and the guardrail is explicit that `caveman` affects
    communication only. `specs` exit criteria: `AGENTS.md`, README,
    `specs/workflow-contract.md`, and `specs/repo-surface.md` match the chosen
    status. `tests` exit criteria: evals fail if terse style causes missing
    findings, weak plan sections, skipped checks, unclear durable truth, or
    contract override. Commit: one `caveman` commit.

11. Improve architecture adjunct decision: decide whether Matt-style
    `improve-codebase-architecture` becomes a standalone `src/improve/` skill,
    a `consult` reference/mode, or no shipped surface yet. Candidate behavior
    must inspect repo truth and code to surface architecture friction; present
    numbered candidates with files, problem, solution, benefits, testing
    impact, and conflicts with repo truth; ask the user which candidate to
    explore before designing interfaces or implementation slices; and hand off
    chosen work to `grill` or `plan` when durable state is needed. Do not import
    provider-specific subagent mechanics, hard-code `CONTEXT.md` or ADRs, or
    generate speculative refactor backlogs. `specs` exit criteria: docs/specs
    record the decision if shipped. `tests` exit criteria: evals fail
    speculative refactor lists, provider-native dependency, and architecture
    claims without code/spec evidence. Commit: decision/reference commit, with
    implementation split if shipped.

12. Shared per-skill script convention: define a repo-wide optional helper
   pattern for skill amplification:
   `src/<skill>/scripts/loop.py`,
   `src/<skill>/scripts/providers/codex_loop.py`,
   dashboard wrappers only when useful, and
   `src/<skill>/references/optional-helper.md`. Done when docs/specs explain
   that scripts own execution strategy while skills own semantics, and when
   installed-layout path resolution works equally from `src/<skill>/...` and
   `.agents/skills/<skill>/...`. `specs` exit criteria:
   `specs/repo-surface.md` and `specs/workflow-contract.md` updated. `tests`
   exit criteria: helper validation or dry-run coverage where scripts exist.
   Commit: one helper-convention commit.

13. Planning-only loop: ship `src/plan/scripts/loop.py`,
    `src/plan/scripts/providers/codex_loop.py`, optional
    `src/plan/scripts/providers/codex_loop_dashboard.py` only after repeated
    operator pain proves dashboard value, and
    `src/plan/references/optional-helper.md`. The loop must automate
    `consult -> plan -> verify(plan)` while creating or checkpointing one
    explicit canonical plan path early, before brainstorming exhausts context.
    It should use deterministic consult/verify angles, require the orchestrator
    to run its own first-party consult/verify pass, treat worker outputs as
    scratch evidence only, and allow only one canonical plan writer. It must
    include a run directory, file lock or equivalent single-writer guard,
    stale-plan digest check before writes, and refusal if the plan changed
    mid-run. It must never invoke `execute`, implement code, or edit repo truth
    outside the canonical plan file. Done when outcomes such as `ready`,
    `needs_input`, `blocked`, and `complete` are machine-readable, and
    `complete` means plan verified for later execute sessions. `specs` exit
    criteria: workflow and repo-surface specs updated. `tests` exit criteria:
    `make validate`, helper dry-run tests, parse/outcome checks, and evals that
    fail side workers mutating canonical plan state or the orchestrator writing
    without lock/stale-plan protection. Commit: one planning-loop commit.

14. Execute-loop verification fan-out: strengthen the provider-specific execute
    runner layer so actual `verify <plan>` invocations can run multiple
    verification angles and synthesize one verdict without changing the generic
    `src/execute/scripts/loop.py` contract. Done when verification cadence
    distinguishes lighter slice-level review from heavier whole-plan review,
    synthesis writes the plan once, closure reruns whole-plan verification
    until a fresh pass yields no new material findings, and final strict
    `verify=pass` still gates completion. `specs` exit criteria: helper
    references and workflow spec updated. `tests` exit criteria: dry-runs or
    evals cover fan-out, synthesis, no duplicate canonical writes, rerun
    closure, and final pass gate. Commit: one execute-wrapper commit.

15. Implemented-plan verification campaign reference: define the wrapper
    contract for verifying already-implemented branches against an immutable
    original `commit:path` plan ref and a mutable living `plans/*.md` execution
    log. Keep verifier shards read-only; one parent orchestrator accepts or
    rejects findings after local confirmation; accepted findings become bounded
    execute fix batches; commits happen only after fix-audit. Do not build a
    full campaign runner until smaller loops prove repeated real need. Done
    when `src/execute/references/verification-campaign.md` records the
    verification matrix schema, wave behavior, shard output requirements,
    accepted-finding fix flow, synthesis-confirmation pass, fix-audit pass,
    synthesis rules, and final PR readiness gates. `specs` exit criteria:
    workflow/helper references updated. `tests` exit criteria: evals fail shard
    mutation, scope weakening, unsupported accepted/rejected findings, missing
    file/line evidence, skipped fix-audit, or final readiness claims without
    evidence. Commit: one campaign-reference commit; runner implementation is a
    later milestone only after evidence supports it.

16. Operations interface: after loop-facing contracts are strong and CLI loops
    have real usage evidence, design the
    operator surface. Tighten machine-facing plan parse rules, event schemas,
    outcomes, pause/resume states, log retention, and locking; extract shared
    operations plumbing for plan indexing, process launching, JSON event
    ingestion, logs, file locks, and run history; then consider one local TUI
    over intake replacement, plan creation/review, planning-loop runs,
    execute-loop runs, blockers, verdicts, diffs, and logs. Keep a Phoenix
    dashboard as a later option only if the TUI proves there is real need.
    `specs` exit criteria: repo-surface and maintenance docs updated. `tests`
    exit criteria: helper-level smoke/dry-run checks where applicable. Commit:
    one ops-contract commit before any UI implementation.

17. Downstream cryptoli refresh and fixture update: after source decisions
    settle, refresh `/home/scrip/Code/cryptoli` without overwriting unrelated
    dirty product work. Sync updated shipped skills into cryptoli's
    `.agents/skills/`, update cryptoli `AGENTS.md` and `specs/` to the stricter
    repo-truth boundary, add or preserve cryptoli-specific adjunct skills
    according to the final source stack, run a 6+1 specs-agent campaign, and
    refresh `evals/fixtures/cryptoli.json` if the live repo is the better eval
    target. Preserve the current grounding until refreshed: pinned fixture
    commit `5c634bd5018eba27b5d6881116d5328e287c03c3` from April 16, 2026; the
    local cryptoli worktree was dirty on May 6, 2026 with schema, backend
    service/test, migration, plan, and `specs/data-model.md` changes. The 6+1
    cryptoli specs audit angles are backend, frontend, admin,
    data/auth/realtime, testing, ops/deploy, plus one orchestrator writer.
    Require explicit user approval before isolated skill/spec refresh on a
    dirty tree, and record refreshed cryptoli commit SHA and fixture pin
    changes. `specs` exit criteria: cryptoli `AGENTS.md` and `specs/` reflect
    code reality and no-planning spec boundary. `tests` exit criteria: relevant
    cryptoli checks or explicitly documented blocked checks, plus source repo
    fixture validation. Commit: separate cryptoli repo commit(s) and one source
    repo fixture commit if fixture changes.

18. Final whole-plan verification and cleanup: run a strict plan review after
    all milestones are complete. Confirm shipped docs, specs, skills, helpers,
    evals, downstream sync behavior, and cryptoli fixture state are aligned.
    Correct `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
    `Outcomes / Retrospective`. Done when `make validate` passes, no required
    follow-up is missing from this plan, and any remaining non-blocking risks
    are explicitly recorded. `specs` exit criteria: all touched source specs
    have current "Last verified" dates or equivalent status updates when the
    repo convention requires them. `tests` exit criteria: final validation and
    focused helper/eval checks. Commit: final docs/eval cleanup commit if
    needed.

## Detailed Carry-Forward Requirements

These requirements preserve `TODO.md` details that must not be lost during
execution.

Provider-agnostic runtime boundary:

- Audit `src/*/SKILL.md`, `src/*/README.md`, `agents/openai.yaml`,
  `AGENTS.md`, README, specs, helper references, and eval assertions for
  required provider-native features.
- Evals must fail when a skill or wrapper requires provider-native plugins,
  built-in skills, MCPs, rules, hooks, subagents, auto-memory, native
  background workers, or hidden client state.
- Scripted skill use must invoke normal skill contracts with explicit prompts,
  repo paths, plan paths, permission boundaries, output contracts, logs, and
  exit-code handling.
- Provider wrappers may translate generic run specs into provider CLI commands,
  but workflow semantics must remain in skills and repo-owned contracts.

Dependency and external grounding:

- Identify exact local dependency versions from manifests, lockfiles, generated
  clients, vendored code, installed packages, or build config before choosing
  dependency-sensitive implementation targets.
- Prefer exact local artifacts first: `node_modules`, `site-packages`, vendored
  code, generated SDK files, type definitions, package tarballs, or source
  distributions.
- If local artifacts are absent or insufficient, inspect official upstream
  source at the exact tag, commit, release archive, or package version.
- Read implementation, tests, types, fixtures, and official examples for the
  version under review.
- Compare source behavior with versioned docs, API references, changelogs,
  release notes, and migration guides; record conflicts as risks.
- Distinguish current code behavior from public contract support; avoid private
  internals unless the task accepts that tradeoff.
- For upgrade/latest work, compare current repo version, target version, and
  latest available version.
- Treat community posts, issue threads, snippets, blogs, and model memory as
  clues only, never primary evidence for current API behavior.

Standards, trigger, compatibility, and eval portability:

- Check whether the local validation surface rejects unknown or missing
  frontmatter too aggressively.
- Test one strict cross-client or reference-validator path before settling
  `argument-hint` portability.
- Use should-trigger and near-miss should-not-trigger evals, not wording-only
  reviews.
- Check whether simple bounded requests under-trigger because descriptions
  overemphasize repo-local mechanics.
- Record `consult` / `plan` / `execute` boundary cases that are easy for
  clients to mis-trigger.
- Decide whether all six skills share one compatibility baseline or whether
  `execute`, `specs`, `tests`, and `verify` need stricter requirements.
- Document the boundary between upstream-aligned eval intent and this repo's
  extra governance around train/validation splits, previous-skill baselines,
  required review, and must-run repetition.
- Decide whether the harness remains validate-and-scaffold-only or grows more
  of the upstream run/grade/review loop.

Specs hard boundary:

- Specs may describe intended system contracts only when grounded in code,
  durable design docs, migrations, schemas, tests, or explicit repo policy.
- If the contract is not grounded, specs must state the current gap as current
  truth instead of smuggling planned work into specs.
- Verification sections in specs should contain commands, grep checks, file
  path checks, or source inspections that confirm the spec against code; they
  must not become task checklists.

Six-skill lean contract:

- `consult`: keep clarification, repo-truth reading, option comparison,
  recommendation, and copy-ready plan carry-forward; compress repeated handoff
  wording; make `Options` conditional for pure current-behavior explanations;
  move multi-angle/fan-out specifics to wrapper documentation.
- `plan`: keep durable-state trigger, one explicit plan path,
  update-in-place behavior, canonical-plan handoff, and decision-complete
  next-slice requirements; move exhaustive section schema and parseability
  details into `assets/plan-template.md` and validators; inspect enough repo
  truth for accuracy without turning planning into implementation research or
  architecture audit; remove duplicate `specs` / `tests` obligation wording.
- `execute`: keep direct and plan-driven entry modes, explicit-plan safety, one
  bounded slice, under-specified-slice stop behavior, mechanical checks,
  required `specs` / `tests` follow-through, plan updates, and `verify`
  handoff; make follow-through slice-scoped so `execute` does not broaden into
  general cleanup; move helper invocation details and continuous-loop quality
  bars to references or provider wrappers.
- `verify`: keep adversarial target typing, findings-first output, verdict
  rubric, strict final completion semantics, and canonical plan updates; check
  test coverage required by repo policy, risk, or plan rather than implying
  every applicable tier must change; condense weak-next-slice and missing-sync
  failure rules; move independent-pass and swarm execution strategy to
  wrapper/helper docs.
- `specs`: keep only bootstrap/sync/gap-close work for `AGENTS.md`,
  `CLAUDE.md` symlink when required, `specs/README.md`, and `specs/*.md`;
  inspect codebase structure only as evidence for truthful updates; remove
  standalone topology mapping, architecture audit, agentic-readiness
  assessment, proportional organization improvements, navigation-map work,
  historical narration, duplicate `audit -> consult -> verify -> apply`
  wording, provider-specific mirror mechanics where not required,
  template-detail bloat better owned by assets, and repo-readiness
  certification claims.
- `tests`: keep bootstrap/sync/gap-close triggers, test-topology discovery,
  smallest credible layer selection, existing helper reuse, blocked-layer
  reporting, and meaningful checks; remove the `specs` analogy, broad
  recent-change inference in dirty worktrees, duplicate internal meta-process,
  and mandates to update every applicable existing layer in favor of risk- and
  policy-required layers.

Planning and verification automation:

- Planning-loop fan-out must be deterministic about how many consult/verify
  angles run and which angles are expected.
- The planning-loop orchestrator must run its own consult/verify effort before
  synthesizing side-agent input.
- Follow-up clarifications and changed decisions are deltas against the same
  explicit plan file; reopen only affected milestones.
- Execute-loop verification fan-out must synthesize one verdict and should
  rerun whole-plan verification after fixes until a fresh pass yields no new
  material findings, then still require final strict `verify=pass`.

Implemented-plan verification campaign:

- The immutable original contract is a required `commit:path` plan ref.
- The mutable living execution log is the current explicit `plans/*.md` file.
- Living-plan edits must not silently weaken original scope unless a
  repo-truth-backed and previously verified scope change is recorded.
- Shard agents are read-only and write scratch reports only.
- Accepted findings become bounded `execute` fix batches; verifier shards
  remain separate from fixer workers.
- Require synthesis confirmation before fixes and fix-audit before commit or
  final readiness.

Adjunct skills:

- `grill` must ask one question at a time, include a recommended answer, inspect
  code/specs before asking when possible, and preserve plan carry-forward.
- `grill` is not a replacement for `consult`, does not create implementation
  plans unless handing off to `plan`, and does not write `specs/` directly by
  default.
- `improve` candidates must be evidence-backed, numbered, file-referenced, and
  user-selected before design; avoid speculative refactor backlogs.
- `caveman` affects communication only and must not weaken findings, plan
  sections, checks, durable truth, commands, errors, code comments, docs,
  plan files, tests, or safety warnings.
- `caveman` must be added under `src/caveman/` as a permanent citizen of this
  source repo; only its downstream default-install status remains to be
  decided.

Cryptoli refresh:

- Current fixture pin: `5c634bd5018eba27b5d6881116d5328e287c03c3`, committed
  April 16, 2026.
- Current local repo path: `/home/scrip/Code/cryptoli`.
- Current dirty-worktree categories observed on May 6, 2026: schema, backend
  service/test, migration, plan, and `specs/data-model.md`.
- Cryptoli 6+1 specs audit angles: backend, frontend, admin,
  data/auth/realtime, testing, ops/deploy, plus one orchestrator writer.
- Do not refresh skills/specs on the dirty tree without explicit user approval;
  record refreshed commit SHA and fixture pin changes.

## Verification

Planned proof points:

- Run two consultation agents and two verification agents against `TODO.md`
  and this plan before deleting `TODO.md`.
- Run `make validate` after plan creation and after `TODO.md` deletion.
- Run `git diff --check` before commit when practical.
- Run targeted `rg` checks after milestones that change provider-boundary,
  specs-boundary, or helper naming language.
- For helper/script milestones, run `python3 <script> --help` and dry-run
  checks where the helper supports them.
- For eval/harness changes, run `python3 evals/scripts/harness.py validate`
  directly or through `make validate`.
- For downstream cryptoli sync, inspect cryptoli dirty worktree first and avoid
  unrelated product changes.

Initial review gate for this conversion:

- [2026-05-06] Consult agent 1 coverage review: fail before patch. Required
  expanding TODO detail for provider-boundary evals, dependency grounding,
  standards/trigger checks, specs guardrails, per-skill lean-contract edits,
  planning/verify fan-out, adjunct skills, and cryptoli facts.
- [2026-05-06] Verify agent 1 plan-skill and TODO coverage review: fail before
  patch. Required preserving missing TODO details before deleting `TODO.md`.
- [2026-05-06] Verify agent 2 workflow-safety review: pass, with suggestions
  to split later broad milestones and recheck external sources before
  freshness-sensitive work.
- [2026-05-06] Consult agent 2 practical architecture review: pass with risks.
  Accepted safeguards: adjunct registry/sync decision before adding skill dirs,
  minimal worker contract first, lock/stale-plan guard before planning-loop
  writes, split adjunct work, campaign reference before full runner, and TUI
  only after real CLI usage evidence.
- [2026-05-06] Plan patched to address the failing review findings by adding
  `Detailed Carry-Forward Requirements`, splitting adjunct milestones, adding
  lock/stale-plan safeguards, and preserving cryptoli grounding details.
- [2026-05-06] Re-review round: consult coverage review passed; consult
  practical architecture review passed; verify workflow-safety review passed;
  verify plan/TODO coverage review failed on `caveman` being weakened from
  "permanent citizen" to optional/local-only. Plan patched to preserve
  `caveman` as a permanent source-repo adjunct skill while leaving only
  downstream default-install status as the decision.
- [2026-05-06] Focused final re-verification of the `caveman` patch passed.
  `TODO.md` deletion approved from the final blocking-review perspective.
- [2026-05-06] `TODO.md` deleted after review gate passed and the backlog was
  preserved in this plan.

## Risks

- Wrapper scripts could become hidden workflow truth. Mitigation: keep skills
  as semantic owners and wrappers as optional adapters with observable,
  replaceable contracts.
- Fan-out could become expensive, noisy, or performative. Mitigation: define
  deterministic shard roles, acceptance rules, and cadence before adding TUI or
  dashboards.
- `specs/` could accidentally become another backlog. Mitigation: hard-rule
  specs to durable code/system truth and fail evals when specs contain plans or
  TODOs.
- `grill`, `caveman`, or `improve` could blur the six-skill contract.
  Mitigation: treat them as adjunct skills with explicit non-interference
  evals.
- Milestone commits could mix unrelated work or grant too much authority to
  automation. Mitigation: make commit gates wrapper/operator behavior only and
  stop on unrelated dirty worktree.
- Cryptoli refresh could overwrite dirty product work. Mitigation: wait for a
  stable branch or run an explicitly isolated skill/spec refresh with dirty
  state acknowledged.
- External guidance could drift. Mitigation: recheck upstream sources when
  freshness affects a milestone.
- The overall program could become over-engineered. Mitigation: ship in small
  milestones, verify each milestone, and keep generic helpers thin until there
  is demonstrated operator value.

## Open Questions

- Should `grill` ship by default during downstream sync, or remain optional via
  `SKILL=...`?
- Should `caveman` ship by default, or remain a local optional style skill?
- Should `improve` become `src/improve/`, a `consult` reference/mode, or no
  shipped surface yet?
- Which provider wrapper should be implemented first for the planning loop:
  raw `codex_loop.py` only, or dashboard at the same time?
- Should milestone commit gates live only in provider wrappers, or also in a
  generic operator helper that can be provider-neutral?
- When should cryptoli sync happen relative to its current dirty product
  branch?
- Which real-client smoke path should be used for frontmatter and trigger
  portability?

## Blockers

- None currently.

## Progress

- [x] Milestone 1: Intake conversion and TODO removal
- [ ] Milestone 2: Provider-agnostic runtime boundary and generic worker contract
- [ ] Milestone 3: Repo truth and specs hard boundary
- [ ] Milestone 4: Six-skill lean contract and Karpathy quality bars
- [ ] Milestone 5: Dependency-sensitive external grounding
- [ ] Milestone 6: Standards alignment, compatibility metadata, trigger ergonomics, and eval portability
- [ ] Milestone 7: Milestone commit cadence
- [ ] Milestone 8: Adjunct skill governance and install-surface decision
- [ ] Milestone 9: Grill adjunct skill
- [ ] Milestone 10: Caveman adjunct skill
- [ ] Milestone 11: Improve architecture adjunct decision
- [ ] Milestone 12: Shared per-skill script convention
- [ ] Milestone 13: Planning-only loop
- [ ] Milestone 14: Execute-loop verification fan-out
- [ ] Milestone 15: Implemented-plan verification campaign reference
- [ ] Milestone 16: Operations interface
- [ ] Milestone 17: Downstream cryptoli refresh and fixture update
- [ ] Milestone 18: Final whole-plan verification and cleanup

## Decision Log

- [2026-05-06] Converted `TODO.md` backlog into this plan path so future work
  has one canonical plan-driven state file and `TODO.md` can be removed after
  the requested review gate passes.
- [2026-05-06] Kept the six workflow skills as the core semantic contract and
  treated `grill`, `caveman`, and possible `improve` as adjunct skills so they
  cannot override `consult`, `plan`, `execute`, `verify`, `specs`, or `tests`.
- [2026-05-06] Chose `src/plan/scripts/loop.py` naming for the planning loop to
  mirror execute's helper naming and avoid redundant `plan_loop.py` naming
  under the plan skill directory.
- [2026-05-06] Kept commit authority out of base skills; milestone commit gates
  belong in wrapper/operator flows and verification-campaign flows.
- [2026-05-06] Deleted `TODO.md`; this plan is now the canonical task record
  for the workflow automation architecture backlog.

## Discoveries

- [2026-05-06] Existing repo truth already separates `AGENTS.md`,
  `specs/`, and `plans/*.md`, but `TODO.md` carried durable future workflow
  state that now belongs in this plan.
- [2026-05-06] `src/specs/SKILL.md` already says specs are not task plans or
  TODO lists, but future work should make that boundary stricter and enforce it
  through assets and evals.
- [2026-05-06] Only `execute` ships helper scripts today; per-skill scripts are
  future optional amplification surfaces, not current workflow truth.
- [2026-05-06] Local `/home/scrip/Code/cryptoli` exists and has a dirty product
  worktree, so downstream sync needs explicit dirty-worktree handling.

## Outcomes / Retrospective

- Pending.
