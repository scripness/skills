# Maintenance

This repo is the upstream source of truth for the shipped six-skill workflow.
Use this guide to update skills, refresh local eval workspaces, and upstream
durable improvements discovered while using copied skills in downstream repos.

## Scope

- Keep this repo focused on provider-agnostic skills, shared skill assets,
  tracked eval metadata, thin maintenance tooling, and the docs that describe
  the shipped workflow.
- Do not add required orchestration, provider-specific workflow truth, or
  downstream-repo-specific assumptions here.
- Keep `.agents/` plus `AGENTS.md` as the authoritative cross-client surface.

## Durable State

- `AGENTS.md` and a target repo's `specs/` = repo truth
- tests = executable truth
- `src/<skill>/evals/evals.json` and `evals/` = tracked eval truth
- `plans/*.md` = task truth
- code = implemented reality
- `.tmp/evals/` = generated local run artifacts

## Update Loop

1. Change the owning skill or doc paths directly:
   `src/<skill>/SKILL.md`, `src/<skill>/agents/openai.yaml`, local assets,
   `src/<skill>/evals/evals.json`, `README.md`, `AGENTS.md`, `evals/README.md`,
   or this file as needed.
2. Keep boundaries sharp. Durable workflow truth belongs in repo docs and
   skills, not in shell wrappers or chat-only instructions.
3. If shipped behavior changed, sync the owning docs in the same slice before
   you call the work done.
4. Run the smallest meaningful local checks for the changed surface.
5. If the slice changes a skill, eval definition, or maintenance behavior,
   scaffold a fresh eval workspace and review the generated artifacts.
6. Record discoveries, decisions, blockers, and verification in the active
   plan or other durable change record before stopping.

## Local Operator Surface

- `make help`
  Lists the thin repo-level maintenance targets.
- `make validate`
  Runs repo-level validation for shipped skill structure, frontmatter, local
  asset integrity, tracked eval definitions, fixture manifests, runtime
  metadata, must-run selection, and `.tmp/evals/` ignore coverage.
- `make eval-init-run RUN_ID=<run-id> [SELECTION=must-run|validation|all] [SKILL="consult execute"] [PROFILE=<profile>]`
  Scaffolds `.tmp/evals/<run-id>/` through `evals/scripts/harness.py` without
  duplicating harness logic in the wrapper.
- `python3 evals/scripts/harness.py --help`
  Shows the direct harness interface behind the Makefile wrappers.
- `python3 evals/scripts/harness.py validate`
  Runs the same validation surface without going through `make`.
- `python3 evals/scripts/harness.py init-run --run-id <run-id> --selection must-run`
  Scaffolds a direct run workspace when you want the harness entrypoint
  instead of the Makefile wrapper.
- `python3 src/execute/scripts/loop.py --help`
  Shows the optional plan-driven helper contract shipped with `src/execute/`.
- `python3 src/execute/scripts/loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"`
  Dry-runs the optional execute/verify loop helper against one explicit plan
  path and one explicit external runner.
- `python3 src/execute/scripts/loop.py --yes --continue-after-fail --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"`
  Runs the opt-in continuous helper mode that may continue after repairable
  verify failures and requires a strict final verify pass before success.
- `python3 src/execute/scripts/providers/codex_loop.py --help`
  Shows the optional repo-local Codex convenience wrapper around the generic
  helper.
- `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/<file>.md`
  Dry-runs the repo-local Codex wrapper while keeping its default provider
  command and continuous-mode settings visible.
- `python3 src/execute/scripts/providers/codex_loop.py --plan plans/<file>.md`
  Runs the repo-local Codex wrapper with its default real-run behavior:
  implicit `--yes`, implicit `--continue-after-fail`, and an internal runner
  that uses `codex exec --yolo` as shorthand for dangerous bypass.
- `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plan plans/<file>.md`
  Runs the repo-local Codex dashboard wrapper over the same Codex flow while
  keeping loop control and plan truth in the underlying helpers.
- `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --plan plans/<file>.md`
  Bypasses the dashboard explicitly and forwards straight to the raw Codex
  wrapper surface. The dashboard wrapper also falls back automatically when
  stdout is not a TTY.

## Eval Refresh

- Treat `make eval-init-run` and `python3 evals/scripts/harness.py init-run`
  as scaffolding commands only. They create a repeatable workspace, but they
  do not execute model calls, grade runs, or accept changes automatically.
- Choose a descriptive `RUN_ID` and keep generated outputs under
  `.tmp/evals/<run-id>/`.
- Start artifact review from the generated `review-template.md`, then inspect
  outputs, transcripts, and other generated files before accepting a skill
  change.
- Compare against the previous committed version of the same skill by default.
  Add a no-skill baseline only when it adds real signal.
- Do not commit generated eval artifacts. Refresh them locally as needed.

## Upstreaming Downstream Discoveries

- When copied skills reveal a durable workflow gap in another repo, upstream
  the portable fix here first if it should apply across repos.
- Upstream only portable truth: skill instructions, shared assets, eval
  definitions, thin maintenance tooling, and repo docs.
- Do not encode downstream-specific stack details or one-off project habits as
  shared workflow truth in this repo.
- After upstreaming a portable fix here, refresh downstream repos by re-copying
  only the changed skill directories and supporting assets into
  `.agents/skills/`.
