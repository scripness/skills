# TODO

Follow-up items from the April 22, 2026 comparison between this repo's
six-skill workflow and the official Agent Skills docs:

## Source Grounding

This note is grounded in a point-in-time review on April 22, 2026.
Re-evaluate these items if the upstream Agent Skills format or guidance changes,
or if this repo materially changes its own workflow contract.

Upstream sources reviewed:

- `https://agentskills.io/home`
- `https://agentskills.io/what-are-skills`
- `https://agentskills.io/specification`
- `https://agentskills.io/skill-creation/best-practices`
- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
- `https://agentskills.io/skill-creation/using-scripts`
- `https://agentskills.io/client-implementation/adding-skills-support`

Local repo sources reviewed:

- `AGENTS.md`
- `README.md`
- `specs/workflow-contract.md`
- `specs/evaluation-harness.md`
- `src/*/SKILL.md`
- `src/execute/scripts/loop.py`

When revisiting this file later, confirm whether:

- the published Agent Skills spec still treats `name` and `description` as the
  core discovery fields and still documents the same optional frontmatter set
- upstream trigger guidance still centers on description quality and
  progressive disclosure
- upstream script guidance still assumes non-interactive execution and
  structured, agent-friendly interfaces
- upstream evaluation guidance still favors repeated runs, validation splits,
  baselines, and human review
- this repo still intends to optimize for coding-agent environments rather than
  generic drop-in marketplace portability

## Dependency And External Grounding

- [ ] Design and ship dependency-sensitive source grounding rules across the
  six-skill workflow.
  The goal is to stop agents from relying on training-memory assumptions when
  work depends on current library, framework, SDK, API, security, deployment,
  or "best practice" behavior.
  Follow-through:
  - require agents to identify the repo's actual dependency version from local
    manifests, lockfiles, generated clients, vendored source, installed
    packages, or build configuration before choosing an implementation target
  - prefer the exact shipped artifact first when available, such as
    `node_modules`, `site-packages`, vendored code, generated SDK files, type
    definitions, package tarballs, or source distributions
  - when local artifacts are absent or insufficient, inspect the official
    upstream source at the exact tag, commit, release archive, or package
    version; clone locally only when that is more reliable than remote
    inspection
  - read implementation, tests, types, fixtures, and official examples for the
    version under review so behavior and supported usage are grounded in actual
    evidence
  - compare source behavior with versioned official docs, API references,
    changelogs, release notes, and migration guides; record conflicts as risks
    rather than silently choosing the convenient source
  - distinguish "what the code currently does" from "what the public contract
    supports"; avoid depending on private internals unless the task explicitly
    accepts that tradeoff
  - for upgrade or latest-version work, compare current repo version, target
    version, and latest available version instead of blindly applying latest
    docs to the pinned repo state
  - label community posts, issue threads, search snippets, blogs, and model
    memory as supporting clues only; they must not be the primary evidence for
    current API behavior
  - add a plan-template `External Grounding` section that records freshness
    requirement, local version evidence, official source/docs checked, accessed
    date, decision impact, recheck trigger, and unresolved gaps
  - update `consult`, `plan`, `execute`, `verify`, `specs`, and `tests` so this
    grounding is required when dependency freshness materially affects safe
    planning, implementation, verification, repo truth, or test truth
  - add eval cases that fail when agents make dependency-sensitive claims
    without exact-version evidence, source inspection, and docs/source
    comparison

## Standards Alignment

- [ ] Revisit `argument-hint` in skill frontmatter.
  The local harness currently requires `argument-hint`, but the published
  Agent Skills spec documents `name`, `description`, `license`,
  `compatibility`, `metadata`, and `allowed-tools` instead.
  Decide whether to:
  - make `argument-hint` optional in the local harness
  - move it under `metadata`
  - or keep it as a documented local extension with an explicit portability
    note for strict validators and non-local clients
  Follow-through:
  - check whether the current local validation surface rejects unknown or
    missing frontmatter fields too aggressively
  - test one strict cross-client or reference-validator path so this decision
    is grounded in actual compatibility behavior rather than assumption

## Trigger Ergonomics

- [ ] Tighten skill descriptions toward upstream trigger guidance.
  Review whether each skill description should more directly express
  user intent in "Use this skill when..." terms and rely less on repo-local
  concepts such as `plans/`, `AGENTS.md`, and `specs/` in the short
  discovery-facing description.
  Follow-through:
  - run per-skill trigger evals with should-trigger and near-miss
    should-not-trigger prompts rather than only revising descriptions by eye
  - check whether simple bounded requests under-trigger because the current
    descriptions overemphasize internal workflow mechanics instead of user
    intent
  - record any boundary cases where `consult` vs `plan` vs `execute` are
    especially easy for clients to mis-trigger

## Compatibility Metadata

- [ ] Add explicit `compatibility` metadata where environment assumptions
  matter.
  The workflow assumes repo access and common local tools such as `python3`,
  `make`, and `rg`. Capture those assumptions using the standard compatibility
  field where that improves cross-client portability.
  Follow-through:
  - decide whether all six skills share one common compatibility baseline or
    whether `execute`, `specs`, `tests`, and `verify` need stricter tool and
    filesystem requirements than `consult`
  - document that these skills are optimized for coding-agent environments
    with repo truth files, writable working trees, and non-interactive shell
    access

## Eval Portability

- [ ] Decide how much of the shared eval harness should be presented as
  repo-local policy versus generic Agent Skills interoperability.
  The current harness is stronger than the upstream baseline, but it is also
  more custom. Document the mapping between local eval governance and the
  standard `evals/evals.json` expectations so downstream users understand what
  is portable versus repo-specific.
  Follow-through:
  - make the boundary explicit between upstream-aligned eval intent and this
    repo's additional governance around train/validation splits, previous-skill
    baselines, required review, and must-run repetition
  - decide whether to keep the current validate-and-scaffold-only harness as
    the long-term contract or grow optional tooling for more of the upstream
    run/grade/review loop
  - add at least one real-client smoke path that exercises trigger behavior and
    frontmatter portability outside the local happy path

## Workflow Automation

- [ ] Design and ship a plan loop for large task planning work.
  The plan loop should automate the current manual
  `consult -> plan -> verify(plan)` workflow while staying file-backed and
  resumable from the explicit `plans/*.md` path.
  Clear orchestration note:
  - the plan loop should spawn multiple `consult` and `verify` angles rather
    than rely on a single pass
  - the orchestrator should also run its own `consult` / `verify` effort so it
    has a first-party view of the problem before synthesizing side-agent input
  - those agent outputs should be treated as inputs to one synthesizing
    orchestrator agent
  - only that orchestrator should update the canonical plan file
  Follow-through:
  - define how clarifications, approvals, and changed decisions pause the loop
    and resume against the same plan path
  - define explicit loop outcomes such as `ready`, `needs_input`, `blocked`,
    and `complete` so pause/resume behavior stays machine-readable instead of
    hiding in prose
  - treat follow-up clarifications and changed decisions as deltas against the
    same explicit plan file, reopening only the affected milestones instead of
    creating replacement plans or restarting broad research
  - define the default consult/verify fan-out shape and how it scales for
    larger work without turning the generic workflow contract provider-specific
  - make the wrapper-owned swarm policy deterministic about how many consult or
    verify angles run and which ones are expected, rather than leaving that to
    ad hoc model behavior

- [ ] Strengthen execute-loop verification fan-out in the provider-specific
  runner layer.
  The existing generic execute loop can stay thin, but the actual
  `verify <plan>` implementation should be upgraded to run multiple
  verification angles and synthesize them before returning one verdict.
  Clear orchestration note:
  - make the execute loop spawn more verification agents in the same general
    way the future plan loop should spawn multiple consult/verify angles
  - the orchestrator should also run its own `verify` effort so it is not only
    relaying swarm output when updating the canonical plan and verdict
  - feed those independent syntheses to one orchestrator agent that updates
    the plan once and returns the final verdict code back to the loop
  Follow-through:
  - keep the generic `src/execute/scripts/loop.py` contract unchanged
  - put multi-agent fan-out and synthesis in provider-specific wrappers or
    optional helper layers rather than in the provider-agnostic skill contract
  - define verification cadence so lighter slice-level review and heavier
    whole-plan swarm passes happen at predictable points instead of every pass
    using the same maximal fan-out
  - define closure explicitly: after fixes, rerun the whole-plan verify swarm
    until a fresh pass yields no new material findings, then still require the
    final strict `verify=pass` completion gate
