# skills

Provider-agnostic source repo for the shipped six-skill workflow.

This repo is not an application. It stores portable workflow truth, source
skill payloads, shared eval metadata, and thin local helpers that can be
copied into other repos.

## Start Here

Read this repo from shipped reality in this order:

1. `AGENTS.md`
2. `specs/README.md` and the relevant `specs/*.md`
3. `README.md`
4. `docs/maintenance.md` and `docs/sources.md` when the task needs operator
   guidance or design grounding
5. the shipped surfaces under `src/`, `evals/`, `Makefile`, and
   `src/execute/scripts/loop.py`
6. `plans/*.md` only when a task names an explicit plan path or when you need
   historical background

Code and checked-in files are reality. Docs must stay synced to the shipped
surface.

The shipped `src/*/SKILL.md` files are the workflow source of truth. Helper
scripts in `src/execute/scripts/` may standardize invocation, exit-code
mapping, machine-readable events, or terminal presentation, but they must not
become a competing workflow contract.

This source repo also tracks `.agents/skills -> ../src` as a local symlink
mirror so copied-layout paths can be exercised without duplicating files.
Edit the owning files under `src/`; do not treat the mirror as a second truth
layer.

## Repo Truth

- `AGENTS.md` = repo-wide operational truth
- `specs/` = durable topic truth for this repo
- `README.md` = overview and usage surface
- `docs/maintenance.md` = operator loop for updates and eval refresh
- `docs/sources.md` = durable external grounding
- `plans/*.md` = task-local plans for new work, a small number of tracked
  plan-shaped eval fixtures, plus completed historical build records
- `src/` = source-of-truth skill payloads
- `.agents/skills/` = local symlink mirror of `src/` for copied-layout checks;
  not an owning truth layer
- `evals/` = shared harness metadata and helper surface
- `.tmp/evals/` = generated local run artifacts; never treat them as tracked
  truth

Completed historical plan records remain under `plans/` as background
reference material, not default operational reading.

## Local Agent Toolbox

The shipped source skills live under `src/`:

- `src/consult/`
- `src/execute/`
- `src/plan/`
- `src/specs/`
- `src/tests/`
- `src/verify/`

This source repo also exposes the same skill tree through `.agents/skills/`
via the tracked `skills -> ../src` symlink mirror. `src/` remains
authoritative.

When copied into a target repo, these directories are intended to live under
`.agents/skills/`.

## Shipped Surface

- Each skill directory ships `SKILL.md`, `agents/openai.yaml`, and
  `evals/evals.json`.
- `src/plan/` also ships `assets/plan-template.md`.
- `src/specs/` also ships bootstrap assets for `AGENTS.md` and `specs/`.
- `src/execute/` also ships `scripts/loop.py` as an optional explicit-plan
  execute/verify helper with an opt-in continuous repair mode and strict final
  review before success.
- This source repo also ships `scripts/providers/codex_loop.py` as an optional
  repo-local Codex convenience wrapper that delegates back to the generic
  `scripts/loop.py` contract. It is a local accelerator only, not workflow
  truth.
- This source repo also ships
  `scripts/providers/codex_loop_dashboard.py` as an optional repo-local
  terminal dashboard for the Codex wrapper. It is presentation only and falls
  back to the raw wrapper output when the dashboard is unsuitable.
- `evals/runtime.json` pins the default runtime profile and machine-readable
  governance settings for the shared eval harness.
- `evals/fixtures/cryptoli.json` pins the first real-repo fixture manifest.
- `evals/scripts/harness.py` validates tracked harness truth and scaffolds
  `.tmp/evals/<run-id>/`.
- `Makefile` is a thin wrapper over the harness helper.
- `.agents/skills -> ../src` is a tracked local convenience mirror for copied
  layout testing only.
- `CLAUDE.md` must remain a thin symlink mirror to `AGENTS.md`.

## Skill Roles

- `consult`: clarify current behavior, viable options, risks, and the safest
  next move when the work is not yet clear enough to execute or plan.
- `execute`: implement one bounded task directly or one bounded slice from one
  explicit plan path, read the current plan context before choosing the slice,
  run the smallest meaningful checks, complete required `specs` or `tests`
  follow-through, update the plan in place, and hand off to `verify`.
- `plan`: create or maintain one explicit
  `plans/YYYY-MM-DD-short-task-slug.md` file when durable task state is needed
  across sessions, milestones, or review loops.
- `specs`: bootstrap or sync repo truth when `AGENTS.md`, `specs/`, or other
  durable guidance is missing, stale, or too weak for safe work.
- `tests`: bootstrap or sync executable truth when test coverage is missing,
  stale, or clearly below what safe execution and verification require.
- `verify`: adversarially judge one concrete plan, implementation slice, diff,
  or claim; when verifying an explicit plan file, write the review back to that
  same plan file so it remains the canonical task record; reopen or append one
  bounded follow-up slice when review disproves completion but the work remains
  repairable; return findings first; treat missing required `specs` or `tests`
  sync as `fail` when the obligation is clear.

Keep generic `plans/*.md` references where they are part of the shipped
`plan` and `execute` contracts. Never guess the latest plan file.

## Refresh Workflow

- Use manual copy as the default distribution and refresh workflow.
- Copy the shipped skill directories from `src/` into `.agents/skills/` in the
  target repo.
- In this source repo, keep using `src/` as the owning surface; the local
  `.agents/skills` mirror is convenience only.
- Refresh downstream repos by re-copying only the changed skill directories
  and supporting assets.
- Treat install helpers, git subtree wiring, provider-specific plugins, and
  other automation as optional accelerators only.

## Architecture

```text
.
├── .agents/
│   └── skills -> ../src
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── README.md
├── docs/
│   ├── maintenance.md
│   └── sources.md
├── specs/
├── evals/
│   ├── README.md
│   ├── fixtures/
│   ├── runtime.json
│   └── scripts/
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

Bootstrap assets for target-repo truth live under `src/specs/assets/`.
Generated eval outputs live under ignored `.tmp/evals/`.
Completed historical records also remain under `plans/`.

## Commands

| Purpose | Command |
|---------|---------|
| List files | `rg --files .` |
| Search text | `rg "pattern" .` |
| Read the specs index | `sed -n '1,220p' specs/README.md` |
| Show the repo maintenance targets | `make help` |
| Validate shipped skill metadata and eval invariants | `make validate` |
| Scaffold a repeatable eval workspace | `make eval-init-run RUN_ID=<run-id> [SELECTION=must-run\|validation\|all] [SKILL="consult execute"] [PROFILE=<profile>]` |
| Show the direct harness CLI | `python3 evals/scripts/harness.py --help` |
| Run validation directly | `python3 evals/scripts/harness.py validate` |
| Show the optional loop helper | `python3 src/execute/scripts/loop.py --help` |
| Dry-run the optional loop helper | `python3 src/execute/scripts/loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"` |
| Run the optional continuous loop helper | `python3 src/execute/scripts/loop.py --yes --continue-after-fail --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"` |
| Show the optional Codex loop wrapper | `python3 src/execute/scripts/providers/codex_loop.py --help` |
| Dry-run the optional Codex loop wrapper | `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/<file>.md` |
| Run the optional Codex loop wrapper | `python3 src/execute/scripts/providers/codex_loop.py --plan plans/<file>.md` |
| Run the optional Codex loop dashboard | `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plan plans/<file>.md` |
| Bypass the dashboard and use the raw Codex wrapper | `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --plan plans/<file>.md` |
| Check git status | `git status --short` |

## Boundaries

Always:

- keep this repo provider-agnostic
- keep docs synced to the shipped files under `src/`, `evals/`, `Makefile`,
  and repo docs
- keep `AGENTS.md` concise and put durable topic truth in `specs/`
- keep skill boundaries sharp
- keep active task state in one explicit plan file when work becomes
  plan-driven
- keep completed historical build records available as background unless there
  is a deliberate later archive change

Ask first:

- broad workflow changes that alter the six-skill model
- required orchestration, automation, or provider-specific workflow primitives
- moving, deleting, or rewriting the completed historical build records under
  `plans/`
- gating or fixture-policy changes that broaden the eval contract

Never:

- treat plan modes, plugins, auto-memory, or other client-specific features as
  required workflow primitives
- guess the latest plan file in plan-driven work
- let docs claim shipped behavior that the repo does not implement
- commit generated `.tmp/evals/` artifacts

## Conventions

- Use ASCII by default.
- Prefer proportional edits over broad rewrites.
- Keep durable repo truth in `specs/` and task-local state in `plans/*.md`.
- Keep `README.md` focused on shipped-system truth, not historical build
  narration.

## Git

Do not amend or rewrite history unless explicitly requested.
Do not revert unrelated user changes.
