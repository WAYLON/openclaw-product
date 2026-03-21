#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: bash scripts/browser_use_open.sh <url>"
  exit 1
fi

browser-use --browser real open "$1"
