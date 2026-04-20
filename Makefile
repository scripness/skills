.DEFAULT_GOAL := help

PYTHON ?= python3
SELECTION ?= must-run
PROFILE ?=
SKILL ?=

.PHONY: help validate eval-init-run

help:
	@printf '%s\n' \
		'Repo maintenance surface:' \
		'  make validate' \
		'      Run repo-level validation for skill metadata, local asset integrity, and eval harness invariants.' \
		'  make eval-init-run RUN_ID=<run-id> [SELECTION=must-run|validation|all] [SKILL="consult execute"] [PROFILE=<profile>]' \
		'      Scaffold .tmp/evals/<run-id>/ through evals/scripts/harness.py without duplicating its logic.' \
		'  python3 evals/scripts/harness.py --help' \
		'      Show the direct script interface behind the Makefile wrappers.' \
		'  python3 src/execute/scripts/plan_loop.py --help' \
		'      Show the optional explicit-plan execute/verify helper contract.' \
		'  python3 src/execute/scripts/plan_loop.py --dry-run --plan plans/<file>.md --provider-command "./path/to/non-interactive-runner"' \
		'      Preview the optional explicit-plan execute/verify helper without stateful work.'

validate:
	$(PYTHON) evals/scripts/harness.py validate

eval-init-run:
	@if [ -z "$(RUN_ID)" ]; then \
		echo "RUN_ID is required, e.g. make eval-init-run RUN_ID=eval-refresh-01" >&2; \
		exit 2; \
	fi
	$(PYTHON) evals/scripts/harness.py init-run --run-id "$(RUN_ID)" --selection "$(SELECTION)" $(if $(strip $(PROFILE)),--profile "$(PROFILE)",) $(foreach skill,$(SKILL),--skill "$(skill)")
