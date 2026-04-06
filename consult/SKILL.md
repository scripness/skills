---
name: consult
description: Clarify an ambiguous problem, architecture question, or tradeoff before committing to a direction.
argument-hint: [question, topic, or task to clarify]
---

Use this skill when the next move is not obvious yet.

Examples:

- how does this subsystem work today?
- what is the safest way to add feature X?
- what are the tradeoffs between approach A and B?
- what code paths will this change likely touch?

Do not use this skill when:

- the task is already clear
- the answer is a simple file lookup
- the user asked for implementation now

## Inputs

- the user task or question
- `AGENTS.md`
- relevant `specs/*`
- the current codebase

## Process

1. Frame the real question.
   - Separate understanding questions from execution questions.
   - Narrow the scope to the smallest useful decision.

2. Read the repo before opining.
   - Inspect `AGENTS.md`.
   - Read the relevant spec files.
   - Trace the relevant code paths.

3. Consult from multiple angles.
   - At minimum, cover:
     - current behavior
     - options and tradeoffs
     - risks and edge cases
   - Add ecosystem or framework research when that meaningfully affects the
     decision.
   - If the provider supports subagents, parallel threads, or isolated passes,
     use them when the angles are meaningfully separable.
   - If it does not, perform the same multi-angle consultation in one session.

4. Synthesize only what matters.
   - What is true now
   - What options exist
   - What you recommend and why

## Output

Return:

1. `Understanding`
   - What the code and specs currently say
2. `Options`
   - Flat list of viable approaches with tradeoffs
3. `Recommendation`
   - The best next move
4. `Open questions`
   - Only the unresolved questions that block action

Every non-trivial claim should point to code or spec references.

## Quality Bar

- Prefer evidence over opinion.
- Keep the answer short enough to act on.
- If the task premise is wrong, say so directly.
- If a decision should change `specs/`, say that explicitly.
- If the task is large enough to merit a durable plan artifact, surface what
  should be carried into that plan.
