---
name: specs
description: Bootstrap, sync, or repair repo truth in AGENTS.md and specs/ when current guidance is missing, stale, or too weak for safe work.
argument-hint: [task to prepare or area to sync]
---

Use this skill in three user-facing situations:

1. bootstrap a repo that is missing `AGENTS.md`, `specs/`, or both
2. sync `AGENTS.md` and `specs/` with current code reality
3. close repo-truth gaps that are blocking safe planning, execution, or
   verification even though the harness already exists

This skill may also be auto-invoked during implementation when the current task
is clearly blocked by weak or missing repo truth.

This skill replaces separate "write specs", "reverse engineer specs", and
"sync specs" workflows with one repo-truth skill.

Specs are durable domain and system truth for provider-native agents. They are
not task plans, execution plans, or TODO lists.

Treat repo-topology discovery and agentic-readiness assessment as part of
bootstrap, sync, and gap-close work. Before writing guidance, determine what
the repo actually owns, how it is organized, and which paths are real
source-of-truth versus generated or vendor noise.

This is the only skill that should create or modify the codebase harness layer:

- `AGENTS.md`
- `CLAUDE.md` symlink
- `specs/`

Bootstrap assets live alongside this skill in:

- `assets/AGENTS.md`
- `assets/specs/README.md`
- `assets/specs/spec-template.md`

## Inputs

- the user task, if there is one
- `AGENTS.md` if present
- `specs/README.md` and relevant `specs/*` if present
- current codebase and repo layout

## Process

1. Determine intent.
   - `bootstrap`: `AGENTS.md`, `specs/`, or core index docs are missing or too
     weak to support work
   - `sync`: docs may have drifted from code reality
   - `gap-close`: the harness exists, but key repo truth is too weak for safe
     planning, execution, or verification
   - if invoked automatically during a task, treat task-scoped fixes as part of
     syncing the repo truth needed for that work

2. Audit the current truth layer and repo shape.
   - Read `AGENTS.md`, `specs/README.md`, and the relevant `specs/*`.
   - Inspect the current codebase before drafting guidance.
   - Map the actual repo topology:
     - monorepo vs single package
     - `apps/`, `packages/`, `services/`, tools, or other top-level ownership
     - `src/` vs flat layouts
     - shared libraries, entrypoints, config roots, schemas, migrations, and
       other paths agents will need to navigate
   - Separate owning code and docs from non-owning trees. Ignore vendor,
     generated, or copied noise by default unless the task explicitly targets
     it:
     - `node_modules/`
     - package-manager stores and framework caches
     - build outputs such as `dist/`, `build/`, `.next/`, or coverage reports
     - vendored dependencies and copied artifacts
   - Evaluate whether the current organization is ready for reliable agent
     work:
     - boundaries between apps, packages, services, and shared code
     - naming clarity and ownership discoverability
     - navigability to the relevant code, commands, and specs
     - whether the current structure will mislead a fresh agent
   - Identify:
     - the owning spec(s)
     - stale claims
     - missing topic specs
     - stale `specs/README.md` entries
     - stale repo-wide operational guidance in `AGENTS.md`
     - related config, schema, CI, migration, or generated-artifact truth that
       affects what the docs should claim
     - related specs that mention the same subsystem or invariant
     - weak structure, unclear boundaries, or missing guidance that reduce the
       odds of safe agent execution

3. Consult before applying broad or ambiguous changes.
   - If the task is ambiguous, the area is poorly understood, or multiple
     interpretations are plausible, perform a short internal consultation.
   - Cover at least:
     - current behavior and structure
     - intended task impact
     - risks of writing the wrong spec or AGENTS guidance
   - If the provider supports independent passes, use them. Otherwise do this
     in one session.

4. Verify the intended updates before writing.
   - Check that the planned spec and AGENTS updates match code reality.
   - For non-trivial changes, adversarially check whether the update would
     introduce a stale or over-broad claim.

5. Update the truth layer.
   - Read `AGENTS.md` and `specs/README.md` first.
   - If `AGENTS.md` is missing, create it from `assets/AGENTS.md` and
     immediately specialize it to the repo's actual topology and commands.
   - Ensure `CLAUDE.md` points to `AGENTS.md` when the provider expects it.
   - If `specs/` is missing, create it from `assets/specs/README.md` and
     `assets/specs/spec-template.md`, then create the first topic specs needed
     for the codebase.
   - Bootstrap minimally: create only the docs needed to make safe work
     possible, not a speculative doc forest.
   - Refine an existing spec when the topic already exists.
   - Create a new topic spec when the area is not documented and the topic is
     large enough to deserve one.
   - Update `specs/README.md` when spec inventory, owning paths, or navigation
     guidance changes.
   - Update `AGENTS.md` only when repo-wide operational truth changed:
     commands, structure, topology, boundaries, testing policy, or
     conventions.
   - Make proportional organization improvements through the truth layer when
     the current repo shape is weakening agent reliability:
     - clarify ownership boundaries and navigation paths
     - document generated or vendor exclusions that should not drive guidance
     - add or repair indexes, maps, and cross-references that help a fresh
       agent get oriented
     - surface structural risks honestly when documentation alone cannot fully
       fix the problem
   - Do not silently reorganize product code or invent a large doc system
     unless the repo clearly needs it and the user asked for that scope.

6. Keep specs useful for agents.
   - topology-aware rather than template-driven
   - one topic of concern per file
   - concrete enough to guide implementation
   - light on implementation prescription
   - biased toward the mature house style:
     - `Overview`
     - `Non-Goals`
     - `Key Patterns`
     - topic-specific sections
     - `Verification`

## Output

Return a short summary with:

- which spec(s) own the task or changed area
- what was created or updated
- whether the repo is now ready for planning/execution
- any ambiguity that still requires human direction

## Rules

- Code is reality; specs express intent.
- Start by discovering the repo that exists, not the layout you expected.
- The internal shape of this skill is: audit -> consult -> verify -> apply.
- On mature repos, existing harness quality is the floor. Preserve and extend
  the local house style rather than normalizing rich docs down to the generic
  template.
- Use the local skill assets as scaffolding for missing structure, not as a
  reason to thin or flatten already-strong specs.
- Treat the generic spec template as bootstrap scaffolding only. Do not
  reintroduce broad filler sections unless the repo's actual house style uses
  them or the topic genuinely needs them.
- Specs should capture durable topic truth. They should not read like task
  breakdowns or implementation checklists.
- Verification commands or concrete checks in specs are encouraged when they
  materially help future agents confirm reality.
- User-facing role: bootstrap, sync, or close repo-truth gaps. Task-scoped
  spec preparation is an internal behavior of this same skill when clearly
  needed.
- Prefer proportional fixes. Small unrelated drift should usually be noted, not
  expanded into a broad rewrite.
- Ignore vendor, generated, cache, and copied-artifact noise by default unless
  the task explicitly targets it.
- Do not turn one repo's concrete layout into a portable default. The guidance
  should survive monorepos, flat trees, mixed stacks, and repos without
  `src/`.
- Keep related specs consistent when they share terms, boundaries, or
  invariants.
- Do not silently broaden task scope.
- Prefer updating one good spec over creating many tiny docs.
- Keep `AGENTS.md` compact; avoid dumping architecture details that belong in
  `specs/`.
- If the task intent, owning topology, or boundary mapping is ambiguous, stop
  and surface the ambiguity instead of writing confident but weak specs.
