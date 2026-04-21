# Codex Loop Dashboard

Use this file as a living task plan. Keep it updated in place. A fresh session
should be able to resume from repo truth plus this file alone.

Update `Progress`, `Decision Log`, `Discoveries`, `Verification`, and
`Blockers` after each bounded slice or plan-driven verification pass. Hand off
later `execute` and `verify` sessions with this exact file path.

## Goal

Ship an optional provider-specific terminal dashboard for the local Codex loop
workflow without changing the canonical loop contract. Done means a user can
run one dashboard command, watch live progress for execute, verify, and final
review, and still fall back cleanly to the existing raw loop output when the
dashboard is unavailable or unsuitable.

## Scope

- Add one repo-local dashboard wrapper above `src/execute/scripts/providers/codex_loop.py`.
- Keep `src/execute/scripts/loop.py` as the canonical engine and limit any
  changes there to additive, backward-compatible event surface improvements.
- Render live loop state from machine-readable events and minimal local
  process metadata rather than from chat memory or task-local shadow state.
- Update shipped docs and specs so the new command and boundaries match repo
  reality.

## Non-Goals

- Replacing the raw JSONL loop output as the canonical automation surface.
- Turning the dashboard into workflow truth, plan storage, or a smart
  orchestrator.
- Adding required third-party dependencies or a repo-wide Python packaging
  surface.
- Redesigning `codex_loop.py` or the generic loop argument contract beyond
  what the dashboard needs to stay read-only and accurate.

## Deliverables

- `src/execute/scripts/providers/codex_loop_dashboard.py` as an optional
  terminal dashboard wrapper for local Codex runs.
- Additive loop event support in `src/execute/scripts/loop.py` if needed so
  the dashboard can track live phases without scraping stderr.
- Synced docs in `AGENTS.md`, `README.md`, `MAINTENANCE.md`,
  `src/execute/SKILL.md`, `Makefile`, and relevant `specs/*.md` for the new
  helper and its boundaries.

## Repo Context

- Task source: user request to plan, adversarially verify, and implement a
  terminal dashboard for the Codex loop workflow.
- Owning code paths: `src/execute/scripts/loop.py`,
  `src/execute/scripts/providers/codex_loop.py`,
  `src/execute/scripts/providers/codex_loop_dashboard.py`
- Owning spec paths: `specs/workflow-contract.md`, `specs/repo-surface.md`
- Owning test paths: `N/A` for dedicated automated tests; rely on focused
  mechanical checks and synthetic temporary providers
- Related docs, commands, or external dependencies: `AGENTS.md`, `README.md`,
  `MAINTENANCE.md`, `src/execute/SKILL.md`, `Makefile`,
  `python3 src/execute/scripts/providers/codex_loop.py --help`

## Dependencies

- Existing provider-specific wrapper in
  `src/execute/scripts/providers/codex_loop.py`
- Existing generic loop event stream and helper contract in
  `src/execute/scripts/loop.py`
- None for third-party Python packages; keep the dashboard stdlib-only unless a
  later explicit decision changes repo packaging expectations

## Sync Expectations

State the repo-truth and test-truth follow-through explicitly. If
implementation changes durable behavior, boundaries, operating guidance, or
coverage expectations, follow through with `specs` and `tests` rather than
leaving drift behind.

- `specs`: Update `specs/workflow-contract.md` and `specs/repo-surface.md` if
  the dashboard script ships and if the generic loop gains additive event
  types. Sync `AGENTS.md`, `README.md`, `MAINTENANCE.md`, `Makefile`, and
  `src/execute/SKILL.md` where they expose the helper surface.
- `tests`: No dedicated automated test layer exists for these local helper
  scripts today. Do not invent a new test framework in this slice. Instead run
  focused mechanical checks: `py_compile`, `--help`, `--dry-run`, and
  synthetic loop/dashboard runs against temporary non-interactive providers.

## Milestones

1. Dashboard contract: confirm the wrapper stays read-only, provider-specific,
   and separate from the generic loop; decide the dashboard command, fallback
   behavior, and the minimum live data it needs.
2. Additive loop events: add backward-compatible phase events to
   `src/execute/scripts/loop.py` so a dashboard can observe execute, verify,
   and strict final review starts and finishes without scraping stderr.
3. Dashboard implementation: add
   `src/execute/scripts/providers/codex_loop_dashboard.py` as a full-screen
   terminal view over the Codex wrapper that falls back cleanly when not on a
   TTY.
4. Repo-truth sync: update top-level docs and specs for the new dashboard
   command and keep the raw loop and Codex wrapper contracts clearly separate
   from the UI layer.
5. Validation: run focused checks and synthetic temporary-provider runs that
   prove raw output still works, the dashboard renders current state, and the
   final exit code still comes from the underlying loop.
6. Helper layering hardening: tighten the helper docs and provider prompts so
   the skills remain the workflow source of truth and the scripts only add
   invocation mechanics, transport constraints, and presentation.

## Verification

Keep planned proof points here, then append dated execution and verification
results, findings, verdicts, and remaining gaps so later sessions can resume
from this file alone.

If a strict final review finds cross-cutting work that does not fit an
existing milestone cleanly, append one new bounded follow-up milestone and
record the provenance here plus in `Decision Log`.

- Inspect `src/execute/scripts/loop.py` and confirm the dashboard plan keeps
  the loop provider-agnostic and machine-readable.
- Inspect `src/execute/scripts/providers/codex_loop.py` and confirm the
  dashboard sits above it rather than duplicating its runner logic.
- Run `python3 -m py_compile` on the changed scripts.
- Run `python3 src/execute/scripts/providers/codex_loop_dashboard.py --help`.
- Run a dashboard dry run and confirm it delegates to the existing Codex
  wrapper.
- Run synthetic temporary-provider loop and dashboard checks that prove live
  phase/status rendering and correct exit-code passthrough.
- Run a redirected or otherwise non-TTY dashboard invocation and confirm it
  falls back cleanly to the raw Codex loop output surface.
- [2026-04-21] Plan verification: found and fixed two scope gaps before
  implementation. The first draft omitted `Makefile` and `src/execute/SKILL.md`
  from expected sync even though both currently expose helper commands or
  wrapper guidance. The first draft also did not explicitly require a non-TTY
  fallback check even though the goal promises safe fallback when the dashboard
  is unsuitable. Verdict after correction: pass.
- [2026-04-21] `python3 -m py_compile src/execute/scripts/loop.py src/execute/scripts/providers/codex_loop.py src/execute/scripts/providers/codex_loop_dashboard.py` passed.
- [2026-04-21] `python3 src/execute/scripts/providers/codex_loop_dashboard.py --help` passed by forwarding to the raw `codex_loop.py` help surface.
- [2026-04-21] `python3 src/execute/scripts/providers/codex_loop_dashboard.py --dry-run --plan plans/2026-04-21-codex-loop-dashboard.md` passed and emitted the raw JSON `start` event surface in non-TTY mode.
- [2026-04-21] Synthetic TTY dashboard run against a temporary provider passed and showed live phase transitions for `execute`, `verify`, repairable `fail -> continue`, and final `completed_strict`.
- [2026-04-21] Redirected non-TTY dashboard output passed through the raw wrapper JSON without ANSI escape sequences.
- [2026-04-21] `make validate` passed after the new dashboard script and doc sync.
- [2026-04-21] `git diff --check` passed after the implementation slice.
- [2026-04-21] Helper-layering hardening passed: `python3 -m py_compile ...`,
  `python3 src/execute/scripts/providers/codex_loop.py --help`,
  `python3 src/execute/scripts/providers/codex_loop_dashboard.py --dry-run --plan plans/2026-04-21-codex-loop-dashboard.md`,
  `make validate`, and `git diff --check` all succeeded after tightening the
  docs and provider prompts so skill contracts remain authoritative.

## Risks

- If the dashboard depends on parsing stderr or undocumented output, it will
  drift and break when the loop changes.
- If the dashboard becomes the new place where workflow state is derived, it
  will blur the clean split between engine, provider wrapper, and UI.
- If the dashboard requires non-stdlib dependencies, the repo will gain
  packaging and operator burden that the current helper surface does not own.

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

- [x] Milestone 1 - Dashboard contract
- [x] Milestone 2 - Additive loop events
- [x] Milestone 3 - Dashboard implementation
- [x] Milestone 4 - Repo-truth sync
- [x] Milestone 5 - Validation
- [x] Milestone 6 - Helper layering hardening

## Decision Log

- [2026-04-21] Keep the proposed dashboard as a separate provider-specific
  wrapper rather than merging UI behavior into `codex_loop.py` or the generic
  `loop.py`.
- [2026-04-21] Plan against a stdlib-only implementation by default to avoid
  introducing new repo-wide dependency management for a local helper.
- [2026-04-21] During plan verification, expand expected sync to include
  `Makefile` and `src/execute/SKILL.md`, and require an explicit non-TTY
  fallback check in validation.
- [2026-04-21] Keep the dashboard wrapper read-only and forward all normal loop
  arguments to `codex_loop.py`, with only a small dashboard-specific
  `--plain` bypass instead of duplicating the Codex wrapper CLI.
- [2026-04-21] Add one additive `phase` event with `start` or `end` status to
  the generic loop rather than inventing a second output channel for live UI.
- [2026-04-21] Make `codex_loop.py` prompts explicitly defer to
  `src/execute/SKILL.md` and `src/verify/SKILL.md`, and keep only
  invocation-specific constraints plus verify JSON transport in the wrapper.

## Discoveries

- [2026-04-21] The current generic loop emits machine-readable `start`,
  `iteration`, `final_review`, and `stop` events, but it does not yet emit
  structured phase-start or phase-end events for live execute/verify progress.
- [2026-04-21] The repo has no Python dependency manifest, so a hard dependency
  such as `rich` would add packaging surface that does not currently exist.
- [2026-04-21] The current helper surface is also exposed through `Makefile`
  help text and `src/execute/SKILL.md`, so those need sync if a new dashboard
  command ships.
- [2026-04-21] Forwarding `--help` straight to `codex_loop.py` keeps the
  dashboard wrapper thin, but it means the dashboard-only `--plain` bypass
  lives in repo docs rather than in the inherited child help text.
- [2026-04-21] The live dashboard view is already useful with simple ANSI
  redraws and the additive loop events; no dependency or full TUI framework
  was needed for this slice.
- [2026-04-21] The main remaining drift risk was in provider-wrapper prompt
  wording, not in the generic loop itself; tightening those prompts was enough
  to keep the helper layer compounding on top of the skills instead of
  restating workflow policy.

## Outcomes / Retrospective

- Shipped `src/execute/scripts/providers/codex_loop_dashboard.py` as an
  optional repo-local presentation layer over `codex_loop.py`.
- Added backward-compatible `phase` events in `src/execute/scripts/loop.py` so
  local dashboards can observe live execute, verify, and final-review progress
  without scraping stderr.
- Synced `AGENTS.md`, `README.md`, `MAINTENANCE.md`, `Makefile`,
  `specs/workflow-contract.md`, `specs/repo-surface.md`, and
  `src/execute/SKILL.md` to the new helper surface.
- Tightened the helper-layering contract so the shipped skills remain the
  workflow source of truth and the execute helper scripts only add invocation,
  exit-code transport, machine-readable events, and presentation.
