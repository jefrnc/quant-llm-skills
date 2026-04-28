#!/usr/bin/env python3
"""Sync .cursor/rules/<name>.mdc from skills/<name>/SKILL.md.

The Cursor rule is the same body as the Claude Code skill, with a
different frontmatter: alwaysApply=false (Cursor decides via description),
no license/name fields.

Run after editing any SKILL.md to keep the two formats in sync.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
RULES = ROOT / ".cursor" / "rules"

RULES.mkdir(parents=True, exist_ok=True)

count = 0
for skill_dir in sorted(SKILLS.iterdir()):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        continue

    content = skill_md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not m:
        sys.exit(f"No frontmatter in {skill_md}")

    fm = yaml.safe_load(m.group(1))
    body = m.group(2)
    description = (fm.get("description") or "").strip()

    rule_path = RULES / f"{skill_dir.name}.mdc"
    rule_content = (
        f"---\n"
        f"description: {description}\n"
        f"alwaysApply: false\n"
        f"---\n"
        f"{body}"
    )
    rule_path.write_text(rule_content)
    print(f"  synced  {rule_path.relative_to(ROOT)}")
    count += 1

print(f"Synced {count} cursor rules from {SKILLS.relative_to(ROOT)}/")
