---
name: insider-dedup
description: Use when aggregating beneficial-ownership filings (Schedule 13D, 13G, amendments) or insider transaction filings (Form 3, 4, 5, 144) to compute total insider holdings or insider activity. Defines the joint-filer, group, and shared-voting-power deduplication rules so that a single position is not double-counted across N filers.
license: MIT
---

# Insider Holdings Dedup

The default join of "all insider filings → sum of shares" overcounts
positions, often by 2–10x. The reason: SEC rules require multiple
related parties (funds, GPs, advisers, family members, trustees,
beneficial owners) to each file a 13D/G or Form 4 covering the SAME
underlying shares. Naive summation = fictional ownership numbers.

## Core principle

**Beneficial ownership is per-share, not per-filer.** If three filers
report the same 1,000,000 shares because of a shared-voting-power
arrangement, the position is 1,000,000 — not 3,000,000.

The reverse is also true: separate parties may individually file
13D/G for distinct positions. You cannot blindly dedup either; you
must read the filings.

## Where double-counting happens

### Schedule 13D / 13G groups

A typical activist or institutional 13D group:

```
Filer 1: The fund (Limited Partnership)        — reports 1,000,000 sh
Filer 2: The fund's GP (LLC)                   — reports 1,000,000 sh
Filer 3: The investment manager / adviser      — reports 1,000,000 sh
Filer 4: The CEO / managing member (individual) — reports 1,000,000 sh
```

All four are filing the same SC 13D as a "group". The cover page of
each filing reports the same 1,000,000 shares. Naive sum = 4,000,000;
true position = 1,000,000.

### Form 4 transaction filings

When an executive transacts through a trust, an LLC, or a family
office, multiple Form 4s may be filed for the same transaction:

- One by the executive
- One by the trust / LLC entity
- One by the family member (spouse / dependent) if reporting required

The transaction `S 50,000 @ $10.00` may appear three times for what
is one sale.

### 13G institutional cluster

Vanguard, BlackRock, and similar issuers file at the asset-manager
level with multiple subsidiary entities. Same beneficial position,
multiple cover-page disclosures.

## Dedup rules (in priority order)

1. **Group identity (Item 2)**. If multiple 13D/G filings list each
   other as members of the same Section 13(d) group, treat as ONE
   position. The cover-page share counts of all members are typically
   identical (or report sub-allocations summing to the group total).

2. **Shared voting / dispositive power**. Schedule 13D Item 5 reports
   "sole" vs "shared" voting and dispositive power. When two filers
   each report shared power over the same N shares, those N shares
   appear once, not twice.

3. **Family attribution**. Spouse and dependent-children holdings
   are reported on the executive's Form 4 with footnotes ("shares
   held by spouse"). If the spouse files separately, dedup against
   the executive's filing.

4. **Entity layering**. Fund → GP → Adviser → Managing Member is one
   chain. If the chain reports the SAME shares at each level, dedup
   to the lowest economic owner (typically the fund / LP).

5. **Joint reporters on a single 13D/G**. The cover page lists all
   joint filers; the agreement under Item 6 typically attaches the
   joint filing agreement. Treat as one filing for sum purposes.

## What is NOT a duplicate

These look similar but represent distinct positions:

- **Different share classes.** Class A and Class B common are distinct
  even when held by the same entity.
- **Different Section 13(d) groups.** Two unrelated activist funds
  each filing 13Ds at the same time on the same issuer are
  independent positions.
- **Direct vs derivative holdings.** A Form 4 reporting common stock
  + an option = two distinct economic exposures, not a duplicate.
- **Old amendments superseded by new ones.** When SC 13D/A (amendment
  3) supersedes SC 13D/A (amendment 2), only the latest counts toward
  current holdings — but for an event-time series, both matter.

## Workflow when computing total insider holdings

1. Pull all 13D, 13G, 13D/A, 13G/A filings for the issuer in the
   target window.
2. Group filings by reported group identity (Item 2):
   - All filings citing each other on the cover page = one group.
   - Each group has ONE position (use the cover-page share count of
     any member; they should match).
3. For each independent group, compute the LATEST reported holding
   per amendment chain.
4. Compute sum across DISTINCT groups only.
5. Cross-check against `atm-detection` and recent 424B activity:
   total beneficial holdings + ATM-issued shares + outstanding shares
   should reconcile to total shares outstanding within ~5%.
   Larger gaps = missed dilution event or missed group.

## Workflow when computing insider transaction volume (Form 4)

1. Pull all Form 4s for the issuer in the target window.
2. Group by transaction date + transaction code + share count +
   per-share price. Identical-tuple Form 4s filed by related parties
   are likely the same transaction reported through multiple filers
   (e.g., trust + executive + spouse).
3. Apply attribution: footnotes commonly say "shares held by [X]
   for the benefit of [Y]". The economic owner is one party.
4. Sum DEDUPED transactions only.

## Special cases

- **Form 144 (notice of intent to sell).** Not an executed transaction;
  do not include in completed-sale tallies. The actual sale (if it
  occurs) shows up later as a Form 4. Treating 144s as Form 4s is
  one of the most common quant bugs. (See `sec-filing-types`.)
- **13F filings.** Are NOT 13D/G — they cover institutional MANAGER
  holdings with a 45-day lag, no 5% ownership threshold, and no
  filer-group dedup logic applies. Don't mix 13F and 13D/G summation.
- **CUSIP changes (reverse splits / mergers).** If the issuer's CUSIP
  changed mid-window, ownership filings on the old CUSIP and new CUSIP
  are the same position; reconcile by ticker history, not by CUSIP.

## Phrases that should trigger this skill

- "total insider holdings"
- "insider ownership %"
- "13D vs 13G dedup"
- "joint filers"
- "are these Form 4s duplicates"
- "13D group"
- "beneficial ownership reconciliation"

## What this skill is NOT

This is not a beneficial-ownership extractor. It defines the
deduplication semantics so a downstream summation produces a real
number rather than a multi-counted fiction. Combine with
`sec-filing-types` for form context and `lookahead-safety` for
historical reconstruction of holdings.
