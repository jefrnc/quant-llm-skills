# Common tasks for quant-llm-skills.

.DEFAULT_GOAL := help

.PHONY: help validate smoke sync clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate:  ## Run static checks (manifest, frontmatter, cursor sync)
	@bash scripts/validate.sh

smoke:  ## Live dispatch test via claude --plugin-dir
	@bash scripts/smoke-test.sh

sync:  ## Regenerate .cursor/rules/*.mdc from skills/*/SKILL.md
	@python3 scripts/sync-cursor.py

clean:  ## Remove generated artifacts (regeneratable via `make sync`)
	@rm -rf .cursor/rules
	@echo "Removed .cursor/rules/ — run 'make sync' to regenerate"
