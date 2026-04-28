---
name: code-review-for-quant
description: Use when reviewing or writing Python/Go/SQL code for quant research, backtests, market-data pipelines, or trading systems. Provides a structured checklist of failure modes specific to time-series financial code (lookahead, splits, snapshots, currency, NaN propagation, joint-filer dedup) that generic code review skips.
license: MIT
---

# Code review for quant

Generic code review catches off-by-one errors and missing `with` blocks.
Quant code has its own failure modes — and they're the ones that
silently corrupt research output without raising. This skill enforces
a domain-specific checklist before approving any quant-touching code.

## Core principle

**Quant bugs hide as plausible numbers.** A backtest that runs cleanly
and produces a nice equity curve can still be using future data. The
test "did it crash?" is meaningless. The test is "did each datapoint
trace to a publication date that precedes the query?".

## The checklist

Run this against any function that touches historical financial data.

### A. Time semantics

- [ ] Every read of historical state takes a `query_date` argument
      (or equivalent) and filters on `filing_date <= query_date`
      (or `accepted <= query_date`).
- [ ] No use of `period_end`, `report_date`, or `as_of_date` as the
      known-date for filing data.
- [ ] No use of "current" snapshots (`ticker.info`, latest API value)
      for historical queries.
- [ ] Splits / reverse splits applied with split-date as the cutoff
      (not retroactively to all prior dates).
- [ ] Adjusted prices not used for absolute price thresholds — adjusted
      values change as new splits happen.
- [ ] Earnings revisions / amendments treated as known only from the
      amendment's own filing date.

### B. Data shape

- [ ] Fall-through on missing fields (no `KeyError` crashes when XBRL
      has alternate tags or FPI structure differs).
- [ ] Fall-through to text-extraction when XBRL returns 404 (FPIs,
      SPACs, recent IPOs).
- [ ] Multi-class share structures handled (Class A + Class B, ADSs +
      ordinary shares with ratio conversion).
- [ ] Currency conversion uses point-in-time FX rate, not current.

### C. Aggregation hygiene

- [ ] Joint-filer / Section 13(d) group dedup applied before summing
      insider holdings.
- [ ] Form 144 (intent) NOT counted as Form 4 (executed transaction).
- [ ] 13F filings treated separately from 13D/G (different lag, different
      threshold, different dedup rules).
- [ ] CUSIP changes (mergers, reverse splits) reconciled by ticker
      history, not by CUSIP.

### D. Numerical hygiene

- [ ] Division-by-zero guarded (volume / float, returns / price).
- [ ] `None` / `NaN` propagation explicit — no silent coverage gaps.
- [ ] Outlier handling explicit — bid/ask crosses, halt periods,
      suspicious prints (penny stocks: trades flagged with `condition_codes`
      indicating odd lot / late / out-of-sequence).
- [ ] Currency precision (Decimal vs float) consistent — float drift
      compounds over millions of trades.

### E. Friction realism

- [ ] Slippage modeled as % of price or absolute spread, NOT zero.
- [ ] Borrow / hard-to-borrow APR included for short-side simulations.
- [ ] Locate-failure probability for very-low-float tickers.
- [ ] Bid-ask spread for microcaps (often >5% on actual trades).
- [ ] Halts and circuit breakers handled — not all volume is tradeable.

### F. Reproducibility

- [ ] Random seeds set explicitly for any stochastic component.
- [ ] Data freshness recorded (which day was the underlying CSV pulled).
- [ ] Environment locked (requirements.txt / go.sum / package-lock).
- [ ] Output stamped with both `run_date` and `data_as_of_date`.

### G. Performance traps

- [ ] No O(N) re-reads of the same JSON/CSV inside a `.apply()` loop.
- [ ] No per-bar HTTP / DB calls in tight backtest loops; pre-fetch.
- [ ] No accidental quadratic time on date filtering (use indexed
      lookups, not list comprehensions over the full universe).

## Priority order when reviewing

When listing bugs found in a code review, ALWAYS rank by silent-corruption
potential, not by severity-of-symptom:

1. **Look-ahead bias** — silently wrong, looks fine
2. **Snapshot used for history** — silently wrong, looks fine
3. **Joint-filer over-count** — silently wrong, looks fine
4. **Survivorship bias** — silently wrong, looks fine
5. **Split / adjusted-price misuse** — silently wrong, looks fine
6. **Friction-free assumption** — silently optimistic
7. **Performance bug** — visible, will be fixed when run
8. **Crash bug** — visible, will be fixed at runtime
9. **Style / hygiene** — least urgent

Anti-pattern: leading the review with "you should use a context
manager for `open()`" while the function silently uses `period_end`
as a publication date. The first one is cosmetic; the second corrupts
every backtest result.

## Workflow when handed a snippet

1. Identify what the function does (state lookup, aggregation,
   calculation, simulation).
2. Walk the relevant section of the checklist above.
3. List bugs in **silent-corruption order**, not in code order.
4. For each lookahead-class bug: cite the specific datapoint that
   would leak (e.g., "row with `period_end: 2023-12-31` is unknowable
   on 2024-02-01 if the 10-K was filed 2024-02-15").
5. Propose fixes that align with `lookahead-safety` and other relevant
   skills — don't reinvent the rule.

## Phrases that should trigger this skill

- "review this code"
- "is this backtest correct"
- "audit my pipeline"
- "find bugs in this script"
- "code review"
- any code block containing `pd.DataFrame`, `yfinance`, `requests`,
  `polygon`, `sec`, `companyfacts`, `period_end`, `filing_date`,
  `apply(lambda`

## What this skill is NOT

This is not a generic linter. It does not catch missing semicolons,
unused imports, or PEP8 violations — those are the pre-existing
linter's job. It catches the ~20 quant-specific failure modes that
generic code review consistently misses. Combine with `lookahead-safety`,
`xbrl-fallbacks`, `insider-dedup` and other domain skills for
specific-rule fixes.
