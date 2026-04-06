---
name: specs
description: Prepare and maintain repo truth by creating, refining, indexing, and syncing AGENTS.md and specs/ against task intent and code reality.
argument-hint: [task to prepare or area to sync]
---

Use this skill in two situations:

1. before work, to make sure the relevant spec exists and is good enough
2. after work, to keep `AGENTS.md` and `specs/` aligned with reality

This skill replaces separate "write specs", "reverse engineer specs", and
"sync specs" workflows with one repo-truth skill.

## Inputs

- the user task, if there is one
- `AGENTS.md` if present
- `specs/README.md` and relevant `specs/*` if present
- current codebase

## Process

1. Determine intent.
   - `prepare`: a task arrived and specs must be ready for planning/execution
   - `sync`: docs may have drifted from code reality
   - if no task is given, default to sync

2. Audit the current truth layer.
   - Read `AGENTS.md`, `specs/README.md`, and the relevant `specs/*`.
   - Search the current codebase and changed areas.
   - Identify:
     - the owning spec(s)
     - stale claims
     - missing topic specs
     - stale `specs/README.md` entries
     - stale repo-wide operational guidance in `AGENTS.md`

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
- Use templates as scaffolding for missing structure, not as a reason to thin
  or flatten already-strong specs.
- Do not silently broaden task scope.
- Prefer updating one good spec over creating many tiny docs.
- Keep `AGENTS.md` compact; avoid dumping architecture details that belong in
  `specs/`.
- If the task intent is ambiguous, stop and surface the ambiguity instead of
  writing confident but weak specs.
