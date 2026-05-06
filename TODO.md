# TODO

Follow-up items from the April 22, 2026 comparison between this repo's
six-skill workflow and the official Agent Skills docs, plus the May 6, 2026
workflow synthesis around planning automation, adjunct skills, specs hardening,
and downstream cryptoli refresh.

## Source Grounding

This note is grounded in a point-in-time review on April 22, 2026.
Re-evaluate these items if the upstream Agent Skills format or guidance changes,
or if this repo materially changes its own workflow contract.

Upstream sources reviewed:

- `https://agentskills.io/home`
- `https://agentskills.io/what-are-skills`
- `https://agentskills.io/specification`
- `https://agentskills.io/skill-creation/best-practices`
- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
- `https://agentskills.io/skill-creation/using-scripts`
- `https://agentskills.io/client-implementation/adding-skills-support`

Additional May 6, 2026 sources reviewed:

- `https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md`
- `https://github.com/mattpocock/skills`
- `https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me`
- `https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs`
- `https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture`
- selected Matt Pocock engineering skills for surrounding patterns:
  `diagnose`, `tdd`, `to-issues`, and `zoom-out`

Local repo sources reviewed:

- `AGENTS.md`
- `README.md`
- `specs/workflow-contract.md`
- `specs/evaluation-harness.md`
- `src/*/SKILL.md`
- `src/execute/scripts/loop.py`
- `src/specs/assets/AGENTS.md`
- `src/specs/assets/specs/README.md`
- `src/specs/assets/specs/spec-template.md`
- local `/home/scrip/Code/cryptoli/AGENTS.md` and
  `/home/scrip/Code/cryptoli/specs/`

When revisiting this file later, confirm whether:

- the published Agent Skills spec still treats `name` and `description` as the
  core discovery fields and still documents the same optional frontmatter set
- upstream trigger guidance still centers on description quality and
  progressive disclosure
- upstream script guidance still assumes non-interactive execution and
  structured, agent-friendly interfaces
- upstream evaluation guidance still favors repeated runs, validation splits,
  baselines, and human review
- this repo still intends to optimize for coding-agent environments rather than
  generic drop-in marketplace portability

## May 6, 2026 Final Synthesis

This is the current intake decision before converting the backlog into one or
more explicit plan files.

Core workflow shape:

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

Repo truth direction:

- `AGENTS.md` should be stronger, shorter, and more operational.
- `specs/` must explain durable code and system truth only. Specs must not
  contain task plans, task lists, future-work backlogs, milestone status, or
  implementation TODOs.
- The `specs` skill and bootstrap assets must enforce that boundary.
- A mature repo should preserve its house style, but the generic assets must
  make the no-planning/no-TODO rule explicit.
- Use repo-owned specs as the default durable language layer. `CONTEXT.md` and
  ADRs may be optional target-repo conventions, not required workflow truth.

Automation direction:

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

Planning loop direction:

- Ship a planning-only loop under `src/plan/scripts/loop.py`.
- It creates or checkpoints one explicit canonical plan path early, before
  brainstorming exhausts session context.
- It may launch read-only `consult` and `verify` workers; only the orchestrator
  writes the canonical plan.
- It must never invoke `execute`, implement code, or edit repo truth outside
  the canonical plan file.
- `complete` means the plan is verified and ready for later execute sessions,
  not that implementation is complete.

Milestone and commit direction:

- Plans should be smaller, with bounded milestones that can be executed and
  verified one at a time.
- A coherent completed milestone should normally become one commit after:
  execution, checks, verification, plan evidence updates, and unrelated dirty
  worktree review.
- Base skills should not auto-commit. Commit gates belong in wrapper/operator
  flows and verification-campaign flows.

Specs-agent campaign direction:

- Use "6+1 specs agents" as orchestration topology: six read-only specs audit
  angles plus one orchestrator that writes `AGENTS.md` and `specs/`.
- For this source repo, suggested angles are workflow contract, repo surface,
  eval harness, skill payloads, helper/scripts, and downstream sync/assets.
- For cryptoli, suggested angles are backend, frontend, admin,
  data/auth/realtime, testing, and ops/deploy.
- Read-only agents must write scratch reports only; the orchestrator owns the
  canonical repo-truth edits.

Downstream direction:

- Both this `skills` repo and `/home/scrip/Code/cryptoli` need repo-truth and
  skill refresh after the source workflow decisions settle.
- Cryptoli currently has a dirty product worktree; downstream sync should wait
  for that branch to stabilize or be done as an explicitly isolated skill/spec
  refresh with dirty-worktree risk acknowledged.
- After source changes land, refresh cryptoli's installed skills, `AGENTS.md`,
  and `specs/`, then refresh the pinned cryptoli eval fixture if the fixture is
  no longer representative.

Recommended conversion order:

1. Finalize this `TODO.md` as the intake backlog.
2. Convert the selected architecture slice into one explicit plan file.
3. First plan milestone: provider-agnostic runtime boundary and generic
   worker/session contract.
4. Second: harden `AGENTS.md`, `specs/`, and the `specs` skill/assets.
5. Third: trim the six skills and add quality-bar guidance.
6. Fourth: add `grill` and settle `caveman` status.
7. Fifth: define shared per-skill script conventions.
8. Sixth: ship the planning-only loop and provider wrappers.
9. Seventh: strengthen execute verification fan-out and verification campaign.
10. Eighth: sync/update cryptoli.

## Provider-Agnostic Runtime Boundary

- [ ] Promote a strict provider-agnostic runtime boundary across the repo.
  Fundamental note:
  - this source repo, the current six skills, and future skills must not rely on
    any provider's built-in workflow features as required primitives
  - provider features such as built-in skills, plugins, MCPs, rules, hooks, plan
    modes, auto-memory, native subagents, background workers, or client-specific
    agent APIs may be used only as optional local conveniences behind adapters
  - direct-chat skill use must remain self-sufficient: each skill should do one
    focused job accurately from repo truth, explicit user input, and the normal
    tools available to the agent session
  - scripted skill use must invoke the same skill contracts with explicit
    prompts, repo paths, plan paths, permission boundaries, output contracts,
    logs, and exit-code handling rather than depending on hidden provider state
  - helper and wrapper scripts are authored in this source repo, then synced
    into downstream repos and run from the downstream install surface such as
    `<repo>/.agents/skills/<skill>/scripts/...`; they must resolve repo paths,
    skill paths, assets, references, and logs from that installed layout rather
    than assuming execution from this source repo
  - "multi-agent" or "fan-out" in this repo should mean repo-owned wrappers
    launching isolated provider sessions or processes through adapters, with
    clear role prompts and file-backed inputs/outputs
  - provider-specific wrappers under `src/execute/scripts/providers/` may
    translate generic run specs into provider CLI commands, but they must not
    move workflow semantics into provider-native subagent APIs, plugins, hooks,
    rules, MCPs, or other client-specific surfaces
  - if a provider-native feature is useful locally, keep it replaceable and
    require a process-based fallback with the same observable contract
  Follow-through:
  - define a generic worker/session launch contract for wrappers: command
    template, working directory, prompt payload, skill invocation, read/write
    policy, timeout, log path, structured output schema, and exit-code mapping
  - define installed-layout path rules for wrappers so source paths under
    `src/<skill>/...` and downstream paths under
    `.agents/skills/<skill>/...` stay equivalent after `make sync`
  - replace ambiguous `subagent` wording in repo docs with generic terms such
    as `worker`, `shard`, `session`, or `provider process` unless discussing a
    provider feature explicitly as non-required
  - audit `src/*/SKILL.md`, `README.md`, `AGENTS.md`,
    `specs/workflow-contract.md`, helper references, and eval assertions so
    they say provider features are optional adapters, not workflow truth
  - add eval cases that fail when skills or wrappers require provider-native
    plugins, built-in skills, MCPs, rules, hooks, subagents, auto-memory, or
    other hidden client state

## Dependency And External Grounding

- [ ] Design and ship dependency-sensitive source grounding rules across the
  six-skill workflow.
  The goal is to stop agents from relying on training-memory assumptions when
  work depends on current library, framework, SDK, API, security, deployment,
  or "best practice" behavior.
  Follow-through:
  - require agents to identify the repo's actual dependency version from local
    manifests, lockfiles, generated clients, vendored source, installed
    packages, or build configuration before choosing an implementation target
  - prefer the exact shipped artifact first when available, such as
    `node_modules`, `site-packages`, vendored code, generated SDK files, type
    definitions, package tarballs, or source distributions
  - when local artifacts are absent or insufficient, inspect the official
    upstream source at the exact tag, commit, release archive, or package
    version; clone locally only when that is more reliable than remote
    inspection
  - read implementation, tests, types, fixtures, and official examples for the
    version under review so behavior and supported usage are grounded in actual
    evidence
  - compare source behavior with versioned official docs, API references,
    changelogs, release notes, and migration guides; record conflicts as risks
    rather than silently choosing the convenient source
  - distinguish "what the code currently does" from "what the public contract
    supports"; avoid depending on private internals unless the task explicitly
    accepts that tradeoff
  - for upgrade or latest-version work, compare current repo version, target
    version, and latest available version instead of blindly applying latest
    docs to the pinned repo state
  - label community posts, issue threads, search snippets, blogs, and model
    memory as supporting clues only; they must not be the primary evidence for
    current API behavior
  - add a plan-template `External Grounding` section that records freshness
    requirement, local version evidence, official source/docs checked, accessed
    date, decision impact, recheck trigger, and unresolved gaps
  - update `consult`, `plan`, `execute`, `verify`, `specs`, and `tests` so this
    grounding is required when dependency freshness materially affects safe
    planning, implementation, verification, repo truth, or test truth
  - add eval cases that fail when agents make dependency-sensitive claims
    without exact-version evidence, source inspection, and docs/source
    comparison

## Standards Alignment

- [ ] Revisit `argument-hint` in skill frontmatter.
  The local harness currently requires `argument-hint`, but the published
  Agent Skills spec documents `name`, `description`, `license`,
  `compatibility`, `metadata`, and `allowed-tools` instead.
  Decide whether to:
  - make `argument-hint` optional in the local harness
  - move it under `metadata`
  - or keep it as a documented local extension with an explicit portability
    note for strict validators and non-local clients
  Follow-through:
  - check whether the current local validation surface rejects unknown or
    missing frontmatter fields too aggressively
  - test one strict cross-client or reference-validator path so this decision
    is grounded in actual compatibility behavior rather than assumption

## Trigger Ergonomics

- [ ] Tighten skill descriptions toward upstream trigger guidance.
  Review whether each skill description should more directly express
  user intent in "Use this skill when..." terms and rely less on repo-local
  concepts such as `plans/`, `AGENTS.md`, and `specs/` in the short
  discovery-facing description.
  Follow-through:
  - run per-skill trigger evals with should-trigger and near-miss
    should-not-trigger prompts rather than only revising descriptions by eye
  - check whether simple bounded requests under-trigger because the current
    descriptions overemphasize internal workflow mechanics instead of user
    intent
  - record any boundary cases where `consult` vs `plan` vs `execute` are
    especially easy for clients to mis-trigger

## Repo Truth And Specs Hard Boundary

- [ ] Improve `AGENTS.md` and `specs/` so repo truth is easier for fresh agents
  to apply without confusing durable system truth with task planning.
  Core rule:
  - `AGENTS.md` owns concise repo-wide operational truth: reading order,
    commands, boundaries, skill inventory, git conventions, and non-obvious
    workflow rules
  - `specs/` owns durable code, domain, architecture, operational, and testing
    truth by topic
  - `specs/` must not contain task plans, task lists, future-work backlogs,
    implementation TODOs, milestone state, active blockers, or status prose
    that belongs in `plans/*.md`
  - specs may describe intended system contracts only when those contracts are
    grounded in code, durable design docs, migrations, schemas, tests, or
    explicit repo policy; otherwise they must state the gap as current truth
    rather than smuggling planned work into specs
  - verification sections in specs should contain commands, code-path checks,
    or source inspections that confirm the spec against the repo; they should
    not become task checklists
  Follow-through:
  - update `AGENTS.md`, `specs/README.md`, `specs/workflow-contract.md`,
    `specs/repo-surface.md`, `README.md`, `docs/maintenance.md`, and
    `docs/sources.md` to reflect the stricter boundary
  - update `src/specs/SKILL.md` so it bootstraps, syncs, and repairs repo truth
    without producing readiness certifications, architecture-audit backlogs, or
    planning content
  - update `src/specs/assets/AGENTS.md`,
    `src/specs/assets/specs/README.md`, and
    `src/specs/assets/specs/spec-template.md` so downstream repos inherit the
    same hard boundary
  - add eval cases that fail when the `specs` skill writes TODOs, milestones,
    execution plans, stale desired behavior, or broad repo-readiness claims
    into `AGENTS.md` or `specs/`
  - use a 6+1 specs-agent campaign for broad syncs: six read-only audit angles
    plus one orchestrator that writes canonical `AGENTS.md` and `specs/`

## Six-Skill Lean Contract

- [ ] Trim and sharpen the six source skills while preserving direct-chat
  usefulness.
  The goal is for each `src/*/SKILL.md` to remain fully useful when invoked
  directly in a normal agent session, while optional loop wrappers amplify the
  same skill contract with fan-out, retries, logs, dashboards, and exit-code
  transport.
  Contract boundary:
  - skill contracts own task semantics: trigger boundaries, repo evidence to
    inspect, allowed canonical writes, output shape, verdict rules, and
    required follow-through
  - a skill may inspect files outside its owning write surface as evidence, but
    it should only create or update canonical artifacts in its own domain
  - wrapper/helper layers own execution strategy: number of agents, side-agent
    roles, parallelism, cadence, scratch artifacts, log retention, dashboards,
    JSON events, and provider-specific invocation details
  - wrapper output is supporting evidence only; canonical task truth remains in
    repo files, especially the explicit plan file for plan-driven work
  - direct chat must not require a loop helper; wrappers may deepen scrutiny
    but must not redefine what the skill means
  - keep `verify` plan writes as core behavior: when verifying plan-driven
    work, `verify` updates the same explicit plan with findings, verdict,
    blockers, progress corrections, and repairable follow-up slices
  - replace exact subagent/fan-out wording inside skills with portable scrutiny
    language such as using stronger checks, a fresh pass, or available
    independent review when risk warrants it; deterministic swarm policy
    belongs to the loop wrapper
  - remove generic boilerplate across all skills and keep only skill-specific
    inputs, outputs, and quality gates; a skill may inspect surrounding repo
    truth to avoid false claims, but must not turn that inspection into a
    second job or broaden writes beyond its domain
  Follow-through:
  - `consult`: keep clarification, repo-truth reading, option comparison,
    recommendation, and copy-ready plan carry-forward; compress repeated
    handoff wording; make output headings flexible enough for concise direct
    chat; make `Options` conditional when the request is pure current-behavior
    explanation; move multi-angle/fan-out specifics to wrapper documentation
  - `plan`: keep durable-state trigger, one explicit plan path, update-in-place
    behavior, canonical-plan handoff, and decision-complete next-slice
    requirements; move exhaustive section schema and parseability details into
    `assets/plan-template.md` and validators; inspect enough repo truth to
    make the plan accurate without turning planning into implementation
    research or architecture audit; remove duplicate `specs` / `tests`
    obligation wording
  - `execute`: keep direct and plan-driven entry modes, explicit-plan safety,
    one bounded slice, under-specified-slice stop behavior, mechanical checks,
    required `specs` / `tests` follow-through, plan updates, and `verify`
    handoff; make the follow-through boundary explicit so `execute` completes
    only slice-required `specs` / `tests` updates and does not broaden into
    general cleanup; move helper invocation details and continuous-loop quality
    bars to `references/optional-helper.md` or provider wrappers
  - `verify`: keep adversarial target typing, findings-first output, verdict
    rubric, strict final completion semantics, and canonical plan updates;
    check test coverage required by repo policy, risk, or plan rather than
    implying every applicable test tier must change; condense repeated
    weak-next-slice and missing-sync failure rules; move independent-pass and
    swarm execution strategy to wrapper/helper docs
  - `specs`: keep only bootstrap/sync/gap-close work for `AGENTS.md`,
    `CLAUDE.md` symlink when required by repo convention, `specs/README.md`,
    and `specs/*.md`; inspect codebase structure only as evidence for truthful
    updates; remove standalone topology mapping, codebase architecture audit,
    agentic-readiness assessment, proportional organization improvements,
    navigation-map work, historical narration, duplicate internal
    `audit -> consult -> verify -> apply` wording, provider-specific mirror
    mechanics where not required, template-detail bloat better owned by assets,
    and output claims that certify the whole repo as ready for
    planning/execution instead of reporting changed truth files and remaining
    repo-truth gaps for the named scope
  - `tests`: keep bootstrap/sync/gap-close triggers, test-topology discovery,
    smallest credible layer selection, existing helper reuse, blocked-layer
    reporting, and meaningful checks; remove the `specs` analogy, broad
    recent-change inference in dirty worktrees, duplicate internal
    meta-process, and the mandate to update "every applicable existing layer"
    in favor of risk- and policy-required layers
  - update `src/*/README.md`, `agents/openai.yaml`, specs, README, and eval
    assertions when skill contract wording changes so shipped surfaces stay
    aligned
  - add or update eval cases that fail when skills become wrapper-dependent,
    over-trigger, skip canonical plan writes, over-prescribe broad test/spec
    work, or let wrapper artifacts replace repo truth

## Milestone Commit Cadence

- [ ] Bake smaller plans and milestone commit gates into plan-driven workflow
  guidance without making base skills auto-commit.
  Contract boundary:
  - plans should be small enough that each milestone can be executed, checked,
    verified, and reasoned about independently
  - each milestone should define a clear done condition, owning paths, required
    `specs` / `tests` exit criteria, and the intended commit boundary when
    commit cadence applies
  - a completed milestone should normally become one coherent commit only after
    execution, mechanical checks, required `specs` / `tests` follow-through,
    `verify`, and plan evidence updates
  - base skills should not auto-commit because that mixes workflow semantics
    with repository authority; commit gates belong in wrapper/operator flows or
    verification-campaign flows
  - if the worktree contains unrelated dirty changes, the milestone commit gate
    must stop or require explicit user approval rather than sweeping unrelated
    work into the commit
  Follow-through:
  - update `src/plan/SKILL.md` and `src/plan/assets/plan-template.md` so plans
    can record intended commit boundaries and post-verify commit evidence
    without turning every task into an overbearing process
  - update `src/execute/SKILL.md` and `src/verify/SKILL.md` so they preserve
    milestone evidence needed for a later commit gate, while still avoiding
    direct commit authority
  - update execute helper or provider wrapper references to describe the
    optional milestone commit gate, dirty-worktree handling, and commit SHA
    recording
  - add eval cases that fail when milestones are too broad, commit unrelated
    work, skip verification before commit, or leave no commit evidence in the
    plan when commit cadence was required

## Compatibility Metadata

- [ ] Add explicit `compatibility` metadata where environment assumptions
  matter.
  The workflow assumes repo access and common local tools such as `python3`,
  `make`, and `rg`. Capture those assumptions using the standard compatibility
  field where that improves cross-client portability.
  Follow-through:
  - decide whether all six skills share one common compatibility baseline or
    whether `execute`, `specs`, `tests`, and `verify` need stricter tool and
    filesystem requirements than `consult`
  - document that these skills are optimized for coding-agent environments
    with repo truth files, writable working trees, and non-interactive shell
    access

## Eval Portability

- [ ] Decide how much of the shared eval harness should be presented as
  repo-local policy versus generic Agent Skills interoperability.
  The current harness is stronger than the upstream baseline, but it is also
  more custom. Document the mapping between local eval governance and the
  standard `evals/evals.json` expectations so downstream users understand what
  is portable versus repo-specific.
  Follow-through:
  - make the boundary explicit between upstream-aligned eval intent and this
    repo's additional governance around train/validation splits, previous-skill
    baselines, required review, and must-run repetition
  - decide whether to keep the current validate-and-scaffold-only harness as
    the long-term contract or grow optional tooling for more of the upstream
    run/grade/review loop
  - add at least one real-client smoke path that exercises trigger behavior and
    frontmatter portability outside the local happy path

## Workflow Automation

- [ ] Design and ship a planning-only loop for large task planning work.
  The loop should automate the current manual
  `consult -> plan -> verify(plan)` workflow while staying file-backed and
  resumable from the explicit `plans/*.md` path.
  Clear orchestration note:
  - the loop is planning-only: it must not invoke `execute`, implement
    code, or modify repo truth outside the canonical plan file
  - create the explicit canonical plan path early, before brainstorming can
    consume the session context, and checkpoint emerging facts into that same
    file as synthesis proceeds
  - spawn multiple `consult` and `verify` angles rather
    than rely on a single pass
  - the orchestrator should also run its own `consult` / `verify` effort so it
    has a first-party view of the problem before synthesizing side-agent input
  - those agent outputs should be treated as inputs to one synthesizing
    orchestrator agent
  - only that orchestrator should update the canonical plan file
  - side `consult` and `verify` agents are read-only inputs to synthesis; they
    must write to logs or scratch copies only, not the canonical plan file
  Follow-through:
  - ship the generic helper under `src/plan/scripts/loop.py`, mirroring the
    execute helper naming convention
  - ship provider-specific wrappers under `src/plan/scripts/providers/`, such
    as `codex_loop.py` and, if there is a real planning operator need,
    `codex_loop_dashboard.py`
  - add a reference contract under `src/plan/references/optional-helper.md`
    that defines invocation, installed-layout path resolution, scratch logs,
    structured reports, outcomes, and exit-code mapping
  - define how clarifications, approvals, and changed decisions pause the loop
    and resume against the same plan path
  - define explicit loop outcomes such as `ready`, `needs_input`, `blocked`,
    and `complete` so pause/resume behavior stays machine-readable instead of
    hiding in prose
  - define `complete` as "the plan is verified and ready for later execute
    sessions", not "the planned implementation work is complete"
  - treat follow-up clarifications and changed decisions as deltas against the
    same explicit plan file, reopening only the affected milestones instead of
    creating replacement plans or restarting broad research
  - define the default consult/verify fan-out shape and how it scales for
    larger work without turning the generic workflow contract provider-specific
  - make the wrapper-owned swarm policy deterministic about how many consult or
    verify angles run and which ones are expected, rather than leaving that to
    ad hoc model behavior

- [ ] Strengthen execute-loop verification fan-out in the provider-specific
  runner layer.
  The existing generic execute loop can stay thin, but the actual
  `verify <plan>` implementation should be upgraded to run multiple
  verification angles and synthesize them before returning one verdict.
  Clear orchestration note:
  - make the execute loop spawn more verification agents in the same general
    way the future planning-only loop should spawn multiple consult/verify
    angles
  - the orchestrator should also run its own `verify` effort so it is not only
    relaying swarm output when updating the canonical plan and verdict
  - feed those independent syntheses to one orchestrator agent that updates
    the plan once and returns the final verdict code back to the loop
  Follow-through:
  - keep the generic `src/execute/scripts/loop.py` contract unchanged
  - put multi-agent fan-out and synthesis in provider-specific wrappers or
    optional helper layers rather than in the provider-agnostic skill contract
  - define verification cadence so lighter slice-level review and heavier
    whole-plan swarm passes happen at predictable points instead of every pass
    using the same maximal fan-out
  - define closure explicitly: after fixes, rerun the whole-plan verify swarm
    until a fresh pass yields no new material findings, then still require the
    final strict `verify=pass` completion gate

- [ ] Design and ship an implemented-plan verification campaign wrapper for
  already-implemented branches.
  The campaign should make the current manual "verify an implemented branch
  against the original plan, fix real issues, and leave the PR ready" prompt a
  native optional workflow without bloating the `verify` skill itself.
  Contract boundary:
  - the campaign is an orchestrated wrapper over lean skills, not a new
    provider-agnostic skill contract
  - the immutable original contract is a required `commit:path` plan ref
  - the mutable living execution log is the current explicit `plans/*.md` file
  - the original contract defines required scope unless the living plan records
    an explicit, repo-truth-backed, previously verified change in scope
  - read-only shard agents use `verify` and write scratch reports only, not
    code, commits, or canonical plan edits
  - one synthesizing orchestrator dedupes shard findings, locally checks each
    candidate issue before accepting it, and performs the canonical plan update
  - accepted findings become bounded `execute` fix batches; use `consult` for
    disputed architecture judgment and `tests` when coverage or test topology
    is unclear
  - commit and push coherent verified fix batches using the target repo's
    commit style
  Follow-through:
  - add a reference contract such as
    `src/execute/references/verification-campaign.md`
  - decide whether generic plumbing belongs in `src/execute/scripts/` and
    provider-specific Codex fan-out belongs under
    `src/execute/scripts/providers/`
  - define the verification matrix schema: scope item, original-plan
    requirement, current-plan notes, owning paths/specs/tests, assigned shard,
    verdict, findings, accepted/rejected status, fix commit, and recheck status
  - define wave behavior for large campaigns so wrappers can queue 30+ shards
    in smaller read-only waves without skipping scope
  - define shard output requirements: pass/fail verdict, real findings with
    file/line references, missing implementation, scope drift, missing or weak
    tests, spec drift, risk level, checks run, and suggested fix scope
  - keep verification shards read-only even when they find real issues; do not
    let finding agents self-fix, because that mixes diagnosis, false-positive
    filtering, mutation, and plan authority in one worker
  - define accepted-finding fix flow: the parent orchestrator creates bounded
    fix briefs from accepted findings, then either fixes locally or dispatches
    separate `execute` worker sessions with explicit write scopes and required
    checks; verifier shards remain separate from fixer workers
  - make the parent orchestrator own final decisions, canonical plan updates,
    fix ordering, commits, pushes, and final readiness verdicts; worker outputs
    are evidence until the parent accepts them with local confirmation
  - require an independent synthesis-confirmation pass after the synthesizing
    orchestrator proposes accepted/rejected findings and before any fixes begin;
    the campaign must not treat first synthesis as authoritative without this
    confirmation
  - define synthesis-confirmation checks: dropped real shard findings, accepted
    false positives, weakened original-plan scope, unsupported severity/status,
    missing file/line evidence, rejected findings without evidence, overbroad
    fix briefs, unsafe plan-update text, and readiness claims that outpace the
    evidence
  - require a fix-audit pass after each accepted fix batch and before commit or
    final readiness when the batch changes code, specs, tests, migrations, or
    plan state
  - define synthesis rules for rejecting false positives with evidence,
    severity ordering, fix batching, rerunning focused verification after fixes,
    and final whole-plan verification
  - define final readiness gates: accepted findings fixed or explicitly
    documented as non-blocking, living plan complete, required checks recorded,
    worktree clean, branch pushed, final commit SHA known, and PR ready for
    review
  - add eval cases that fail when shard agents mutate canonical state, living
    plan edits silently weaken the original contract, findings are accepted
    without local double-check, or final output omits agent matrix, finding
    status, checks, remaining risk, final SHA, or PR readiness

## Downstream Cryptoli Refresh

- [ ] Update the live cryptoli repo after this source repo's workflow decisions
  settle.
  Current grounding:
  - local repo path: `/home/scrip/Code/cryptoli`
  - pinned eval fixture: `evals/fixtures/cryptoli.json`, currently pinned to
    commit `5c634bd5018eba27b5d6881116d5328e287c03c3` from April 16, 2026
  - local cryptoli currently has a dirty product worktree, including schema,
    backend service/test, migration, plan, and `specs/data-model.md` changes
  Refresh scope:
  - sync updated shipped skills into cryptoli's `.agents/skills/`
  - update cryptoli `AGENTS.md` and `specs/` to the stricter repo-truth
    boundary: specs explain durable code/system truth, not plans or TODOs
  - add or preserve cryptoli-specific adjunct skills such as `caveman` and
    `grill` according to the final source-repo stack decision
  - use a 6+1 specs-agent campaign for broad cryptoli repo-truth sync:
    backend, frontend, admin, data/auth/realtime, testing, ops/deploy, plus one
    orchestrator writer
  - refresh the cryptoli fixture manifest when the live repo becomes the better
    representative target for evals
  Safety:
  - do not overwrite or commit unrelated dirty product work during skill/spec
    refresh
  - prefer waiting until the current cryptoli branch stabilizes, unless the
    user explicitly asks for an isolated skill/spec refresh on the dirty tree
  - record any refreshed cryptoli commit SHA and fixture pin changes in the
    relevant plan or eval fixture update

## Operations Interface

- [ ] Design the operator surface after the loop-facing workflow contracts are
  stronger.
  Likely sequence:
  - tighten the machine-facing contracts needed by both loops, including plan
    parse rules, event schemas, outcomes, pause/resume states, log retention,
    and locking
  - add a file-backed `src/plan/scripts/loop.py` for the automated
    `consult -> plan -> verify(plan)` flow described above
  - extract shared operations plumbing for plan indexing, process launching,
    JSON event ingestion, logs, file locks, and run history
  - build one local TUI over TODO intake, plan creation/review,
    planning-loop runs, execute-loop runs, blockers, verdicts, diffs, and logs
  - keep a Phoenix dashboard as a later option only if the TUI proves there is
    real need for richer browsing, multi-session use, or cross-repo operations

## Adjunct Skill Stack

- [ ] Add `grill` as a workflow-adjacent alignment skill.
  Source references:
  - `https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me`
  - `https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs`
  Role:
  - interview the user one question at a time about a plan, design, or
    high-risk implementation direction until the decision tree is resolved
  - provide the recommended answer with each question so the user can accept,
    correct, or sharpen the decision quickly
  - inspect repo code and specs instead of asking when the repo can answer the
    question
  - preserve copy-ready carry-forward for `plan` when the grilling session
    produces durable decisions, risks, rejected options, naming choices, or
    open questions
  - use repo-owned `AGENTS.md` and `specs/` as the durable language and
    decision layer by default; treat `CONTEXT.md` and ADRs as optional
    target-repo conventions only
  Boundaries:
  - `grill` does not replace `consult`; it is a sharper alignment/interview
    mode used when user understanding and decision quality are the risk
  - `grill` does not create implementation plans unless it hands off to `plan`
  - `grill` does not write `specs/` directly unless a future explicit
    repo-truth sync flow defines that behavior; by default it returns
    carry-forward
  Follow-through:
  - add `src/grill/SKILL.md`, `README.md`, `agents/openai.yaml`, and
    `evals/evals.json`
  - decide whether `grill` ships by default in downstream sync or remains an
    optional adjunct skill selected by `SKILL=...`
  - update `AGENTS.md`, `README.md`, `specs/workflow-contract.md`,
    `specs/repo-surface.md`, sync behavior, and managed README wording
  - add eval cases for one-question-at-a-time behavior, code/spec lookup before
    asking, copy-ready plan carry-forward, and non-interference with
    `consult`, `plan`, and `specs`

- [ ] Decide whether to add an `improve` adjunct skill or fold architecture
  improvement into `consult`.
  Source reference:
  - `https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture`
  Candidate behavior:
  - inspect repo truth and code to surface architecture friction and deepening
    opportunities
  - present numbered candidates with files, problem, solution, benefits,
    testing impact, and any conflict with existing repo truth
  - ask the user which candidate to explore before designing interfaces or
    implementation slices
  - hand off chosen work to `grill` for design-tree clarification or to `plan`
    when durable task state is warranted
  Boundaries:
  - do not import provider-specific subagent mechanics as required behavior
  - do not hard-code `CONTEXT.md`, ADRs, or Matt's glossary as required repo
    truth
  - do not generate broad refactor backlogs by default; keep candidates
    evidence-backed and user-selected
  Follow-through:
  - decide whether the repo wants a standalone `src/improve/` skill, a
    `consult` reference/mode, or no shipped surface yet
  - if shipped, add companion files, sync behavior, docs, specs, and evals
  - add eval cases that fail on speculative refactor lists, provider-native
    dependency, or architecture claims without code/spec evidence

## Communication Style Skill

- [ ] Add `caveman` as a permanent citizen in this source repo.
  The goal is to make terse user-facing chat a first-class, guardrailed skill
  that composes with the six-skill workflow without weakening workflow quality.
  Source reference:
  - `https://github.com/mattpocock/skills/blob/main/skills/productivity/caveman/SKILL.md`
  Follow-through:
  - add the source skill payload under `src/caveman/`
  - decide whether `caveman` is a shipped workflow-adjacent skill or a local
    optional style skill, and update `AGENTS.md`, `README.md`, and
    `specs/workflow-contract.md` accordingly
  - add required companion files for the source skill surface, including
    `README.md`, `agents/openai.yaml`, and `evals/evals.json`
  - update downstream sync behavior and managed README wording if `caveman`
    should install alongside the existing shipped skills by default
  - keep the guardrail explicit: `caveman` affects user-facing chat only and
    must not override workflow skill contracts, repo docs, plan files, tests,
    code comments, error text, commands, or safety warnings
  - add trigger and quality eval cases that fail when terse style causes
    missing findings, weak plan sections, skipped checks, or unclear durable
    repo truth
