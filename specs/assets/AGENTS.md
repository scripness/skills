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

- Use `.agents/skills/consult/SKILL.md` when ambiguity, architecture, or
  tradeoffs block progress, or when a task benefits from independent
  multi-angle analysis before implementation.
- Use `.agents/skills/verify/SKILL.md` as a review and final verification step
  for plans, implementations, or technical claims.
- Use `.agents/skills/specs/SKILL.md` when repo truth is missing or stale:
  missing `AGENTS.md`, missing `specs/`, missing owning spec for the current
  task, stale spec guidance, stale `specs/README.md`, or repo-wide operating
  guidance that no longer matches reality.
- Use `.agents/skills/tests/SKILL.md` when changed behavior is not clearly
  covered by the repo's existing test layers or when tests have drifted from
  current code behavior.

Agents may invoke `consult` and `verify` proactively when the trigger
conditions are met. Treat `specs` and `tests` as manual-first, but invoke them
when missing or stale repo truth is clearly blocking good work or safe
verification.

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
- repo boundaries
- architecture tree
- specs index
- testing tiers and shared helpers

## Boundaries

**Always:** Search the codebase before adding new code. Run the required checks
before marking work done. Write or update tests at every applicable tier.

**Ask first:** Changes to `specs/`. Changes affecting multiple apps or services.
Major dependency upgrades. New packages or modules.

**Never:** Commit secrets or `.env` files. Push directly to `main`. Modify
generated files or migrations by hand unless the project explicitly requires it.

## Architecture

```text
[top-level structure, 8-12 entries max]
```

Entry: `[main entrypoint]` | Config: `[config location]` | Schema:
`[schema location if applicable]`

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

Document the test tiers the repo actually uses.

| Tier | Location | What it tests | When required |
|------|----------|---------------|---------------|
| Unit | `[path]` | `[scope]` | `[when required]` |
| Integration | `[path]` | `[scope]` | `[when required]` |
| E2E | `[path]` | `[scope]` | `[when required]` |

List shared helpers, fixtures, factories, and app-specific testing rules here.
Add non-standard layers here too: smoke, browser, contract, visual,
performance, or CI-only checks if the repo uses them.

## Git

Commit format: `[type(scope): description]`

Example: `feat(auth): add refresh token rotation`
