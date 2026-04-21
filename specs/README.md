# skills Specifications

This spec set covers the shipped repo contract for the provider-agnostic
six-skill workflow, the repo surface that carries it, and the shared
evaluation harness around it.

## How To Use These Specs

- Read the relevant spec before changing repo-wide workflow, source skill
  layout, or the evaluation harness.
- Treat these specs as durable topic truth and the checked-in files under
  `src/`, `evals/`, `Makefile`, and the top-level docs as implemented reality.
- Keep task-local execution details in explicit `plans/*.md` files, not in
  these specs.
- Completed historical plan records under `plans/` are background records, not
  default operational truth.
- Update this index when specs are added, renamed, or materially repurposed.

## Product And Domain

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`workflow-contract.md`](./workflow-contract.md) | `AGENTS.md`, `README.md`, `MAINTENANCE.md`, `SOURCES.md`, `src/*/SKILL.md` | Defines the shipped six-skill workflow, truth layers, refresh workflow, and plan semantics for this repo. |

## Architecture And Shared Systems

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`repo-surface.md`](./repo-surface.md) | `src/`, `plans/`, `CLAUDE.md`, top-level repo docs | Maps the actual repo layout, skill directory structure, helper placement, and the distinction between live task plans and completed historical records. |

## Quality And Operations

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`evaluation-harness.md`](./evaluation-harness.md) | `src/*/evals/evals.json`, `evals/`, `Makefile`, `.tmp/evals/` | Defines the tracked eval layout, runtime and fixture metadata, generated artifact boundaries, and the thin validation/scaffolding surface. |
