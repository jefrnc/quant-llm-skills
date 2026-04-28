# quant-llm-skills

> 🇺🇸 **English** | [🇪🇸 Español](./README.es.md) | [🇨🇳 简体中文](./README.zh.md)

> **Skills for quant research with LLMs that don't fall for the traps
> nobody talks about.**

Most "AI trading" skill packs teach Claude how to backtest CANSLIM and
parse 10-Ks for AAPL. They fail the moment you point them at a real
small-cap with sparse XBRL, an active ATM, and four 13D filers reporting
the same shares.

This pack distills hard rules from running production quant pipelines
into Claude Code skills the LLM applies automatically — no system-prompt
hacking, no manual invocation, no extra glue.

## What it catches that a baseline LLM misses

- **Lookahead bias** in any historical query — `period_end` is not a
  publication date.
- **Capacity vs action** — an effective S-3 alone is not a dilution event.
- **ATM vs registered direct vs ELOC** — same 424B5, different trades.
- **The placement agent matters** — Goldman on a secondary ≠ Wainwright
  on an ATM.
- **XBRL gaps for FPIs and SPACs** — the data is in the filing text,
  not the structured feed.
- **13D group double-counting** — naive sum of cover pages overstates
  insider ownership 2–10x.
- **Quantitative dilution scoring** — 0–100 with auditable component
  weights, not vibes.

See [EXAMPLES.md](./EXAMPLES.md) for real prompt-and-response transcripts.

## Skills

| Skill | What it does |
|---|---|
| [**lookahead-safety**](./skills/lookahead-safety/SKILL.md) | Forces `filing_date` as known-date, never `period_end`. The #1 quant-backtest bug. |
| [**sec-filing-types**](./skills/sec-filing-types/SKILL.md) | Disambiguates SEC forms (S-3, 424B, 8-K items, 13D/G, Form 4, 20-F, 6-K, NT 10-K). Knows that a shelf is *capacity*, not action. |
| [**atm-detection**](./skills/atm-detection/SKILL.md) | Multi-signal inference for active ATMs. Distinguishes ATM from ELOC and registered direct. Catches dilution that 8-K-only scanners miss. |
| [**bank-tier-classification**](./skills/bank-tier-classification/SKILL.md) | 4-tier framework mapping placement agents (bulge bracket → small-cap specialist) to expected deal behavior. |
| [**xbrl-fallbacks**](./skills/xbrl-fallbacks/SKILL.md) | When SEC XBRL is empty or 404 (FPIs, recent IPOs, SPACs), defines the cover-page hierarchy and extraction rules. |
| [**dilution-event-scoring**](./skills/dilution-event-scoring/SKILL.md) | 0–100 framework integrating ATM + agent tier + recency + cash runway + structure + history. Reproducible, auditable, with action thresholds. |
| [**insider-dedup**](./skills/insider-dedup/SKILL.md) | Joint-filer / group / family-attribution dedup rules for 13D/G and Form 4 aggregation. Stops the cover-page-sum bug. |

The skills compose: ask "score X's dilution risk" and the scoring skill
calls the ATM, agent-tier, and lookahead skills automatically.

## Install

**Once published to GitHub:**

```
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**For local testing now:**

```
/plugin marketplace add /absolute/path/to/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**Or one-shot via CLI without installing:**

```
claude --plugin-dir /absolute/path/to/quant-llm-skills -p "your prompt"
```

## Who this is for

- Quant retail / boutique funds running point-in-time backtests on
  small caps.
- Anyone using Claude / Cursor for SEC EDGAR research who has been
  burned by lookahead bias or XBRL gaps.
- Trading-system devs who want the LLM to *automatically* apply
  dilution-detection rules without re-explaining them every session.

## Who this is NOT for

- Index / ETF / large-cap-only research where structured data is dense
  and dilution is rare.
- Pure-fundamental long-term investors uninterested in placement
  mechanics.
- Anyone expecting the LLM to *predict* prices — these skills make
  the LLM more rigorous about the data, not clairvoyant about the
  future.

## Tradeoff

These skills bias toward **flagging more risk** than baseline. False
positives on dilution risk are cheap; false negatives are expensive
(unexpected printing into your long). Adjust the scoring thresholds
in [`dilution-event-scoring`](./skills/dilution-event-scoring/SKILL.md)
if you want a less conservative profile.

## Validate

```
claude plugin validate /path/to/quant-llm-skills
```

All skills pass `claude plugin validate` and load via `--plugin-dir`.

## Cursor support

Equivalent rules for Cursor live under [`.cursor/rules/`](./.cursor/rules/).
They are auto-generated from the canonical `SKILL.md` files via
[`scripts/sync-cursor.py`](./scripts/sync-cursor.py); see
[CURSOR.md](./CURSOR.md) for details.

## License

MIT
