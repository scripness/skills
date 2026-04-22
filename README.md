# skills

Provider-agnostic source repo for a portable six-skill workflow.

The model is simple:

- provider = runtime shell
- model = intelligence level
- skills = workflow
- repo files = durable state

This repo is not an application. It ships source skills, repo-truth docs,
shared eval metadata, and thin local helpers that can be copied into other
repos.

The shipped `src/*/SKILL.md` files remain the workflow source of truth.
Helper scripts are optional accelerators only: they may change invocation,
machine-readable transport, and presentation, but they must not redefine the
skills themselves.

This source repo also tracks `.agents/skills -> ../src` as a local symlink
mirror so copied-layout skill paths work while editing here. `src/` remains
the owning surface.

## Start With Shipped Reality

Read this repo in the same order the shipped workflow expects:

1. `AGENTS.md`
2. `specs/README.md` and the relevant `specs/*.md`
3. `README.md`
4. `MAINTENANCE.md` and `SOURCES.md` as needed
5. `src/`, `evals/`, `Makefile`, and `src/execute/scripts/loop.py`

Completed historical plan records remain available under `plans/` as
background, but they are not the default operational reading chain.

## What Ships

- six source skills under `src/`: `consult`, `execute`, `plan`, `specs`,
  `tests`, and `verify`
- tracked local mirror: `.agents/skills -> ../src` for copied-layout
  ergonomics in this source repo only
- live repo-truth docs: `AGENTS.md`, `specs/`, `README.md`,
  `MAINTENANCE.md`, and `SOURCES.md`
- shared eval surface: `src/<skill>/evals/evals.json`, `evals/runtime.json`,
  `evals/fixtures/cryptoli.json`, and `evals/scripts/harness.py`
- thin repo maintenance wrapper: `Makefile`
- optional explicit-plan execute/verify helper with opt-in continuous
  repair flow and strict final review:
  `src/execute/scripts/loop.py`
- optional repo-local Codex convenience wrapper that delegates to the generic
  helper and defaults real runs to continuous repair mode:
  `src/execute/scripts/providers/codex_loop.py`
- optional repo-local Codex terminal dashboard that sits above the Codex
  wrapper and renders loop progress without changing the raw loop contract:
  `src/execute/scripts/providers/codex_loop_dashboard.py`
- `CLAUDE.md` as a symlink mirror to `AGENTS.md`

## Durable State

- `AGENTS.md` and `specs/` = repo truth
- checks and tests = executable truth
- `src/<skill>/evals/evals.json` and `evals/` = tracked eval truth
- `.agents/skills/` = local symlink mirror of `src/`, not a second truth layer
- `plans/*.md` = canonical task truth for plan-driven work plus plan-shaped
  eval fixtures used by tracked skill evals
- code and checked-in docs = implemented reality
- `.tmp/evals/` = generated local artifacts

## Repo Layout

```text
.
├── .agents/
│   └── skills -> ../src
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── README.md
├── MAINTENANCE.md
├── SOURCES.md
├── specs/
├── evals/
├── Makefile
├── src/
│   ├── consult/
│   ├── execute/
│   ├── plan/
│   ├── specs/
│   ├── tests/
│   └── verify/
└── plans/
    └── YYYY-MM-DD-short-task-slug.md
```

Completed historical records also remain under `plans/`.

Each `src/<skill>/` directory ships `SKILL.md`, `agents/openai.yaml`, and
`evals/evals.json`. `plan` and `specs` also ship local assets, and `execute`
ships the optional `scripts/loop.py` helper.

In this source repo, `.agents/skills` resolves to the same files through the
tracked symlink mirror. Edit `src/`; use the mirror only when you need
copied-layout paths locally.

## Six-Skill Workflow

- `specs`: bootstrap or sync repo truth when `AGENTS.md`, `specs/`, or owning
  guidance is missing, stale, or too weak for safe work
- `tests`: bootstrap or sync test truth when coverage is missing, stale, or
  clearly below what safe execution and verification need
- `consult`: clarify the safest next move when the work is not yet clear enough
  to execute or plan
- `plan`: create or maintain one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` file when work needs durable state
- `execute`: implement one bounded task directly or one bounded slice from one
  explicit plan file, using the current plan context to stay bounded and
  resumable, then run the smallest meaningful checks
- `verify`: adversarially review a concrete plan, implementation slice, diff,
  or claim, return findings first, and in plan-driven work write the review
  back into the same explicit plan file so repairable failures can reopen or
  append bounded follow-up work

## Target Repo Flow

1. Copy the shipped skill directories from `src/` into `.agents/skills/` in
   the target repo.
2. Run `specs` when repo truth is weak, missing, stale, or blocking safe work.
3. Run `tests` when test truth is weak, missing, stale, or clearly below what
   the repo needs.
4. Run `consult` when the next move is not yet clear.
5. If the task is still locally clear and bounded, use `execute` directly,
   then run `verify`.
6. If the work needs durable task state, use `plan` and create or update one
   explicit `plans/YYYY-MM-DD-short-task-slug.md` path.
7. In plan-driven work, run `verify` on the plan, then run `execute` against
   that exact path, update the plan after the slice, and hand back to
   `verify` so the verification findings stay in that same canonical task
   record.
8. If you want one opt-in helper run to carry repairable verify failures and a
   strict final completion review, use
   `python3 src/execute/scripts/loop.py --yes --continue-after-fail ...`
   against that same explicit plan path.
9. In this source repo, if you want the same flow through the local Codex CLI
   without restating the generic helper defaults each time, use
   `python3 src/execute/scripts/providers/codex_loop.py --plan ...`.
   That wrapper is a repo-local convenience layer only; the generic contract
   still lives in `src/execute/scripts/loop.py`.
10. If you want a terminal dashboard over that same Codex flow in this source
    repo, use
    `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plan ...`.
    That dashboard is presentation only. It falls back to the raw Codex
    wrapper output when the dashboard is unsuitable, and `--plain` bypasses it
    explicitly.

Keep provider features such as plan modes, subagents, plugins, or auto-memory
optional only. The baseline workflow should work from repo files plus a normal
interactive session.

## Evaluation Harness

- Each skill owns tracked eval intent under `src/<skill>/evals/evals.json`.
- `evals/runtime.json` pins the canonical default profile and machine-readable
  governance settings.
- `evals/fixtures/cryptoli.json` pins the first shared real-repo fixture.
- `evals/scripts/harness.py` validates the tracked harness surface and
  scaffolds repeatable workspaces under `.tmp/evals/<run-id>/`.
- Generated outputs stay under `.tmp/evals/`; do not commit them.
- The current harness validates and scaffolds. It does not execute model calls
  or grade runs automatically.

## Maintenance Surface

- `make help`
- `make validate`
- `make eval-init-run RUN_ID=<run-id> [SELECTION=must-run|validation|all] [SKILL="consult execute"] [PROFILE=<profile>]`
- `python3 evals/scripts/harness.py --help`
- `python3 evals/scripts/harness.py validate`
- `python3 src/execute/scripts/loop.py --help`
- `python3 src/execute/scripts/loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"`
- `python3 src/execute/scripts/loop.py --yes --continue-after-fail --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"`
- `python3 src/execute/scripts/providers/codex_loop.py --help`
- `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/<file>.md`
- `python3 src/execute/scripts/providers/codex_loop.py --plan plans/<file>.md`
- `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plan plans/<file>.md`
- `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --plan plans/<file>.md`

See `MAINTENANCE.md` for the operator loop and `SOURCES.md` for the durable
reference grounding.

## Historical Records

Completed historical plan records remain in the repo under `plans/`. Keep them
available for background context, but do not treat them as the default reading
path for current repo work.
