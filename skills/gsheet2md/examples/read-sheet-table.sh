#!/usr/bin/env bash
set -eu

# Run this from your current workspace after replacing the placeholders.
# The script path is resolved relative to the installed skill directory.

mkdir -p ./docs
python3 ../scripts/read_sheet.py \
  --spreadsheet-id "<SPREADSHEET_ID>" \
  --gid "<GID>" \
  --format table \
  --output ./docs/sheet-table.md
