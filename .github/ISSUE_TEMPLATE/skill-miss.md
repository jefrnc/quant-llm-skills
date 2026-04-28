---
name: Skill miss
about: Report a prompt where a skill should have fired but didn't, or fired wrong
title: "[skill-miss] <one-line summary>"
labels: skill-miss
assignees: ""
---

## Skill that should have fired

<!-- e.g. lookahead-safety, atm-detection, etc. -->

## Prompt you used

```
<paste your prompt here>
```

## What Claude actually answered (relevant excerpt)

```
<paste the response excerpt — no need for the full thing>
```

## What you expected the skill to apply

<!--
Briefly describe the rule from the SKILL.md that should have surfaced.
Quote the SKILL.md line if helpful.
-->

## Environment

- Claude Code version: `<output of claude --version>`
- Plugin source: `marketplace add jefrnc/quant-llm-skills` / `--plugin-dir <path>` / other
- Model: Opus / Sonnet / Haiku / other

## Additional context

<!-- Anything else: was this a baseline-also-correct case? a partial fire? -->
