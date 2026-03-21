#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOCK_FILE="$ROOT_DIR/core/skills/basic-10.lock.json"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if [ ! -f "$LOCK_FILE" ]; then
  echo "错误: 基础技能锁定文件不存在: $LOCK_FILE"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误: 需要先安装 python3 才能读取 $LOCK_FILE"
  exit 1
fi

echo "开始安装 core 基础技能预设..."

if ! command -v openclaw >/dev/null 2>&1; then
  echo "错误: 当前机器未找到 openclaw 命令，请先安装 OpenClaw 本体"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "错误: 当前机器未找到 node，请先安装 Node.js"
  exit 1
fi

run_install() {
  local name="$1"
  local kind="$2"
  local package="$3"
  local skill="$4"
  local args_json="$5"
  local required="$6"
  local status=0

  case "$kind" in
    builtin)
      echo "跳过安装: $name 属于 OpenClaw 内置能力"
      return 0
      ;;
    clawhub)
      if ! command -v clawhub >/dev/null 2>&1; then
        echo "错误: 未找到 clawhub，无法安装 $name"
        [ "$required" = "true" ] && return 1
        return 0
      fi
      clawhub install "$package" || status=$?
      if [ "$status" -ne 0 ]; then
        echo "安装命令失败: $name (clawhub install $package)"
      fi
      ;;
    npx)
      if [ -n "$skill" ] && [ "$skill" != "null" ]; then
        node - "$package" "$skill" "$args_json" <<'NODE' || status=$?
const { spawnSync } = require('child_process');
const [pkg, skill, argsJson] = process.argv.slice(2);
const extraArgs = argsJson ? JSON.parse(argsJson) : [];
const result = spawnSync(
  'npx',
  ['skills', 'add', pkg, '--skill', skill, ...extraArgs],
  { stdio: 'inherit' }
);
process.exit(result.status ?? 1);
NODE
        if [ "$status" -ne 0 ]; then
          echo "安装命令失败: $name (npx skills add $package --skill $skill)"
        fi
      else
        node - "$package" "$args_json" <<'NODE' || status=$?
const { spawnSync } = require('child_process');
const [pkg, argsJson] = process.argv.slice(2);
const extraArgs = argsJson ? JSON.parse(argsJson) : [];
const result = spawnSync(
  'npx',
  ['skills', 'add', pkg, ...extraArgs],
  { stdio: 'inherit' }
);
process.exit(result.status ?? 1);
NODE
        if [ "$status" -ne 0 ]; then
          echo "安装命令失败: $name (npx skills add $package)"
        fi
      fi
      ;;
    *)
      echo "错误: 未知安装类型 $kind ($name)"
      return 1
      ;;
  esac

  if [ "$status" -ne 0 ]; then
    if [ "$required" = "true" ]; then
      echo "错误: 必装技能安装失败: $name"
      return "$status"
    fi
    echo "警告: 可选技能安装失败，已跳过: $name"
  fi
}

check_installed() {
  local name="$1"
  local kind="$2"
  local snapshot="$3"

  if [ "$kind" = "builtin" ]; then
    echo "内置能力: $name 不做目录验收"
    return 0
  fi

  if grep -Fqi "$name" "$snapshot"; then
    echo "已识别: $name"
    return 0
  fi

  echo "未识别: $name"
  return 1
}

while IFS=$'\t' read -r name kind package skill args_json required; do

  echo ""
  echo "==> $name ($kind)"
  run_install "$name" "$kind" "$package" "$skill" "$args_json" "$required"
done < <(
  python3 - "$LOCK_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
for item in data["skills"]:
    print(
        "\t".join(
            [
                item["name"],
                item["kind"],
                item.get("package", ""),
                item.get("skill", ""),
                json.dumps(item.get("install_args", []), ensure_ascii=False),
                "true" if item.get("required") else "false",
            ]
        )
    )
PY
)

echo ""
echo "开始做安装验收..."
SNAPSHOT="$TMP_DIR/skills-check.txt"
openclaw skills check >"$SNAPSHOT" 2>&1 || true

missing_required=0
while IFS=$'\t' read -r name kind _package _skill _args_json required; do
  if ! check_installed "$name" "$kind" "$SNAPSHOT"; then
    if [ "$required" = "true" ]; then
      missing_required=1
    fi
  fi
done < <(
  python3 - "$LOCK_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
for item in data["skills"]:
    print(
        "\t".join(
            [
                item["name"],
                item["kind"],
                item.get("package", ""),
                item.get("skill", ""),
                json.dumps(item.get("install_args", []), ensure_ascii=False),
                "true" if item.get("required") else "false",
            ]
        )
    )
PY
)

echo ""
if [ "$missing_required" -ne 0 ]; then
  echo "错误: 存在必装基础技能未被 OpenClaw 识别，请先检查安装日志和 openclaw skills check 输出"
  exit 1
fi

echo "基础技能安装结束，必装项已通过识别验收。"
