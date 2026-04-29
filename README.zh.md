# quant-llm-skills

> 🇨🇳 **简体中文** | [🇺🇸 English](./README.md) | [🇪🇸 Español](./README.es.md)

[![validate](https://github.com/jefrnc/quant-llm-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/jefrnc/quant-llm-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill%20pack-orange)](https://docs.anthropic.com/en/docs/claude-code)

> **专为 LLM 量化研究设计的 skills，规避那些没人讨论但会让回测失真的陷阱。**

GitHub 上大多数 "AI for trading" skill 包教 Claude 回测 CANSLIM、解析
AAPL 的 10-K。一旦你把它们指向一个真实的 small-cap（XBRL 数据稀疏、
ATM 正在执行、四个 13D filer 报告同样的股份），它们就会失败。

这个 skill 包把生产环境量化 pipeline 中的硬规则提炼为 Claude Code
skills，LLM 自动应用 —— 无需修改 system prompt、无需手动触发、无需
额外胶水代码。

## 它能捕获、而 baseline LLM 会漏掉的内容

- **任何历史查询中的 lookahead 偏差** —— `period_end` 不是发布日期。
- **能力 vs 行动** —— 一份生效的 S-3 本身并非稀释事件。
- **ATM vs 注册直接发行 vs ELOC** —— 同一份 424B5，交易完全不同。
- **placement agent 至关重要** —— Goldman 承销的 secondary ≠ Wainwright
  做的 ATM。
- **FPI 和 SPAC 的 XBRL 缺口** —— 数据在 filing 文本里，不在结构化 feed
  里。
- **13D 团体重复计数** —— 简单加和 cover page 会高估持股 2-10 倍。
- **可量化的稀释评分** —— 0-100 分，权重可审计，不靠感觉。

参见 [EXAMPLES.md](./EXAMPLES.md) 查看真实 prompt 与响应记录。

## Skills

| Skill | 作用 |
|---|---|
| [**lookahead-safety**](./skills/lookahead-safety/SKILL.md) | 强制使用 `filing_date` 作为已知日期，绝不使用 `period_end`。量化回测中 #1 的 bug。 |
| [**sec-filing-types**](./skills/sec-filing-types/SKILL.md) | 区分 SEC 表格类型（S-3、424B、8-K items、13D/G、Form 4、20-F、6-K、NT 10-K）。理解 shelf 是 *能力*、不是行动。 |
| [**atm-detection**](./skills/atm-detection/SKILL.md) | 多信号推断活跃的 At-The-Market offering。区分 ATM 与 ELOC、注册直接发行。捕获只看 8-K 的 scanner 漏掉的稀释。 |
| [**bank-tier-classification**](./skills/bank-tier-classification/SKILL.md) | 把 placement agent（顶级投行 → small-cap 专家）映射到预期交易行为的 4 层框架。 |
| [**xbrl-fallbacks**](./skills/xbrl-fallbacks/SKILL.md) | 当 SEC XBRL 为空或 404（FPI、近期 IPO、SPAC）时，定义 cover page 的层级与提取规则。 |
| [**dilution-event-scoring**](./skills/dilution-event-scoring/SKILL.md) | 整合 ATM + agent tier + 时效 + 现金跑道 + 结构 + 历史的 0-100 评分框架。可复现、可审计、含可执行阈值。 |
| [**insider-dedup**](./skills/insider-dedup/SKILL.md) | 13D/G 与 Form 4 聚合中的联合 filer / 团体 / 家庭归属去重规则。阻止 cover-page-sum 的 bug。 |
| [**code-review-for-quant**](./skills/code-review-for-quant/SKILL.md) | 量化代码审查清单（lookahead、splits、snapshots、NaN、联合 filer 去重）。按*静默腐蚀*潜力排序 bug，而非按表面严重性。 |
| [**transaction-cost-modeling**](./skills/transaction-cost-modeling/SKILL.md) | 小盘股的现实摩擦默认值。捕获 borrow APR 失真（Reg SHO 名称上 3% 而非 50–500%）、locate-failure 被错误建模为 slippage、以及引擎接近零摩擦的默认值。 |
| [**survivorship-bias**](./skills/survivorship-bias/SKILL.md) | 捕获"用今天幸存者构建宇宙"陷阱。特别关注小盘股模式：reverse-split-then-delist 幻象收益、ATM-into-delisting、SPAC 合并翻转。 |

各 skill 互相组合：让它 "score X's dilution risk"，scoring skill 会
自动调用 ATM、agent-tier 和 lookahead 等 skills。

## 安装

**发布到 GitHub 之后：**

```
/plugin marketplace add jefrnc/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**当前本地测试：**

```
/plugin marketplace add /绝对路径/quant-llm-skills
/plugin install quant-llm-skills@quant-llm-skills
```

**或者通过 CLI 一次性使用、不安装：**

```
claude --plugin-dir /绝对路径/quant-llm-skills -p "你的 prompt"
```

## 适用人群

- 在 small caps 上做 point-in-time 回测的量化散户 / boutique fund。
- 用 Claude / Cursor 做 SEC EDGAR 研究、被 lookahead 偏差或 XBRL 缺口
  坑过的人。
- 希望 LLM *自动* 应用稀释检测规则、不需要每个 session 重新解释一遍
  的 trading-system 开发者。

## 不适用人群

- 指数 / ETF / 仅 large-cap 研究 —— 那里结构化数据稠密、稀释罕见。
- 对 placement 机制不感兴趣的纯基本面长线投资者。
- 期待 LLM *预测* 价格的人 —— 这些 skill 让 LLM 在数据上更严谨，
  不是让它对未来有预知能力。

## 权衡

这些 skill 倾向于 **比 baseline 更频繁地标记风险**。稀释风险的假阳性
代价很低；假阴性代价很高（你做多时被意外印发砸下来）。如果你想要
更不保守的画像，可以调整
[`dilution-event-scoring`](./skills/dilution-event-scoring/SKILL.md)
里的 threshold。

## 验证

```
claude plugin validate /quant-llm-skills 路径
```

7 个 skill 全部通过 `claude plugin validate`，并能通过 `--plugin-dir`
加载。

## Cursor

在 [`.cursor/rules/`](./.cursor/rules/) 下有 Cursor 等价规则。详见
[CURSOR.md](./CURSOR.md)。

## 许可证

MIT

---

> *本中文翻译由 LLM 辅助生成，欢迎母语者提交 PR 改进措辞。*
