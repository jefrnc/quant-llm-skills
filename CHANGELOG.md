# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `code-review-for-quant` skill — domain-specific code-review checklist
  ranking bugs by silent-corruption potential.
- `BENCHMARKS.md` — empirical Haiku / Sonnet / Opus comparisons.
  Highlight: Haiku catches the XBRL lookahead bug 0% baseline → 100%
  with plugin.
- `evals/` regression test suite (Anthropic skill-creator pattern):
  `evals.yaml` manifest with one eval per skill, `run_evals.py` runner
  with optional baseline comparison, optional GitHub Actions workflow
  gated on `RUN_EVALS=true` repo variable + `ANTHROPIC_API_KEY` secret.
  `make evals` and `make evals-baseline` targets added.
- `transaction-cost-modeling` skill — realistic friction defaults for
  small caps (slippage floors, borrow APR, locate-failure handling,
  PFOF, Almgren-Chriss applicability). Two evals: `cost-borrow-apr-realism`
  and `cost-locate-failure-not-slippage`.
- `survivorship-bias` skill — universe-construction trap with focus on
  small-cap-specific patterns: reverse-split-then-delist phantom returns,
  ATM-into-delisting, SPAC merger flips. Eval: `survivorship-reverse-split-delist`.
- BENCHMARKS headline updated to typically 8–9 of 11 differentiators
  on Haiku 4.5 (with run-to-run variance honestly disclosed).

## [0.1.0] — 2026-04-27

Initial release.

### Added

- Seven Claude Code skills covering quant-research traps:
  - `lookahead-safety` — `filing_date` as known-date, never `period_end`
  - `sec-filing-types` — taxonomy for S-3, 424B, 8-K items, 13D/G,
    Form 4, 20-F, 6-K, NT 10-K
  - `atm-detection` — multi-signal inference for active ATM /
    distinguishes ATM vs ELOC vs registered direct
  - `bank-tier-classification` — 4-tier placement-agent framework
  - `xbrl-fallbacks` — cover-page hierarchy when XBRL is empty/404
  - `dilution-event-scoring` — 0-100 framework with auditable
    component breakdown
  - `insider-dedup` — joint-filer / group / family-attribution rules
- Cursor rules under `.cursor/rules/` auto-generated from canonical
  `SKILL.md` files via `scripts/sync-cursor.py`
- Trilingual READMEs (English, Spanish, Chinese)
- `EXAMPLES.md` with 5 reproducible prompt-and-response transcripts
- `LAUNCH.md` playbook with concrete pre-launch checklist and
  T+0 / T+1 / T+2 motion across X / HN / Reddit / aggregator PRs
- `scripts/validate.sh` static-validation suite for CI
- `scripts/smoke-test.sh` live dispatch check via `claude --plugin-dir`
- GitHub Actions workflow that runs `validate.sh` on every push and PR
