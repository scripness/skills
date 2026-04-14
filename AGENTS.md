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
- `plan`
- `specs`
- `tests`
- `verify`

Planned next skill:

- `execute`

Current roadmap:
- [TODO.md](TODO.md)

Current execution plans for building the missing system:
- [plans/2026-04-14-phase-01-plan-skill-and-contract.md](plans/2026-04-14-phase-01-plan-skill-and-contract.md)
- [plans/2026-04-14-phase-02-execute-skill.md](plans/2026-04-14-phase-02-execute-skill.md)
- [plans/2026-04-14-phase-03-consult-and-verify-refresh.md](plans/2026-04-14-phase-03-consult-and-verify-refresh.md)
- [plans/2026-04-14-phase-04-specs-and-tests-refresh.md](plans/2026-04-14-phase-04-specs-and-tests-refresh.md)
- [plans/2026-04-14-phase-05-evaluation-harness.md](plans/2026-04-14-phase-05-evaluation-harness.md)
- [plans/2026-04-14-phase-06-tooling-and-final-docs.md](plans/2026-04-14-phase-06-tooling-and-final-docs.md)

Temporary fresh-session prompts for executing that roadmap:
- [PROMPT_execute.md](PROMPT_execute.md)
- [PROMPT_verify.md](PROMPT_verify.md)

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

In this repo, the skills live at the repo root:

- [consult/SKILL.md](consult/SKILL.md)
- [plan/SKILL.md](plan/SKILL.md)
- [specs/SKILL.md](specs/SKILL.md)
- [tests/SKILL.md](tests/SKILL.md)
- [verify/SKILL.md](verify/SKILL.md)

When these skills are copied into a target repo, they are intended to live
under `.agents/skills/`.

## Target-Repo Refresh Workflow

`AGENTS.md` owns the authoritative refresh-workflow contract for this repo.

- Use manual copy as the initial distribution and refresh workflow.
- Copy the shipped skill directories from this repo into `.agents/skills/` in
  the target repo.
- Refresh a target repo by re-copying the skill directories and supporting
  assets that changed here.
- Keep install helpers, subtree wiring, and provider-specific plugins optional
  future accelerators only; they are not baseline workflow requirements.

Use the current shipped skills as follows:

- `consult`: clarify repo direction, workflow design, tradeoffs, and roadmap
  decisions before implementation.
- `plan`: create or maintain living task plans when work needs durable state
  across sessions, milestones, review loops, or fresh-session restarts.
- `specs`: bootstrap or sync repo truth when `AGENTS.md`, spec assets, or
  durable workflow docs drift from the shipped system.
- `tests`: bootstrap or sync executable truth when this repo starts gaining real
  validators, eval runners, or other testable behavior.
- `verify`: adversarially review plans, docs, implementation, and claimed
  workflow behavior.

Until `execute` is shipped, use the phase plans, the shipped `plan` skill, and
`PROMPT_execute.md` plus `PROMPT_verify.md` to emulate the future
plan-driven execution workflow in fresh sessions.

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

Planned `execute` contract for this repo:

- `execute` owns implementation and bounded mechanical checks only; `verify`
  owns adversarial review
- direct mode is only for bounded work that is still locally clear and does not
  need durable task state
- plan-driven mode must start from one explicit `plans/*.md` path produced by
  `plan`; never guess the latest plan file
- in plan-driven mode, implement only one milestone or other bounded slice in a
  fresh session, then update the plan before stopping
- hand off explicitly to `verify` after each slice rather than absorbing review
  behavior into `execute`

## Working Loop For This Repo

When working on the roadmap:

1. Read `AGENTS.md`, `TODO.md`, and the active phase plan.
2. Use a fresh session per bounded milestone or slice.
3. Use [PROMPT_execute.md](PROMPT_execute.md) with the explicit plan path for
   implementation while `execute` is still not shipped here.
4. Use [PROMPT_verify.md](PROMPT_verify.md) with the same plan path for review.
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
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── README.md
├── TODO.md
├── PROMPT_execute.md
├── PROMPT_verify.md
├── consult/
├── plan/
├── specs/
├── tests/
├── verify/
└── plans/
```

Bootstrap assets live under `specs/assets/`.

## Commands

There is currently no package manifest, CI, or formal test runner in this repo.
Most work today is docs and skill-definition work.

Useful local commands:

| Purpose | Command |
|---------|---------|
| List files | `rg --files .` |
| Search text | `rg "pattern" .` |
| Inspect roadmap | `sed -n '1,260p' TODO.md` |
| Inspect active plan | `sed -n '1,220p' plans/<file>.md` |
| Check git status | `git status --short` |

If a phase introduces executable helpers or eval runners, document the exact
commands here and keep them current.

## Conventions

- Keep `AGENTS.md` concise and operational.
- Keep durable roadmap and contract truth in `TODO.md` and `README.md`.
- Keep phase-local state in `plans/*.md`.
- Keep temporary plan-driven execution protocol in `PROMPT_execute.md` and
  `PROMPT_verify.md` until the real `execute` skill ships.
- Use ASCII by default.
- Prefer proportional edits over broad rewrites.

## Git

Do not amend or rewrite history unless explicitly requested.
Do not revert unrelated user changes.
