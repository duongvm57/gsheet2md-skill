# Install Paths

The `gsheet2md` skill is installed into agent-specific directories. Use the table below to locate `SKILL_DIR` for your agent and install type.

| Agent       | Global install                            | Project-local install               |
| ----------- | ----------------------------------------- | ----------------------------------- |
| Claude Code | `~/.claude/skills/gsheet2md`              | `.claude/skills/gsheet2md`          |
| Cursor      | `~/.cursor/skills/gsheet2md`              | `.cursor/skills/gsheet2md`          |
| Codex       | `~/.codex/skills/gsheet2md`               | `.codex/skills/gsheet2md`           |
| Antigravity | `~/.agent/skills/gsheet2md`               | `.agent/skills/gsheet2md`           |
| OpenCode    | `~/.config/opencode/skills/gsheet2md`     | `.opencode/skills/gsheet2md`        |

For Antigravity, the global path may be `~/.gemini/antigravity/skills/gsheet2md` when that directory already exists.

## Install via CLI

```bash
npx gsheet2md install
```

Or non-interactively:

```bash
gsheet2md install --tool <claude-code|cursor|codex|antigravity|opencode|all> --location <global|project-local>
```
