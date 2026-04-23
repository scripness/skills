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

- [2026-04-22] A later heavy verification pass found that the fixed six-skill
  downstream root README copy and the path-based cross-skill README references
  were not truthful under subset sync. Treat the shipped files under
  `scripts/sync_downstream.py` and `src/*/README.md` as the current truth; the
  older draft text below remains as historical design background.

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
4. Downstream README truth sync: update
   `src/consult/README.md`, `src/execute/README.md`, `src/plan/README.md`,
   `src/specs/README.md`, `src/tests/README.md`, and
   `src/verify/README.md` so their `Local Files` sections describe `evals/`
   as upstream-only metadata rather than a local downstream path, then rerun
   the disposable sync proof. Done when a synced downstream install no longer
   claims `evals/` exists locally and the rest of the managed README sync
   behavior still matches the contract. Owning paths: the six skill
   `README.md` files. Slice-level `specs` exit criteria: not required unless
   the wording change exposes broader repo-doc drift. Slice-level `tests` exit
   criteria: rerun targeted helper checks plus `make validate`; no `tests`
   skill sync required.
5. Preflight malformed-README handling: change `scripts/sync_downstream.py` so
   duplicate or otherwise invalid downstream `README.md`
   `## Agentic Workflow` input is rejected before any downstream skill
   directory is created, deleted, or replaced, then rerun the malformed-README
   proof plus the normal disposable sync proof. Done when a target repo with
   multiple `## Agentic Workflow` headings fails without mutating
   `.agents/skills/` and the normal sync path still behaves as documented.
   Owning paths: `scripts/sync_downstream.py` and `Makefile` only if the
   operator surface changes. Slice-level `specs` exit criteria: not required
   unless the user-facing contract or error behavior changes materially.
   Slice-level `tests` exit criteria: rerun the malformed-README proof, the
   normal disposable sync proof, and `make validate`; no `tests` skill sync
   required.
6. Source-repo target safety and remaining repo-truth sync: harden
   `scripts/sync_downstream.py` so it rejects the source repo itself and any
   downstream `.agents/skills/` symlink before printing a normal sync plan or
   mutating files, then sync the remaining repo-truth docs that still describe
   `Makefile` too narrowly after `make sync` shipped. Done when
   `python3 scripts/sync_downstream.py --target . --dry-run` fails fast with a
   downstream-target error, a disposable repo with `.agents/skills` as a
   symlink also fails fast before mutation, and the repo docs/specs no longer
   claim `Makefile` is only a harness wrapper. Owning paths:
   `scripts/sync_downstream.py`, `AGENTS.md`, `specs/repo-surface.md`,
   `evals/README.md`, and `specs/evaluation-harness.md`. Slice-level `specs`
   exit criteria: update any remaining repo-truth wording in the same slice.
   Slice-level `tests` exit criteria: rerun the new target-rejection proofs,
   the disposable sync proof, and `make validate`; no `tests` skill sync
   required.
7. Subset-safe README truth and heading hardening: update
   `scripts/sync_downstream.py`, `src/<skill>/README.md`, and the owning
   docs/specs so subset sync leaves truthful human-facing copy, managed
   heading detection ignores indented code examples, and later setext headings
   are preserved instead of being swallowed by the replacement. Done when a
   subset sync advertises only the currently installed shipped skills, the
   copied skill `README.md` files no longer depend on sibling skill paths,
   indented or nested code examples containing `## Agentic Workflow` no longer
   trigger false matches, setext `Keep Me` sections survive replacement, and
   the repo-truth docs describe the subset-safe managed section truthfully.
   Owning paths: `scripts/sync_downstream.py`, `src/<skill>/README.md`,
   `AGENTS.md`, `specs/workflow-contract.md`, and `specs/repo-surface.md`.
   Slice-level `specs` exit criteria: sync the affected repo-truth wording in
   the same slice. Slice-level `tests` exit criteria: rerun the subset-sync
   proof, indented-code proof, nested-fence proof, setext-boundary proof,
   malformed-README preflight, `make validate`, and `git diff --check`; no
   `tests` skill sync required.

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
- [2026-04-22] `make validate` passed after adding six skill-local
  `README.md` files and syncing the shipped-surface docs/specs.
- [2026-04-22] `rg --files src | rg '/README\.md$'` confirmed the six new
  skill `README.md` files plus the pre-existing `src/specs/assets/specs/README.md`.
- [2026-04-22] `git diff --check` passed for the slice.
- [2026-04-22] Verify verdict: `pass with risks` for the README/docs slice.
  No shipped-surface drift was found in the new skill-local `README.md` files
  or the synced docs/specs. The later helper/docs slice resolved the temporary
  milestone-ordering mismatch that this review noted.
- [2026-04-22] `make help` passed and documented
  `make sync TARGET=/abs/path/to/repo [SKILL="consult execute"]` plus
  `python3 scripts/sync_downstream.py --help`.
- [2026-04-22] `python3 scripts/sync_downstream.py --help` passed.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp> --skill consult --skill execute --dry-run`
  showed exact-name subset replacement plus managed downstream README sync
  without writing files.
- [2026-04-22] `make sync TARGET=<tmp>` against a disposable repo replaced the
  matching shipped skill paths, preserved an unrelated custom skill, excluded
  skill-local `evals/`, copied the new per-skill `README.md` files plus
  execute helper assets, and fully replaced the downstream `README.md`
  `## Agentic Workflow` section while leaving later `## Keep Me` content
  intact.
- [2026-04-22] The synced disposable repo contained no `__pycache__/` or
  `*.py[cod]` files after the helper run.
- [2026-04-22] A second `make sync TARGET=<tmp>` run left the disposable repo
  file manifest unchanged and reported the managed downstream `README.md`
  section as already current.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp> --skill nope`
  failed with exit 2 and listed the available shipped skill names.
- [2026-04-22] `make validate` passed after adding
  `scripts/sync_downstream.py`, `make sync`, and the downstream-sync
  docs/spec updates.
- [2026-04-22] `git diff --check` passed for the helper/docs slice.
- [2026-04-22] `make help`, `python3 scripts/sync_downstream.py --help`,
  `make validate`, and `git diff --check` all passed again during final plan
  verification.
- [2026-04-22] `make sync TARGET=<tmp>` still produced the expected filtered
  install surface, but `find <tmp>/.agents/skills -maxdepth 2 -type d`
  confirmed no downstream `evals/` directories while the copied skill
  `README.md` files still listed `evals/` under `Local Files`.
- [2026-04-22] `rg -n "tracked eval metadata in this source repo"
  src/*/README.md` matched all six shipped skill `README.md` files, so every
  downstream-installed copy currently carries the same incorrect `evals/`
  claim.
- [2026-04-22] Verify verdict: `fail`. `src/consult/README.md:40`,
  `src/execute/README.md:48`, `src/plan/README.md:40`,
  `src/specs/README.md:44`, `src/tests/README.md:40`, and
  `src/verify/README.md:43` describe `evals/` as a local file even though
  `scripts/sync_downstream.py` intentionally filters `evals/` out of
  downstream installs. The helper behavior and repo-level docs/specs otherwise
  matched the current contract.
- [2026-04-22] `make sync TARGET=/tmp/tmp.8U1ujuScaA` against a fresh
  disposable repo copied the six skill `README.md` files with
  `evals/` described as upstream-only metadata, preserved an unrelated custom
  downstream skill, and still refreshed the managed downstream `README.md`
  `## Agentic Workflow` section.
- [2026-04-22] `rg -n "upstream-only eval metadata|tracked eval metadata"
  /tmp/tmp.8U1ujuScaA/.agents/skills` matched the new upstream-only wording in
  all six copied skill `README.md` files and found no stale "tracked eval
  metadata" wording downstream.
- [2026-04-22] `find /tmp/tmp.8U1ujuScaA/.agents/skills -type d -name evals`
  returned no results after the sync proof, so the copied README wording now
  matches the filtered install surface.
- [2026-04-22] `make validate` passed after the milestone 4 README wording
  fix.
- [2026-04-22] `git diff --check` passed for the milestone 4 slice.
- [2026-04-22] `make sync TARGET=/tmp/tmp.B4rr8J69Sq SKILL="consult execute"`
  passed and copied only `consult` and `execute` while leaving an unrelated
  downstream custom skill in place, so the documented subset operator surface
  works as advertised.
- [2026-04-22] `python3 scripts/sync_downstream.py --target /tmp/tmp.xdZIJ9aocB`
  against a `README.md` with two `## Agentic Workflow` headings exited with
  status 1 but still created
  `/tmp/tmp.xdZIJ9aocB/.agents/skills/{consult,execute,plan,specs,tests,verify}`.
- [2026-04-22] Verify verdict: `fail`. `scripts/sync_downstream.py:257-260`
  copies downstream skill directories before `sync_readme()` validates the
  downstream `README.md`, and duplicate-heading detection only happens later in
  `find_managed_section()` at `scripts/sync_downstream.py:171-180`. A target
  repo that should fail cleanly on malformed managed-section input is left in a
  partially synced state instead.
- [2026-04-22] `python3 scripts/sync_downstream.py --target /tmp/tmp.a1dQTa2Dyp`
  against a `README.md` with two `## Agentic Workflow` headings exited with
  status 1 before any downstream mutation. The existing
  `.agents/skills/consult/old.txt`, `.agents/skills/custom/custom.txt`, and
  downstream `README.md` hash all stayed unchanged, and no new
  `.agents/skills/plan` directory was created.
- [2026-04-22] `make sync TARGET=/tmp/tmp.jdEs70jPR7` against a fresh
  disposable repo still replaced a stale downstream `consult` payload,
  installed all six shipped skills, preserved an unrelated custom skill,
  refreshed the managed downstream `README.md` `## Agentic Workflow` section,
  kept later `## Keep Me` content intact, and produced no downstream
  `evals/` directories.
- [2026-04-22] `make validate` passed after the milestone 5 preflight fix.
- [2026-04-22] `git diff --check` passed for the milestone 5 slice.
- [2026-04-22] `make sync TARGET=/tmp/tmp.dtLdsvLgRG` against a disposable
  repo with a fenced code block, stale managed workflow text, a stale
  downstream `consult` payload, and later `## Keep Me` content replaced the
  selected shipped skill paths, preserved the later section, left the fenced
  heading-like text untouched, and removed the stale managed section text.
- [2026-04-22] A second `make sync TARGET=/tmp/tmp.dtLdsvLgRG` run restored a
  manual edit inside the managed workflow section, so reruns fully replace
  drift inside `README.md` `## Agentic Workflow` instead of preserving it.
- [2026-04-22] `make sync TARGET=/tmp/tmp.QsBExMBEXo SKILL="consult execute"`
  created only `consult` and `execute`, preserved an unrelated custom skill,
  replaced the stale `consult` payload, and created a downstream `README.md`
  when it was missing.
- [2026-04-22] `python3 scripts/sync_downstream.py --target /tmp/tmp.QsBExMBEXo --skill nope`
  exited with status 2 and listed the available shipped skill names.
- [2026-04-22] Strict final verify verdict: `pass`. `make help`,
  `python3 scripts/sync_downstream.py --help`, `make validate`,
  `git diff --check`, full sync/rerun, subset sync, invalid-skill rejection,
  and malformed-README preflight all matched the documented downstream sync
  contract, and no additional `specs` or `tests` follow-through is required.
- [2026-04-22] A later seven-way read-only verification pass (six GPT-5.4
  xhigh subagents plus one main-session review) disproved that strict-final
  completion claim. Five of the six subagents failed on one or more of:
  helper self-target/symlink safety, stale `Makefile` wording in repo-truth
  docs, and the still-uncommitted helper surface at that moment.
- [2026-04-22] `python3 scripts/sync_downstream.py --target . --skill consult --dry-run`
  exposed a destructive self-target path: this source repo ships
  `.agents/skills -> ../src`, so a real run against the source repo would
  delete through the mirror into `src/`.
- [2026-04-22] `AGENTS.md`, `specs/repo-surface.md`, `evals/README.md`, and
  `specs/evaluation-harness.md` still described `Makefile` too narrowly as a
  harness wrapper even though the shipped operator surface now also includes
  `make sync`.
- [2026-04-22] `python3 scripts/sync_downstream.py --target . --skill consult --dry-run`
  now exits 2 with `target repo must be a downstream repo`, so the source repo
  itself is rejected before any normal sync progress lines or mutations.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-symlinked-skills> --skill consult`
  now exits 2 with `downstream skills path must not be a symlink`, so a
  symlinked downstream `.agents/skills/` root is rejected before mutation.
- [2026-04-22] `make validate`, `git diff --check`, `make help`, and
  `python3 scripts/sync_downstream.py --help` all passed again after the
  target-safety and repo-truth sync fix.
- [2026-04-22] `make sync TARGET=<tmp>` still replaced stale downstream skill
  payloads, preserved unrelated custom skills, copied the filtered skill
  payload without downstream `evals/` directories, and left the managed
  downstream `README.md` section stable on rerun after the target-safety fix.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-duplicate-readme>`
  still fails before downstream mutation when the target `README.md` contains
  duplicate `## Agentic Workflow` headings.
- [2026-04-22] A later seven-way read-only verification pass (six GPT-5.4
  xhigh subagents plus one main-session review) disproved completion again:
  subset sync still wrote a fixed six-skill root README block, the copied
  skill `README.md` files still referenced sibling skill paths that might not
  exist under subset installs, and `line.strip() == SECTION_HEADING` still
  treated indented or nested code examples as real managed headings.
- [2026-04-22] `make sync TARGET=<tmp-subset> SKILL="consult execute"` now
  creates only `consult` and `execute`, preserves an unrelated custom skill,
  writes a managed downstream `README.md` section that lists only the
  currently installed shipped skills, and keeps the execute-helper commands
  conditional on `execute` actually being present.
- [2026-04-22] The copied `consult` and `execute` README files from that
  subset proof now use skill-name guidance rather than sibling file paths, so
  the downstream human-facing copy stays truthful even when other shipped
  skills are absent.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-indented-code> --skill consult`
  now leaves an indented `    ## Agentic Workflow` code example untouched and
  appends the managed section later in the file instead of treating the code
  line as the managed heading.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-nested-fence> --skill consult`
  now succeeds when a nested fenced code example contains
  `## Agentic Workflow`; the helper ignores that example text and updates only
  the real managed section.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-setext> --skill consult`
  now preserves a later setext `Keep Me` heading instead of swallowing it into
  the managed section replacement.
- [2026-04-22] `make help`, `python3 scripts/sync_downstream.py --help`,
  `make validate`, and `git diff --check` all passed again after the
  subset-truth and heading-hardening fix.
- [2026-04-22] A fresh post-repair verification pass found one remaining
  milestone 6 gap: the helper rejected a direct symlinked
  `.agents/skills` leaf but still accepted a symlinked `.agents` parent, and
  the highest-level shipped-reality summaries in `README.md`, `AGENTS.md`, and
  `specs/workflow-contract.md` still omitted `scripts/`.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-parent-symlink> --skill consult`
  unexpectedly passed before the final safety fix when `.agents` itself was a
  symlink, so writes still followed that redirected path chain.
- [2026-04-22] `python3 scripts/sync_downstream.py --target <tmp-leaf-symlink> --skill consult`
  now exits 2 when `.agents/skills` is a symlink, and
  `python3 scripts/sync_downstream.py --target <tmp-parent-symlink> --skill consult`
  also now exits 2 when `.agents` is a symlink, so the helper rejects any
  symlink traversal anywhere in the downstream `.agents/skills` path chain.
- [2026-04-22] `README.md`, `AGENTS.md`, and `specs/workflow-contract.md` now
  include `scripts/` anywhere they enumerate the shipped reality or shipped
  implementation surface.
- [2026-04-22] `make help`, `python3 scripts/sync_downstream.py --help`,
  `make validate`, `git diff --check`, `rg --files src evals specs scripts`,
  and the refreshed source-target plus both symlink-chain rejection proofs all
  passed after the final milestone 6 hardening.
- [2026-04-23] `python3 scripts/sync_downstream.py --target <tmp-reviewer-repro> --skill consult`
  reproduced the later PR review finding on the pre-fix tree: a downstream
  `README.md` containing `- item` then `---` inside the managed section kept
  stale trailing content after replacement instead of deleting the full stale
  section body.
- [2026-04-23] `python3 scripts/sync_downstream.py --target <tmp-list-break> --skill consult`,
  the ordered-list variant, and the blockquote variant now all remove stale
  managed tail text and preserve later `## Keep Me` content instead of
  treating the thematic break as a section boundary.
- [2026-04-23] `python3 scripts/sync_downstream.py --target <tmp-setext> --skill consult`
  still preserves a later real setext heading `Keep Me` plus `-------` after
  the thematic-break hardening.
- [2026-04-23] `python3 scripts/sync_downstream.py --target <tmp-indented-code> --skill consult`
  and `python3 scripts/sync_downstream.py --target <tmp-nested-fence> --skill consult`
  still ignore heading-like text inside indented code and nested fenced
  examples.
- [2026-04-23] `python3 scripts/sync_downstream.py --target <tmp-duplicate-readme>`
  still fails before downstream mutation when duplicate managed headings are
  present.
- [2026-04-23] `make sync TARGET=<tmp> SKILL="consult execute"` still installs
  only the selected skills and writes the subset-truthful managed downstream
  `README.md` section with execute helper commands.
- [2026-04-23] `make help`, `python3 scripts/sync_downstream.py --help`,
  `make validate`, and `git diff --check` all passed after the thematic-break
  hardening fix.
- [2026-04-23] Verify verdict: `pass`. `scripts/sync_downstream.py` now
  distinguishes real later setext headings from thematic breaks after list
  items, ordered-list items, blockquotes, ATX headings, fences, and indented
  code, so the managed downstream `README.md` section is fully replaced
  without regressing the earlier heading-hardening cases. No additional
  `specs` or `tests` follow-through is required.

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

- None currently.

## Blockers

- None currently.

## Progress

- [x] Milestone 1: Contract and README block design
- [x] Milestone 2: Sync helper implementation
- [x] Milestone 3: Verification and rollout proof
- [x] Milestone 4: Downstream README truth sync
- [x] Milestone 5: Preflight malformed-README handling
- [x] Milestone 6: Source-repo target safety and remaining repo-truth sync
- [x] Milestone 7: Subset-safe README truth and heading hardening

- [2026-04-22] Partial milestone 2 progress: added concise
  `src/<skill>/README.md` files for all six shipped skills and synced
  `AGENTS.md`, `README.md`, `docs/maintenance.md`,
  `specs/repo-surface.md`, and `specs/workflow-contract.md` so the shipped
  surface now describes those human-facing overviews accurately.
- [2026-04-22] Completed the sync-helper slice: added
  `scripts/sync_downstream.py`, wired `make sync`, and synced
  `AGENTS.md`, `README.md`, `docs/maintenance.md`,
  `specs/workflow-contract.md`, and `specs/repo-surface.md` to the new
  required downstream install contract.
- [2026-04-22] The shipped surface now distinguishes full upstream
  `src/<skill>/` payloads from filtered downstream `.agents/skills/<skill>/`
  installs and documents the managed downstream `README.md`
  `## Agentic Workflow` section.
- [2026-04-22] Milestone ordering was realigned before final verification so
  the next safe move at that point was milestone 3 verification and rollout
  proof rather than more implementation.
- [2026-04-22] Final verification completed the rollout-proof slice and found
  one repairable docs mismatch: all six synced skill `README.md` files still
  say `evals/` is a local file even though downstream installs exclude it.
- [2026-04-22] Completed milestone 4 by updating all six skill `README.md`
  files so `Local Files` describes `evals/` as upstream-only metadata that is
  excluded from normal downstream installs.
- [2026-04-22] A fresh disposable `make sync TARGET=/tmp/tmp.8U1ujuScaA` run
  confirmed the corrected wording copies downstream, no downstream `evals/`
  directories are installed, and an unrelated custom skill still remains in
  place.
- [2026-04-22] Strict final verification found one remaining helper bug:
  malformed downstream `README.md` input with duplicate managed headings fails
  only after the helper has already copied skill directories, so this plan is
  not complete yet and needs one bounded hardening slice.
- [2026-04-22] Completed milestone 5 by moving downstream `README.md`
  rendering and validation ahead of any `.agents/skills/` creation or
  replacement in `scripts/sync_downstream.py`.
- [2026-04-22] The malformed-README proof now fails cleanly without changing
  an existing downstream skill tree or `README.md`, and a fresh normal
  `make sync` run still matches the documented filtered install contract.
- [2026-04-22] Strict final verification passed with no new findings. All
  five milestones remain complete, and this plan no longer needs another
  execute slice.
- [2026-04-22] A later seven-way read-only verification disproved completion:
  the helper would accept this source repo's own `.agents/skills -> ../src`
  mirror as a downstream target, and some repo-truth docs still described
  `Makefile` too narrowly after `make sync` shipped.
- [2026-04-22] Completed milestone 6 by rejecting the source repo root and
  any symlinked downstream `.agents/skills/` path before sync progress begins,
  and by syncing the remaining repo-truth wording in `AGENTS.md`,
  `specs/repo-surface.md`, `evals/README.md`, and
  `specs/evaluation-harness.md`.
- [2026-04-22] Post-fix proof reran the source-target rejection, symlinked
  skills-root rejection, normal disposable sync/rerun, malformed-README
  preflight, `make validate`, `git diff --check`, `make help`, and helper
  `--help`, so the plan is back to an honest complete state.
- [2026-04-22] A later seven-way read-only verification disproved completion
  again: subset sync still wrote a fixed six-skill managed README block, the
  copied skill `README.md` files still assumed sibling skill paths existed,
  and indented or nested code examples could still trigger false managed
  heading matches.
- [2026-04-22] Completed milestone 7 by making the managed downstream
  `README.md` section list the currently installed shipped skills, making the
  execute-helper copy conditional on `execute` actually being present,
  removing subset-unsafe cross-skill path references from the six skill
  `README.md` files, and hardening heading detection so indented code examples
  and nested fenced examples no longer count as managed headings while later
  setext headings stay intact.
- [2026-04-22] Post-fix proof reran the subset-sync truth check, indented-code
  proof, nested-fence proof, setext-boundary proof, malformed-README
  preflight, `make validate`, `git diff --check`, `make help`, and helper
  `--help`, so the plan is back to an honest complete state after the deeper
  verification pass.
- [2026-04-22] A later fresh verification disproved milestone 6 completeness
  one more time: the helper rejected a direct symlinked `.agents/skills` leaf
  but still accepted a symlinked `.agents` parent, and the highest-level
  shipped-reality summaries still omitted `scripts/`.
- [2026-04-22] Completed milestone 6 fully by rejecting any symlink anywhere
  in the downstream `.agents/skills` path chain and by adding `scripts/` to
  the remaining high-level shipped-reality summaries in `README.md`,
  `AGENTS.md`, and `specs/workflow-contract.md`.
- [2026-04-22] Final post-fix proof reran the source-target rejection, direct
  `.agents/skills` symlink rejection, parent `.agents` symlink rejection,
  subset-truth proof, parser-edge-case proofs, malformed-README preflight,
  `make help`, helper `--help`, `make validate`, `git diff --check`, and
  `rg --files src evals specs scripts`, so the plan is back to an honest
  complete state on the final repaired tree.
- [2026-04-23] A later PR review disproved milestone 7 completeness one more
  time: the README parser still treated any non-empty line before `---` as
  setext heading text, so a thematic break after a list item could stop
  replacement early and leave stale managed-section tail content behind.
- [2026-04-23] Completed milestone 7 fully by tightening
  `scripts/sync_downstream.py` setext-boundary detection so only
  paragraph-like lines can start later setext headings; list items,
  ordered-list items, blockquotes, ATX headings, fences, and indented code no
  longer count as the next section boundary.
- [2026-04-23] Post-fix proof reran the reviewer repro, ordered-list and
  blockquote thematic-break proofs, the preserved-setext proof, indented-code
  proof, nested-fence proof, duplicate-heading preflight, subset `make sync`
  proof, `make help`, helper `--help`, `make validate`, and `git diff --check`,
  so the plan is back to an honest complete state after the PR-review repair.

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
- [2026-04-22] Until the downstream sync helper exists, repo docs and new
  skill `README.md` files must stay aligned to current shipped behavior rather
  than claiming filtered downstream installs that the repo does not yet
  implement.
- [2026-04-22] The helper should refresh the managed downstream
  `README.md` `## Agentic Workflow` section on every run, including subset
  skill syncs, so the human-facing workflow text does not drift behind the
  installed skill surface.
- [2026-04-22] Invalid skill selections should fail fast with exit 2 and list
  the available shipped skill names.
- [2026-04-22] Because the skill `README.md` files are copied downstream, any
  source-repo-only file descriptions inside them must say so explicitly rather
  than assuming the full upstream tree is present.
- [2026-04-22] The milestone 4 repair should stay in the skill-local
  `README.md` files; the sync helper and repo-level docs already describe the
  filtered downstream payload correctly.
- [2026-04-22] Malformed downstream `README.md` input must be validated before
  any skill directory replacement so the required fail-fast path does not leave
  a partial install behind.
- [2026-04-22] Reuse the same `render_readme()` path for malformed-README
  preflight and the eventual write step so early validation does not introduce
  a second README parsing contract.
- [2026-04-22] The managed downstream `README.md` section should describe the
  current installed shipped skill set rather than always claiming all six
  local skills are present under subset sync.
- [2026-04-22] Skill-local `README.md` files should avoid sibling skill file
  paths in their shipped copy because subset sync may intentionally omit those
  sibling directories.
- [2026-04-22] Managed heading detection should match only real
  `## Agentic Workflow` H2 lines with up to three leading spaces, not indented
  code examples, and preserving later setext headings is worth the small extra
  parser complexity.
- [2026-04-22] Downstream target safety should reject any symlink anywhere in
  the `.agents/skills` path chain, not only a direct symlink at the final
  `.agents/skills` leaf.
- [2026-04-22] High-level shipped-reality summaries must mention `scripts/`
  wherever they enumerate the shipped implementation surface, not only the
  more detailed maintenance and repo-surface docs.
- [2026-04-22] Reject the source repo root and any symlinked downstream
  `.agents/skills/` path during target validation so the helper never deletes
  through this repo's local `.agents/skills -> ../src` mirror.
- [2026-04-22] Repo-truth docs that mention `Makefile` must describe the full
  shipped maintenance surface, not only the eval harness wrapper subset.
- [2026-04-23] Keep later setext-heading support in downstream `README.md`
  replacement, but only when the preceding line looks like plain paragraph
  text; do not drop setext support just to avoid thematic-break false
  positives.

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
- [2026-04-22] Only `src/specs/assets/specs/README.md` existed under `src/`
  before this slice; none of the six shipped skill directories had their own
  human-facing `README.md`.
- [2026-04-22] The per-skill README drafts in `Content Drafts` assume the
  future filtered downstream install contract, so this slice had to rewrite
  their `evals/` wording to current shipped truth instead of copying the draft
  verbatim.
- [2026-04-22] The current source skill trees do not ship skill-local
  `__pycache__/` or `*.py[cod]` files, so this slice verified those exclusions
  by confirming they did not appear in the synced target rather than by
  seeding artificial upstream noise.
- [2026-04-22] The fence-aware heading scan was sufficient to replace the
  managed downstream `README.md` section while ignoring heading-like text
  inside a fenced code block in the disposable target.
- [2026-04-22] The denylist copy approach preserved extra runtime assets such
  as `src/execute/scripts/.gitignore` in downstream installs without needing a
  narrow allowlist.
- [2026-04-22] The copied skill `README.md` files are part of the downstream
  user-facing install surface, so wording in `Local Files` must distinguish
  source-repo-only metadata from files a downstream reader can actually open.
- [2026-04-22] The new skill-local `README.md` files are themselves part of the
  downstream install surface, so their `Local Files` sections must stay
  truthful for filtered downstream copies rather than only for the upstream
  source tree.
- [2026-04-22] The current helper order validates the downstream `README.md`
  only after copying skills, so duplicate managed headings currently leave a
  partially updated `.agents/skills/` tree behind even though the command
  exits with an error.
- [2026-04-22] Precomputing the downstream README render result before any
  `.agents/skills/` mutation is enough to fail fast on malformed managed
  sections without changing the helper's visible operator surface on normal
  runs.
- [2026-04-22] The current helper also restores manual edits inside the
  managed downstream workflow section on rerun while still preserving later
  sibling sections and fenced code blocks.
- [2026-04-22] Fixed six-skill managed README copy becomes untruthful on a
  fresh subset sync because the helper installs only the selected skills while
  still advertising all six local skills and the execute helpers.
- [2026-04-22] Cross-skill path references inside the shipped skill README
  files become untruthful under subset sync because the referenced sibling
  skill directories may not exist locally.
- [2026-04-22] Using `line.strip() == SECTION_HEADING` lets indented code
  examples and nested code-fence content count as real managed headings even
  though they are not part of the Markdown section structure.
- [2026-04-22] Preserving later setext headings during replacement avoids
  swallowing realistic downstream sections such as `Keep Me` plus `-------`.
- [2026-04-22] Checking only whether the final `.agents/skills` leaf is a
  symlink misses redirected writes through a symlinked `.agents` parent.
- [2026-04-22] High-level repo summaries can still drift even when the more
  detailed maintenance docs and repo-surface spec are already accurate, so the
  final verify pass still needs to read those summary layers directly.
- [2026-04-22] This source repo's tracked `.agents/skills -> ../src` mirror
  creates a real destructive edge case for any downstream sync helper that
  blindly treats `.agents/skills/` as a writable directory instead of
  rejecting symlinked skill roots up front.
- [2026-04-22] Repo-truth docs outside the main downstream-sync contract
  (`evals/README.md` and `specs/evaluation-harness.md`) also needed wording
  updates because `Makefile` no longer wraps only the eval harness surface.
- [2026-04-23] Treating any non-empty line before `---` as setext heading text
  misclassifies thematic breaks after list items, ordered-list items, and
  blockquotes as section boundaries and can leave stale managed-section tail
  text in downstream `README.md`.

## Outcomes / Retrospective

- Complete. This plan shipped a required `make sync` / `scripts/sync_downstream.py`
  downstream refresh path, added human-facing skill `README.md` files to the
  shipped source surface, hardened the helper against source-repo and symlinked
  target misuse, and aligned the repo docs/specs with the filtered downstream
  install contract.
