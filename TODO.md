# TODO

## 1. Define Repo Contract

- Make this repo the canonical source of the four shared core skills: `consult`, `specs`, `tests`, and `verify`.
- Document the downstream usage model explicitly:
  downstream codebases vendor and use these skills, but should not casually fork or mutate the canonical versions in place.
- Decide the refresh workflow for downstream repos: manual copy, install script, subtree, or another sync mechanism.

## 2. Improve The Four Core Skills

- Tighten each skill's trigger description so activation is clearer and more reliable.
- Keep each skill narrowly owned and avoid overlap between `consult`, `specs`, `tests`, and `verify`.
- Improve `consult` so it stays evidence-backed, bounded, and explicitly oriented around current behavior, options, risks, and recommendation.
- Improve `specs` so it cleanly owns repo truth, harness bootstrapping, and durable code-organization guidance without drifting into task plans.
- Improve `tests` so it handles both sync and bootstrap: proportional test-layer selection, weak-repo testing strategy, and honest coverage-gap reporting.
- Improve `verify` so it remains findings-first, adversarial, grounded in evidence, and explicit about blocked checks, stale truth, and remaining gaps.

## 3. Ground The Skills In Official Sources

- Re-review and capture durable guidance from the official sources used during the design work:
  - https://developers.openai.com/codex/skills
  - https://agentskills.io/specification
  - https://agentskills.io/skill-creation/best-practices
  - https://agentskills.io/skill-creation/optimizing-descriptions
  - https://agentskills.io/skill-creation/evaluating-skills
  - https://agentskills.io/skill-creation/using-scripts
  - https://agentskills.io/client-implementation/adding-skills-support
- Re-review the official example corpora and extract only durable composition patterns:
  - https://github.com/openai/skills
  - https://github.com/anthropics/skills
- Keep provider-specific features additive only; do not let Codex-only or Claude-only extensions define the portable baseline.

## 4. Add Full Evaluation Coverage

- Add trigger eval fixtures for all four skills with should-trigger and should-not-trigger prompts.
- Add workflow eval fixtures for all four skills, including baseline-vs-with-skill review cases.
- Add repeatable local runners for trigger and workflow evals.
- Keep the eval harness honest: use it to scaffold comparison and regression review, not to pretend open-ended model quality can be auto-scored perfectly.
- Decide which workflow cases are the must-run regression surface for daily maintenance.

## 5. Add Repo-Level Maintenance Tooling

- Add a small command surface for validation and eval refresh.
- Decide whether a `Makefile`, shell scripts, or another lightweight interface is the right operator surface for this repo.
- Ensure a skill change is not considered done until validation and the relevant eval reports have been refreshed.
- Consider adding CI later, but keep the local maintenance loop usable first.

## 6. Add Core Repo Docs

- Add a focused `README.md` describing what this repo is, how skills are organized, and how downstream repos should consume them.
- Add a short maintenance guide for updating skills, running evals, and upstreaming improvements discovered in downstream project work.
- Keep this repo focused on skills only; avoid mixing in unrelated machine config concerns.
