---
name: specs
description: Prepare and maintain repo truth by creating, refining, indexing, and syncing AGENTS.md and specs/ against task intent and code reality.
argument-hint: [task to prepare or area to sync]
---

Use this skill in two user-facing situations:

1. bootstrap a repo that is missing `AGENTS.md`, `specs/`, or both
2. sync `AGENTS.md` and `specs/` with current code reality

This skill may also be auto-invoked during implementation when the current task
is clearly blocked by weak or missing repo truth.

This skill replaces separate "write specs", "reverse engineer specs", and
"sync specs" workflows with one repo-truth skill.

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
- current codebase

## Process

1. Determine intent.
   - `bootstrap`: `AGENTS.md`, `specs/`, or core index docs are missing or too
     weak to support work
   - `sync`: docs may have drifted from code reality
   - if invoked automatically during a task, treat task-scoped fixes as part of
     syncing the repo truth needed for that work

2. Audit the current truth layer.
   - Read `AGENTS.md`, `specs/README.md`, and the relevant `specs/*`.
   - Search the current codebase and changed areas.
   - Identify:
     - the owning spec(s)
     - stale claims
     - missing topic specs
     - stale `specs/README.md` entries
     - stale repo-wide operational guidance in `AGENTS.md`
     - related config, schema, CI, migration, or generated-artifact truth that
       affects what the docs should claim
     - related specs that mention the same subsystem or invariant

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
     immediately specialize it to the repo.
   - Ensure `CLAUDE.md` points to `AGENTS.md` when the provider expects it.
   - If `specs/` is missing, create it from `assets/specs/README.md` and
     `assets/specs/spec-template.md`, then create the first topic specs needed
     for the codebase.
   - Bootstrap minimally: create only the docs needed to make safe work
     possible, not a speculative doc forest.
   - Refine an existing spec when the topic already exists.
   - Create a new topic spec when the area is not documented and the topic is
     large enough to deserve one.
   - Update `specs/README.md` when spec inventory changes.
   - Update `AGENTS.md` only when repo-wide operational truth changed:
     commands, structure, boundaries, testing policy, or conventions.

6. Keep specs useful for agents.
   - one topic of concern per file
   - outcome-oriented
   - concrete enough to guide implementation
   - light on implementation prescription

## Output

Return a short summary with:

- which spec(s) own the task or changed area
- what was created or updated
- whether the repo is now ready for planning/execution
- any ambiguity that still requires human direction

## Rules

- Code is reality; specs express intent.
- The internal shape of this skill is: audit -> consult -> verify -> apply.
- On mature repos, existing harness quality is the floor. Preserve and extend
  the local house style rather than normalizing rich docs down to the generic
  template.
- Use the local skill assets as scaffolding for missing structure, not as a
  reason to thin or flatten already-strong specs.
- User-facing role: bootstrap or sync. Task-scoped spec preparation is an
  internal behavior of this same skill when clearly needed.
- Prefer proportional fixes. Small unrelated drift should usually be noted, not
  expanded into a broad rewrite.
- Keep related specs consistent when they share terms, boundaries, or
  invariants.
- Do not silently broaden task scope.
- Prefer updating one good spec over creating many tiny docs.
- Keep `AGENTS.md` compact; avoid dumping architecture details that belong in
  `specs/`.
- If the task intent is ambiguous, stop and surface the ambiguity instead of
  writing confident but weak specs.
