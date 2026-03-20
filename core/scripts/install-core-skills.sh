#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOCK_FILE="$ROOT_DIR/core/skills/basic-10.lock.json"

if [ ! -f "$LOCK_FILE" ]; then
  echo "错误: 基础技能锁定文件不存在: $LOCK_FILE"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误: 需要先安装 python3 才能读取 $LOCK_FILE"
  exit 1
fi

echo "开始安装 core 基础技能预设..."

while IFS=$'\t' read -r name kind cmd; do

  echo ""
  echo "==> $name ($kind)"

  if [ "$kind" = "builtin" ]; then
    echo "跳过安装: $name 属于 OpenClaw 内置能力"
    continue
  fi

  if [ -z "$cmd" ] || [ "$cmd" = "null" ]; then
    echo "跳过安装: $name 未提供安装命令"
    continue
  fi

  eval "$cmd"
done < <(
  python3 - "$LOCK_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
for item in data["skills"]:
    print(f'{item["name"]}\t{item["kind"]}\t{item.get("install_command","")}')
PY
)

echo ""
echo "基础技能安装结束，建议执行:"
echo "openclaw skills check"
