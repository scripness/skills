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
  layers, durable discovery promotion, and preferred independent-pass behavior
  for `consult` and `verify`.
- For `consult` and `verify`, make the preferred independent-pass policy
  explicit: the main agent should use the skill itself, dispatch the same skill
  independently when supported, and compare or synthesize both results rather
  than blindly trusting either side alone.
- Fold in the highest-signal workflow refinements from the audit without
  changing the six-skill model: structured `consult -> plan` carry-forward,
  decision-complete plan slices, `execute` bounce on under-specified slices,
  `verify(plan)` failure for weak slice contracts, and slice-level `specs` /
  `tests` exit criteria.
- Update the AGENTS bootstrap template Git section to cover commits, branches,
  and PR titles.
- Add a broader `tests` eval case covering frontend/UI/e2e layer selection on
  the pinned `cryptoli` fixture so that this contract is not only textual.
- Re-verify source-repo and copied-layout behavior with bounded local checks.

## Non-Goals

- Redesigning the six-skill model or making subagents a required primitive for
  every skill.
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
- Synced skill-local agent shims and eval metadata wherever contract changes
  require shipped-surface follow-through.
- Updated `consult`, `plan`, `execute`, and `verify` contract expectations in
  the plan so the contract-tightening slice also captures the approved
  baton-pass improvements before implementation starts.
- Updated `tests` eval metadata and any owning eval-harness docs/runtime
  metadata needed for the broader frontend/UI/e2e must-run coverage addition,
  with `evals/runtime.json` selecting the broader case as the tests must-run
  workflow and the narrower backend-only case retained as non-must-run
  validation when it still adds signal.
- Verification evidence proving the copied execute helper surface and copied
  dashboard passthrough user mode work from a simulated target layout.

## Repo Context

- Task source: user request on clean `refine-02` to consult the current repo
  deeply, use six consultation subagents, then implement the final batch of
  copy-readiness and workflow-clarity changes before downstream copy into
  `~/Code/cryptoli`.
- Owning code paths: `src/execute/scripts/loop.py`,
  `src/consult/SKILL.md`, `src/consult/agents/openai.yaml`,
  `src/plan/SKILL.md`, `src/plan/agents/openai.yaml`,
  `src/plan/assets/plan-template.md`, `src/execute/SKILL.md`,
  `src/execute/agents/openai.yaml`, `src/verify/SKILL.md`,
  `src/verify/agents/openai.yaml`,
  `src/execute/scripts/providers/codex_loop.py`,
  `src/execute/scripts/providers/codex_loop_dashboard.py`,
  `src/consult/evals/evals.json`, `src/execute/evals/evals.json`,
  `src/plan/evals/evals.json`, `src/tests/evals/evals.json`,
  `src/verify/evals/evals.json`
- Owning spec paths: `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `specs/workflow-contract.md`, `specs/repo-surface.md`,
  `specs/evaluation-harness.md`, `src/specs/SKILL.md`,
  `src/specs/assets/AGENTS.md`, `evals/README.md`
- Owning eval/test paths: `src/consult/evals/evals.json`,
  `src/execute/evals/evals.json`, `src/plan/evals/evals.json`,
  `src/tests/evals/evals.json`, `src/verify/evals/evals.json`,
  `evals/runtime.json`, `evals/fixtures/cryptoli.json`; there is still no
  dedicated automated helper-test suite, so rely on focused mechanical
  validation, eval-workspace refresh, and synthetic copied-layout smoke checks
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
  runs, copied-layout user-mode and runner-mode smoke checks against temporary
  workspaces, and eval-workspace refresh plus artifact review when a slice
  changes a shipped skill contract, `agents/openai.yaml`, `evals/evals.json`,
  or eval-harness governance metadata. Milestone 5 should update
  `src/tests/evals/evals.json` with one broader cryptoli layer-selection case,
  switch `evals/runtime.json` to select that broader case as the tests
  must-run workflow, and keep the narrower backend-only workflow case as
  non-must-run validation if it still adds signal.

## Milestones

1. Portability hardening: make the Codex provider wrappers resolve repo/skill
   paths correctly in both source and copied layouts, including copied
   user-mode proof for `codex_loop.py` and `codex_loop_dashboard.py`.
2. Local mirror + repo-truth sync: add `.agents/skills` symlink support and
   update repo docs/specs to describe source-of-truth vs local mirror clearly.
3. Consult/verify handoff tightening: update `consult`, `verify`,
   `src/plan/assets/plan-template.md`, and any owning shims/evals for
   structured `consult -> plan` carry-forward, durable discovery promotion,
   preferred independent-pass behavior with fresh-session fallback, and
   explicit compare-and-synthesize guidance when both the main agent and an
   independent pass are available.
4. Plan/execute/Git tightening: update `plan`, `execute`, the relevant
   `verify(plan)` slice-quality rules, and the AGENTS bootstrap Git section so
   future plans demand decision-complete next slices, `execute` bounces on
   under-specified work, `verify(plan)` fails weak slice contracts, and
   slice-level `specs` / `tests` exit criteria are explicit.
5. Eval coverage addition: broaden the `tests` skill eval surface so the
   frontend/UI/e2e layer-selection expectation is represented in tracked eval
   metadata, keep the narrower backend-only case as non-must-run validation
   when it still adds signal, and update `evals/runtime.json` so the broader
   case becomes the selected tests must-run workflow.
6. Validation: run bounded checks in the source repo and a synthetic copied
   layout, then scaffold and review fresh eval workspaces for the changed
   skill/eval surfaces so the shipped surface is both copy-safe and truth-synced.

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
- Run `make eval-init-run RUN_ID=<run-id> SELECTION=must-run SKILL="<changed skills>"`
  or the equivalent direct harness command for each changed skill/eval surface,
  then review the generated artifacts before calling the work done.
- Run a temporary copied-layout smoke check that executes
  `.agents/skills/execute/scripts/providers/codex_loop.py --dry-run --plan <plan>`
  and
  `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan <plan>`.
- Run a temporary copied-layout smoke check that executes
  `.agents/skills/execute/scripts/providers/codex_loop.py --runner ...` and
  proves the resolved repo root and referenced skill paths are correct after
  copy.
- Inspect the updated `tests` eval surface and confirm the broader frontend/UI
  or e2e coverage expectation is now represented in tracked eval truth, with
  `evals/runtime.json` selecting the broader tests case and the narrower
  backend-only case retained only as non-must-run validation when it still
  adds signal.

## Risks

- Overstating provider-agnostic guarantees by implying reviewer independence or
  automated `specs`/`tests` enforcement that the repo does not actually have.
- Fixing the copied-layout wrapper pathing incompletely and leaving one prompt
  or help surface still hardcoded to `src/...`.
- Adding local `.agents/skills` support without updating the repo truth, which
  would create a misleading second apparent source of truth.
- Over-correcting and turning `consult` or `verify` into subagent-required
  workflows instead of keeping independent passes as the preferred path and
  fresh-session reuse as the fallback.
- Letting the main agent defer too much to a subagent result even when the main
  session has broader context, which would weaken accuracy instead of improving
  it.
- Pulling in too much of the audit verbatim and bloating the plan template with
  duplicate state instead of keeping only the high-signal handoff
  improvements.

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
- [ ] Milestone 3 - Consult/verify handoff tightening
- [ ] Milestone 4 - Plan/execute/Git tightening
- [ ] Milestone 5 - Eval coverage addition
- [ ] Milestone 6 - Validation

## Decision Log

- [2026-04-21] Use one explicit plan because the work crosses scripts, docs,
  bootstrap assets, and copy-layout validation and should remain resumable from
  repo truth plus one task file.
- [2026-04-21] Fold the broader frontend/UI/e2e `tests` eval addition into this
  same slice instead of deferring it, because the current portability pass is
  already tightening the copy contract and workflow guarantees before
  downstream rollout.
- [2026-04-21] Treat independent subagent dispatch as the preferred accuracy
  policy for `consult` and `verify` only, while keeping the rest of the
  workflow provider-agnostic and file-backed with fresh-session fallback.
- [2026-04-21] When `consult` or `verify` uses an independent pass, require the
  main agent to also apply the skill itself and compare or synthesize the two
  results, because the main session may hold broader context while the
  independent pass contributes reduced anchoring and better adversarial
  pressure.
- [2026-04-21] Keep only the high-signal audit improvements: stronger
  `consult -> plan` carry-forward, decision-complete slices, `execute` bounce
  on under-specified work, `verify(plan)` plan-quality failure, and slice-level
  `specs` / `tests` exit criteria. Do not import heavier template additions
  that would duplicate state or complicate simple tasks.
- [2026-04-21] Replace the current selected tests must-run workflow case in
  `evals/runtime.json` with one broader cryptoli layer-selection case, while
  keeping the narrower backend-only case as non-must-run validation if it
  continues to add signal. This keeps the must-run surface compact at one
  high-signal workflow case per skill while preserving extra validation depth.

## Discoveries

- [2026-04-21] A copied-layout smoke check proved `src/execute/scripts/providers/codex_loop.py`
  currently resolves the repo root to `.agents` after copy and still prompts
  against `src/...` paths, so downstream copy is not yet safe without changes.

## Outcomes / Retrospective

- Pending.
