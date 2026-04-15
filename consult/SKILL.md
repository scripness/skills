---
name: consult
description: Clarify current behavior, viable options, and key risks when the safest next move is not yet clear enough to execute or plan.
argument-hint: [question, topic, or task to clarify]
---

Use this skill when the next move is not yet clear enough to safely hand off to
`execute` or `plan`.

Examples:

- how does this subsystem work today?
- what is the safest way to add feature X?
- what are the tradeoffs between approach A and B?
- what code paths will this change likely touch?
- what should be decided before this turns into a plan?

Do not use this skill when:

- the task is already clear
- the answer is a simple file lookup
- the user asked for implementation now
- there is already a concrete plan, implementation slice, diff, or claim to
  judge; use `verify`
- the direction is already clear and the work mainly needs durable task state;
  use `plan`
- the only open question is a narrow implementation detail that can be resolved
  during coding

## Inputs

- the user task or question
- `AGENTS.md`
- relevant `specs/*`
- relevant tests or current behavior checks when they matter to the decision
- the current codebase

## Process

1. Frame the real question.
   - Separate understanding questions from execution questions.
   - Narrow the scope to the smallest useful decision.
   - If the work is already locally clear and bounded, recommend `execute`
     instead of stretching `consult`.
   - If the direction is already clear but the work now needs durable task
     state, recommend `plan` instead of drafting a hidden plan in chat.

2. Read the current repo truth before opining.
   - Inspect `AGENTS.md`.
   - Read the relevant spec files, tests, and code paths.
   - Prefer current behavior over assumptions or aspirational docs.
   - If required repo truth is missing, stale, or contradictory, say so
     explicitly.

3. Consult from only the angles needed to decide safely.
   - At minimum, cover:
     - current behavior
     - relevant constraints
     - options and tradeoffs
     - risks and edge cases
   - Add external or ecosystem research only when repo truth is not enough to
     answer the question safely.
   - Keep the work bounded. Do not turn a small decision into a broad survey.

4. Synthesize only what matters for the next move.
   - What is true now
   - What options exist
   - What you recommend and why
   - What belongs in a durable plan, if the work should become plan-driven
   - What remains unresolved, if anything

## Output

Return:

1. `Understanding`
   - What the current code, specs, tests, or commands show
2. `Options`
   - Flat list of viable approaches with tradeoffs
3. `Recommendation`
   - The best next move
4. `Plan carry-forward`
   - Only when durable task state is warranted: the concrete facts, decisions,
     risks, blockers, or owning paths that should be copied into a plan
5. `Open questions`
   - Only the unresolved questions that block action

If the angles materially disagree, say so explicitly and recommend the safest
bounded next move rather than pretending the answer is settled.

Every non-trivial claim should point to code, spec, test, command, or external
source references.

## Rules

- `consult` owns clarification and recommendation, not plan-file maintenance or
  implementation.
- If external research is used, say why repo truth was insufficient and prefer
  primary or official sources.
- If the task premise is wrong, say so directly.

## Quality Bar

- Prefer evidence over opinion.
- Prefer current behavior over hypotheticals.
- Keep the answer short enough to act on.
- If a decision should change `specs/`, say that explicitly.
- If the work should become plan-driven, surface exactly what should be carried
  into that plan rather than vaguely saying "make a plan."
- Stop once there is a safe evidence-backed recommendation. Do not turn small
  tasks into research theater.
