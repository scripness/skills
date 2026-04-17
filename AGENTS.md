# skills

Provider-agnostic skills repo for end-to-end repository work.

This repo is not an application. It is the upstream source of truth for a skill
system that should let a fresh agent go from `0 -> 100` in any target repo:

- provider = runtime shell
- model = intelligence level
- skills = workflow
- repo files = durable state

## Current State

Shipped skills today:

- `consult`
- `execute`
- `plan`
- `specs`
- `tests`
- `verify`

Current roadmap:
- [TODO.md](TODO.md)

Operator guidance for updating skills, refreshing eval workspaces, and
upstreaming durable improvements from downstream repos lives in
[MAINTENANCE.md](MAINTENANCE.md).

Durable source grounding for the workflow lives in [SOURCES.md](SOURCES.md).

Current execution plans for building the missing system:
- [plans/2026-04-14-phase-01-plan-skill-and-contract.md](plans/2026-04-14-phase-01-plan-skill-and-contract.md)
- [plans/2026-04-14-phase-02-execute-skill.md](plans/2026-04-14-phase-02-execute-skill.md)
- [plans/2026-04-14-phase-03-consult-and-verify-refresh.md](plans/2026-04-14-phase-03-consult-and-verify-refresh.md)
- [plans/2026-04-14-phase-04-specs-and-tests-refresh.md](plans/2026-04-14-phase-04-specs-and-tests-refresh.md)
- [plans/2026-04-14-phase-05-evaluation-harness.md](plans/2026-04-14-phase-05-evaluation-harness.md)
- [plans/2026-04-14-phase-06-tooling-and-final-docs.md](plans/2026-04-14-phase-06-tooling-and-final-docs.md)

## Source Of Truth

For this repo, use these files in this order:

1. `AGENTS.md`
2. `TODO.md`
3. the active `plans/*.md` file for the current phase
4. `README.md`
5. the relevant skill directories and assets

Important:

- `TODO.md` is the roadmap, not the active execution artifact.
- `plans/*.md` are the active task artifacts for the current phase.
- `README.md` should reflect shipped truth, not aspirational behavior.
- Code and checked-in files are reality. Docs must stay synced to what is
  actually shipped.

## Local Agent Toolbox

In this repo, the source-of-truth skill directories live under `src/`:

- [src/consult/SKILL.md](src/consult/SKILL.md)
- [src/execute/SKILL.md](src/execute/SKILL.md)
- [src/plan/SKILL.md](src/plan/SKILL.md)
- [src/specs/SKILL.md](src/specs/SKILL.md)
- [src/tests/SKILL.md](src/tests/SKILL.md)
- [src/verify/SKILL.md](src/verify/SKILL.md)

When these skills are copied into a target repo, they are intended to live
under `.agents/skills/`.

## Evaluation Harness Layout

- Tracked eval definitions live with the skills they validate under
  `src/<skill>/evals/evals.json`.
- Shared harness metadata lives under repo-root `evals/`;
  `evals/README.md` owns the artifact contract, governance rules, and
  regression-review procedure, `evals/runtime.json` pins the default gating
  profile and the machine-readable default governance settings, and
  `evals/fixtures/cryptoli.json` pins the first official real-repo fixture.
- Shared fixture manifests and thin runner helpers also live under repo-root
  `evals/`; `evals/scripts/harness.py` is the first shared runner entrypoint.
- Generated eval outputs, temporary fixture clones, and other run artifacts
  must stay outside tracked source under ignored `.tmp/evals/`.
- Compare against the previous committed version of the same skill by default;
  add a no-skill baseline only when it adds signal.
- Use `train` splits for tuning and `validation` splits for gating; reserve
  must-run cases for the validation split and repeat them three times by
  default.
- The initial must-run surface is the validation boundary trigger pack for
  each shipped skill plus one pinned `cryptoli` real-repo workflow case per
  skill.
- Grade each eval as `assertion`, `rubric`, or `hybrid`, and do not accept a
  skill change until regression artifacts have been reviewed.

## Target-Repo Refresh Workflow

`AGENTS.md` owns the authoritative refresh-workflow contract for this repo.

- Use manual copy as the initial distribution and refresh workflow.
- Copy the shipped skill directories from `src/` in this repo into
  `.agents/skills/` in the target repo.
- Refresh a target repo by re-copying the skill directories and supporting
  assets that changed here.
- Keep install helpers, subtree wiring, and provider-specific plugins optional
  future accelerators only; they are not baseline workflow requirements.

Use the current shipped skills as follows:

- `consult`: clarify current behavior, viable options, key risks, and the
  safest next move when the work is not yet clear enough to execute or plan;
  do not use it for already-clear work or for judging a concrete target.
- `execute`: implement one bounded task directly when it is still locally
  clear, or execute one bounded slice from an explicit plan path, run the
  smallest meaningful checks, complete required `specs`/`tests` follow-through,
  and hand off adversarial review to `verify`.
- `plan`: create or maintain living task plans when work needs durable state
  across sessions, milestones, review loops, or fresh-session restarts.
- `specs`: bootstrap or sync repo truth when `AGENTS.md`, `specs/`, or other
  durable workflow guidance is missing, stale, or too weak to support safe
  planning, execution, or verification.
- `tests`: bootstrap or sync executable truth when test coverage is missing,
  stale, or clearly below what the repo needs for safe execution and
  verification.
- `verify`: adversarially review a concrete plan, implementation slice, diff,
  doc change, or claim against repo truth and checks; treat plan review,
  implementation review, and claim review as distinct targets; return findings
  first, report blocked checks honestly, and treat missing required
  `specs`/`tests` sync as `fail` when the obligation is clear; do not use it
  for open-ended exploration or implementation.

For roadmap execution in this repo, use the phase plans plus the shipped
`execute` and `verify` skills in fresh sessions.

Shipped `plan` contract for this repo:

- invoke `plan` when work needs durable task state across sessions,
  milestone checkpoints, review loops, or fresh-session restarts
- do not invoke `plan` for simple lookups, short clarification work, or
  bounded implementation that is still locally clear; do not promote based on
  abstract task size alone
- `consult` owns clarification and recommendation; `plan` starts only once the
  next move is clear enough to structure execution
- each invocation should create or update one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` path rather than leaving the active
  plan implied in chat
- `plan` owns task-local files under `plans/`; it does not own durable repo
  truth (`specs`), and `execute` owns implementation from an explicit plan path
- every plan must make `specs` and `tests` follow-through explicit: name the
  owning specs or missing specs, the applicable test layers, and when sync is
  required
- every plan must capture blockers that matter for fresh-session resumption
- every plan must be resumable from repo truth plus the plan file alone
- hand off to `execute` and `verify` with the explicit plan path rather than
  asking a later session to guess the active plan

Shipped `execute` contract for this repo:

- `execute` owns implementation and bounded mechanical checks only; `verify`
  owns adversarial review
- invoke `execute` when the user wants implementation now and either the work
  is still locally clear or `plan` already produced an explicit plan path
- do not invoke `execute` when the next move is still unclear and needs
  clarification, option comparison, or a recommendation; use `consult`
- do not invoke `execute` to create or recover durable task state when no
  explicit plan path exists yet; use `plan`
- do not invoke `execute` for adversarial sign-off, final judgment, or fact
  checking; use `verify`
- direct mode is only for bounded work that is still locally clear and does not
  need durable task state
- if direct-mode work stops being locally clear or starts needing durable task
  state, stop and hand off to `plan` rather than improvising a hidden plan in
  chat
- plan-driven mode must start from one explicit `plans/*.md` path produced by
  `plan`; never guess the latest plan file
- in plan-driven mode, implement only one milestone or other bounded slice in a
  fresh session, then update the plan before stopping
- complete required `specs` or `tests` follow-through before claiming a slice
  is done; if that follow-through is blocked, stop and report the blocker
- hand off explicitly to `verify` after each slice rather than absorbing review
  behavior into `execute`

## Working Loop For This Repo

When working on the roadmap:

1. Read `AGENTS.md`, `TODO.md`, and the active phase plan.
2. Use a fresh session per bounded milestone or slice.
3. Use [src/execute/SKILL.md](src/execute/SKILL.md) with the explicit plan path for
   implementation.
4. Use [src/verify/SKILL.md](src/verify/SKILL.md) with the same plan path for review.
5. Update the plan before stopping.
6. Move to the next phase only after the current phase is actually complete.

Preferred phase order:

1. Phase 01: `plan`
2. Phase 02: `execute`
3. Phase 03: `consult` and `verify`
4. Phase 04: `specs` and `tests`
5. Phase 05: evaluation harness
6. Phase 06: tooling and final docs

## Boundaries

Always:

- keep this repo provider-agnostic
- keep `.agents/` and `AGENTS.md` as the authoritative cross-client surface
- keep `CLAUDE.md` as a thin symlink mirror only
- keep skill boundaries sharp
- prefer durable state in files over chat memory
- update the active plan when a milestone changes status

Ask first:

- broad workflow changes that alter the six-skill model
- adding heavy automation or orchestration that becomes required for correctness
- widening a phase beyond its owned TODO sections

Never:

- treat provider plan modes, plugins, or auto-memory as required workflow
  primitives
- turn `TODO.md` into a single giant execution plan
- guess the latest active plan file in plan-driven work
- let docs claim shipped behavior that the repo does not yet implement

## Architecture

```text
.
├── Makefile
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── SOURCES.md
├── README.md
├── TODO.md
├── evals/
├── src/
│   ├── consult/
│   ├── execute/
│   ├── plan/
│   ├── specs/
│   ├── tests/
│   └── verify/
└── plans/
```

Bootstrap assets live under `src/specs/assets/`.
Generated eval outputs live under ignored `.tmp/evals/`.

## Commands

There is still no package manifest or CI in this repo. Phase 06 now ships a
repo-root `Makefile` as the thin local maintenance surface above the existing
Python harness helper.

Useful local commands:

| Purpose | Command |
|---------|---------|
| List files | `rg --files .` |
| Search text | `rg "pattern" .` |
| Inspect roadmap | `sed -n '1,260p' TODO.md` |
| Inspect maintenance guide | `sed -n '1,260p' MAINTENANCE.md` |
| Inspect active plan | `sed -n '1,220p' plans/<file>.md` |
| Check git status | `git status --short` |
| Show the repo-level maintenance targets | `make help` |
| Run repo-level validation for skill metadata, asset integrity, and eval invariants | `make validate` |
| Scaffold a repeatable eval workspace through the repo-level wrapper | `make eval-init-run RUN_ID=<run-id> [SELECTION=must-run|validation|all] [SKILL="consult execute"] [PROFILE=<profile>]` |
| Show the direct harness CLI help | `python3 evals/scripts/harness.py --help` |
| Run validation directly without the Makefile | `python3 evals/scripts/harness.py validate` |
| Scaffold a repeatable must-run eval workspace directly | `python3 evals/scripts/harness.py init-run --run-id <run-id> --selection must-run` |
| Show the optional plan-driven loop helper contract | `python3 src/execute/scripts/plan_loop.py --help` |
| Dry-run the optional plan-driven execute/verify helper with an explicit external runner | `python3 src/execute/scripts/plan_loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"` |

If a phase introduces executable helpers or eval runners, document the exact
commands here and keep them current.

## Conventions

- Keep `AGENTS.md` concise and operational.
- Keep durable roadmap and contract truth in `TODO.md` and `README.md`.
- Keep phase-local state in `plans/*.md`.
- Keep the six source skills under `src/` so the repo-root workflow docs and
  tooling stay clearly separated from the shipped skill payloads.
- Use ASCII by default.
- Prefer proportional edits over broad rewrites.

## Git

Do not amend or rewrite history unless explicitly requested.
Do not revert unrelated user changes.
