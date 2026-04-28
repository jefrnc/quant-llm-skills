#!/usr/bin/env bash
# Static validation of the quant-llm-skills repo.
# Designed to run in CI without requiring the `claude` CLI.
#
# Checks:
#   - Every skill listed in plugin.json has a SKILL.md.
#   - Every SKILL.md has valid frontmatter (name + description).
#   - Every SKILL.md has a corresponding .cursor/rules/<name>.mdc.
#   - .cursor/rules/*.mdc are up to date with sync-cursor.py.
#   - Optional: runs `claude plugin validate` if claude is on PATH.
#
# Usage:  bash scripts/validate.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
errors=0

fail() {
    echo "  ✗ $*" >&2
    errors=$((errors + 1))
}

ok() {
    echo "  ✓ $*"
}

echo "==> plugin.json: skill paths exist"
python3 - "$REPO" <<'PY' || fail "plugin.json check failed"
import json, os, sys
repo = sys.argv[1]
data = json.load(open(f"{repo}/.claude-plugin/plugin.json"))
missing = [s for s in data["skills"] if not os.path.isfile(f"{repo}/{s}/SKILL.md")]
if missing:
    print(f"  missing SKILL.md for: {missing}")
    sys.exit(1)
print(f"  all {len(data['skills'])} skill paths resolve")
PY

echo "==> SKILL.md frontmatter"
for f in "$REPO"/skills/*/SKILL.md; do
    name=$(basename "$(dirname "$f")")
    python3 - "$f" "$name" <<'PY' || fail "frontmatter invalid in $name"
import re, sys, yaml
content = open(sys.argv[1]).read()
m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
if not m:
    print("  no frontmatter"); sys.exit(1)
fm = yaml.safe_load(m.group(1))
if not fm.get("name"):
    print("  missing name"); sys.exit(1)
if not fm.get("description"):
    print("  missing description"); sys.exit(1)
if fm["name"] != sys.argv[2]:
    print(f"  name mismatch: frontmatter={fm['name']} dir={sys.argv[2]}"); sys.exit(1)
PY
    ok "$name"
done

echo "==> Cursor rules exist for every skill"
for skill_dir in "$REPO"/skills/*/; do
    name=$(basename "$skill_dir")
    if [[ -f "$REPO/.cursor/rules/${name}.mdc" ]]; then
        ok "$name.mdc"
    else
        fail "missing .cursor/rules/${name}.mdc"
    fi
done

echo "==> Cursor rules in sync with SKILL.md (run sync-cursor.py if this fails)"
tmpdir=$(mktemp -d)
cp -r "$REPO/.cursor/rules" "$tmpdir/before"
python3 "$REPO/scripts/sync-cursor.py" >/dev/null
if diff -rq "$tmpdir/before" "$REPO/.cursor/rules" >/dev/null; then
    ok "all .mdc files match generated output"
else
    fail "out of sync — run: python3 scripts/sync-cursor.py"
fi
rm -rf "$tmpdir"

if command -v claude >/dev/null 2>&1; then
    echo "==> claude plugin validate (CLI present)"
    if claude plugin validate "$REPO" >/dev/null 2>&1; then
        ok "manifest validates"
    else
        fail "claude plugin validate failed"
    fi
else
    echo "==> skipping claude plugin validate (CLI not on PATH)"
fi

echo
if (( errors > 0 )); then
    echo "✗ $errors check(s) failed"
    exit 1
fi
echo "✓ all static checks passed"
