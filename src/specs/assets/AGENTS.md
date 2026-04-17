# [Project Name]

[One sentence describing the product and stack.]

## Specifications

**IMPORTANT:** Before implementing any feature, consult the specifications in
[specs/README.md](specs/README.md).

- **Assume NOT implemented.** Specs may describe planned or desired behavior
  that is not yet present in code.
- **Check the codebase first.** Specs describe intent; code describes reality.
- **Use specs as guidance.** Follow the relevant spec's patterns, types,
  boundaries, and terminology when implementing work in that area.
- **Treat specs as durable system truth.** They document stable domain and
  architecture rules, not task-by-task execution plans.

## Local Agent Toolbox

This repo uses the local `.agents/skills/` directory as its provider-agnostic
agent toolbox and workflow layer.

- Use `.agents/skills/specs/SKILL.md` when repo truth is missing or stale:
  missing `AGENTS.md`, missing `specs/`, missing owning spec for the current
  task, stale spec guidance, stale `specs/README.md`, repo topology that is
  poorly documented, or repo-wide operating guidance that no longer matches
  reality.
- Use `.agents/skills/tests/SKILL.md` when changed behavior is not clearly
  covered by the repo's existing test layers, when the test topology is weak
  or stale, or when tests have drifted from current code behavior.
- Use `.agents/skills/consult/SKILL.md` when ambiguity, architecture, tradeoffs,
  or unclear repo behavior block safe implementation.
- Use `.agents/skills/plan/SKILL.md` when the work needs durable task state
  across milestones, review loops, blockers, or fresh-session restarts.
- Use `.agents/skills/execute/SKILL.md` when the implementation is still
  locally clear or there is already one explicit `plans/*.md` file to execute.
- Use `.agents/skills/verify/SKILL.md` as the adversarial review and final
  verification step for plans, implementation slices, diffs, or technical
  claims.

Agents may invoke `consult` and `verify` proactively when the trigger
conditions are met. Treat `specs` and `tests` as manual-first, but invoke them
when missing or stale repo truth, weak topology guidance, or missing test truth
is clearly blocking safe planning, execution, or verification. Promote to
`plan` only when the work needs durable task state. Use `execute` for bounded
implementation work, not long-lived task planning or final judgment.

## Commands

| Purpose | Command |
|---------|---------|
| Dev | `[exact dev command]` |
| Build | `[exact build command]` |
| Test | `[exact full test command]` |
| Test one | `[smallest useful targeted test command]` |
| Typecheck | `[exact typecheck command]` |
| Lint | `[exact lint command]` |
| Format | `[exact format command]` |
| Migrate | `[migration command if applicable]` |

Fill these first:

- exact dev/build/test/typecheck/lint commands
- repo topology, ownership boundaries, and architecture tree
- generated, vendor, cache, and copied-artifact paths agents should ignore
- specs index
- testing layers, owning suite roots, shared helpers, and targeted commands

## Boundaries

**Always:** Search the codebase before adding new code. Run the required checks
before marking work done. Write or update tests at every applicable tier.

**Ask first:** Changes to `specs/` or `AGENTS.md`. Changes affecting multiple
apps, packages, or services. Major dependency upgrades. New packages, modules,
or services.

**Never:** Commit secrets or `.env` files. Push directly to `main`. Modify
generated files or migrations by hand unless the project explicitly requires it.

## Architecture

Document the real repo topology, not an assumed single-app layout. Capture the
top-level owning apps, packages, services, and shared systems that agents need
to navigate, and call out any major generated or vendor trees that should not
drive repo guidance.

```text
[top-level structure, 8-12 entries max]
```

Entrypoints: `[main app or service entrypoints]` | Config roots:
`[config locations]` | Schemas/migrations: `[schema or migration locations if
applicable]` | Generated/vendor roots to ignore: `[paths or n/a]`

## Conventions

Only include non-obvious rules an agent would not reliably infer from code.

- **[Category]** [specific rule]
- **[Category]** [specific rule]
- **[Category]** [specific rule]

## Specs Index

> When working on a topic below, read the corresponding spec before changes.

| When you're working on... | Read |
|---------------------------|------|
| [topic area] | `specs/[file].md` |
| [topic area] | `specs/[file].md` |
| [topic area] | `specs/[file].md` |

Full index with summaries: [specs/README.md](specs/README.md)

## Testing

Document only the test layers the repo actually uses. A repo may have per-app,
per-package, per-service, or shared suites; do not invent a single shared test
root if the codebase does not have one.

| Layer | Owning path or suite root | Command | What it tests | When required |
|-------|----------------------------|---------|---------------|---------------|
| `[unit/integration/e2e/etc.]` | `[path or package]` | `[command]` | `[scope]` | `[when required]` |
| `[unit/integration/e2e/etc.]` | `[path or package]` | `[command]` | `[scope]` | `[when required]` |
| `[unit/integration/e2e/etc.]` | `[path or package]` | `[command]` | `[scope]` | `[when required]` |

List shared helpers, fixtures, factories, and app-specific testing rules here.
Add non-standard layers here too: smoke, browser, contract, visual,
performance, security, or CI-only checks if the repo uses them. Note any
generated, vendor, cache, or coverage-report paths that should not be treated
as owning test surfaces.

## Git

Commit format: `[type(scope): description]`

Example: `feat(auth): add refresh token rotation`
