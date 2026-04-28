#!/usr/bin/env bash
# Smoke test: validates the plugin manifest and confirms all 7 skills
# load correctly via --plugin-dir. Run before publishing or after any
# change to a SKILL.md or manifest.
#
# Usage:  bash scripts/smoke-test.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Validating plugin manifest…"
claude plugin validate "$REPO" >/dev/null

echo "==> Listing loaded skills…"
output=$(claude --plugin-dir "$REPO" -p \
    "List ONLY the skill names starting with 'quant-llm-skills'. Just names, one per line." \
    2>/dev/null)

expected=(
    "lookahead-safety"
    "sec-filing-types"
    "atm-detection"
    "bank-tier-classification"
    "xbrl-fallbacks"
    "dilution-event-scoring"
    "insider-dedup"
)

missing=0
for name in "${expected[@]}"; do
    if grep -q "quant-llm-skills:${name}" <<< "$output"; then
        echo "    ✓ ${name}"
    else
        echo "    ✗ MISSING: ${name}"
        missing=$((missing + 1))
    fi
done

if (( missing > 0 )); then
    echo
    echo "✗ Smoke test failed: $missing skill(s) missing"
    exit 1
fi

echo
echo "✓ All 7 skills loaded correctly. Plugin is ready to publish."
