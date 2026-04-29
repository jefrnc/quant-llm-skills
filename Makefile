# Common tasks for quant-llm-skills.

.DEFAULT_GOAL := help

.PHONY: help validate smoke sync evals evals-baseline clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

validate:  ## Run static checks (manifest, frontmatter, cursor sync)
	@bash scripts/validate.sh

smoke:  ## Live dispatch test via claude --plugin-dir
	@bash scripts/smoke-test.sh

sync:  ## Regenerate .cursor/rules/*.mdc from skills/*/SKILL.md
	@python3 scripts/sync-cursor.py

evals:  ## Run skill regression evals on Haiku
	@python3 evals/run_evals.py

evals-baseline:  ## Run evals with baseline (no plugin) comparison
	@python3 evals/run_evals.py --baseline

clean:  ## Remove generated artifacts (regeneratable via `make sync`)
	@rm -rf .cursor/rules
	@echo "Removed .cursor/rules/ — run 'make sync' to regenerate"
