# Refine-02 Portability And Copy Readiness

Use this file as a living task plan. Keep it updated in place. A fresh session
should be able to resume from repo truth plus this file alone.

Update `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
`Blockers` after each bounded slice or plan-driven verification pass. Hand off
later `execute` and `verify` sessions with this exact file path.

## Goal

Finish the final `refine-02` hardening pass so the shipped skills and helper
scripts stay provider-agnostic, clarify the intended `specs`/`tests`/`verify`
workflow guarantees, work cleanly when copied into `.agents/skills/` in a real
repo, and remain easy to use locally while editing this source repo.

## Scope

- Fix any shipped helper path assumptions that break after copying
  `src/execute/` into `.agents/skills/execute/`.
- Add the local `.agents/skills/` symlink mirror requested for working on the
  skills from this repo.
- Tighten the shipped skill/docs/template surface where important guarantees
  are currently only implied: `specs`/`tests` follow-through, applicable test
  layers, durable discovery promotion, and optional fresh/independent
  verification.
- Update the AGENTS bootstrap template Git section to cover commits, branches,
  and PR titles.
- Add a broader `tests` eval case covering frontend/UI/e2e layer selection on
  the pinned `cryptoli` fixture so that this contract is not only textual.
- Re-verify source-repo and copied-layout behavior with bounded local checks.

## Non-Goals

- Redesigning the six-skill model or making subagents a required primitive.
- Building a new automated test framework for helper scripts.
- Changing the downstream `cryptoli` repo directly in this slice.
- Rewriting historical plans or broadening into unrelated eval-policy work.

## Deliverables

- Location-safe execute provider wrappers that work both under `src/execute/`
  and after copy into `.agents/skills/execute/`.
- A tracked local `.agents/skills` symlink mirror pointing at the shipped
  source skills.
- Synced repo-truth docs, skill contracts, and bootstrap assets for the new
  portability and workflow clarifications.
- Updated `tests` eval metadata and any owning eval-harness docs/runtime
  metadata needed for the broader frontend/UI/e2e must-run coverage addition.
- Verification evidence proving the copied execute helper surface works from a
  simulated target layout.

## Repo Context

- Task source: user request on clean `refine-02` to consult the current repo
  deeply, use six consultation subagents, then implement the final batch of
  copy-readiness and workflow-clarity changes before downstream copy into
  `~/Code/cryptoli`.
- Owning code paths: `src/execute/scripts/loop.py`,
  `src/execute/scripts/providers/codex_loop.py`,
  `src/execute/scripts/providers/codex_loop_dashboard.py`,
  `src/tests/evals/evals.json`
- Owning spec paths: `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `specs/workflow-contract.md`, `specs/repo-surface.md`,
  `specs/evaluation-harness.md`, `src/specs/SKILL.md`,
  `src/specs/assets/AGENTS.md`, `evals/README.md`
- Owning test paths: `src/tests/evals/evals.json`, `evals/runtime.json`,
  `evals/fixtures/cryptoli.json`; there is still no dedicated automated
  helper-test suite, so rely on focused mechanical validation plus synthetic
  copied-layout smoke checks
- Related docs and commands: `src/consult/SKILL.md`, `src/execute/SKILL.md`,
  `src/plan/SKILL.md`, `src/tests/SKILL.md`, `src/verify/SKILL.md`,
  `make validate`

## Dependencies

- The existing copy contract that moves `src/*` into `.agents/skills/`.
- The existing generic loop contract in `src/execute/scripts/loop.py`.
- The current repo-truth contract that keeps `src/*/SKILL.md` authoritative and
  treats wrappers as optional helpers only.

## Sync Expectations

State the repo-truth and test-truth follow-through explicitly. If
implementation changes durable behavior, boundaries, operating guidance, or
coverage expectations, follow through with `specs` and `tests` rather than
leaving drift behind.

- `specs`: Required. Sync `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `specs/workflow-contract.md`, `specs/repo-surface.md`,
  `specs/evaluation-harness.md`, `evals/README.md`, `src/specs/SKILL.md`, and
  `src/specs/assets/AGENTS.md` where the shipped portability and workflow
  contract changes.
- `tests`: No dedicated automated helper-test layer exists today. Use focused
  mechanical checks instead: `py_compile`, `make validate`, source-layout dry
  runs, and copied-layout smoke checks against temporary workspaces. If a
  durable test-layer addition becomes necessary, stop and reassess before
  inventing one casually.

## Milestones

1. Portability hardening: make the Codex provider wrappers resolve repo/skill
   paths correctly in both source and copied layouts.
2. Local mirror + repo-truth sync: add `.agents/skills` symlink support and
   update repo docs/specs to describe source-of-truth vs local mirror clearly.
3. Contract tightening: update the relevant skills and AGENTS bootstrap asset
   for explicit `specs`/`tests` follow-through, applicable test layers,
   discovery promotion, Git naming, and optional fresh/independent verification.
4. Eval coverage addition: broaden the `tests` skill eval surface so the
   frontend/UI/e2e layer-selection expectation is represented in tracked eval
   metadata and any owning harness docs/runtime mirror.
5. Validation: run bounded checks in the source repo and a synthetic copied
   layout to prove the shipped surface is copy-safe.

## Verification

Keep planned proof points here, then append dated execution and verification
results, findings, verdicts, and remaining gaps so later sessions can resume
from this file alone.

If a strict final review finds cross-cutting work that does not fit an
existing milestone cleanly, append one new bounded follow-up milestone and
record the provenance here plus in `Decision Log`.

- Confirm the current portability bug before fixing it with a copied-layout
  smoke run.
- Run `python3 -m py_compile` on changed helper scripts.
- Run `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan <plan>`.
- Run `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan <plan>`.
- Run `make validate`.
- Run a temporary copied-layout smoke check that executes
  `.agents/skills/execute/scripts/providers/codex_loop.py --runner ...` and
  proves the resolved repo root and referenced skill paths are correct after
  copy.
- Inspect the updated `tests` eval surface and confirm the broader frontend/UI
  or e2e coverage expectation is now represented in tracked eval truth.

## Risks

- Overstating provider-agnostic guarantees by implying reviewer independence or
  automated `specs`/`tests` enforcement that the repo does not actually have.
- Fixing the copied-layout wrapper pathing incompletely and leaving one prompt
  or help surface still hardcoded to `src/...`.
- Adding local `.agents/skills` support without updating the repo truth, which
  would create a misleading second apparent source of truth.

## Open Questions

- None currently.

## Blockers

Use this section for anything that blocks the next safe execute slice,
including unresolved verification failures.

Do not treat every repairable verify failure as a blocker. If the next safe
move is another bounded execute slice, reopen or append that work in
`Progress` instead.

- None currently.

## Progress

Reflect the current task state for each milestone. If later verification proves
that an earlier completion claim was too optimistic, correct it here.

When a strict final review uncovers a cross-cutting failure that does not map
cleanly to an existing milestone, append one new bounded follow-up milestone
instead of overwriting unrelated historical progress.

- [ ] Milestone 1 - Portability hardening
- [ ] Milestone 2 - Local mirror + repo-truth sync
- [ ] Milestone 3 - Contract tightening
- [ ] Milestone 4 - Eval coverage addition
- [ ] Milestone 5 - Validation

## Decision Log

- [2026-04-21] Use one explicit plan because the work crosses scripts, docs,
  bootstrap assets, and copy-layout validation and should remain resumable from
  repo truth plus one task file.
- [2026-04-21] Fold the broader frontend/UI/e2e `tests` eval addition into this
  same slice instead of deferring it, because the current portability pass is
  already tightening the copy contract and workflow guarantees before
  downstream rollout.

## Discoveries

- [2026-04-21] A copied-layout smoke check proved `src/execute/scripts/providers/codex_loop.py`
  currently resolves the repo root to `.agents` after copy and still prompts
  against `src/...` paths, so downstream copy is not yet safe without changes.

## Outcomes / Retrospective

- Pending.
