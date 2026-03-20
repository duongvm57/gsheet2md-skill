# Troubleshooting

## Credentials file not found

The script expects OAuth credentials at `~/.config/google-sheets/oauth-token.json` unless `--credentials` is provided.

Check:

- The file exists.
- The file is valid JSON.
- It includes `client_id`, `client_secret`, and `refresh_token`.

## Google Sheets API access fails

If token exchange or sheet reads fail:

- Confirm the Google Sheets API is enabled for the OAuth app.
- Confirm the refresh token is still valid.
- Recreate credentials if the OAuth client was rotated.

## Spreadsheet or sheet name errors

If the script reports an API error for the spreadsheet or sheet:

- Verify `--spreadsheet-id` is correct.
- Verify `--sheet-name` matches the tab title exactly.
- Try omitting `--sheet-name` to read the first sheet.

## Output path issues

Generated markdown belongs in `./docs` of the current workspace, not in the installed skill directory.

Recommended flow:

```bash
mkdir -p ./docs
python3 <skill-dir>/scripts/read_sheet.py --spreadsheet-id "<id>" --format table --output ./docs/<name>.md
```

If the agent is writing the markdown after inspecting JSON output, it should still create `./docs` first and save the final file there.
