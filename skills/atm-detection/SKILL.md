---
name: atm-detection
description: Use when determining whether a company has an active At-The-Market (ATM) offering, controlled equity offering, or equity line (ELOC). Defines the multi-signal inference required to distinguish ACTIVE dilution from dormant shelf capacity, and disambiguates ATM from ELOC.
license: MIT
---

# ATM Detection

ATM offerings are the dominant slow-bleed dilution mechanism in small caps.
Detecting them requires **inference from multiple co-occurring signals** —
no single filing or phrase is sufficient. Most quant pipelines either
miss them entirely (looking only for 8-K item 3.02) or flag every S-3
as ATM (false positives that drown the signal).

## Core inference rule

**An ATM is ACTIVE only when all three are true:**

1. There is an **effective shelf registration** (S-3, S-3ASR, F-3) AND
2. There is a **sales agreement** with a placement agent referenced
   in a recent 424B prospectus supplement (typically 424B5 for US, 424B4
   for FPIs) AND
3. The agreement / supplement contains language explicitly authorizing
   **at-the-market** sales (vs. a one-shot registered direct).

Missing any one of these = NOT an active ATM (could be dormant shelf,
could be a registered direct, could be a private placement).

## Required signals (decision matrix)

| Signal | Where it lives | What to look for |
|--------|---------------|------------------|
| Effective shelf | S-3 / S-3ASR / F-3 with `effective` status | `effectiveDate` is set |
| Placement agent retained | 424B5 / 424B4 cover or "Plan of Distribution" section | Named agent (one or more) |
| ATM authorization language | 424B prospectus supplement OR underlying sales agreement (often filed as Ex-1.1 or Ex-10.x to an 8-K) | See phrase list below |
| Active ATM (not just authorized) | Subsequent 10-Q "Stockholders' Equity" or "Subsequent Events" note | Discloses shares sold under ATM during period, OR confirms agreement remains in effect |

The first two confirm STRUCTURE. The third confirms TYPE (ATM vs.
registered direct). The fourth confirms ACTIVITY (in-use vs. dormant).

## Phrases that indicate ATM (not exhaustive)

In the prospectus supplement or sales agreement:

- "at-the-market offering" / "at the market offerings"
- "**sales agreement**" with a placement agent (this phrase is the
  highest-precision single signal in 424B documents)
- "**controlled equity offering**" / "**Controlled Equity Offering**"
  (a Cantor Fitzgerald trademarked term — same mechanism)
- "**common stock purchase agreement**" — usually ELOC, not ATM (see
  below)
- "ordinary brokers' transactions"
- "negotiated transactions"
- "block trades, if and when negotiated"
- "as defined in Rule 415(a)(4)" (the regulatory hook for ATMs)
- "any method permitted by law deemed to be an 'at the market' offering"

## ATM vs ELOC vs Registered Direct (the three confusions)

These mechanisms all use a shelf and dribble shares into the market,
but they are NOT the same and have different toxicity profiles.

| Mechanism | Counterparty | Pricing | Discretion | Typical agreement language |
|-----------|--------------|---------|------------|----------------------------|
| **ATM** | Placement agent (bank) selling into open market | Market price | Issuer-controlled volume | "Sales Agreement" / "at-the-market" |
| **ELOC** | Specific investor (e.g., Lincoln Park, Yorkville, B. Riley) | Discount to recent VWAP | Issuer-initiated puts | "Common Stock Purchase Agreement" / "Equity Line" / "Standby Equity Purchase Agreement" |
| **Registered Direct** | One-time investor(s) | Negotiated, typically discount | Single-shot | "Securities Purchase Agreement" + 424B5 covering only that takedown |

ELOCs are typically MORE toxic per share than ATMs (forced discount,
counterparty incentivized to short into puts) but often slower per day.
A registered direct is one-and-done — confirm via 8-K item 1.01 + 3.02
within days.

## Common false positives and false negatives

**False positives (saying "ATM active" when it isn't):**

- Effective S-3 with no 424B in 6+ months → dormant shelf, no ATM in flight.
- 424B5 for a registered direct (one-time financing) — language will
  reference a "Securities Purchase Agreement" with named investors,
  not a "Sales Agreement" with an agent.
- 424B5 for an underwritten secondary — has an "Underwriting Agreement",
  fixed share count, single offering.

**False negatives (missing an active ATM):**

- ATM established years ago, recently re-upped via prospectus supplement
  amendment (424B3) — easy to miss if you only watch B5.
- ATM language buried in the SALES AGREEMENT (Ex-1.1) rather than the
  424B itself; some issuers reference but do not duplicate.
- FPIs use 424B4 instead of 424B5 — searching only B5 misses them.
- Re-stated/amended 424Bs (e.g., 424B5/A) that supersede prior versions.

## Workflow when asked "does company X have an ATM"

1. **Pull all forms in the last ~12 months**: S-3, S-3ASR, F-3, plus
   all 424B variants (B1–B7) plus 8-Ks with attached agreements.
2. **Confirm shelf is effective.** If no effective S-3/F-3, stop —
   no ATM possible.
3. **Look for 424B with sales-agreement language.** Highest-precision
   single phrase: "sales agreement" + named agent in the cover/Plan
   of Distribution.
4. **Distinguish from registered direct / ELOC.** Apply the table above.
   If the agreement is a "Common Stock Purchase Agreement" with a single
   investor, it's an ELOC, not an ATM.
5. **Check active vs dormant.** Pull the most recent 10-Q. The
   "Stockholders' Equity" or "Subsequent Events" note usually states
   whether the ATM remains effective and how much has been sold during
   the period.
6. **Stamp with `lookahead-safety`.** Whatever you conclude is true
   only as of the LATEST filing in your set. An ATM established last
   week was not active last month.

## Decision rule for "is dilution imminent"

Active ATM + low cash runway (<6 months) in last 10-Q + recent strength
(green day, gap up) = **highest-probability dilution window**. Issuers
with active ATMs sell aggressively into strength because that is when
they get the best price.

## Phrases that should trigger this skill

- "is X doing an ATM"
- "active ATM" / "at-the-market offering"
- "controlled equity offering"
- "ELOC" / "equity line of credit"
- "shelf takedown"
- "is this S-3 in use"
- "registered direct vs ATM"
- "Sales Agreement" / "Common Stock Purchase Agreement"
- "Lincoln Park" / "Yorkville" / "B. Riley" + offering context

## What this skill is NOT

This is not a parser. It does not extract numbers from filings. It
provides the inference rules needed to interpret the parsed data
correctly — i.e., to decide whether a set of filings constitutes
an active ATM. Combine with `sec-filing-types` for form semantics,
`lookahead-safety` for time semantics, and (when available)
`bank-tier-classification` for placement-agent toxicity grading.
