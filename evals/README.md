# Evals

Regression test suite for `quant-llm-skills`. One eval per skill,
following the [Anthropic skill-creator pattern](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
adapted to a YAML manifest.

## What it tests

Each eval runs a prompt through `claude --plugin-dir` and asserts:
- **`must_contain`** — substrings or `{regex: "..."}` patterns the
  response must include (the skill's reasoning surfaced).
- **`must_not_contain`** — patterns the response must NOT include
  (no false negatives or wrong framing).

Evals marked `differentiator: true` are the ones we expect the baseline
(no plugin) to FAIL — they prove the skill is doing real work, not just
mirroring what the model already knows.

The headline differentiator is `lookahead-xbrl-period-end`:
**Haiku catches the bug 0% of the time without the plugin and 100% with it.**

## Run locally

```bash
make evals                                  # via Makefile
python3 evals/run_evals.py                  # direct
python3 evals/run_evals.py --baseline       # also run without plugin
python3 evals/run_evals.py --filter dilution # subset
python3 evals/run_evals.py --verbose         # print full responses
```

Requires the `claude` CLI on `PATH` and authentication (subscription
or `ANTHROPIC_API_KEY`).

## Add a new eval

Edit `evals.yaml` and append:

```yaml
  - id: <unique-id>
    skill: <skill-name>          # informational; not enforced
    prompt: |
      <multi-line prompt>
    must_contain:
      - <substring>
      - {regex: "<python-regex>"}
    must_not_contain:
      - <substring>
    description: <one-line summary>
    differentiator: true   # optional
```

Run `python3 evals/run_evals.py --filter <id>` to verify the new eval
in isolation before committing.

## Cost

Each eval is one Haiku call (~$0.001-0.01). Full suite of 8 evals with
`--baseline` = 16 calls = ~$0.10. CI runs add up over time but remain
negligible compared to the value of catching a regression.

## CI integration

`.github/workflows/evals.yml` runs the suite on every push and PR if
the `ANTHROPIC_API_KEY` secret is set on the repository. Without the
secret, only the static `validate.sh` workflow runs.
