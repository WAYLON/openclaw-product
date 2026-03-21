#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: bash scripts/browser_use_extract.sh <query>"
  exit 1
fi

browser-use --browser real extract "$1"
