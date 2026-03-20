#!/usr/bin/env python3
"""
Google Sheets Reader - Reads a Google Sheet and converts to markdown.
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError


def get_access_token(credentials: dict) -> str:
    """Exchange refresh token for access token."""
    token_url = "https://oauth2.googleapis.com/token"
    data = urlencode({
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "refresh_token": credentials["refresh_token"],
        "grant_type": "refresh_token"
    }).encode()

    req = Request(token_url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result["access_token"]
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Error getting access token: {error_body}", file=sys.stderr)
        sys.exit(1)


def get_spreadsheet_metadata(spreadsheet_id: str, access_token: str) -> dict:
    """Fetch spreadsheet metadata from Google Sheets API."""
    base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    req = Request(base_url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")

    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Error getting spreadsheet info: {error_body}", file=sys.stderr)
        sys.exit(1)


def resolve_sheet_name(metadata: dict, sheet_name: str, gid: str) -> str:
    """Resolve the target sheet name from gid, explicit name, or first sheet."""
    sheets = metadata.get("sheets", [])
    if not sheets:
        print("Error getting spreadsheet info: spreadsheet has no sheets", file=sys.stderr)
        sys.exit(1)

    if gid:
        for sheet in sheets:
            properties = sheet.get("properties", {})
            if str(properties.get("sheetId")) == str(gid):
                return properties["title"]
        print(f"Error getting spreadsheet info: no sheet found for gid {gid}", file=sys.stderr)
        sys.exit(1)

    if sheet_name:
        return sheet_name

    return sheets[0]["properties"]["title"]


def get_sheet_data(spreadsheet_id: str, sheet_name: str, gid: str, access_token: str) -> list:
    """Fetch data from Google Sheets API."""
    base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    metadata = get_spreadsheet_metadata(spreadsheet_id, access_token)
    resolved_sheet_name = resolve_sheet_name(metadata, sheet_name, gid)
    range_param = f"'{resolved_sheet_name}'"

    range_encoded = quote(range_param, safe='')
    values_url = f"{base_url}/values/{range_encoded}"
    req = Request(values_url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get("values", [])
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Error getting sheet data: {error_body}", file=sys.stderr)
        sys.exit(1)


def clean_data(data: list) -> list:
    """Remove empty rows and columns."""
    if not data:
        return []

    max_cols = max(len(row) for row in data)
    normalized = [row + [""] * (max_cols - len(row)) for row in data]

    non_empty_cols = []
    for col_idx in range(max_cols):
        has_content = any(
            str(row[col_idx]).strip()
            for row in normalized
        )
        if has_content:
            non_empty_cols.append(col_idx)

    cleaned = []
    for row in normalized:
        new_row = [row[col_idx] for col_idx in non_empty_cols]
        if any(str(cell).strip() for cell in new_row):
            cleaned.append(new_row)

    return cleaned


def to_markdown_text(data: list) -> str:
    """Convert 2D array to readable markdown text."""
    if not data:
        return ""

    def escape_cell(cell):
        s = str(cell)
        s = s.replace("\n", " ")
        return s.strip()

    lines = []
    for row in data:
        cleaned = [escape_cell(cell) for cell in row]
        non_empty = [c for c in cleaned if c]
        if non_empty:
            lines.append(" | ".join(non_empty))

    return "\n".join(lines)


def to_markdown_table(data: list) -> str:
    """Convert 2D array to markdown table."""
    if not data:
        return ""

    def escape_cell(cell):
        s = str(cell)
        s = s.replace("\n", " ").replace("|", "\\|")
        return s.strip()

    escaped_data = [[escape_cell(cell) for cell in row] for row in data]

    num_cols = len(escaped_data[0]) if escaped_data else 0
    col_widths = []
    for col_idx in range(num_cols):
        width = max(len(row[col_idx]) if col_idx < len(row) else 0 for row in escaped_data)
        col_widths.append(max(width, 3))

    lines = []

    header = escaped_data[0]
    header_cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(header)]
    lines.append("| " + " | ".join(header_cells) + " |")

    separator_cells = ["-" * col_widths[i] for i in range(num_cols)]
    lines.append("| " + " | ".join(separator_cells) + " |")

    for row in escaped_data[1:]:
        cells = [(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(num_cols)]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Read Google Sheet and convert to markdown")
    parser.add_argument("--spreadsheet-id", required=True, help="Google Spreadsheet ID")
    parser.add_argument("--sheet-name", default="", help="Sheet name (default: first sheet)")
    parser.add_argument("--gid", default="", help="Google Sheets gid / sheetId (overrides --sheet-name)")
    parser.add_argument("--credentials", default="~/.config/google-sheets/oauth-token.json", help="Path to OAuth credentials JSON")
    parser.add_argument("--output", default="", help="Output file path (default: stdout)")
    parser.add_argument("--raw", action="store_true", help="Keep all columns including empty ones")
    parser.add_argument("--format", choices=["table", "text", "json"], default="json", help="Output format (default: json)")

    args = parser.parse_args()

    credentials_path = os.path.expanduser(args.credentials)

    try:
        with open(credentials_path, "r") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        print(f"Credentials file not found: {args.credentials}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in credentials file: {args.credentials}", file=sys.stderr)
        sys.exit(1)

    required_fields = ["client_id", "client_secret", "refresh_token"]
    for field in required_fields:
        if not credentials.get(field):
            print(f"Missing required field in credentials: {field}", file=sys.stderr)
            sys.exit(1)

    access_token = get_access_token(credentials)
    data = get_sheet_data(args.spreadsheet_id, args.sheet_name, args.gid, access_token)

    if not args.raw:
        data = clean_data(data)

    if args.format == "table":
        output = to_markdown_table(data)
    elif args.format == "text":
        output = to_markdown_text(data)
    else:
        output = json.dumps(data, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
