# Using this repo with Cursor

`quant-llm-skills` ships **Cursor project rules** so the same skills
apply automatically when you open the project in Cursor.

## In this repository

1. Open the folder in Cursor.
2. The rules under [`.cursor/rules/`](./.cursor/rules/) are committed
   with `alwaysApply: false`. Cursor's "Auto Attached" / "Agent
   Requested" rule mode evaluates each rule's `description` against
   your current context and attaches the relevant ones automatically.
3. Confirm under **Settings → Rules** in Cursor — all 7 rules should
   appear.

## Use the same rules in another project

Copy `.cursor/rules/*.mdc` into that project's `.cursor/rules/`
directory (create folders if needed). You can copy individual rules
or all of them.

## Cursor rule generation

The `.cursor/rules/<name>.mdc` files are **generated** from the
canonical `skills/<name>/SKILL.md` files by [`scripts/sync-cursor.py`](./scripts/sync-cursor.py).
Body content is identical between the two; only the frontmatter
differs.

**For contributors:** when editing a `SKILL.md`, run:

```
python3 scripts/sync-cursor.py
```

…and commit the regenerated `.mdc` alongside your `SKILL.md` change.
A pre-commit hook is left as an exercise for now; the script is
idempotent.

## Claude Code vs Cursor

- **Claude Code:** install via the plugin marketplace (see
  [`README.md`](./README.md)). The plugin exposes the seven skills.
- **Cursor:** use the committed `.cursor/rules/` files. Cursor does
  not read `.claude-plugin/`, so the rules layer is required for
  Cursor users.
- **Codex CLI / Gemini CLI / others:** point your tool at the
  `.cursor/rules/` files or the `skills/*/SKILL.md` bodies. The
  content is identical and tool-agnostic.
