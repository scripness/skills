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
5. Eval coverage addition: update `src/tests/evals/evals.json`,
   `evals/runtime.json`, `specs/evaluation-harness.md`, and `evals/README.md`
   so the tests skill ships one broader `cryptoli` layer-selection workflow
   case, keeps the narrower backend-only workflow case as non-must-run
   validation when it still adds signal, and selects the broader case as the
   tests must-run workflow. Done when `make validate` passes, `make eval-init-run
   RUN_ID=<run-id> SELECTION=all SKILL="tests"` scaffolds the refreshed tests
   case set, `run.json` shows both the broader selected workflow and the
   retained narrower validation case in their intended roles, and the generated
   `review-template.md`, `fixtures/`, `outputs/`, and `transcripts/`
   scaffolding has been inspected. Slice-level `specs` follow-through is
   required for `specs/evaluation-harness.md` and `evals/README.md`;
   slice-level `tests` follow-through is required for
   `src/tests/evals/evals.json` and `evals/runtime.json`. If this slice would
   require broader fixture-manifest or eval-governance changes, stop and reopen
   planning instead of guessing.
6. Validation: close the plan with one validation-only slice across the
   changed wrapper, skill, and eval surfaces without widening scope. In the
   source layout, run
   `python3 -m py_compile src/execute/scripts/providers/codex_loop.py src/execute/scripts/providers/codex_loop_dashboard.py`,
   `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
   `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
   and `make validate`. In a temporary copied repo containing the tracked
   `.agents/skills` mirror plus this plan file, run
   `.agents/skills/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
   `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
   and copied-layout runner smokes for both `execute` and `verify` with a
   temporary fake Codex adapter that honors `--output-schema -o` so the
   resolved repo root and referenced skill paths can be inspected after copy.
   Then run
   `make eval-init-run RUN_ID=<run-id> SELECTION=all SKILL="consult execute plan tests verify"`
   and inspect the generated `run.json`, `review-template.md`, `fixtures/`,
   `outputs/`, and `transcripts/` scaffolding for the changed eval surfaces.
   Done when all of those commands pass, the copied-layout runner smokes still
   target `.agents/skills/...` rather than `src/...`, and the refreshed eval
   workspace reflects the changed `consult`, `execute`, `plan`, `tests`, and
   `verify` eval surfaces. Slice-level `specs` and `tests` follow-through are
   not needed for this validation-only slice unless these checks expose drift;
   if they do, stop and reopen the owning milestone instead of editing repo
   truth opportunistically.

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
- Run `make eval-init-run RUN_ID=<run-id> SELECTION=<milestone-specific selection> SKILL="<changed skills>"`
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
- For Milestone 5 specifically, inspect `specs/evaluation-harness.md` and
  `evals/README.md` for the required eval-governance follow-through, then run
  `make eval-init-run RUN_ID=<run-id> SELECTION=all SKILL="tests"` and confirm
  the generated `run.json` and `review-template.md` reflect the broader tests
  must-run case plus the retained narrower validation case.
- For Milestone 6 specifically, rerun
  `python3 -m py_compile src/execute/scripts/providers/codex_loop.py src/execute/scripts/providers/codex_loop_dashboard.py`,
  `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  and `make validate`, then in a temporary copied repo rerun
  `.agents/skills/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  and copied-layout runner smokes for both `execute` and `verify` with a fake
  Codex adapter that honors `--output-schema -o`. Then run
  `make eval-init-run RUN_ID=<run-id> SELECTION=all SKILL="consult execute plan tests verify"`
  and confirm the generated `run.json`, `review-template.md`, `fixtures/`,
  `outputs/`, and `transcripts/` scaffolding cover the changed eval surfaces.
  No new `specs` or `tests` edits are expected in this validation-only slice;
  if any of these checks expose drift, reopen the owning milestone instead of
  patching repo truth opportunistically.
- [2026-04-21 execute] Pre-fix copied-layout runner smoke in a temporary repo
  copy showed the current bug directly: `codex_loop.py --runner execute`
  passed `-C <repo>/.agents` to the fake Codex command and prompted against
  `src/execute/SKILL.md`, confirming the copied layout was not safe yet.
- [2026-04-21 execute] `python3 -m py_compile src/execute/scripts/providers/codex_loop.py`
  passed after the wrapper update.
- [2026-04-21 execute] `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed in the source layout.
- [2026-04-21 execute] In a temporary copied repo containing `.agents/skills/*`
  plus the plan file, both
  `.agents/skills/execute/scripts/providers/codex_loop.py --dry-run --plan plans/plan.md`
  and
  `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/plan.md`
  passed and emitted provider commands rooted at the copied
  `.agents/skills/execute/scripts/providers/codex_loop.py`.
- [2026-04-21 execute] Copied-layout runner smokes with a fake Codex command
  now pass `-C <repo>` and prompt against `.agents/skills/execute/SKILL.md`,
  `.agents/skills/verify/SKILL.md`, and
  `.agents/skills/plan/assets/plan-template.md`, proving the wrapper now
  follows the active installed skill tree after copy.
- [2026-04-21 verify] Findings: none for Milestone 1 portability hardening.
  Re-ran `python3 -m py_compile src/execute/scripts/providers/codex_loop.py`,
  the source-layout dry run, copied-layout user-mode dry runs for
  `codex_loop.py` and `codex_loop_dashboard.py --plain`, and copied-layout
  runner smokes for both `execute` and `verify` with a fake Codex adapter that
  honored `--output-schema -o`; all passed. Verdict: `pass`. Remaining gaps:
  Milestones 2-6 are still open, and this review did not cover their planned
  docs/specs/tests/eval follow-through yet.
- [2026-04-21 execute] `test -L .agents/skills && readlink .agents/skills`
  returned `../src`, confirming the tracked local mirror points at the shipped
  source skill tree.
- [2026-04-21 execute] `make validate` passed after the local mirror addition
  and repo-truth sync for Milestone 2.
- [2026-04-21 verify] Findings: Milestone 2 local mirror + repo-truth sync is
  not complete yet. `git status --short` still reports `?? .agents/`, so the
  claimed tracked mirror in `AGENTS.md:31-33`, `README.md:21-23`, and this
  plan does not exist in tracked repo state yet even though the local symlink
  works.
  Mechanical results: `git status --short` failed the tracked-state claim;
  `make validate`, `test -L .agents/skills && readlink .agents/skills && test -L CLAUDE.md`,
  `rg -n '\.agents/skills|symlink mirror|copied-layout' AGENTS.md README.md MAINTENANCE.md specs/workflow-contract.md specs/repo-surface.md`,
  and `find . -maxdepth 2 \( -path './.git' -o -path './.tmp' \) -prune -o -maxdepth 2 -type d | sort`
  all passed. Verdict: `fail`. Remaining gaps: add the `.agents/skills ->
  ../src` mirror to tracked source (or remove the new tracked-mirror claims),
  then rerun the same checks; Milestones 3-6 remain open.
- [2026-04-21 execute] Added `.agents/skills` to git-tracked repo state for
  the existing local mirror. `git status --short` now reports
  `A  .agents/skills` instead of `?? .agents/`, and
  `git ls-files -s .agents/skills` shows mode `120000`, matching the tracked
  symlink contract already documented in repo truth.
- [2026-04-21 execute] Re-ran the Milestone 2 mirror checks after adding the
  symlink to git-tracked state:
  `test -L .agents/skills && readlink .agents/skills && test -L CLAUDE.md`,
  `rg -n '\.agents/skills|symlink mirror|copied-layout' AGENTS.md README.md MAINTENANCE.md specs/workflow-contract.md specs/repo-surface.md`,
  `find . -maxdepth 2 \( -path './.git' -o -path './.tmp' \) -prune -o -maxdepth 2 -type d | sort`,
  and `make validate`; all passed. Milestone 2 is now ready for later
  `verify`, while Milestones 3-6 remain open.
- [2026-04-21 verify] Findings: none for Milestone 2 local mirror + repo-truth
  sync. Re-ran `git status --short`, `git ls-files -s .agents/skills`,
  `test -L .agents/skills && readlink .agents/skills && test -L CLAUDE.md && readlink CLAUDE.md`,
  `rg -n '\.agents/skills|symlink mirror|copied-layout' AGENTS.md README.md MAINTENANCE.md specs/workflow-contract.md specs/repo-surface.md`,
  `find . -maxdepth 2 \( -path './.git' -o -path './.tmp' \) -prune -o -maxdepth 2 -type d | sort`,
  and `make validate`; all passed, and the tracked-mirror claims now match repo
  state. Verdict: `pass`. Remaining gaps: Milestones 3-6 remain open, and this
  review did not cover their planned workflow, eval, or validation follow-through.
- [2026-04-21 execute] Milestone 3 updated the shipped consult/verify contract
  and handoff surface without widening into Milestone 4: `src/consult/SKILL.md`
  and `src/verify/SKILL.md` now prefer independent passes only when supported,
  keep the main session responsible for compare-and-synthesize judgment, and
  require copy-ready consult carry-forward for plan-driven work. Synced
  follow-through landed in `src/consult/agents/openai.yaml`,
  `src/verify/agents/openai.yaml`, `src/consult/evals/evals.json`,
  `src/verify/evals/evals.json`, `src/plan/assets/plan-template.md`, and
  `specs/workflow-contract.md`.
- [2026-04-21 execute] `make validate` passed after the Milestone 3 contract,
  template, eval, and workflow-spec updates.
- [2026-04-21 execute] `make eval-init-run RUN_ID=2026-04-21-refine-02-m3-consult-verify SELECTION=must-run SKILL="consult verify"`
  initialized `.tmp/evals/2026-04-21-refine-02-m3-consult-verify`. Inspecting
  `run.json`, `review-template.md`, and the generated `fixtures/`, `outputs/`,
  and `transcripts/` directories confirmed the expected four must-run
  consult/verify cases and the pinned `cryptoli` fixture scaffold.
- [2026-04-21 execute] `git diff --check -- specs/workflow-contract.md src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/plan/assets/plan-template.md src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed with no whitespace or merge-marker issues in the Milestone 3 slice.
- [2026-04-21 verify] Findings: Milestone 3 consult/verify handoff tightening
  is not complete yet. The changed eval assertions live in the train workflow
  cases at `src/consult/evals/evals.json:76-117` and
  `src/verify/evals/evals.json:76-118`, but the refreshed eval workspace used
  `SELECTION=must-run`, and
  `.tmp/evals/2026-04-21-refine-02-m3-consult-verify-verify/run.json:12-18`
  plus `:36-123` show that scaffold only selected validation must-run cases.
  That leaves the required eval-workspace refresh and artifact review
  incomplete for the changed eval surface. Mechanical results:
  `make validate` passed; `git diff --check -- AGENTS.md README.md MAINTENANCE.md specs/workflow-contract.md specs/repo-surface.md src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/plan/assets/plan-template.md src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed; `rg -n "independent consult pass|copy-ready plan carry-forward|compare or synthesize|durable discoveries" src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/plan/assets/plan-template.md`
  and
  `rg -n "independent verify pass|final verdict|compare them explicitly|supporting evidence" src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json`
  passed; `python3 evals/scripts/harness.py init-run --help` confirmed
  `--selection {must-run,validation,all}`. Verdict: `fail`. Remaining gaps:
  rerun the consult/verify eval-workspace refresh with a selection that
  includes the changed train workflow cases, review the generated artifacts,
  and then re-run `verify` for Milestone 3.
- [2026-04-21 execute] `make eval-init-run RUN_ID=2026-04-21-refine-02-m3-consult-verify-all SELECTION=all SKILL="consult verify"`
  initialized `.tmp/evals/2026-04-21-refine-02-m3-consult-verify-all`.
  Inspecting `run.json`, `review-template.md`, and the generated `fixtures/`,
  `outputs/`, and `transcripts/` directories confirmed the scaffold now covers
  all 10 consult/verify cases, including the changed train workflow cases
  `consult-workflow-train-recommend-plan` and
  `verify-workflow-train-plan-review`, while the review template carries the
  later required artifact checklist. This closes the Milestone 3 execute-side
  eval refresh gap and leaves the milestone ready for later `verify`.
- [2026-04-21 verify] Findings: none for the Milestone 3 consult/verify
  handoff-tightening slice. `make validate` passed; `git diff --check -- specs/workflow-contract.md src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/plan/assets/plan-template.md src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed; `rg -n 'recommend-plan|plan-review|independent consult pass|copy-ready plan carry-forward|compare or synthesize|independent verify pass|final verdict|supporting evidence' src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/plan/assets/plan-template.md src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json specs/workflow-contract.md`
  confirmed the shipped contract, shim, eval, template, and spec language; and
  inspection of
  `.tmp/evals/2026-04-21-refine-02-m3-consult-verify-all/run.json` plus
  `review-template.md` confirmed `selection.mode` is `all`, all 10
  consult/verify cases are scaffolded, and the later artifact checklist is
  present. No independent verify pass was used because this invocation only
  provided one plan-driven verify call; the main-session review remained the
  authoritative verdict. Verdict: `pass`. Remaining gaps: Milestones 4-6
  remain open, and the scaffolded eval workspace still needs actual run
  artifacts plus review before any broader eval outcome can be claimed.
- [2026-04-21 execute] Milestone 4 tightened the shipped
  `plan`/`execute`/`verify` contract without widening into Milestone 5:
  `src/plan/SKILL.md` and `src/plan/assets/plan-template.md` now require the
  next unfinished slice to be decision-complete, `src/execute/SKILL.md` now
  bounces on under-specified plan slices and honors slice-level `specs` /
  `tests` exit criteria, `src/verify/SKILL.md` now fails weak next-slice
  contracts during plan review, and `src/specs/assets/AGENTS.md` now covers
  commit, branch, and PR title conventions. Synced follow-through landed in
  `src/plan/agents/openai.yaml`, `src/execute/agents/openai.yaml`,
  `src/verify/agents/openai.yaml`, `src/plan/evals/evals.json`,
  `src/execute/evals/evals.json`, `src/verify/evals/evals.json`, and
  `specs/workflow-contract.md`. No new automated helper-test layer was added;
  the required test-truth follow-through for this slice was the eval-workspace
  refresh recorded below.
- [2026-04-21 execute] `make validate` passed after the Milestone 4 contract,
  template, eval, workflow-spec, and bootstrap-asset updates. Repository
  validation reported 20 workflow cases across the shipped harness surface.
- [2026-04-21 execute] `git diff --check -- specs/workflow-contract.md src/specs/assets/AGENTS.md src/plan/SKILL.md src/plan/agents/openai.yaml src/plan/evals/evals.json src/plan/assets/plan-template.md src/execute/SKILL.md src/execute/agents/openai.yaml src/execute/evals/evals.json src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json`
  passed with no whitespace or merge-marker issues in the Milestone 4 slice.
- [2026-04-21 execute] `make eval-init-run RUN_ID=2026-04-21-refine-02-m4-plan-execute-verify-all SELECTION=all SKILL="plan execute verify"`
  initialized `.tmp/evals/2026-04-21-refine-02-m4-plan-execute-verify-all`.
  Inspecting `run.json`, `review-template.md`, and the generated `fixtures/`,
  `outputs/`, and `transcripts/` directories confirmed `selection.mode` is
  `all`, 17 `plan`/`execute`/`verify` cases are scaffolded, and the newly
  added train workflow cases
  `execute-workflow-train-plan-driven-under-specified-slice` and
  `verify-workflow-train-plan-review-weak-slice-contract` are present
  alongside the updated plan workflow cases. This closes the Milestone 4
  execute-side eval refresh gap and leaves the milestone ready for later
  `verify`.
- [2026-04-21 execute] Re-ran `git diff --check -- plans/2026-04-21-refine-02-portability-and-copy-readiness.md specs/workflow-contract.md src/specs/assets/AGENTS.md src/plan/SKILL.md src/plan/agents/openai.yaml src/plan/evals/evals.json src/plan/assets/plan-template.md src/execute/SKILL.md src/execute/agents/openai.yaml src/execute/evals/evals.json src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json`
  after updating this plan file; it also passed with no whitespace or
  merge-marker issues.
- [2026-04-21 verify] Findings: the primary target is this explicit plan file.
  Milestone 4's tightened `plan`/`execute`/`verify` surface looks structurally
  sound, but the next unfinished slice at `plans/2026-04-21-refine-02-portability-and-copy-readiness.md:150-154`
  is still not decision-complete. It says what to change, but it does not
  spell out the slice-level `specs` / `tests` exit criteria or concrete proof
  points that later `execute` now requires per `src/execute/SKILL.md:50-56`,
  `src/verify/SKILL.md:84-93`, and
  `src/plan/assets/plan-template.md:70-80`. Mechanical results: `make validate`
  passed; `git diff --check -- specs/workflow-contract.md src/specs/assets/AGENTS.md src/plan/SKILL.md src/plan/agents/openai.yaml src/plan/evals/evals.json src/plan/assets/plan-template.md src/execute/SKILL.md src/execute/agents/openai.yaml src/execute/evals/evals.json src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed; `rg -n "decision-complete|under-specified|slice-level|Git|branch|PR title|commit" src/plan/SKILL.md src/plan/assets/plan-template.md src/execute/SKILL.md src/verify/SKILL.md src/specs/assets/AGENTS.md specs/workflow-contract.md`
  confirmed the tightened shipped contract; and inspection of
  `.tmp/evals/2026-04-21-refine-02-m4-plan-execute-verify-all/run.json` plus
  `review-template.md` confirmed the Milestone 4 eval workspace exists and
  includes the new `plan`/`execute`/`verify` cases. Verdict: `fail`. Remaining
  gaps: before the next safe `execute` pass, tighten Milestone 5 so it names
  the concrete owning paths plus slice-level `specs` / `tests` exit criteria,
  including the required `specs/evaluation-harness.md` / `evals/README.md`
  follow-through and the specific `make validate` plus
  `make eval-init-run ... SELECTION=all SKILL="tests"` evidence that should
  exist before calling the slice done.
- [2026-04-22 execute] Milestone 5 updated the shipped tests eval surface and
  eval-harness follow-through without widening into Milestone 6:
  `src/tests/evals/evals.json` now ships a broader
  `tests-workflow-validation-cryptoli-layer-selection` must-run workflow plus
  a retained narrower non-must-run
  `tests-workflow-validation-cryptoli-backend-coverage` validation case, while
  `evals/runtime.json`, `specs/evaluation-harness.md`, and `evals/README.md`
  now describe and select that broader tests workflow as the must-run case.
- [2026-04-22 execute] `make validate` passed after the Milestone 5 tests eval,
  runtime, and eval-governance sync. Repository validation reported 21
  workflow cases across the shipped harness surface.
- [2026-04-22 execute] `make eval-init-run RUN_ID=2026-04-22-refine-02-m5-tests-all SELECTION=all SKILL="tests"`
  initialized `.tmp/evals/2026-04-22-refine-02-m5-tests-all`. Inspecting
  `run.json`, `review-template.md`, and the generated `fixtures/`, `outputs/`,
  and `transcripts/` directories confirmed `selection.mode` is `all`, six
  tests cases are scaffolded, the broader
  `tests-workflow-validation-cryptoli-layer-selection` case is the selected
  must-run workflow with `fixture_id = cryptoli`, and the retained narrower
  `tests-workflow-validation-cryptoli-backend-coverage` case remains
  non-must-run validation coverage. This closes the Milestone 5 execute-side
  eval refresh gap and leaves the milestone ready for later `verify`.
- [2026-04-22 verify] Findings: the primary target is this explicit plan file.
  The Milestone 5 tests eval surface is aligned with shipped repo truth, but
  the next unfinished slice at
  `plans/2026-04-21-refine-02-portability-and-copy-readiness.md:166-168`
  is still not decision-complete under the tightened plan contract. It names a
  final validation theme, but it does not spell out the exact source-layout
  and copied-layout commands to rerun, which changed skill/eval surfaces need
  refreshed eval scaffolds, or whether slice-level `specs` / `tests`
  follow-through is explicitly not needed for this validation-only slice. The
  generic verification checklist at
  `plans/2026-04-21-refine-02-portability-and-copy-readiness.md:186-205` still
  mixes `SELECTION=must-run` guidance with later slice-specific
  `SELECTION=all` proof points, so a fresh `execute` pass would have to guess
  the concrete Milestone 6 contract. Mechanical results: `make validate`
  passed; `git diff --check -- AGENTS.md MAINTENANCE.md README.md
  evals/README.md evals/runtime.json
  plans/2026-04-21-refine-02-portability-and-copy-readiness.md
  specs/evaluation-harness.md specs/repo-surface.md
  specs/workflow-contract.md src/consult/SKILL.md
  src/consult/agents/openai.yaml src/consult/evals/evals.json
  src/execute/SKILL.md src/execute/agents/openai.yaml
  src/execute/evals/evals.json
  src/execute/scripts/providers/codex_loop.py src/plan/SKILL.md
  src/plan/agents/openai.yaml src/plan/assets/plan-template.md
  src/plan/evals/evals.json src/specs/assets/AGENTS.md
  src/tests/evals/evals.json src/verify/SKILL.md
  src/verify/agents/openai.yaml src/verify/evals/evals.json .agents/skills`
  passed; `test -L .agents/skills && readlink .agents/skills` returned
  `../src`; `rg -n "tests-workflow-validation-cryptoli-layer-selection|tests-workflow-validation-cryptoli-backend-coverage|must_run|must-run|selected_workflow" src/tests/evals/evals.json evals/runtime.json specs/evaluation-harness.md evals/README.md`
  confirmed the broader tests must-run case plus the retained narrower
  validation case in tracked repo truth; and inspection of
  `.tmp/evals/2026-04-22-refine-02-m5-tests-all/run.json` plus
  `review-template.md` confirmed the scaffolded tests workspace still reflects
  that Milestone 5 selection correctly. Verdict: `fail`. Remaining gaps:
  rewrite Milestone 6 into one decision-complete validation slice that names
  the exact source-layout dry runs, copied-layout smoke commands, and explicit
  `make eval-init-run ...` selections for the changed skills, and state
  whether additional slice-level `specs` / `tests` sync is not needed before
  the next safe `execute` pass.
- [2026-04-22 execute] Milestone 6 reran the planned validation-only checks
  without reopening repo truth. In the source layout,
  `python3 -m py_compile src/execute/scripts/providers/codex_loop.py src/execute/scripts/providers/codex_loop_dashboard.py`,
  `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  and `make validate` all passed. `make validate` reported 21 workflow cases
  across the shipped harness surface.
- [2026-04-22 execute] In a temporary copied repo containing `.agents/skills/*`
  plus this plan file, both
  `.agents/skills/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  and
  `.agents/skills/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`
  passed and emitted provider commands rooted at the copied
  `.agents/skills/execute/scripts/providers/codex_loop.py`. Copied-layout
  runner smokes for both `execute` and `verify` with a fake Codex adapter that
  honored `--output-schema -o` also passed: both invocations used `-C <repo>`
  rather than `-C <repo>/.agents`, the execute prompt referenced
  `.agents/skills/execute/SKILL.md`, and the verify prompt referenced
  `.agents/skills/verify/SKILL.md`,
  `.agents/skills/execute/SKILL.md`, and
  `.agents/skills/plan/assets/plan-template.md` rather than `src/...` paths.
- [2026-04-22 execute] `make eval-init-run RUN_ID=2026-04-22-refine-02-m6-validation-all SELECTION=all SKILL="consult execute plan tests verify"`
  initialized `.tmp/evals/2026-04-22-refine-02-m6-validation-all`. Inspecting
  `run.json`, `review-template.md`, and the generated `fixtures/`, `outputs/`,
  and `transcripts/` directories confirmed `selection.mode` is `all`, 28
  selected cases cover `consult`, `execute`, `plan`, `tests`, and `verify`,
  the pinned `cryptoli` fixture is present, and the scaffolded review template
  still lists the required later artifacts. No additional `specs` or `tests`
  edits were needed because this validation-only slice exposed no repo-truth
  or eval-truth drift.
- [2026-04-22 verify] Findings: none. Re-ran `make validate`,
  `git diff --check -- AGENTS.md MAINTENANCE.md README.md evals/README.md
  evals/runtime.json
  plans/2026-04-21-refine-02-portability-and-copy-readiness.md
  specs/evaluation-harness.md specs/repo-surface.md
  specs/workflow-contract.md src/consult/SKILL.md
  src/consult/agents/openai.yaml src/consult/evals/evals.json
  src/execute/SKILL.md src/execute/agents/openai.yaml
  src/execute/evals/evals.json
  src/execute/scripts/providers/codex_loop.py
  src/execute/scripts/providers/codex_loop_dashboard.py
  src/plan/SKILL.md src/plan/agents/openai.yaml
  src/plan/assets/plan-template.md src/plan/evals/evals.json
  src/specs/assets/AGENTS.md src/tests/evals/evals.json
  src/verify/SKILL.md src/verify/agents/openai.yaml
  src/verify/evals/evals.json .agents/skills`,
  `test -L .agents/skills && readlink .agents/skills && test -L CLAUDE.md && readlink CLAUDE.md`,
  `git ls-files -s .agents/skills`,
  `python3 -m py_compile src/execute/scripts/providers/codex_loop.py src/execute/scripts/providers/codex_loop_dashboard.py`,
  `python3 src/execute/scripts/providers/codex_loop.py --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  `python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --dry-run --plan plans/2026-04-21-refine-02-portability-and-copy-readiness.md`,
  `rg -n "\\.agents/skills|symlink mirror|copied-layout|decision-complete|under-specified|slice-level|compare or synthesize|independent (consult|verify) pass|tests-workflow-validation-cryptoli-layer-selection|tests-workflow-validation-cryptoli-backend-coverage|branch|PR title|commit" AGENTS.md README.md MAINTENANCE.md evals/README.md specs/workflow-contract.md specs/repo-surface.md specs/evaluation-harness.md src/consult/SKILL.md src/consult/agents/openai.yaml src/consult/evals/evals.json src/execute/SKILL.md src/execute/agents/openai.yaml src/execute/evals/evals.json src/plan/SKILL.md src/plan/agents/openai.yaml src/plan/assets/plan-template.md src/plan/evals/evals.json src/specs/assets/AGENTS.md src/tests/evals/evals.json src/verify/SKILL.md src/verify/agents/openai.yaml src/verify/evals/evals.json evals/runtime.json`,
  and inspected `.tmp/evals/2026-04-22-refine-02-m6-validation-all/run.json`
  plus `review-template.md`; all matched the tightened workflow and eval
  contract, including 28 scaffolded selected cases across the five changed
  skills. Re-ran copied-layout user-mode dry runs plus copied-layout runner
  smokes in a temporary repo copy with a fake Codex adapter that honored
  `--output-schema -o`; both runner modes still used `-C <copied-repo>`, the
  execute prompt referenced `.agents/skills/execute/SKILL.md`, and the verify
  prompt referenced `.agents/skills/verify/SKILL.md`,
  `.agents/skills/execute/SKILL.md`, and
  `.agents/skills/plan/assets/plan-template.md` without leaking `src/...`
  paths. No independent verify pass was used because this invocation only
  provided one plan-driven verify call. Verdict: `pass`. Remaining gaps: none
  for this plan; generated eval workspaces are still scaffolds until a future
  run populates review artifacts, but that is outside this portability slice.

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

- [x] Milestone 1 - Portability hardening
- [x] Milestone 2 - Local mirror + repo-truth sync
- [x] Milestone 3 - Consult/verify handoff tightening
- [x] Milestone 4 - Plan/execute/Git tightening
- [x] Milestone 5 - Eval coverage addition
- [x] Milestone 6 - Validation

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
- [2026-04-21] Resolve the Codex execute-wrapper paths from the current
  installed skill tree (`src/*` in the source repo or `.agents/skills/*`
  after copy) so the helper prompts and Codex `-C` target follow the active
  layout instead of hardcoded source-repo assumptions.
- [2026-04-21] Implement the local mirror as one tracked
  `.agents/skills -> ../src` symlink instead of per-skill links so the source
  repo always exposes copied-layout paths without duplicating files or
  creating a second owning tree.
- [2026-04-21] Close the Milestone 2 tracked-state gap by adding only
  `.agents/skills` to git-tracked repo state and re-running the mirror checks,
  leaving the other in-progress repo-truth edits untouched in this execute
  slice.
- [2026-04-21] Keep independent `consult` and `verify` passes preferred but
  optional. When supported, they should reduce anchoring, but the main session
  still owns the final compare-and-synthesize recommendation or verdict.
- [2026-04-21] Add one explicit `Consult Carry-Forward` section to the plan
  template instead of spreading consult handoff details across unrelated plan
  sections. This keeps durable discoveries and rejected options visible
  without reshaping the broader plan contract before Milestone 4.
- [2026-04-21] When a consult/verify slice changes train-only workflow eval
  cases, complete the required eval-workspace refresh with `SELECTION=all` so
  the scaffold and artifact review cover the changed surface instead of only
  the must-run validation subset.
- [2026-04-21] Treat "decision-complete" as a requirement on the next
  unfinished slice, not on every future milestone equally, so plans stay
  compact while later `execute` passes still have a no-guess contract.
- [2026-04-21] Keep Milestone 4 repo-truth sync scoped to
  `specs/workflow-contract.md` plus the shipped plan template and bootstrap
  AGENTS asset. The top-level repo docs already remained accurate at their
  current summary level, so widening this slice into more doc churn would not
  add signal.
- [2026-04-21] After Milestone 4 verify blocked the next pass, tighten
  Milestone 5 in place rather than reopening Milestone 4. The blocker was on
  the next-slice contract, not on the completed Milestone 4 implementation.
- [2026-04-22] Keep the broader cryptoli tests workflow as the only
  fixture-backed must-run case and retain the narrower backend-only coverage
  scenario as extra non-must-run validation signal. This lands Milestone 5
  without reopening the broader eval-governance contract that still requires
  pinned-fixture workflow evals to remain must-run.
- [2026-04-22] Treat Milestone 6 as a validation-only close-out slice: rerun
  the shipped source-layout and copied-layout wrapper checks, refresh one
  `SELECTION=all` eval workspace across the changed skills, and avoid any new
  repo-truth edits unless those checks expose drift.

## Discoveries

- [2026-04-21] A copied-layout smoke check proved `src/execute/scripts/providers/codex_loop.py`
  currently resolves the repo root to `.agents` after copy and still prompts
  against `src/...` paths, so downstream copy is not yet safe without changes.
- [2026-04-21] The copied dashboard wrapper did not need its own path fix for
  this milestone: once the raw wrapper became location-safe, copied
  `codex_loop_dashboard.py --plain` correctly forwarded to the copied wrapper
  path in user-mode dry runs.
- [2026-04-21] The repo already documented downstream copy into
  `.agents/skills/`, but it lacked a tracked local mirror and explicit
  source-vs-mirror guidance. One repo-level symlink plus synced repo-truth
  docs closes that gap without changing the downstream copy contract.
- [2026-04-21] The local `.agents/skills -> ../src` mirror currently works in
  the worktree and passes validation checks, but `git status --short` still
  shows `?? .agents/`; until that path is tracked, the new docs overstate
  shipped reality.
- [2026-04-21] For the local mirror milestone, filesystem checks alone were
  not enough. The repo-truth claim only became accurate once
  `git status --short` and `git ls-files -s .agents/skills` both reflected the
  symlink entry in git-tracked state.
- [2026-04-21] Milestone 2 verification confirmed the local mirror remains one
  tracked symlink entry, not a duplicated skill tree: `git ls-files -s
  .agents/skills` reports mode `120000`, `readlink .agents/skills` returns
  `../src`, and the top-level layout still matches the documented surface.
- [2026-04-21] The existing plan template already covered repo context,
  blockers, risks, and discoveries, but consult handoff still lacked a named
  landing zone. Adding one small `Consult Carry-Forward` section was enough to
  make the durable handoff explicit without broadening into Milestone 4's
  wider plan-contract tightening.
- [2026-04-21] The consult/verify must-run eval scaffold still selects the
  boundary packs and pinned `cryptoli` validation cases. The new
  compare-and-synthesize guidance was captured in synced train eval truth and
  validated structurally through `make validate`, without broadening this slice
  into must-run policy changes.
- [2026-04-21] `make eval-init-run ... SELECTION=must-run SKILL="consult
  verify"` only scaffolds the validation must-run cases. When a slice changes
  train-only consult/verify workflow evals, the required artifact review needs
  `SELECTION=all` or an equivalent direct harness invocation that includes the
  changed train cases.
- [2026-04-21] `make eval-init-run ... SELECTION=all SKILL="consult verify"`
  scaffolds one combined workspace with both train and validation consult and
  verify cases. The resulting `run.json` listed all 10 selected cases,
  including the changed train workflow entries, while `review-template.md`
  preserved the expected later artifact checklist without changing must-run
  governance.
- [2026-04-21] Once the generic no-guess contract was tightened in Milestone 4,
  Milestone 5 needed its own concrete owning paths, slice-level
  `specs` / `tests` exit criteria, and explicit eval proof points. Task-level
  `Sync Expectations` alone were no longer enough for the next safe
  `execute` handoff.
- [2026-04-21] Task-level `Sync Expectations` alone were not enough to prevent
  later guesswork. The no-guess contract had to be repeated in the milestone
  template, execute selection rules, and verify(plan) fail criteria to survive
  fresh sessions cleanly.
- [2026-04-21] `make eval-init-run ... SELECTION=all SKILL="plan execute
  verify"` scaffolds 17 selected cases for this tightened surface, so an
  all-selection refresh is the right structural check when a slice changes
  both train and validation eval intent across these three skills.
- [2026-04-21] Even after Milestone 4 tightened the generic no-guess contract,
  this plan's next unfinished Milestone 5 still sits at the older summary-only
  level. Task-level `Sync Expectations` plus repo context are not sufficient on
  their own once the next slice must carry explicit slice-level `specs` /
  `tests` exit criteria for later `execute` and `verify` work.
- [2026-04-22] The eval harness still enforces `must_run: true` for workflow
  evals that declare pinned fixture metadata. Keeping the narrower backend-only
  tests scenario as extra validation signal without reopening harness
  governance meant leaving the broader layer-selection case as the only
  fixture-backed tests workflow in this slice.
- [2026-04-22] `make validate` now passes with 21 workflow cases, and
  `.tmp/evals/2026-04-22-refine-02-m5-tests-all/run.json` still shows
  `tests-workflow-validation-cryptoli-layer-selection` as the tests must-run
  workflow while retaining
  `tests-workflow-validation-cryptoli-backend-coverage` as extra non-must-run
  validation signal.
- [2026-04-22] The copied `codex_loop_dashboard.py --plain` dry run matched the
  copied raw wrapper output exactly, so the dashboard still remains a
  presentation-only passthrough after copy.
- [2026-04-22] `make eval-init-run RUN_ID=2026-04-22-refine-02-m6-validation-all
  SELECTION=all SKILL="consult execute plan tests verify"` scaffolds 28
  selected cases across the five changed skills in one workspace, which is the
  right structural refresh for this final validation slice.
- [2026-04-22] Before the Milestone 6 execute pass, the remaining gap was plan
  quality rather than shipped repo truth: Milestone 6 still summarized
  "Validation" at a high level while the generic checklist mixed
  `SELECTION=must-run` and slice-specific `SELECTION=all` guidance, so the
  next `execute` pass would have had to guess the concrete final validation
  contract.
- [2026-04-22] That Milestone 6 plan-quality gap is now closed. The current
  plan file executed as a no-guess validation slice, and the close-out checks
  found no repo-truth or eval-truth drift that required reopening earlier
  milestones.

## Outcomes / Retrospective

- `refine-02` is complete. The repo now ships copy-safe execute wrappers, a
  tracked local `.agents/skills` mirror, tighter
  consult/plan/execute/verify/tests workflow contracts, and refreshed eval
  truth that has been mechanically rechecked in both the source layout and a
  copied `.agents/skills/*` layout. The strict final verify pass against this
  explicit plan file passed with no remaining follow-up slice.
