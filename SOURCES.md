# Sources

This note captures the durable workflow guidance that shaped the repo.

Use it as a stable reference when updating the skills, the eval harness, or the
maintenance surface. It exists so the design grounding is recoverable from repo
truth alone rather than from old plans or chat history.

## Official Docs

The current workflow is grounded in these references:

- `https://developers.openai.com/codex/learn/best-practices`
- `https://developers.openai.com/cookbook/articles/codex_exec_plans`
- `https://developers.openai.com/codex/skills`
- `https://agentskills.io/specification`
- `https://agentskills.io/skill-creation/best-practices`
- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
- `https://agentskills.io/skill-creation/using-scripts`
- `https://agentskills.io/client-implementation/adding-skills-support`

Durable takeaways applied in this repo:

- Keep skills narrowly scoped with explicit trigger boundaries and anti-triggers.
- Prefer durable state in files over chat memory.
- Keep planning, implementation, and adversarial review as distinct steps.
- Make fresh-session resumability a first-class constraint.
- Use progressive disclosure: concise skill entrypoints, local assets only where
  they materially help.
- Keep automation thin and file-backed rather than moving workflow truth into
  shell wrappers.
- Validate skill changes with tracked eval intent plus reviewable generated
  artifacts.

## Example Corpora

These example corpora were re-reviewed only for durable composition patterns:

- `https://github.com/openai/skills`
- `https://github.com/anthropics/skills`
- `https://github.com/obra/superpowers`
- `https://github.com/ClaytonFarr/ralph-playbook`

Portable patterns worth keeping:

- Group the actual skill payloads together so users can see what the skills are
  and what repo-level tooling lives around them. In this repo that means
  `src/<skill>/`.
- Keep each skill copyable as a directory with its own `SKILL.md`, optional
  local assets, and local eval metadata.
- Put shared harness metadata and operator tooling outside the skill payloads.
- Favor explicit markdown contracts over hidden orchestration.
- Treat helper scripts as convenience layers only; they should accept explicit
  inputs, avoid guessing state, and stay replaceable.
- Keep examples and commands concrete enough for a fresh agent to recover the
  intended workflow quickly.
- Preserve a clean split between portable workflow truth and provider-specific
  affordances.

## Cross-Provider Rules

These are the durable patterns this repo tries to preserve:

- research before coding
- durable state in files, not chat
- concise repo truth, detailed task truth in dedicated markdown
- focused skills with progressive disclosure
- fresh-context verification and evaluation loops
- separate planning from implementation
- stop, persist, and restart when session quality drops
- decompose large work into bounded execution slices instead of one giant plan
  or one giant session

## Scope Rule

Provider-specific guidance can be useful as a stress test, but it must stay
additive only. The portable baseline in this repo cannot require plan modes,
plugins, auto-memory, or other client-specific primitives.
