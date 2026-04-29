# quant-llm-skills

> 🇪🇸 **Español** | [🇺🇸 English](./README.md) | [🇨🇳 简体中文](./README.zh.md)

[![validate](https://github.com/jefrnc/quant-llm-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/jefrnc/quant-llm-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill%20pack-orange)](https://docs.anthropic.com/en/docs/claude-code)

> **Skills para hacer quant research con LLMs sin caer en las trampas
> de las que nadie habla.**

La mayoría de los "skill packs de AI para trading" en GitHub le enseñan
a Claude a hacer backtest de CANSLIM y a parsear 10-Ks de AAPL. Fallan
apenas los apuntás a un small-cap real con XBRL incompleto, una ATM
activa y cuatro 13D filers reportando las mismas acciones.

Este pack destila reglas duras de pipelines quant en producción a skills
de Claude Code que el LLM aplica automáticamente — sin hackear el system
prompt, sin invocación manual, sin glue extra.

## Lo que detecta y un LLM baseline pasa por alto

- **Sesgo de lookahead** en cualquier query histórico — `period_end`
  no es una fecha de publicación.
- **Capacidad vs acción** — un S-3 efectivo por sí solo no es un evento
  de dilución.
- **ATM vs registered direct vs ELOC** — el mismo 424B5, trades distintos.
- **El placement agent importa** — Goldman en un secondary ≠ Wainwright
  en una ATM.
- **Huecos de XBRL en FPIs y SPACs** — los datos están en el texto del
  filing, no en el feed estructurado.
- **Doble-conteo en grupos 13D** — sumar las cover pages naïve
  sobreestima el ownership 2-10x.
- **Scoring cuantitativo de dilución** — 0-100 con pesos auditables,
  no a ojo.

Ver [EXAMPLES.md](./EXAMPLES.md) para transcripts reales de prompt
y respuesta.

## Skills

| Skill | Qué hace |
|---|---|
| [**lookahead-safety**](./skills/lookahead-safety/SKILL.md) | Fuerza `filing_date` como fecha-conocida, nunca `period_end`. El bug #1 de backtests quant. |
| [**sec-filing-types**](./skills/sec-filing-types/SKILL.md) | Desambigua formas SEC (S-3, 424B, items 8-K, 13D/G, Form 4, 20-F, 6-K, NT 10-K). Sabe que un shelf es *capacidad*, no acción. |
| [**atm-detection**](./skills/atm-detection/SKILL.md) | Inferencia multi-señal para ATMs activas. Distingue ATM de ELOC y registered direct. Captura la dilución que los scanners de solo-8-K se pierden. |
| [**bank-tier-classification**](./skills/bank-tier-classification/SKILL.md) | Framework de 4 tiers que mapea placement agents (bulge bracket → especialistas small-cap) al comportamiento esperado del deal. |
| [**xbrl-fallbacks**](./skills/xbrl-fallbacks/SKILL.md) | Cuando XBRL viene vacío o 404 (FPIs, IPOs recientes, SPACs), define la jerarquía de cover pages y reglas de extracción. |
| [**dilution-event-scoring**](./skills/dilution-event-scoring/SKILL.md) | Framework 0-100 que integra ATM + tier + recencia + cash runway + estructura + historia. Reproducible, auditable, con thresholds accionables. |
| [**insider-dedup**](./skills/insider-dedup/SKILL.md) | Reglas de dedup para joint filers / grupos / atribución familiar en 13D/G y Form 4. Frena el bug del cover-page-sum. |
| [**code-review-for-quant**](./skills/code-review-for-quant/SKILL.md) | Checklist de code review específico de quant (lookahead, splits, snapshots, NaN, dedup de joint filers). Rankea bugs por *silent corruption*, no por severidad-aparente. |
| [**transaction-cost-modeling**](./skills/transaction-cost-modeling/SKILL.md) | Defaults de fricción realistas para small caps. Caza el bug de borrow APR ficticio (3% en nombres Reg SHO en lugar de 50–500%), locate-failure modelado como slippage, y los defaults near-zero de los engines. |
| [**survivorship-bias**](./skills/survivorship-bias/SKILL.md) | Caza el trap de "armar universo con sobrevivientes de hoy". Foco especial en patrones small-cap: phantom returns por reverse-split-y-delist, ATM-hacia-delisting, SPAC merger flips. |

Los skills componen: pedile "score X dilution risk" y el scoring llama
a los skills de ATM, agent-tier y lookahead automáticamente.

## Instalación

**Una vez publicado en GitHub:**

```
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**Para testeo local ahora:**

```
/plugin marketplace add /ruta/absoluta/a/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**O one-shot por CLI sin instalar:**

```
claude --plugin-dir /ruta/absoluta/a/quant-llm-skills -p "tu prompt"
```

## Para quién es

- Quants retail / fondos boutique corriendo backtests point-in-time
  sobre small caps.
- Cualquiera usando Claude / Cursor para investigar SEC EDGAR que
  haya sido quemado por lookahead bias o huecos de XBRL.
- Devs de sistemas de trading que quieren que el LLM aplique
  *automáticamente* las reglas de detección de dilución sin
  re-explicarlas en cada sesión.

## Para quién NO es

- Research índice / ETF / large-cap-only donde la data estructurada
  es densa y la dilución es rara.
- Inversores fundamentales long-term sin interés en mecánica de
  placement.
- Cualquiera esperando que el LLM *prediga* precios — estos skills
  hacen al LLM más riguroso con la data, no clarividente sobre el
  futuro.

## Tradeoff

Los skills sesgan hacia **flaggear más riesgo** que el baseline.
Los falsos positivos en riesgo de dilución son baratos; los falsos
negativos son caros (printing inesperado contra tu long). Ajustá
los thresholds en
[`dilution-event-scoring`](./skills/dilution-event-scoring/SKILL.md)
si querés un perfil menos conservador.

## Validar

```
claude plugin validate /ruta/a/quant-llm-skills
```

Los 7 skills pasan `claude plugin validate` y cargan vía `--plugin-dir`.

## Cursor

Las reglas equivalentes para Cursor están en
[`.cursor/rules/`](./.cursor/rules/). Ver [CURSOR.md](./CURSOR.md) para
detalles.

## Licencia

MIT
