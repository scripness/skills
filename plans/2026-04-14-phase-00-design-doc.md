# Phase 00: Initial Design Doc

This file preserves the initial design that preceded Phase 01 through Phase 06.
It is the design baseline for the repo, not the active execution artifact and
not the shipped-state index.

Execution status of this design:

- Sections `1-3` were executed through Phase 01.
- Section `4` was executed through Phase 02.
- Sections `5-6` were executed through Phases 03 and 04.
- Section `7` was executed through Phase 05.
- Sections `8-9` were executed through Phase 06.

For current shipped truth, use `AGENTS.md`, `README.md`,
`docs/maintenance.md`, `docs/sources.md`, and the completed phase plan files
under `plans/`.

## 1. Define Repo Contract

- Make this repo the canonical source of six shared core skills:
  `consult`, `plan`, `execute`, `specs`, `tests`, and `verify`.
- Document the workflow model explicitly:
  provider = runtime shell, model = intelligence level, skills = workflow,
  repo files = durable state.
- Document target-repo usage explicitly:
  manually copy the shipped skills from this repo into `.agents/skills/` as the
  cross-client canonical path and invoke them from a normal interactive session
  in any compatible client.
- Keep the source-of-truth skill payloads under repo-root `src/` so the six
  skills remain visually separate from repo docs, plans, eval metadata, and
  maintenance tooling.
- Make the copy boundary explicit:
  `src/<skill>/` in this repo becomes `.agents/skills/<skill>/` in a target
  repo.
- Treat provider-native locations and mirrors as optional compatibility shims
  only; keep `.agents/` and `AGENTS.md` as the authoritative provider-agnostic
  surface.
- Name `AGENTS.md` as the authoritative refresh-workflow contract for this
  repo.
- Use manual copy as the initial target-repo refresh workflow, and keep install
  scripts, subtree wiring, plugins, or other sync helpers optional future
  accelerators rather than baseline requirements.
- Keep provider-specific features additive only; do not require plan mode,
  plugins, auto memory, or other client-only mechanisms.

## 2. Define The Six-Skill Workflow

- `specs`: bootstrap and sync `AGENTS.md` and `specs/` as repo truth, and keep
  `CLAUDE.md` symlinked to `AGENTS.md` only as a thin compatibility mirror
  rather than a second source of truth.
- `specs` should prepare and continuously sync the codebase for the best
  possible agentic work so a fresh agent can understand what is going on
  quickly, navigate the right boundaries, and reach the highest practical
  chance of successful reasoning and execution.
- `specs` should discover the target repo topology instead of assuming a
  single-app layout: monorepo vs single package, `apps/` or `packages/`,
  `src/` vs flat code, service boundaries, generated-output locations, and
  other structure that affects how agents should navigate the codebase.
- `specs` should distinguish source-of-truth structure from generated or vendor
  noise by default: ignore `node_modules/`, build outputs, framework caches,
  vendored dependencies, and other non-owning trees unless the task explicitly
  targets them.
- `tests`: bootstrap and sync all sensible automated test layers as executable
  truth.
- `tests` should discover the target repo's actual test topology instead of
  assuming one stack or one location: per-app or per-package suites, unit,
  integration, e2e, smoke, browser, contract, visual, security, performance,
  and any other existing layers that the repo already uses.
- `tests` should distinguish real test surfaces from generated or vendor noise
  by default: prune `node_modules/`, build outputs, framework caches, and other
  copied artifacts so test-layer discovery reflects the codebase the team
  actually owns.
- `consult`: clarify, research, compare options, and recommend the best next
  move; do not own long-lived task state.
- `plan`: create and maintain living task plans in `plans/*.md` when work
  needs durable state across sessions, milestones, review loops, or
  fresh-session restarts; do not promote based on abstract task size alone.
- `plan`: own task-level plan documents only; `consult` owns clarification and
  recommendation, and `execute` owns implementation from an explicit plan path.
- `execute`: implement bounded work directly when it is still locally clear, or
  implement the next milestone from an explicit plan file in a fresh session.
- `verify`: adversarially verify plans, implementations, claims, and final
  diffs or PRs.
- Keep boundaries sharp and avoid overlap, especially between `consult` and
  `plan`, between `plan` and `execute`, and between `plan` and `specs`.
- Write the provider-agnostic daily loop explicitly:
  brainstorm -> consult -> execute directly or plan -> verify plan -> execute
  -> verify implementation -> sync repo truth.

## 3. Add The Plan Skill

- Create `src/plan/SKILL.md` with a narrow scope: own task-level plan documents
  only.
- Bake the planning protocol into the skill instead of requiring a repo-level
  `PLANS.md`.
- Store live plans under `plans/*.md`; use the default filename format
  `plans/YYYY-MM-DD-short-task-slug.md` and keep each plan updated in place.
- `plan` should create the `plans/` directory when it is missing in a target
  repo.
- Add `src/plan/assets/plan-template.md` for a self-contained living plan.
- Use the default plan filename format:
  `plans/YYYY-MM-DD-short-task-slug.md`.
- Ground the plan template in durable ExecPlan guidance:
  - goal or big picture
  - scope and non-goals
  - repo context and owning code, spec, and test paths
  - milestones
  - verification
  - risks and open questions
  - progress
  - surprises and discoveries
  - decision log
  - outcomes and retrospective
- Make the plan explicitly tell the execution workflow that repo truth and test
  truth must stay current: if implementation changes durable behavior,
  boundaries, operating guidance, or coverage expectations, follow through with
  `specs` and `tests` rather than leaving drift behind.
- Make every plan capture the sync expectations explicitly:
  - owning specs or missing specs to create/update
  - applicable test layers and expected coverage follow-through
  - when `specs` sync is required
  - when `tests` sync is required
- Make the trigger and invocation contract explicit:
  - use `plan` only when the work now needs durable task state
  - do not promote simple lookups, short clarification, or bounded locally
    clear implementation
  - hand off to `execute` and `verify` with one explicit `plans/*.md` path
- Define promotion triggers based on need for durable state, not abstract task
  size.
- Define resumption rules so a fresh session can continue from repo truth plus
  the plan file alone.
- Treat repo-local `PLANS.md` as an optional future override only, not part of
  the baseline workflow.

## 4. Add The Execute Skill

- Create `src/execute/SKILL.md` with a narrow scope: own implementation work only.
- Let `execute` handle two valid entry modes:
  - direct bounded execution when the task is still locally clear and does not
    need durable task state
  - plan-driven execution from an explicit `plans/*.md` file
- For plan-driven work, require the explicit plan path rather than guessing the
  "latest" plan file.
- Make `execute` read `AGENTS.md`, relevant `specs/*`, tests, and the plan file
  before editing.
- Make `execute` implement only one milestone or other bounded slice before
  stopping.
- Make `execute` run the relevant mechanical checks for the bounded slice it
  changed before stopping.
- Make `execute` update the plan after each slice with progress, discoveries,
  decisions, blockers, and verification notes.
- Make `execute` hand off explicitly to `verify` after finishing a slice rather
  than trying to self-invoke adversarial review implicitly.
- Make `execute` treat `specs` and `tests` as required follow-through when the
  implementation changed durable repo truth or test truth.
- In direct execution mode, make `execute` infer sync obligations from
  `AGENTS.md`, relevant `specs/*`, the changed code paths, and the existing
  applicable test patterns when no plan file is present.
- Let `execute` proactively invoke `specs` when implementation changed durable
  repo truth or when missing or stale repo truth is blocking safe completion:
  behavior contracts, boundaries, commands, conventions, architecture, file
  placement, testing policy, or other guidance that should persist beyond the
  current task.
- Let `execute` proactively invoke `tests` when changed behavior is not yet
  covered at the applicable existing layers or when the current test truth has
  drifted from code reality enough to make completion or verification unsafe.
- Make `execute` stop and recommend a fresh session when repeated corrections,
  exploratory dead ends, or context clutter have pushed the session out of the
  smart working zone.
- Keep provider features such as plan mode, subagents, or worktrees optional
  accelerators only, never baseline workflow requirements.

## 5. Improve The Six Core Skills

- Tighten each skill's trigger description so activation is clearer and more
  reliable.
- Keep each skill narrowly owned and avoid overlap across `consult`, `plan`,
  `execute`, `specs`, `tests`, and `verify`.
- Improve `consult` so it stays evidence-backed, bounded, and explicitly
  oriented around current behavior, options, risks, and recommendation.
- Improve `plan` so it writes high-signal, self-contained, update-in-place plan
  files rather than vague task notes.
- Improve `execute` so it is reliable in both direct bounded execution and
  explicit plan-driven execution, with strong stop/update/restart behavior.
- Keep `execute` responsible for implementation and mechanical checks only;
  keep adversarial review as a separate `verify` step.
- Improve `specs` so it cleanly owns repo truth, harness bootstrapping, and
  durable code-organization guidance without drifting into task plans.
- Make `specs` explicitly evaluate whether the codebase is organized cleanly
  enough for both humans and agents: boundaries, naming, navigability,
  ownership, and discoverability of the relevant code paths.
- Make `specs` proactively surface weak structure, unclear boundaries, and
  missing or stale guidance that reduce an agent's odds of understanding the
  repo and making correct changes safely.
- Make `specs` drive proportional improvements to codebase readiness for agentic
  work, not just document the current state after the fact.
- Make `specs` work across different repo shapes without path assumptions:
  monorepos, polyrepos vendored into one tree, `apps/`, `packages/`,
  `services/`, `src/`, flat layouts, generated directories, and mixed stacks.
- Improve `tests` so it handles both sync and bootstrap: proportional
  test-layer selection, weak-repo testing strategy, and honest coverage-gap
  reporting.
- Make `tests` work across different code and test layouts without hardcoding
  path assumptions, and discover per-app or per-package commands and tiers from
  repo reality.
- Improve `verify` so it remains findings-first, adversarial, grounded in
  evidence, and explicit about blocked checks, stale truth, and remaining
  gaps.
- Make missing required `specs` sync or `tests` sync a `fail`, not merely
  `pass with risks`, when the obligation was explicit in the plan or clearly
  implied by repo truth in direct execution mode.

## 6. Ground The Skills In Official Sources

- Re-review and capture durable guidance from the official sources used during
  the design work:
  - https://developers.openai.com/codex/learn/best-practices
  - https://developers.openai.com/cookbook/articles/codex_exec_plans
  - https://developers.openai.com/codex/skills
  - https://agentskills.io/specification
  - https://agentskills.io/skill-creation/best-practices
  - https://agentskills.io/skill-creation/optimizing-descriptions
  - https://agentskills.io/skill-creation/evaluating-skills
  - https://agentskills.io/skill-creation/using-scripts
  - https://agentskills.io/client-implementation/adding-skills-support
- Re-review the official example corpora and extract only durable composition
  patterns:
  - https://github.com/openai/skills
  - https://github.com/anthropics/skills
  - https://github.com/obra/superpowers
  - https://github.com/ClaytonFarr/ralph-playbook
- Capture both the official-doc guidance and the example-corpora patterns in a
  durable repo-level reference note rather than leaving them only in plans or
  chat memory.
- Keep provider-specific guidance additive only; use it to stress-test the
  portable workflow rather than define the portable baseline.
- Capture the durable cross-provider patterns explicitly:
  - research before coding
  - durable state in files, not chat
  - concise repo truth, detailed task truth in dedicated markdown
  - focused skills with progressive disclosure
  - fresh-context verification and evaluation loops
  - separate planning from implementation
  - stop, persist, and restart when session quality drops
  - decompose large work into bounded execution slices instead of one giant
    plan or one giant session

## 7. Add Full Evaluation Coverage

- Define a canonical eval runtime for regression gating:
  `codex` + `gpt-5.4` + `xhigh` for now.
- Keep that runtime configurable later so the benchmark profile can be upgraded
  intentionally without rewriting the whole eval system.
- Add trigger eval fixtures for all six skills with should-trigger and
  near-miss should-not-trigger prompts.
- Add workflow eval fixtures for all six skills, including baseline-vs-with-
  skill review cases.
- Define the baseline comparison policy explicitly:
  compare against the previous committed version of the skill, and use no-skill
  baseline runs where that comparison meaningfully clarifies whether the skill
  itself is helping.
- Store tracked eval definitions with each skill in `src/<skill>/evals/` so trigger
  cases, workflow fixtures, and grading notes stay close to the skill they
  validate.
- Make the eval artifact contract explicit:
  author `evals/evals.json` by hand for each skill, and retain generated
  `outputs/`, `timing.json`, `grading.json`, `benchmark.json`, `feedback.json`,
  and execution transcripts or equivalent logs so regressions can be inspected
  instead of guessed at.
- Keep generated eval workspaces, run artifacts, and temporary cloned fixtures
  outside tracked source so the repo stores the eval intent and results can be
  refreshed cleanly.
- Use `scripness/cryptoli` as the first official real-repo eval fixture for
  monorepo-aware skills and workflows:
  repo-topology discovery, codebase-organization assessment, multi-app spec
  syncing, multi-layer test discovery, and plan/execute/verify behavior against
  a real pnpm workspace.
- Pin `cryptoli` to an explicit commit for repeatable eval runs, and refresh
  that pin deliberately rather than letting fixture drift happen silently.
- Add dedicated `plan` evals:
  - plan creation quality
  - plan resumability from fresh context
  - plan update quality after partial implementation
  - baseline-vs-with-skill comparisons for long-running tasks
- Add dedicated `execute` evals:
  - direct bounded execution quality
  - plan-driven execution quality
  - stop/update/restart behavior after context degradation
  - correctness of explicit-plan-path handling
- Add dedicated `verify` evals for reviewing both plans and implementations.
- Use train and validation splits for description tuning and avoid overfitting.
- Add repeatable local runners for trigger and workflow evals.
- Run repeated trials for critical trigger and workflow evals so one lucky or
  unlucky model sample does not masquerade as skill improvement or regression.
- Define pass/fail thresholds for regression gating:
  no unexplained drop in must-run workflow pass rate, no unexplained drop in
  trigger quality, and no increase in unresolved severe findings on real-repo
  fixtures.
- Define the grading protocol per eval:
  assertion-based checks where possible, reviewer rubrics where judgment is
  required, and hybrid grading when both are needed.
- Keep the eval harness honest: use it to scaffold comparison and regression
  review, not to pretend open-ended model quality can be auto-scored perfectly.
- Decide which workflow cases are the must-run regression surface for daily
  maintenance.
- Make `cryptoli` part of that must-run regression surface first, then add a
  simpler single-package fixture later so both monorepo and smaller-repo
  behavior are covered.
- Require regression artifact review before accepting a skill change:
  inspect failures, changed outputs, timing, and grading notes instead of
  trusting a summary number blindly.

## 8. Add Repo-Level Maintenance Tooling

- Status: shipped in Phase 06; preserved here as the original design scope.

- Add a small command surface for validation and eval refresh.
- Validate skill structure, frontmatter, and local asset integrity.
- Decide whether a `Makefile`, shell scripts, or another lightweight interface
  is the right operator surface for this repo.
- Add optional helper scripts under the relevant skill-local `scripts/`
  directory, most likely `src/execute/scripts/`, for convenience only and not as
  required workflow primitives.
- Add a thin helper loop for plan-driven work only:
  take an explicit provider command and explicit plan file, run a fresh
  top-level `execute` invocation, then a fresh top-level `verify` invocation,
  and repeat while plan work remains and verification is acceptable.
- Keep helper scripts dumb and file-backed:
  no hidden session state, no plan invention from nothing, no guessing the
  latest plan, and no workflow logic that exists only in shell code.
- Require helper scripts to be agent-safe interfaces:
  non-interactive only, input through args/env/stdin, documented `--help`,
  clear examples, and meaningful documented exit codes.
- Require helper scripts to separate structured data from diagnostics:
  machine-readable stdout, diagnostics and progress on stderr, helpful error
  messages, and predictable output size.
- Prefer idempotent and reviewable helper behavior:
  retry-safe operations when possible, `--dry-run` or equivalent for stateful
  actions, and explicit confirmation flags for destructive actions.
- Ensure a skill change is not considered done until validation and the
  relevant eval reports have been refreshed.
- Consider adding CI later, but keep the local maintenance loop usable first.

## 9. Add Core Repo Docs

- Status: shipped in Phase 06; preserved here as the original design scope.

- Expand `README.md` so it explains the full `0 -> 100` workflow:
  bootstrap repo truth, bootstrap test truth, consult, plan, execute, verify,
  then sync truth again.
- Add a short maintenance guide for updating skills, running evals, and
  upstreaming improvements discovered in downstream project work.
- Document the durable-state model clearly:
  `AGENTS.md` and `specs/` = repo truth,
  tests = executable truth,
  `plans/*.md` = task truth,
  code = implemented reality.
- Document that `specs` exists to keep the repo in a state where a newly
  entering agent can get oriented fast, find the right code, and work with the
  highest realistic chance of success.
- Keep this repo focused on skills, skill assets, evals, and maintenance
  tooling only; avoid mixing in unrelated machine configuration concerns.
