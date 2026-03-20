#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOCK_FILE="$ROOT_DIR/core/skills/basic-10.lock.json"

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误: 需要先安装 python3 才能读取 $LOCK_FILE"
  exit 1
fi

echo "建议检查以下基础技能是否已经安装或可用:"
echo ""

python3 - "$LOCK_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
for item in data["skills"]:
    print(f'- {item["name"]} [{item["kind"]}]')
PY

echo ""
echo "再执行:"
echo "openclaw skills check"
