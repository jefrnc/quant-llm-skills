# Examples

Real transcripts of `quant-llm-skills` in action. Every response below
was generated with `claude --plugin-dir /path/to/quant-llm-skills` —
no system-prompt tweaks, no manual skill invocation.

> The skill name in parentheses is the one that primarily fired. Many
> responses compose multiple skills automatically.

---

## 1. Scoring real-world dilution risk

**Skills fired:** `dilution-event-scoring`, `atm-detection`,
`bank-tier-classification`, `sec-filing-types`

**Prompt:**

> Score LNAI dilution risk now. Inputs: 424B5 yesterday with H.C.
> Wainwright Sales Agreement, S-3 effective 8 months ago, last 10-Q
> (6 weeks old) shows ~4mo runway + going-concern, 5 prior dilution
> events trailing 12 months. Total + breakdown + verdict only.

**Response:**

> # LNAI Dilution Risk Score — as of 2026-04-27
>
> | Component | Score | Rationale |
> |-----------|------:|-----------|
> | Active ATM detected | **22** | 424B5 + Wainwright Sales Agreement = active ATM, but 10-Q (6 wks old) predates the agreement, so no in-use confirmation yet |
> | Placement agent tier | **20** | H.C. Wainwright on ATM Sales Agreement = Tier 4 |
> | Filing recency | **15** | 424B5 filed yesterday → in last 7 days |
> | Cash runway | **12** | ~4 months → 3–6 month bracket |
> | Structural toxicity | **2** | Going-concern language in last 10-Q (+2). No warrants/discount/ELOC/convert-reset disclosed in inputs |
> | Repeat-dilution history | **7** | 5 events trailing 12 months → 3–5 bracket |
> | **Total** | **78** | |
>
> **Verdict: 🚨 SEVERE (78)** — Treat as continuous selling pressure.
> Fresh ATM with the most aggressive small-cap sales agent, going-concern +
> ~4mo runway means Wainwright is incentivized to print into any strength.
>
> Caveats: ATM points are 22 (not 30) because the 6-week-old 10-Q cannot
> confirm sales under an ATM filed yesterday. Re-score on the next 10-Q —
> if it shows shares sold under the agreement, ATM jumps to 30 → total 86.

**Why this is hard for a baseline LLM:** A naive response would either
give a vibe-based "this is bad" or a 100/100 because everything looks
toxic. The skill enforces *transparent* scoring — each component is
auditable, the 22-vs-30 ATM detail (because the 10-Q predates the
filing) is exactly the kind of nuance that gets lost without the
framework.

---

## 2. Catching the yfinance lookahead trap

**Skill fired:** `lookahead-safety`

**Prompt:**

> I'm building a backtest from 2018-2023. To get shares outstanding
> for each historical date, I'm using yfinance:
> `ticker.info['sharesOutstanding']`. Is this approach correct?
> Be concise.

**Response:**

> **No, this is unsafe.** `ticker.info['sharesOutstanding']` returns the
> **current snapshot only** — yfinance doesn't expose point-in-time
> history through that field. You'd be applying 2026 share counts to
> 2018 dates.
>
> Concrete problem: any company that did a secondary, buyback, split,
> or reverse-split between 2018 and today will have a wrong share count
> for historical dates. For small caps, dilution events make this
> catastrophic — float metrics, market cap, and float rotation will all
> be fictional.
>
> **What to use instead:**
> - **SEC XBRL `CommonStockSharesOutstanding`** — pull from
>   `companyfacts.json`, but key off the **filing's `accepted` date**,
>   not `period_end`. A datapoint covering 2023-12-31 wasn't knowable
>   until the 10-K was filed (often Feb–Mar 2024).
> - **Sharadar SF1 / Polygon financials** — both expose point-in-time
>   share counts with filing dates.
> - If you must use yfinance, `ticker.get_shares_full(start, end)`
>   returns a historical series — verify it's filing-dated, not
>   period-dated, before trusting it.

**Why this is hard for a baseline LLM:** The trap is that the response
*looks* like it's working — `ticker.info['sharesOutstanding']` returns
a number, the backtest runs, the metrics compile. The bug only surfaces
when results don't replicate live trading. The skill catches the bug at
prompt time.

---

## 3. Same filing, different banks → different trades

**Skills fired:** `bank-tier-classification`, `atm-detection`,
`sec-filing-types`

**Prompt:**

> Two tickers. ABCD just announced an underwritten offering led by
> Goldman Sachs and Jefferies. EFGH announced a 424B5 with H.C.
> Wainwright as sales agent for an ATM. Both are small caps. Compare
> the dilution profile briefly.

**Response:**

> **ABCD: underwritten offering, Goldman Sachs + Jefferies**
> - Tier 1 (Goldman) + Tier 2 (Jefferies) — institutional book, "blessed"
>   issuer for a small cap.
> - Underwritten = **firm-commitment, one-shot, fixed share count**.
>   Dilution is discrete and known on pricing.
> - Underwriters have stabilization incentive post-deal; often a price
>   floor near the offering print.
> - **Profile: clean, single dilution event. Low post-deal overhang.**
>
> **EFGH: 424B5 with H.C. Wainwright as sales agent for an ATM**
> - Tier 4 — the dominant small-cap ATM placement agent by deal count.
> - "Sales agent" + 424B5 + ATM language = active at-the-market
>   authorization.
> - ATMs sell into strength. Wainwright-led ATMs frequently coincide with
>   repeat dilution within 30–90 days.
> - **Profile: continuous selling-pressure floor. Every green tick is a
>   potential print until the program is exhausted or terminated.**
>
> **Bottom line:** ABCD is a one-time mark-down with stabilization
> tailwind; EFGH is an open-ended drip with the most aggressive small-cap
> shop running it. Different trades entirely.

**Why this matters:** Both are "small-cap secondaries". A simple
"new offering announced" event tag would treat them identically.
The skill makes the LLM read the agent name as the leading indicator.

---

## 4. Catching the 13D group double-count

**Skill fired:** `insider-dedup`

**Prompt:**

> I'm computing total insider ownership for a small cap. I sum all 13D
> and 13G cover-page share counts and get 47%. The CEO's fund has 4
> related entities (LP, GP, adviser, managing member) that each filed
> separate 13Ds. Is my number right? Be concise.

**Response:**

> No, your 47% is almost certainly inflated ~4x.
>
> The CEO's fund + GP + adviser + managing member chain is a classic
> Section 13(d) **group**. All four 13Ds report the SAME underlying
> shares on their cover pages (Item 2 lists them as joint filers; Item 5
> shows shared voting/dispositive power). Summing them quadruples one
> position.
>
> Fix:
> 1. Group the 4 filings by Item 2 group identity → count as **one**
>    position (use any member's cover-page share count; they'll match).
> 2. Re-sum across distinct groups only.
> 3. Sanity check: deduped insider % + float + ATM-issued shares should
>    reconcile to shares outstanding within ~5%. If you're at 47% naive,
>    you're likely closer to ~15–20% real.

**Why this is hard for a baseline LLM:** The bug is subtle — each 13D
*correctly* reports the position from that filer's perspective. The
double-count only emerges at aggregation. The skill encodes the
"per-share, not per-filer" rule explicitly so the LLM flags it before
the user runs `sum()`.

---

## 5. Recovering shares outstanding when XBRL fails

**Skill fired:** `xbrl-fallbacks`

**Prompt:**

> I'm pulling SEC XBRL for WSHP (a recent FPI listing) but companyfacts
> returns 404. Where do I get shares outstanding? Be concise.

**Response:**

> For WSHP (recent FPI), XBRL gaps are expected. Walk filings in reverse
> chronological order from `submissions/CIK{padded}.json`:
>
> **Source hierarchy (first hit wins):**
> 1. **Most recent 6-K** — interim share-count updates in the body
> 2. **Most recent 20-F cover** — annual, formal cover-page statement
> 3. **F-1 / F-3 / F-3A cover** — registration statements
> 4. **424B prospectus supplement** — discloses pre- and post-offering
>    counts
> 5. DEF 14A as sanity check
>
> **FPI-specific gotchas:**
> - Distinguish **ordinary shares** vs **ADSs** — record the ratio
>   (commonly 1:1, 1:5, 1:10). Float-rotation math uses ADS-equivalent
>   count.
> - Multi-class structures are common — track Class A/B separately,
>   sum for total.
>
> **Tag the result** as `text:SharesOutstanding` with `source_form`,
> `source_accession`, `as_of_date`, `filed_date` — don't silently treat
> as XBRL-quality. Use `filed_date` as the known-date (lookahead-safety),
> not `as_of_date`.

**Why this matters:** Most "AI for SEC data" demos work on AAPL/TSLA
where XBRL is dense. Real small-cap and FPI universes have 30–60% XBRL
gaps. Without this skill, the LLM happily gives the user nothing
(`404`) instead of the actual data sitting in plain text on the filing
cover.

---

## How to reproduce these locally

```
claude --plugin-dir /path/to/quant-llm-skills -p "<the prompt>"
```

Or, after installing the plugin into your Claude Code:

```
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

Then ask the same prompts in any Claude Code session — no flags needed.
