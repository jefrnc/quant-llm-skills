# Launch playbook

Concrete steps to publish `quant-llm-skills` and run a launch motion.
Adapt the cadence to your bandwidth.

## T-0: Pre-launch checklist

- [ ] `bash scripts/smoke-test.sh` passes
- [ ] `python3 scripts/sync-cursor.py` was run after the last SKILL.md edit
- [ ] All three READMEs (en / es / zh) reflect the same skill list
- [ ] `EXAMPLES.md` transcripts still reproduce on the current code
- [ ] Sensitive data scrubbed — no real broker IDs, no production paths,
      no proprietary regex patterns (deliberate: this skill pack ships
      reasoning, not implementation)
- [ ] Repo description on GitHub set: *"Skills for quant research with
      LLMs that don't fall for the traps nobody talks about (lookahead
      bias, filing semantics, ATM detection, dilution scoring)"*
- [ ] Topics added on GitHub: `claude-code`, `claude-skills`, `cursor`,
      `quant`, `trading`, `sec-filings`, `dilution`, `small-caps`

## T-0: Push to GitHub

```bash
gh repo create jefrnc/quant-llm-skills --public \
    --description "Skills for quant research with LLMs without lookahead bias, filing-parsing pitfalls, or naive data assumptions" \
    --source . --push
```

After push, verify the install path works for someone else:

```bash
# In a different machine or different Claude Code session:
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

## T+1 day: 60-90s demo video

Record a screencast that:

1. Opens a Claude Code terminal in any directory.
2. Types one of the EXAMPLES.md prompts (the 88-score scenario is the
   most demo-able — input narrative, output structured score with
   verdict).
3. Cuts to the response with the score table visible.
4. Ends on the install command + repo URL.

No editing required. Phone screen recording into iMovie is enough.
The asset is for embedding in tweets and HN comments — embeddable
videos triple engagement vs link-only posts.

## T+1 day: X (Twitter) thread

Open with a hook that names the gap, not the tool:

> Every "AI for trading" skills pack on GitHub teaches Claude how to
> backtest CANSLIM. None of them know what an S-3 filing means at
> 4:01 AM premarket.
>
> So I built one that does. 7 skills, MIT, Claude + Cursor.
> [video]

Continue with a thread of 4-6 tweets, one per signature skill
(lookahead-safety, atm-detection, dilution-scoring, insider-dedup),
each with a one-line example of the bug it catches.

Tag in the last tweet: relevant accounts (small-cap traders you
respect, the karpathy-skills author, anyone running prominent claude
skills aggregators).

## T+1 day: HN Show post

Title:

> Show HN: I packaged 5 years of small-cap dilution-detection rules
> into Claude skills

Body — 4 short paragraphs:

1. The problem (every trading skills pack works on AAPL, fails on
   small caps with sparse XBRL and active ATMs).
2. What this is (7 SKILL.md files, no code, MIT, Claude + Cursor).
3. The signature skill (dilution-event-scoring — show the 88/100
   transcript).
4. What's next (more skills if there's interest, contributions
   welcome).

Link directly to the GitHub repo, NOT to a personal site.

## T+2 day: Reddit cross-posts

- **r/algotrading** — focus on the lookahead-safety + insider-dedup
  angles (audience is technical, sees through hype).
- **r/Daytrading** — lead with the 88/100 scoring demo (audience is
  practitioner, wants applied output).
- **r/ClaudeAI** and **r/cursor** — focus on the multi-skill
  composition story (audience is tooling-curious).
- **r/SecurityAnalysis** — mention the SEC filing-types and bank-tier
  framework (audience appreciates rigor).

DO NOT cross-post all on the same day; space by 12-24 hours so each
sub gets a fresh post.

## T+2 day: LATAM / Spanish push

Once English traction is established, post the Spanish thread:

- X thread in Spanish referencing `README.es.md`
- LinkedIn post (LATAM fintech audience uses LinkedIn more than X)
- Tag: LATAM quant accounts, Spanish-speaking trading communities

The agent research confirmed near-zero competition in this segment —
a Spanish-language skill pack is novelty.

## T+1 week: Submit to aggregators

Open PRs against:

- [ ] `VoltAgent/awesome-agent-skills` — primary aggregator
- [ ] `travisvn/awesome-claude-skills` — secondary
- [ ] `rohitg00/awesome-claude-code-toolkit` — secondary
- [ ] `awesome-mcp-servers` (finance section) — only if you eventually
      add an MCP server companion

Use a one-line entry that emphasizes the gap, not the count:
*"Skills for small-cap quant research: lookahead safety, ATM detection,
dilution scoring."*

## T+2 weeks: Iterate based on feedback

If the launch traveled:

- [ ] Add the most-requested skill (likely candidates: misprint
      detection, gap-and-go patterns, dark-pool reading, position
      recycling)
- [ ] Bump version to 0.2.0 in `.claude-plugin/plugin.json`
- [ ] Update CHANGELOG.md (create if needed)

If the launch didn't travel:

- [ ] Read the comments / issues — what specifically didn't land?
- [ ] If "too niche" feedback: extract the 2-3 most universal skills
      (lookahead-safety, sec-filing-types) into a separate broader
      pack and re-launch.
- [ ] If "too thin" feedback: add 3-5 more skills before re-launching.

## What NOT to do

- **Don't price-bait.** Saying "Claude can replace your $200/mo
  Bloomberg" is the hype-track that turns serious quants off.
- **Don't claim live trading PnL.** This is a research-discipline pack,
  not a trading system.
- **Don't post the dilution-event-scoring formula as the headline.**
  The framework is the value; the specific weights are calibration
  details.
- **Don't engage with negative comments arguing about specific firms
  in `bank-tier-classification`.** Point to the "this is behavior
  prediction, not firm quality" disclaimer in the skill body and
  move on.

## Star ceiling realism

Per the launch research:

- **Base case (no celebrity boost):** 1.5k–4k stars over 4-8 weeks
  if the launch motion is well-executed.
- **HN front page:** 8k–15k stars in 1-2 weeks.
- **The Karpathy ceiling (90k+):** unlikely without an unrelated
  celebrity tailwind. Don't anchor on it.

The real win is not the star count but the **inbound interest** — DMs
from quants asking about the production pipeline, contributions
expanding the skill set, and the personal-brand compound that lets
your next launch start from a higher baseline.
