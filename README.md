# gsheet2md

`gsheet2md` works in two modes:

- As an npm CLI installer for supported agent skill directories
- As a repo-based skill layout compatible with `skills.sh`

## Install

Run directly with `npx`:

```bash
npx gsheet2md install
```

Or install globally and reuse the CLI:

```bash
npm install -g gsheet2md
gsheet2md install
```

## Quick Start

For most users, this is enough:

```bash
npx gsheet2md install
```

The wizard lets you tick one or more tools and one or both install targets, then installs the same skill assets into the matching directories.

## skills.sh

This repo now includes a `skills.sh`-compatible layout under `skills/gsheet2md/`.

Once the repo is public, users can install it with the Vercel CLI flow:

```bash
npx skills add duongvm57/gsheet2md-skill --skill gsheet2md
```

That path is intended for the Vercel `skills.sh` ecosystem. The npm package remains useful when you want a dedicated installer CLI with explicit global or project-local targets.

When the installed skill is used, the script runs from the skill directory but any generated markdown should be written into `./docs` of the current workspace.
If `./docs` does not exist, create it before writing files.

The default `install` flow is interactive. It prompts for:

- One or more tools: `Claude Code`, `Cursor`, `Codex`, `Antigravity`
- One or both install targets: `Global`, `Project-local`

Interactive controls:

- `Space` to toggle a checkbox
- `↑` / `↓` to move
- `←` to go back
- `→` or `Enter` to continue

For CI or scripts, you can still run non-interactive commands:

```bash
gsheet2md install --tool codex --location project-local
```

## Supported tools

| Tool        | Global path                                   | Project-local path               |
| ----------- | --------------------------------------------- | -------------------------------- |
| Claude Code | `~/.claude/skills/gsheet2md`                  | `./.claude/skills/gsheet2md`     |
| Cursor      | `~/.cursor/skills/gsheet2md`                  | `./.cursor/skills/gsheet2md`     |
| Codex       | `~/.codex/skills/gsheet2md`                   | `./.codex/skills/gsheet2md`      |
| Antigravity | `~/.agent/skills/gsheet2md`                   | `./.agent/skills/gsheet2md`      |
| OpenCode    | `~/.config/opencode/skills/gsheet2md`         | `./.opencode/skills/gsheet2md`   |

For Antigravity global installs, the CLI can prefer `~/.gemini/antigravity/skills/gsheet2md` when that environment already exists.

## CLI

```bash
gsheet2md install
gsheet2md install --tool <name|all> --location <global|project-local> [--project-path <dir>] [--dest <dir>]
```

### Options

- `--tool`: `claude-code`, `claude`, `cursor`, `codex`, `antigravity`, `opencode`, or `all`
- `--location`: `global`, `project-local`, `project`, or `local`
- `--dest`: override the resolved install directory completely

## What gets installed

The package installs only the skill assets:

- `SKILL.md`
- `scripts/read_sheet.py`

Those assets are sourced from `skills/gsheet2md/` inside this repo.

The repository skill also includes:

- `docs/troubleshooting.md`
- `examples/read-sheet-json.sh`
- `examples/read-sheet-table.sh`

## Output Location

The installed skill directory is only for packaged assets. Sheet output belongs in `./docs` of the current workspace.

Example:

```bash
mkdir -p ./docs
python3 <skill-dir>/scripts/read_sheet.py \
  --spreadsheet-id "<SPREADSHEET_ID>" \
  --gid "<GID>" \
  --format table \
  --output ./docs/<sheet-name>.md
```

Use `--sheet-name` when you want to target a tab by title. Use `--gid` when you already have the Google Sheets tab id from a URL such as `.../edit?gid=123#gid=123`. If both are provided, `--gid` wins.

The script always returns the full selected sheet in the requested format. It does not summarize, sample, or truncate output by default.

## Development

```bash
npm test
```

## Release

Run the release smoke check before publishing:

```bash
npm run release:check
```

That command runs:

```bash
npm test
npm pack --dry-run
```

To publish publicly on npm:

```bash
npm login
npm publish --access public
```

If you later host this package in a public git repository, add `repository`, `homepage`, and `bugs` fields in `package.json` to match that repo.
