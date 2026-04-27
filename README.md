# quant-llm-skills

Skills for doing quant research with LLMs without falling into the traps
that nobody talks about: lookahead bias, filing semantics, dilution
detection, point-in-time data hygiene.

> Status: **early WIP** — currently 1 skill, more coming.

## Why

Every "AI for trading" repo on GitHub teaches the LLM to backtest CANSLIM.
None of them teach it that XBRL `period_end` is not a publication date,
or that an S-3 alone doesn't mean an ATM is active, or that a Tier-4
placement agent radically changes the dilution profile.

This pack distills hard-won rules from running production quant pipelines
into Claude/Cursor/Codex skills so the LLM applies them automatically.

## Install (Claude Code)

From within Claude Code:

```
/plugin marketplace add /absolute/path/to/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

Once published to GitHub, the install becomes:

```
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

## Skills

| Skill | What it does |
|---|---|
| **lookahead-safety** | Forces the LLM to use `filing_date` as known-date, never `period_end`. Catches the #1 backtest bug. |

More coming: `sec-filing-types`, `atm-detection`, `bank-tier-classification`,
`xbrl-fallbacks`, `dilution-event-scoring`, `insider-dedup`.

## License

MIT
