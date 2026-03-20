---
name: gsheet2md
description: Reads Google Sheets and converts content to markdown. Use when the user asks to read, fetch, or convert Google Sheets data to markdown.
---

# gsheet2md

Read a Google Sheet by `SPREADSHEET_ID` and turn the result into usable markdown.

## Requirements

- OAuth credentials at `~/.config/google-sheets/oauth-token.json` with:
  - `client_id`
  - `client_secret`
  - `refresh_token`
- Google Sheets API enabled for that OAuth app

## Output Policy

- Use the installed script from the skill directory, but write any authored markdown into `./docs` of the current workspace.
- If `./docs` does not exist, create it before writing files.
- Do not save generated documents into the installed skill directory.

## Usage

### Step 1: Resolve the installed script path

Find the directory that contains this `SKILL.md`. The Python script lives at:

```bash
<skill-dir>/scripts/read_sheet.py
```

### Step 2: Fetch sheet data

```bash
python3 <skill-dir>/scripts/read_sheet.py --spreadsheet-id <SPREADSHEET_ID> --sheet-name <SHEET_NAME>
```

### Step 3: Convert to readable markdown

After fetching the sheet data, the agent should turn it into a well-structured markdown document.

The agent is responsible for:
- Understanding the data structure
- Formatting sections with clear headings, tables, and lists
- Writing short descriptions where needed
- Organizing the content for human readers
- Saving the final markdown file under `./docs/<derived-sheet-name>.md` in the current workspace

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--spreadsheet-id` | Yes | The Google Spreadsheet ID |
| `--sheet-name` | No | Sheet name to read. Defaults to the first sheet. |
| `--credentials` | No | OAuth credentials path. Defaults to `~/.config/google-sheets/oauth-token.json`. |
| `--output` | No | Output file path. Defaults to stdout. |
| `--format` | No | Output format: `json` (default), `table`, or `text`. |
| `--raw` | No | Keep empty columns instead of cleaning them. |

## Example

```bash
# Fetch as JSON
python3 <skill-dir>/scripts/read_sheet.py \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --sheet-name "Sheet1"

# Fetch as markdown table
python3 <skill-dir>/scripts/read_sheet.py \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --format table

# Save raw output directly into the current workspace docs folder
mkdir -p ./docs
python3 <skill-dir>/scripts/read_sheet.py \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --format table \
  --output ./docs/sheet1.md
```

## OAuth Credentials Format

```json
{
  "type": "oauth",
  "client_id": "your-client-id.apps.googleusercontent.com",
  "client_secret": "your-client-secret",
  "refresh_token": "your-refresh-token"
}
```

## Workflow For Markdown Output

1. Run the script to fetch the sheet data.
2. Inspect the returned structure before formatting it.
3. Ensure `./docs` exists in the current workspace. If `./docs` does not exist, create it.
4. Write a markdown document that matches the content shape instead of forcing a fixed template.
5. Save the markdown document under `./docs/` using a filename derived from the sheet name.
