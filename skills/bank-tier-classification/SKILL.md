---
name: bank-tier-classification
description: Use when an SEC filing names a placement agent, underwriter, or sales agent (e.g., Goldman Sachs, H.C. Wainwright, Maxim, Aegis, Roth, B. Riley, Cantor, Jefferies). Classifies the firm into a 4-tier framework that materially changes the dilution risk profile of the offering.
license: MIT
---

# Bank Tier Classification

The same filing (424B5, 8-K) means very different things depending on
**who is selling the shares**. A registered direct led by Goldman Sachs
is a different animal than an ATM run by a tier-4 specialist. Most quant
pipelines ignore the agent identity entirely; this skill restores it as
a primary signal.

## Core principle

**The placement agent is a leading indicator of the offering's
structure, aggression, and post-deal price behavior.**

Tier 1 firms protect their reputation and underwrite institutional
demand. Tier 4 firms specialize in placing offerings that tier 1 firms
will not touch — by definition, those are the harder, more dilutive,
more structured deals.

Same form, different agent = different trade.

## The four tiers

### Tier 1 — Bulge bracket
Global investment banks underwriting at scale. Their participation
implies institutional demand and a "blessed" issuer.

- **Goldman Sachs** (and GS&Co.)
- **Morgan Stanley**
- **J.P. Morgan** / J.P. Morgan Securities
- **Bank of America Securities** (BofA / Merrill)
- **Citigroup Global Markets** / Citi
- **Barclays Capital**
- **Deutsche Bank Securities**
- **UBS Investment Bank**
- **Credit Suisse** (legacy / now UBS)
- **Wells Fargo Securities**

**Implication when seen on a small-cap filing:** rare. If present, the
issuer is a real institutional name or has a strategic reason for the
relationship. Dilution risk: low to moderate, deal is typically clean.

### Tier 2 — Mid-tier full-service
Quality investment banks with research coverage and institutional
distribution. Do legitimate growth-capital raises.

- **Jefferies**
- **TD Cowen** / Cowen
- **Stifel Nicolaus** / KBW (Keefe Bruyette Woods)
- **Piper Sandler**
- **Raymond James**
- **William Blair**
- **Cantor Fitzgerald**
- **Needham & Company**
- **Truist Securities**
- **Mizuho Securities**
- **Nomura Securities**
- **BMO Capital Markets**

**Implication:** legitimate growth capital. Often firm-commitment
underwritten secondaries, not ATMs. Dilution risk: moderate, predictable.

### Tier 3 — Boutique / sector-specialist
Reputable smaller banks with niche specialties (biotech, energy, tech).
Mix of clean and aggressive deals depending on the issuer.

- **Roth Capital Partners** / Roth MKM
- **Oppenheimer & Co.**
- **B. Riley Securities** / B. Riley FBR
- **Lake Street Capital Markets**
- **Craig-Hallum Capital Group**
- **Canaccord Genuity**
- **Wedbush Securities**
- **Northland Capital Markets**
- **D.A. Davidson**
- **Stephens Inc.**
- **Compass Point**
- **JMP Securities** (now Citizens)

**Implication:** mixed bag — read the structure (warrants, discount, ATM
language) carefully. The agent identity alone is not decisive at this
tier. Dilution risk: moderate to high depending on deal terms.

### Tier 4 — Specialized small-cap placement agents
Firms that specialize in placing offerings for issuers that cannot
attract Tier 1–3 underwriting. Heavy concentration in ATMs, registered
directs with warrants, ELOCs, and PIPEs. High-volume, high-frequency
small-cap deal flow.

- **H.C. Wainwright & Co.** (the dominant small-cap placement agent
  by deal count; runs many ATMs)
- **Maxim Group**
- **Aegis Capital**
- **A.G.P. / Alliance Global Partners**
- **EF Hutton** / Kingswood (legacy entity, now separate)
- **ThinkEquity**
- **Dawson James Securities**
- **Joseph Gunnar & Co.**
- **Spartan Capital Securities**
- **Univest Securities**
- **Boustead Securities**
- **Brookline Capital Markets**
- **Laidlaw & Company**
- **WallachBeth Capital**

**Implication:** when one of these agents appears on a 424B5 or sales
agreement, the base rate for: (a) attached warrants, (b) deep discount
to last trade, (c) ATM that sells aggressively into intraday strength,
(d) repeat dilution within 30–90 days, is materially elevated. Dilution
risk: HIGH. Treat the issuer as having a continuous selling pressure
floor until the offering is exhausted or terminated.

## Decision rules

1. **"Is this offering institutional or retail-flow?"**
   Tier 1–2 = institutional book. Tier 4 = retail / quant / market-maker
   absorption with frequent shorting against the cross.

2. **"How fast will this dilute?"**
   Tier 4 ATMs sell every green tick. Tier 2 underwritten secondaries
   are one-shot. The agent tier is the strongest predictor of cadence.

3. **"Should I go long after this offering closes?"**
   Tier 1–2 underwritten secondaries often see post-deal stabilization
   (the underwriter has incentive to support the price). Tier 4 ATMs
   have the opposite incentive — keep selling.

4. **"Multiple agents listed — which tier wins?"**
   Use the LOWEST (most aggressive) tier present. A "Tier 2 + Tier 4"
   joint placement is dominated by the tier-4 dynamics.

## Important caveats

- **The list is not exhaustive.** Many smaller agents exist; classify
  based on observable behavior (ATM frequency, warrant attachment rate,
  client universe) when in doubt.
- **Tier is not a moral judgment.** Tier 4 firms perform a legitimate
  market function placing offerings that would otherwise fail. The
  classification predicts deal behavior, not firm quality.
- **Firms can move tiers over time.** B. Riley's profile, for example,
  has shifted across cycles. Re-validate against recent deal flow rather
  than relying on a frozen list.
- **Same firm, different deal.** A Tier 4 agent doing a one-shot
  registered direct (firm commitment, no warrants, single investor) is
  much less aggressive than the same agent on an open ATM. Always read
  the structure alongside the tier.
- **Avoid defamation.** When writing public-facing content, frame as
  "specialized in" / "frequently associated with" rather than absolute
  toxicity claims about specific firms.

## Workflow when an agent name appears

1. Identify the agent in the 424B cover or "Plan of Distribution".
2. Place into Tier 1–4 using the lists above.
3. Inspect the structure (ATM vs. registered direct vs. underwritten
   secondary; warrants attached; discount to market).
4. Combine tier + structure for the final risk read:
   - Tier 1–2 + underwritten secondary = clean
   - Tier 3 + registered direct = read the warrants
   - Tier 4 + ATM = continuous dilution overhang
   - Tier 4 + ELOC = deeper-discount slow bleed
5. Cross-reference with `atm-detection` if the structure is an ATM,
   and `lookahead-safety` for any historical timing claims.

## Phrases that should trigger this skill

- Any of the firm names above appearing in a filing context
- "placement agent" / "lead underwriter" / "sales agent"
- "who's the bank on this deal"
- "is Wainwright running this" / "is Maxim doing this"
- "tier 4" / "toxic shop" / "bulge bracket"
- "Plan of Distribution"

## What this skill is NOT

This is not a firm-rating service. It is a heuristic that maps observed
firm names to expected deal behavior based on documented patterns of
small-cap deal flow. Always combine with structure (`atm-detection`)
and timing (`lookahead-safety`) for a complete read.
