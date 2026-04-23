.DEFAULT_GOAL := help

PYTHON ?= python3
SELECTION ?= must-run
PROFILE ?=
SKILL ?=
TARGET ?=

.PHONY: help validate eval-init-run sync

help:
	@printf '%s\n' \
		'Repo maintenance surface:' \
		'  make validate' \
		'      Run repo-level validation for skill metadata, local asset integrity, and eval harness invariants.' \
		'  make sync TARGET=/abs/path/to/repo [SKILL="consult execute"]' \
		'      Sync filtered skill payloads into a downstream repo and refresh its managed README.md workflow section.' \
		'  make eval-init-run RUN_ID=<run-id> [SELECTION=must-run|validation|all] [SKILL="consult execute"] [PROFILE=<profile>]' \
		'      Scaffold .tmp/evals/<run-id>/ through evals/scripts/harness.py without duplicating its logic.' \
		'  python3 scripts/sync_downstream.py --help' \
		'      Show the direct downstream sync helper interface behind make sync.' \
		'  python3 evals/scripts/harness.py --help' \
		'      Show the direct script interface behind the Makefile wrappers.' \
		'  python3 src/execute/scripts/loop.py --help' \
		'      Show the optional explicit-plan execute/verify helper contract.' \
		'  python3 src/execute/scripts/loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"' \
		'      Preview the optional explicit-plan execute/verify helper without stateful work.' \
		'  python3 src/execute/scripts/providers/codex_loop.py --help' \
		'      Show the optional repo-local Codex convenience wrapper.' \
		'  python3 src/execute/scripts/providers/codex_loop.py --plan plans/<file>.md' \
		'      Run the repo-local Codex convenience wrapper with its default real-run settings.' \
		'  python3 src/execute/scripts/providers/codex_loop_dashboard.py --plan plans/<file>.md' \
		'      Run the optional repo-local Codex dashboard over the wrapper flow.' \
		'  python3 src/execute/scripts/providers/codex_loop_dashboard.py --plain --plan plans/<file>.md' \
		'      Bypass the dashboard and use the raw Codex wrapper surface.'

validate:
	$(PYTHON) evals/scripts/harness.py validate

sync:
	@if [ -z "$(TARGET)" ]; then \
		echo "TARGET is required, e.g. make sync TARGET=/abs/path/to/repo" >&2; \
		exit 2; \
	fi
	$(PYTHON) scripts/sync_downstream.py --target "$(TARGET)" $(foreach skill,$(SKILL),--skill "$(skill)")

eval-init-run:
	@if [ -z "$(RUN_ID)" ]; then \
		echo "RUN_ID is required, e.g. make eval-init-run RUN_ID=eval-refresh-01" >&2; \
		exit 2; \
	fi
	$(PYTHON) evals/scripts/harness.py init-run --run-id "$(RUN_ID)" --selection "$(SELECTION)" $(if $(strip $(PROFILE)),--profile "$(PROFILE)",) $(foreach skill,$(SKILL),--skill "$(skill)")
