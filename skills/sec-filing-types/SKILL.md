---
name: sec-filing-types
description: Use when interpreting SEC filings, EDGAR data, or specific form types (S-3, 424B, 8-K, 10-K, 13D/G, Form 4, 20-F, 6-K, F-1, NT 10-K, etc.). Disambiguates what each form actually means for a company's float, dilution risk, and material events.
license: MIT
---

# SEC Filing Types

A reference and decision guide for interpreting SEC forms in the context
of small-cap and quant research. Most quant code mishandles forms because
it treats "a filing exists" as the signal — the form TYPE and SPECIFIC
ITEM are the signal.

## Core principle

**A form's name tells you the company's PERMISSION to do something. The
specific item or supplement tells you whether they ACTED on it.**

- An effective `S-3` means a company *can* sell shares from the shelf.
  It does NOT mean they did.
- An `S-3` plus a recent `424B5` plus a 10-Q reference to "at-the-market
  offering" means they ARE selling. That is the dilution signal.
- An `8-K` is a sealed envelope until you read its specific items.
  Item 1.01 is benign or terrifying depending on the agreement.

Always inspect the SPECIFIC item / supplement / amendment, never the
form name alone.

## Form reference (focused on small-cap dilution context)

### Registration and offerings (the dilution machinery)

| Form | What it means | Dilution implication |
|------|---------------|----------------------|
| **S-1** / S-1/A | IPO registration / amendment | New issuer; lockups in effect |
| **S-3** | Shelf registration (US issuer) | Permission, not action. Effective shelf = capacity to sell |
| **S-3ASR** | Automatic shelf (large issuers) | Same as S-3 but no SEC review delay |
| **S-8** | Employee plan registration | Adds shares to float as RSUs/options vest |
| **F-1** / F-3 | Foreign issuer equivalents of S-1 / S-3 | Same logic, FPI |
| **424B1**–**424B7** | Prospectus supplement (actual takedown) | **THIS is the action.** Specifies shares offered, price, agents |
| **FWP** | Free writing prospectus | Marketing material, often pre-pricing of an offering |

### Material events

| Form | Item | Meaning |
|------|------|---------|
| **8-K** | 1.01 | Material definitive agreement (financing, partnership) — read the agreement |
| **8-K** | 1.03 | Bankruptcy / receivership — usually catastrophic |
| **8-K** | 2.01 | Completion of acquisition — share issuance possible |
| **8-K** | 2.02 | Earnings results |
| **8-K** | 3.02 | Unregistered equity sale (private placement / PIPE) — dilution happened |
| **8-K** | 3.03 | Modification of rights of holders |
| **8-K** | 4.01 / 4.02 | Auditor change / non-reliance on prior financials — red flag |
| **8-K** | 5.02 | Officer / director departure or appointment |
| **8-K** | 5.07 | Shareholder vote results |
| **8-K** | 7.01 | Reg FD disclosure (often offering announcement) |
| **8-K** | 8.01 | Other events — read the body |

### Periodic reports

| Form | Cadence | Use for |
|------|---------|---------|
| **10-K** | Annual (US issuer) | Cover-page shares outstanding; full disclosures |
| **10-K/A** | Annual amendment | **Supersedes** the original from its own filing date forward |
| **10-Q** | Quarterly | Cover-page shares; subsequent-events note critical for offerings |
| **20-F** | Annual (FPI) | FPI equivalent of 10-K |
| **6-K** | Interim (FPI) | FPI equivalent of 10-Q + 8-K combined |
| **NT 10-K** / **NT 10-Q** | Late filing notice | Form 12b-25 — flag for compliance / Nasdaq listing risk |

### Ownership

| Form | Filer | Trigger / use |
|------|-------|---------------|
| **SC 13D** | Beneficial owner >5% (active intent) | Activist or controlling stake |
| **SC 13G** | Beneficial owner >5% (passive) | Institutional (Vanguard, BlackRock) |
| **SC 13D/A**, **SC 13G/A** | Amendments | Material change in holdings or intent |
| **13F** | Institutional manager ($100M+) | Quarterly, **45-day lag** — never realtime |
| **Form 3** | Initial insider statement | First-time officer / director / 10% holder |
| **Form 4** | Insider transaction | Buys, sells, option exercises — usually within 2 business days |
| **Form 5** | Annual catch-up insider | Transactions exempt from Form 4 |
| **Form 144** | Notice of intent to sell restricted shares | Affiliate signaling intent (not always executed) |

### Governance & misc

| Form | Use |
|------|-----|
| **DEF 14A** | Proxy statement; record-date share count, exec comp |
| **PRE 14A** | Preliminary proxy |
| **DEFA14A** | Additional proxy materials |
| **CORRESP**, **UPLOAD** | SEC correspondence (letters, comment-letter responses) |

## Decision rules small-cap-relevant

1. **"Is this company actively diluting?"**
   Need (a) effective S-3/F-3 + (b) 424B in the last ~30 days OR
   8-K item 3.02 + (c) low cash runway in last 10-Q. All three together
   = active dilution. Just an S-3 = capacity only.

2. **"Is the offering toxic structure?"**
   Look at the 424B for: warrants attached, pricing at discount to
   market, placement agent identity (see `bank-tier-classification`),
   ELOC / equity line language, "best efforts" vs "firm commitment".

3. **"Should I trust the latest 10-K numbers?"**
   Check for any 10-K/A filed AFTER the 10-K. The amendment supersedes
   from its own filing_date forward (see `lookahead-safety`).

4. **"Does this 8-K matter?"**
   Items 1.01, 1.03, 3.02, 4.01, 4.02, 5.02 require reading the body.
   Item 2.02 (earnings) is routine. Item 7.01 is often a heads-up of
   a pending offering — pair with same-day or next-day 424B watch.

5. **"Is this insider buying or selling?"**
   Form 4 transaction codes: P (open-market purchase) and S (open-market
   sale) matter most. A (grant), M (option exercise), F (tax withhold)
   are noise for sentiment.

6. **"Late filing — should I care?"**
   NT 10-K / NT 10-Q triggers a 15-day extension (5 for 10-Q). Failure
   to file by the extension creates Nasdaq compliance risk and is a
   short-side signal for very small companies.

## Common confusions

- **S-1 vs S-3.** S-1 is for new issuers / first registrations. S-3 is
  for established issuers raising via a shelf. Confusing these mis-frames
  the company's stage.
- **"Effective" vs "filed".** S-3 has both: SEC declares effective some
  weeks after filing. Until effective, no takedown is possible.
- **424B variants.** B1–B7 differ in WHAT is being supplemented. B5 is
  the most common for small-cap shelf takedowns; B2 for IPO-related;
  B4 for FPIs. The variant matters for parsing but all are takedowns.
- **13D vs 13G.** Same threshold (>5%), different intent. 13D = active,
  13G = passive. A 13G → 13D conversion is a strong signal.
- **6-K is not 8-K.** FPIs have no 8-K; material events flow through 6-K.
  Don't filter for "8-K" on FPIs — you'll miss everything.
- **Form 144 ≠ Form 4.** 144 is intent to sell restricted shares; the
  actual sale (if it happens) appears later as a Form 4. Treating 144
  as an executed sale is a common quant bug.

## Workflow when analyzing a filing list

1. Bucket filings by category (registration, periodic, event, ownership).
2. For 8-Ks, immediately partition by item number — don't treat them
   as a single bucket.
3. For each registration form, find the corresponding takedown
   (424B / 8-K item 3.02 / S-8 effective date) — registration without
   takedown is capacity, not action.
4. For amendments (10-K/A, S-3/A, etc.), apply lookahead-safety:
   the amendment is known only from ITS filing date.
5. For ownership filings, dedupe joint filers and treat 13F with the
   45-day lag explicitly.

## Phrases that should trigger this skill

- "what does an 8-K item X mean"
- "is an S-3 a dilution event"
- "should I worry about this 424B"
- "13D vs 13G"
- "explain this filing"
- any specific form name: S-1, S-3, 424B5, 8-K, 10-K, 20-F, 6-K, 13D, 13G, 13F, Form 4, NT 10-K, DEF 14A
- "EDGAR" + analysis
- "is this company diluting"

## What this skill is NOT

This is not a parser or extractor. It does not pull values from filings.
It tells you what each form / item / amendment MEANS so the LLM can
reason correctly about the data once it's pulled. Combine with
`lookahead-safety` for time semantics, and (when available)
`atm-detection` and `bank-tier-classification` for dilution-specific
inference.
