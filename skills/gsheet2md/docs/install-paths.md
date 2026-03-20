# Install Paths

`SKILL_DIR` is the directory containing this skill. Each coding agent resolves it from its own skill registry — you do not need to hardcode the path.

## Pattern

Skills follow a consistent layout:

- **Global install**: `<agent-config-dir>/skills/gsheet2md`
- **Project-local install**: `<project-root>/<agent-config-dir>/skills/gsheet2md`

Your agent knows its own `<agent-config-dir>`. When this skill is loaded, `SKILL_DIR` is the directory from which `SKILL.md` was read.

## Install via CLI

```bash
npx gsheet2md install
```

Or non-interactively:

```bash
gsheet2md install --tool <name|all> --location <global|project-local>
```

Supported tool names: `claude-code`, `cursor`, `codex`, `antigravity`, `opencode`.
