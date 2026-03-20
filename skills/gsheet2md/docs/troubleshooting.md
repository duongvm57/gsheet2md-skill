# Troubleshooting

## First-time setup

The most common blocker is missing OAuth credentials. Follow these steps to create them.

### 1. Create a Google Cloud project and enable the Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Navigate to **APIs & Services → Library**
4. Search for "Google Sheets API" and click **Enable**

### 2. Create an OAuth 2.0 Desktop app credential

1. Navigate to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop app** as the application type
4. Download the JSON file — it contains `client_id` and `client_secret`

### 3. Get a refresh token via OAuth Playground

1. Go to https://developers.google.com/oauthplayground/
2. Click the gear icon (top right) → check **Use your own OAuth credentials**
3. Enter your `client_id` and `client_secret` from the downloaded JSON
4. In the left panel, find and select the scope:
   `https://www.googleapis.com/auth/spreadsheets.readonly`
5. Click **Authorize APIs** and sign in with your Google account
6. Click **Exchange authorization code for tokens**
7. Copy the **Refresh token** value

### 4. Create the credentials file

```bash
mkdir -p ~/.config/google-sheets
cat > ~/.config/google-sheets/oauth-token.json <<'EOF'
{
  "type": "oauth",
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
EOF
```

---

## Credentials file not found

The script expects OAuth credentials at `~/.config/google-sheets/oauth-token.json` unless `--credentials` is provided.

See **First-time setup** above to create the file.

Check:

- The file exists: `ls ~/.config/google-sheets/oauth-token.json`
- The file is valid JSON: `python3 -m json.tool ~/.config/google-sheets/oauth-token.json`
- It includes `client_id`, `client_secret`, and `refresh_token`

---

## API access fails — 403 Permission denied

If the script returns a 403 error:

- The OAuth app may not have the Google Sheets API enabled. Go to **APIs & Services → Library** and enable it.
- The sheet may not be shared with the authenticated Google account. Open the sheet and share it (view access is enough).
- The OAuth scope may be insufficient. Recreate credentials using `spreadsheets.readonly` scope.

## API access fails — 401 / token errors

If the script returns a 401 or token-related error:

- The refresh token may have expired or been revoked. Return to OAuth Playground and generate a new one.
- The OAuth client may have been rotated. Download a new client secret JSON and recreate the credentials file.
- Confirm `client_id` and `client_secret` in the credentials file match the current OAuth client in Cloud Console.

## API access fails — 404 Not found

If the script returns a 404:

- The `--spreadsheet-id` is wrong. Double-check by extracting it from the URL: the ID is the segment between `/d/` and the next `/`.
- The sheet was deleted or moved. Verify the URL in your browser.

---

## Spreadsheet or sheet name errors

If the script reports an error for the spreadsheet or sheet:

- Verify `--spreadsheet-id` is correct.
- Verify `--sheet-name` matches the tab title exactly (case-sensitive).
- Omit `--sheet-name` to read the first sheet — this also lets you inspect available data before specifying a tab.

To see the raw structure before formatting:

```bash
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "$SPREADSHEET_ID" \
  --format json
```

---

## Output path issues

Generated markdown belongs in `./docs` of the current workspace, not in the installed skill directory.

Recommended flow:

```bash
mkdir -p ./docs
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "$SPREADSHEET_ID" \
  --format table \
  --output ./docs/<name>.md
```

If the agent is writing the markdown after inspecting JSON output, it should still create `./docs` first and save the final file there.
