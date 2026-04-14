# skills

Provider-agnostic agent skills for end-to-end repository work.

The goal of this repo is not to store prompts. It is to define a portable
workflow you can bring to any codebase:

- provider = runtime shell
- model = intelligence level
- skills = workflow
- repo files = durable state

Manually copy the shipped skill directories from this repo into
`.agents/skills/` in any target repo and invoke them from a normal interactive
session with the strongest model and effort setting you want. The workflow
should not depend on provider plan modes, plugins, auto-memory, or any other
client-specific feature.

Current shipped skills are:

- `consult`
- `plan`
- `specs`
- `tests`
- `verify`

Planned next skill is:

- `execute`

Until `execute` ships, this repo uses the shipped `plan` skill plus explicit
`plans/*.md` files and [PROMPT_execute.md](./PROMPT_execute.md) plus
[PROMPT_verify.md](./PROMPT_verify.md) to emulate the plan-driven execution
loop in fresh sessions.

The intended six-skill end-state is:

- `specs`
- `tests`
- `consult`
- `plan`
- `execute`
- `verify`

See [TODO.md](./TODO.md) for the implementation roadmap.

## Durable State

- `AGENTS.md` and `specs/` = repo truth
- tests = executable truth
- `plans/*.md` = task truth
- code = implemented reality

The repo should stay in a state where a fresh agent can get oriented quickly,
find the right code paths, and make correct changes with the highest practical
chance of success.

## Refresh Workflow

The authoritative refresh-workflow contract lives in `AGENTS.md`.

- Current default: manually copy the shipped skill directories from this repo
  into `.agents/skills/` in the target repo.
- Refresh by re-copying only the skill directories and supporting assets that
  changed here.
- Treat install helpers, git subtree wiring, and provider-specific plugins as
  optional future accelerators, not baseline workflow requirements.

## Skill Roles

### `specs`

Owns repo truth.

- bootstrap and sync `AGENTS.md`, `CLAUDE.md` symlink, and `specs/`
- evaluate codebase organization quality for agentic work
- improve boundaries, naming, navigability, and discoverability when the
  current structure reduces agent reliability
- keep durable architecture and domain truth aligned with code reality

### `tests`

Owns test truth.

- bootstrap or extend the test layers that make sense for the repo
- sync tests with changed behavior over time
- keep coverage honest across unit, integration, e2e, smoke, security,
  performance, and other applicable layers

### `consult`

Owns research and clarification.

- start from exploration, not blind implementation
- understand the current code and specs
- compare options, risks, and tradeoffs
- recommend the safest next move
- hand off to `plan` only when durable task state is needed after the direction
  is already clear

### `plan`

Owns living task plans.

- trigger when work needs durable state across sessions, milestones, review
  loops, or fresh-session restarts
- do not trigger for simple lookups, short clarification, or bounded
  implementation that is still locally clear
- do not trigger only because a task sounds large; promote based on the need
  to preserve task state
- start once the next move is clear enough to structure execution
- own task-local plan files only, not durable repo truth or implementation
- create or update one explicit `plans/YYYY-MM-DD-short-task-slug.md` path
- create the `plans/` directory when missing
- make `specs` and `tests` follow-through explicit inside the plan: owning or
  missing specs, applicable test layers, and when sync is required
- make each plan resumable from repo truth plus the plan file alone
- hold milestones, verification, discoveries, decisions, blockers, and progress
- hand off to `execute` and `verify` with that explicit plan path

### `execute` (planned)

Will own implementation after it ships.

- trigger when the user wants implementation now and either the task is still
  locally clear or there is already one explicit `plans/*.md` path to execute
- do not use when the next move still needs clarification, tradeoff analysis,
  or a recommendation; use `consult`
- do not use when the work now needs durable task state but no explicit plan
  file exists yet; use `plan`
- do not use for adversarial sign-off, fact-checking, or final judgment; use
  `verify`
- direct mode: implement a bounded task only when it is still locally clear and
  does not need durable task state
- if direct-mode work stops being locally clear or starts needing durable task
  state, stop and hand off to `plan` rather than improvising a hidden plan in
  chat
- plan-driven mode: implement only from one explicit `plans/*.md` path from
  `plan`; never guess the latest plan file
- in plan-driven mode, implement only the next milestone or other bounded slice
  in a fresh session, then update the plan before stopping
- own implementation and bounded mechanical checks only; hand adversarial
  review back to `verify`
- take over after `plan` has produced an explicit path; do not own plan
  creation or task-shaping
- read repo truth before editing
- stop cleanly when blocked or when the session has become noisy enough to
  reduce reasoning quality

### `verify`

Owns adversarial review.

- verify plans before implementation
- verify implementation slices after coding
- verify final diffs or PRs as a code reviewer
- keep findings grounded in code, specs, tests, and command evidence

## Target 0 -> 100 Flow

This is the intended workflow after `execute` ships. Today this repo already
ships `plan`, but still bootstraps the plan-driven execution step with explicit
`plans/*.md` files and the bootstrap prompts in this repo.

1. Manually copy the shipped skill directories from `scripness/skills` into
   `.agents/skills/` in the repo you want to work on.
2. Run `specs` when repo truth is weak, missing, stale, or the codebase is not
   organized cleanly enough for reliable agent work.
3. Run `tests` when test truth is weak, missing, stale, or clearly below what
   the codebase needs.
4. Start every task with `consult` to understand the current code, relevant
   specs, options, and risks.
5. If the task is still bounded and does not need durable task state, use
   `execute` directly, then run `verify`.
6. If the task starts needing durable state across milestones, discoveries,
   review loops, or restarts, run `plan` and create or update one explicit
   `plans/YYYY-MM-DD-short-task-slug.md` path.
   Promote based on durable-state need, not abstract task size, and skip
   `plan` when the work is still locally clear enough to execute directly.
7. Run `verify` on the plan before implementation when the task is plan-driven.
8. Start a fresh session and invoke `execute` against that exact plan path.
   Implement only the next milestone or bounded slice.
9. After each slice, update the plan with progress, discoveries, decisions,
   blockers, verification results, and any changed `specs` or `tests`
   follow-through.
10. If the session leaves the smart working zone, stop, persist truth to the
    plan, and restart from a fresh session rather than relying on compaction or
    chat memory.
11. Run `verify` again on the implementation slice and once more on the final
    diff or PR.
12. Run `specs` and `tests` again when durable repo truth or test truth has
    changed.

## Working Style

- Prefer repo files over chat memory.
- Keep `AGENTS.md` concise and operational.
- Keep durable subsystem truth in `specs/`, not task plans.
- Keep task-local state in `plans/*.md`, not in long conversations.
- Use provider features such as plan modes or subagents only as optional
  accelerators, never as workflow requirements.
- Prefer fresh sessions for serious plan-driven execution.

## Example Invocation Pattern

The `execute` example below describes the target workflow after that skill
ships. Today this repo already ships `plan`, but still bootstraps
plan-driven implementation with explicit plan files plus
[PROMPT_execute.md](./PROMPT_execute.md) and
[PROMPT_verify.md](./PROMPT_verify.md).

Bootstrap repo truth:

```text
Use specs.
Prepare this repo for reliable agentic work.
Create or sync AGENTS.md, specs/, and any missing repo-truth guidance.
Evaluate whether the codebase organization is clean enough for agents.
```

Bootstrap test truth:

```text
Use tests.
Audit the current test layers and bring them up to the level this repo needs.
```

Research a task:

```text
Use consult.
Read the repo, relevant specs, and tests.
Clarify the safest next move for <task>.
```

Write a plan:

```text
Use plan.
The direction is already clear, but this work now needs durable task state
across sessions, milestones, or review loops.
Create or update plans/2026-04-14-short-task-slug.md.
Do not promote based on task size alone.
Make it a self-contained living task plan that a fresh session can resume from.
```

Execute directly:

```text
Use execute.
Read AGENTS.md, relevant specs, tests, and the current code.
Implement <bounded task> directly because it is still locally clear and does
not need durable task state.
Run the smallest meaningful mechanical checks, sync specs/tests if the work
changed durable truth, then stop and hand off to verify.
```

Execute from a plan:

```text
Use execute.
Read AGENTS.md, relevant specs, tests, and
plans/2026-04-14-short-task-slug.md.
Implement only the next milestone or other bounded slice from that exact plan
path.
Update the plan with progress, discoveries, decisions, blockers, verification
notes, and any required specs/tests follow-through before stopping.
```

Review the work:

```text
Use verify.
Review the plan, implementation, or final diff against repo truth and tests.
Findings first.
```
