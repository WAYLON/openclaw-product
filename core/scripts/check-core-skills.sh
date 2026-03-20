#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOCK_FILE="$ROOT_DIR/core/skills/basic-10.lock.json"
TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误: 需要先安装 python3 才能读取 $LOCK_FILE"
  exit 1
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "错误: 当前机器未找到 openclaw 命令，请先安装 OpenClaw 本体"
  exit 1
fi

openclaw skills check >"$TMP_FILE" 2>&1 || true

echo "core 基础技能识别检查："
echo ""

python3 - "$LOCK_FILE" "$TMP_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
with open(sys.argv[2], encoding="utf-8") as f:
    snapshot = f.read().lower()
for item in data["skills"]:
    name = item["name"]
    kind = item["kind"]
    required = item.get("required", False)
    if kind == "builtin":
        status = "内置能力，不做目录验收"
    elif name.lower() in snapshot:
        status = "已识别"
    elif required:
        status = "未识别（必装）"
    else:
        status = "未识别（可选）"
    print(f'- {name} [{kind}] -> {status}')
PY

echo ""
echo "完整输出参考: openclaw skills check"
