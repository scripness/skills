# Downstream Skill Sync

Use this file as a living task plan. Keep it updated in place. A fresh session
should be able to resume from repo truth plus this file alone.

Update `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
`Blockers` after each bounded slice or plan-driven verification pass. Hand off
later `execute` and `verify` sessions with this exact file path.

## Goal

Replace risky manual downstream skill copying with one required upstream sync
path that installs a clean runtime skill surface into a target repo's
`.agents/skills/`, filters out upstream-only eval noise, and keeps a human-only
agentic workflow section in the target `README.md` in sync.

Done means:

- the upstream contract clearly distinguishes the full source skill payload from
  the filtered downstream installed payload
- one thin helper plus one Make target can sync selected or all exact-name
  skills into a target repo idempotently
- downstream `README.md` gets a managed, human-only workflow block without
  broad README rewrites
- upstream docs/specs are consistent with the new required sync workflow

## Scope

- define and document the downstream install surface for `.agents/skills/`
- add a required sync helper in this repo plus a thin Make target wrapper
- replace matching downstream skill directories by exact name before recopy
- filter out `evals/`, `__pycache__/`, and `*.py[cod]` from downstream installs
- create or update a managed downstream `README.md` block for human-facing
  workflow and helper-script discovery
- add a concise `README.md` to each upstream skill directory and ensure it is
  included in downstream installs
- update upstream workflow docs and specs to reflect the new required sync path

## Non-Goals

- changing `AGENTS.md` or the `specs` skill contract to carry human-only helper
  script guidance
- changing downstream `AGENTS.md` or downstream `specs/` as part of this helper
- deleting unrelated downstream custom skills that were not explicitly selected
- making provider-specific wrappers required workflow primitives
- shipping upstream eval harness files into normal downstream installs

## Deliverables

- helper script for syncing filtered skills into a target repo
- concise per-skill `README.md` files in upstream `src/<skill>/`
- Make target that wraps the helper
- managed downstream `README.md` workflow block strategy
- synced upstream docs and specs for the new downstream install contract

## Repo Context

- Current upstream distribution contract still says to copy full skill
  directories from `src/` into downstream `.agents/skills/` manually:
  `README.md`, `specs/workflow-contract.md`, `specs/repo-surface.md`,
  `docs/maintenance.md`, and `AGENTS.md`.
- Current upstream repo also treats `src/<skill>/evals/evals.json` and root
  `evals/` as tracked upstream eval truth. Those files are useful here but add
  noise in normal downstream installs.
- Human-facing helper commands currently live only in upstream docs and helper
  scripts under `src/execute/scripts/`; downstream repos do not get a managed
  human-facing overview for those optional helpers.
- Upstream skill directories currently rely on `SKILL.md` as the primary entry
  document. A human browsing `src/<skill>/` or a synced downstream skill
  directory does not yet get a concise README-oriented overview first.
- The local Makefile currently exposes validation and eval scaffolding only.

## Consult Carry-Forward

- Human-only helper discovery should live in downstream `README.md`, not in
  downstream `AGENTS.md` and not in the `specs` skill.
- Downstream `.agents/skills/` should be treated as a generated install
  surface, not as a byte-for-byte mirror of upstream `src/`.
- The downstream sync path should be required for refreshes; manual copy is too
  error-prone and too likely to leak noise such as eval metadata and generated
  artifacts.
- Filtering should use a denylist, not a narrow allowlist, so future essential
  skill-local files keep flowing downstream automatically.
- The current denylist candidate is:
  - `evals/`
  - `__pycache__/`
  - `*.py[cod]`
- Downstream `README.md` sync should target a clean `## Agentic Workflow`
  section with no marker comments and no visible "managed by" note. The helper
  should update that section by heading rather than by hidden markers.
- Downstream `README.md` sync should be full replacement, not in-place editing
  of subsection content. On each run, delete the existing `## Agentic Workflow`
  section and replace it completely with the latest upstream-generated content
  so the section does not drift stale over time.
- The section boundary rule should be:
  - start at the exact heading line `## Agentic Workflow`
  - end at the next heading of level `<= 2` (`# ` or `## `), or EOF
  - do not treat heading-like text inside fenced code blocks as a boundary
- If the downstream `README.md` contains multiple `## Agentic Workflow`
  headings, fail instead of guessing.
- If the downstream `README.md` does not contain `## Agentic Workflow`, append
  the full section at EOF with normal spacing.
- The generated downstream `## Agentic Workflow` content should stay concise and
  cover:
  - what the six-skill workflow is at a high level
  - that skills can be used individually or composed into a full workflow
  - the typical consult/plan/execute/verify pattern
  - optional helper scripts for `execute`
  - where synced local skills live in the downstream repo
- Exact-name replacement semantics are desired:
  - validate selected skill names against `src/`
  - if `.agents/skills/<name>` exists, delete that exact directory
  - copy the fresh filtered skill from upstream
  - leave unrelated downstream custom skills alone unless explicitly selected
- The operator surface should be intentionally simple:
  - `make sync TARGET=/abs/path/to/repo`
  - when `SKILL` is omitted, sync all skills and the downstream `README.md`
  - optional subset selection remains available, for example
    `make sync TARGET=/abs/path/to/repo SKILL="consult execute"`
- Each upstream skill should ship a concise `README.md` so a human opening
  `src/<skill>/` or a synced downstream skill directory can understand the
  skill without starting from `SKILL.md`.

## Dependencies

- None currently.

## Sync Expectations

- `specs`: Required. This work changes the upstream workflow contract and repo
  surface, so the owning docs/specs must be updated in the same slice:
  `README.md`, `docs/maintenance.md`, `specs/workflow-contract.md`, and
  `specs/repo-surface.md`. If the Make target changes the documented operator
  surface, keep `Makefile` help text aligned too.
- `tests`: No `tests` skill follow-through is currently required by default.
  This repo does not currently ship dedicated automated coverage for the helper
  surface. Validate with targeted mechanical checks such as `make help`,
  helper `--help`, dry-runs against a disposable target, and `make validate`.
  Reassess only if the helper grows enough logic that a dedicated automated
  test surface becomes clearly necessary.

## Content Drafts

These are the working default drafts for implementation. Treat them as the
copy-ready baseline unless later review finds a concrete wording problem.

### Downstream Root README

Use this exact section shape for downstream `README.md`:

```md
## Agentic Workflow

This repo uses a local six-skill workflow under `.agents/skills/`:
`consult`, `plan`, `execute`, `verify`, `specs`, and `tests`.

Use one skill when the task is narrow, or compose them into a full workflow:
`consult` to clarify, `plan` to record durable task state, `execute` to
complete one bounded slice, and `verify` to review the result. Use `specs`
when repo truth is missing or stale, and `tests` when test truth or coverage
needs to be added or synced.

Optional helpers for plan-driven work live under
`.agents/skills/execute/scripts/`:
- `python3 .agents/skills/execute/scripts/loop.py --help`
- `python3 .agents/skills/execute/scripts/providers/codex_loop.py --help`
- `python3 .agents/skills/execute/scripts/providers/codex_loop_dashboard.py --help`

For the longer human-facing description of each skill, open
`.agents/skills/<skill>/README.md`.
```

### Per-Skill README Template

Each `src/<skill>/README.md` should use this shared long-form shape:

```md
# <skill>

[One-sentence summary.]

## What It Owns

[Short paragraph describing the skill's responsibility and boundaries.]

## Use It When

- [Trigger]
- [Trigger]

## Do Not Use It When

- [Anti-trigger]
- [Anti-trigger]

## Workflow Position

[How this skill is used by itself and how it composes with the other skills.]

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `[assets/... or scripts/... when this skill ships them]`
- `evals/`: upstream-only eval metadata when present; not included in normal downstream installs

## Related Scripts

- If this skill ships local scripts, list them directly.
- Otherwise say: "No scripts ship with this skill."
- Also reference the optional execute helpers for humans who want the
  plan-driven loop surface:
  - `../execute/scripts/loop.py`
  - `../execute/scripts/providers/codex_loop.py`
  - `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- [Closest handoff or neighboring skills]
- [Closest handoff or neighboring skills]
```

### Skill README Drafts

#### consult

```md
# consult

Clarify current behavior, viable options, and the safest next move before
committing to execution or planning.

## What It Owns

`consult` owns clarification. It reads repo truth, inspects the current code
and specs, compares viable approaches, and recommends the safest bounded next
move. When the work should become plan-driven, it should leave durable
carry-forward instead of trapping key facts in chat.

## Use It When

- the next move is not yet clear enough to execute safely
- the work needs architecture or tradeoff analysis
- you need to understand current behavior before choosing a direction

## Do Not Use It When

- the task is already clear and implementation should start now
- the work already has an explicit plan path and needs execution
- the task is adversarial review or final judgment

## Workflow Position

Use `consult` by itself for clarification, or as the front door to a larger
workflow:

`consult -> plan -> execute -> verify`

Bring in `specs` if repo truth is weak or stale. Bring in `tests` later if the
chosen implementation changes behavior that needs coverage follow-through.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven helpers for the broader workflow live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../plan/README.md`: use when the direction is clear but the work needs durable task state
- `../execute/README.md`: use when implementation should begin now
- `../verify/README.md`: use when there is already a concrete plan, diff, or claim to judge
```

#### plan

```md
# plan

Create or maintain one explicit `plans/*.md` file when work needs durable task
state across sessions, milestones, or review loops.

## What It Owns

`plan` owns task-local planning. It reads repo truth, chooses one explicit plan
path, and writes a living plan that is resumable from repo files plus that plan
alone. It should make the next unfinished slice decision-complete so later
`execute` work does not need to guess.

## Use It When

- the direction is clear enough to structure
- the work needs durable state across sessions or milestones
- discoveries, blockers, or review history need to survive fresh context

## Do Not Use It When

- the next move is still unclear and needs `consult`
- the task is small and still locally clear enough for one bounded execute pass
- the task is implementation now with no durable-state need

## Workflow Position

`plan` is the durable state layer of the full workflow:

`consult -> plan -> execute -> verify`

In plan-driven work, later `execute` and `verify` runs should keep using the
same exact plan file path.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `assets/plan-template.md`: local plan template
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

No scripts ship directly with this skill.

Optional plan-driven helpers for executing and reviewing plan slices live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../consult/README.md`: use before planning when the direction is not settled
- `../execute/README.md`: use to implement one bounded slice from the plan
- `../verify/README.md`: use to review the plan and later implementation slices
```

#### execute

```md
# execute

Implement one bounded task directly or execute one bounded slice from one
explicit plan file, then hand off to `verify`.

## What It Owns

`execute` owns implementation work. It reads repo truth first, changes only one
bounded slice, runs the smallest meaningful checks, completes required
`specs` or `tests` follow-through, updates the explicit plan when the work is
plan-driven, and then hands off to `verify`.

## Use It When

- the user wants implementation now
- the task is still locally clear and bounded
- there is already one explicit `plans/*.md` file to execute

## Do Not Use It When

- the next move is still unclear; use `consult`
- the work needs durable task state but no explicit plan file exists yet; use `plan`
- the task is review, final judgment, or fact-checking; use `verify`

## Workflow Position

Use `execute` by itself for a small, locally clear task:

`execute -> verify`

Use it as part of the full plan-driven workflow when the work needs durable
task state:

`consult -> plan -> execute -> verify`

Bring in `specs` when repo truth is weak or stale. Bring in `tests` when test
truth or coverage needs to be added or synced.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `references/optional-helper.md`: helper contract and wrapper notes
- `scripts/loop.py`: optional provider-agnostic execute/verify loop helper
- `scripts/providers/codex_loop.py`: optional local Codex wrapper over `loop.py`
- `scripts/providers/codex_loop_dashboard.py`: optional terminal dashboard over the Codex wrapper
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

- `scripts/loop.py`: optional helper for plan-driven execute/verify loops
- `scripts/providers/codex_loop.py`: optional local Codex wrapper over `scripts/loop.py`
- `scripts/providers/codex_loop_dashboard.py`: optional dashboard wrapper over the Codex loop flow

When synced downstream, these live under:
- `.agents/skills/execute/scripts/loop.py`
- `.agents/skills/execute/scripts/providers/codex_loop.py`
- `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../consult/README.md`: use when the next move is still unclear
- `../plan/README.md`: use when the work needs durable task state
- `../verify/README.md`: use after implementation for adversarial review
- `../specs/README.md`: use when repo truth needs syncing
- `../tests/README.md`: use when test truth or coverage needs syncing
```

#### verify

```md
# verify

Adversarially judge a concrete plan, implementation slice, diff, or technical
claim against repo truth and required follow-through.

## What It Owns

`verify` owns review and final judgment. It reads repo truth, checks the
concrete target against code, specs, plans, and mechanical evidence, and
returns findings first. In plan-driven work, it writes its review back into the
same plan file so the task record stays canonical.

## Use It When

- there is already a concrete target to judge
- implementation or plan work needs adversarial review
- a technical claim needs to be fact-checked against current repo reality

## Do Not Use It When

- the next move is still unclear and needs `consult`
- the work needs a new or updated plan file
- implementation fixes should happen now

## Workflow Position

`verify` is the review step after planning or implementation:

`execute -> verify`

or, for longer work:

`consult -> plan -> execute -> verify`

In plan-driven work, repeated `verify` passes keep the same explicit plan file
truthful over time.

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven helpers that call into `verify` live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../execute/README.md`: use before verification when implementation is still pending
- `../plan/README.md`: use when the task-local plan needs to be created or repaired
- `../consult/README.md`: use when the next move is still ambiguous
```

#### specs

```md
# specs

Bootstrap, sync, or repair repo truth in `AGENTS.md`, `CLAUDE.md`, and
`specs/` when the current guidance is missing, stale, or too weak for safe work.

## What It Owns

`specs` owns repo-truth sync. It audits the real repo topology and current
docs, then updates `AGENTS.md`, `CLAUDE.md`, and `specs/` so future planning,
execution, and verification can rely on durable repo truth instead of guesswork.

## Use It When

- `AGENTS.md` or `specs/` is missing or stale
- repo topology or operating guidance is weak enough to block safe work
- a task changed durable repo truth and the docs now need follow-through

## Do Not Use It When

- the task is only a short clarification
- the work mainly needs task-local planning rather than repo-wide truth
- the repo truth is already good enough and implementation should start

## Workflow Position

`specs` is a support skill that can be used before or during the rest of the
workflow whenever repo truth is too weak:

`specs -> consult -> plan -> execute -> verify`

or, for a bounded implementation slice with stale docs:

`execute -> specs -> verify`

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `assets/AGENTS.md`: bootstrap template for downstream `AGENTS.md`
- `assets/specs/README.md`: bootstrap template for downstream specs index
- `assets/specs/spec-template.md`: bootstrap template for downstream topic specs
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven helpers for the broader workflow live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../consult/README.md`: use after repo truth is good enough to choose a direction
- `../plan/README.md`: use when the task needs durable task-local state
- `../tests/README.md`: use when test truth also needs syncing
```

#### tests

```md
# tests

Bootstrap, extend, or sync test truth by discovering the repo's actual test
topology and covering the right layers for safe execution and verification.

## What It Owns

`tests` owns test-truth sync. It audits the real test topology, decides which
layers are applicable, adds or updates the right tests, and runs the required
mechanical checks for the changed behavior.

## Use It When

- changed behavior is not clearly covered by the current test suite
- the repo's test topology or coverage is stale or too weak
- safe execution or verification is blocked by a concrete coverage gap

## Do Not Use It When

- the task is only clarification or planning
- the repo already has adequate coverage for the current slice
- the issue is stale repo docs rather than stale test truth

## Workflow Position

`tests` is a support skill that comes in when behavior changes need coverage
follow-through:

`execute -> tests -> verify`

or, when a repo is weak on both repo truth and test truth:

`specs -> consult -> plan -> execute -> tests -> verify`

## Local Files

- `SKILL.md`: workflow contract and source of truth
- `README.md`: human-facing overview
- `agents/openai.yaml`: local agent shim metadata
- `evals/`: upstream-only eval metadata; not included in normal downstream installs

## Related Scripts

No scripts ship with this skill.

Optional plan-driven helpers for the broader workflow live under:
- `../execute/scripts/loop.py`
- `../execute/scripts/providers/codex_loop.py`
- `../execute/scripts/providers/codex_loop_dashboard.py`

## Related Skills

- `../execute/README.md`: use before test sync when implementation changes are still pending
- `../verify/README.md`: use after test follow-through for adversarial review
- `../specs/README.md`: use when repo-truth docs also need to be corrected
```

## Milestones

1. Contract and README block design: lock the downstream install contract, the
   `README.md` `## Agentic Workflow` section shape, the exact filtering rules,
   the selection semantics for syncing all skills vs a named subset, and the
   per-skill `README.md` contract. Done when the policy is clear enough to
   implement without guessing. Owning paths: `README.md`,
   `docs/maintenance.md`, `specs/workflow-contract.md`,
   `specs/repo-surface.md`. Slice-level `specs` exit criteria: the owning docs
   and specs are updated consistently for the decided contract. Slice-level
   `tests` exit criteria: not required for this docs-first slice.
2. Sync helper implementation: add one thin helper script and one Make target
   that can sync selected or all exact-name skills into a target
   `.agents/skills/`, replacing only matching directories, filtering the agreed
   denylist, and creating or updating the downstream `README.md`
   `## Agentic Workflow` section by deleting that whole section and replacing it
   with the latest upstream content. Also add the concise per-skill
   `README.md` files that should flow downstream. Done when the helper is
   idempotent on repeated runs, rejects invalid skill names clearly, and avoids
   modifying unrelated README content. Owning paths: `Makefile`,
   `scripts/sync_downstream.py`, `src/<skill>/README.md`, and any helper-local
   assets/templates if needed.
   Slice-level `specs` exit criteria: update the owning docs if the implemented
   behavior differs from milestone 1 wording. Slice-level `tests` exit
   criteria: run targeted mechanical checks plus `make validate`; no `tests`
   skill sync unless repo test policy changes.
3. Verification and rollout proof: exercise the helper against a disposable
   local target and optionally one real downstream repo path without pushing,
   confirm the filtered payload and `## Agentic Workflow` section are stable,
   and finish the upstream doc cleanup. Done when the helper output matches the
   contract and repeated runs are clean. Owning paths: helper paths plus the
   owning docs above. Slice-level `specs` exit criteria: docs and Make help
   match the final shipped behavior. Slice-level `tests` exit criteria: no
   additional `tests` skill work unless verification exposes a real gap in the
   repo's maintenance test surface.

## Verification

- Inspect the final contract wording in:
  - `README.md`
  - `docs/maintenance.md`
  - `specs/workflow-contract.md`
  - `specs/repo-surface.md`
- Run `make help` and confirm the new sync command is documented accurately.
- Run the helper with `--help`.
- Dry-run or real-run the helper against a disposable target repo layout and
  confirm:
  - matching downstream skill directories are replaced exactly
  - `evals/` is excluded
  - `__pycache__/` and `*.py[cod]` are excluded
  - per-skill `README.md` files copy through to downstream installs
  - other required skill-local files still copy through
  - the downstream `README.md` `## Agentic Workflow` section is inserted or
    updated by full replacement
  - repeated runs keep the section synced to upstream wording rather than
    preserving stale downstream edits inside that section
- Run `make validate` if the changed surface still relies on the current
  validation expectations.

## Risks

- If the contract keeps describing `src/<skill>/` as the downstream install
  payload, docs and helper behavior will diverge.
- A heading-based README update strategy is cleaner for humans but riskier than
  marker-based replacement. If the helper misidentifies the section boundary,
  it could rewrite downstream prose outside the intended `## Agentic Workflow`
  section.
- Full replacement of the downstream `## Agentic Workflow` section means manual
  downstream edits inside that section will be overwritten on the next sync.
  That is intentional for freshness, but it raises the cost of ad hoc local
  customization.
- An overly broad delete step could remove unrelated downstream custom skills.
- An overly narrow copy filter could accidentally drop future essential
  skill-local assets.
- A sync helper that is not clearly documented could create a new source of
  confusion instead of reducing downstream drift.

## Open Questions

- None currently. The next safe move is implementation from the drafts above.

## Blockers

- None currently.

## Progress

- [ ] Milestone 1: Contract and README block design
- [ ] Milestone 2: Sync helper implementation
- [ ] Milestone 3: Verification and rollout proof

Next safe move: implement the sync helper and supporting README/docs updates
from the locked contract and content drafts above.

## Decision Log

- [2026-04-22] Human-only helper discovery should not be moved into downstream
  `AGENTS.md` or into the `specs` skill; keep it in a managed downstream
  `README.md` block instead.
- [2026-04-22] Downstream `.agents/skills/` should be a generated install
  surface rather than a full mirror of upstream `src/`.
- [2026-04-22] Manual downstream copy is no longer the desired refresh model;
  the target state is one required sync helper.
- [2026-04-22] Downstream filtering should use a denylist so future essential
  skill-local files still copy through automatically.
- [2026-04-22] Downstream `README.md` sync should target a clean
  `## Agentic Workflow` section with no hidden markers and no visible sync
  notice, accepting some extra rewrite risk in exchange for a cleaner file.
- [2026-04-22] Downstream `README.md` sync should replace the full
  `## Agentic Workflow` section on every run so it stays aligned with upstream
  and does not preserve stale downstream edits in that section.
- [2026-04-22] The `## Agentic Workflow` section boundary rule is: replace from
  the exact heading line until the next heading of level `<= 2` or EOF, while
  ignoring heading-like text inside fenced code blocks.
- [2026-04-22] The primary operator surface should be `make sync`, with
  optional exact-name subset selection through `SKILL="..."`.
- [2026-04-22] If a downstream repo is missing `README.md`, create it and
  write the generated `## Agentic Workflow` section instead of failing.
- [2026-04-22] The helper script path should be `scripts/sync_downstream.py`.
- [2026-04-22] When `SKILL` is omitted, `make sync` should sync all skills plus
  the downstream `README.md` `## Agentic Workflow` section.
- [2026-04-22] Each upstream skill should ship a concise `README.md`, and that
  README must be present in downstream installs.
- [2026-04-22] The downstream `README.md` `## Agentic Workflow` section draft in
  `Content Drafts` is the default shipped copy.
- [2026-04-22] The shared per-skill `README.md` template plus the six skill
  drafts in `Content Drafts` are the default shipped copy for implementation.

## Discoveries

- [2026-04-22] Current upstream docs/specs still describe manual full-directory
  copy into downstream `.agents/skills/`, so this task is a contract change,
  not just a tooling addition.
- [2026-04-22] Upstream `evals/` and `src/<skill>/evals/evals.json` are tied to
  the source repo's eval harness and should not be treated as normal downstream
  runtime payload.
- [2026-04-22] Commit `73e19b59cc8e7c5c93f4a7e413f55011423d99b3` moved execute
  helper detail out of `src/execute/SKILL.md` into
  `src/execute/references/optional-helper.md`, so execute-facing human docs
  should mention that reference file as part of the shipped surface.

## Outcomes / Retrospective

- Pending.
