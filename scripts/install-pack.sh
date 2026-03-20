#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "用法: ./scripts/install-pack.sh <pack-path> <skills-only|full>"
  echo "示例: ./scripts/install-pack.sh stocks/openclaw-stock-pack skills-only"
  exit 1
fi

PACK_PATH="$1"
MODE="$2"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ABS_PACK_PATH="$ROOT_DIR/$PACK_PATH"
TARGET_DIR="$HOME/.openclaw"

if [ ! -d "$ABS_PACK_PATH" ]; then
  echo "错误: 产品包不存在: $ABS_PACK_PATH"
  exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
  echo "错误: 目标机器尚未初始化 OpenClaw: $TARGET_DIR 不存在"
  echo "请先阅读 core/安装-openclaw-本体.md"
  exit 1
fi

if [ ! -d "$TARGET_DIR/skills" ]; then
  echo "错误: $TARGET_DIR/skills 不存在"
  exit 1
fi

backup_dir() {
  local src="$1"
  if [ -d "$src" ]; then
    cp -R "$src" "${src}.bak.$(date +%Y%m%d_%H%M%S)"
  fi
}

case "$MODE" in
  skills-only)
    if [ -d "$ABS_PACK_PATH/skills" ]; then
      cp -R "$ABS_PACK_PATH/skills/." "$TARGET_DIR/skills/"
    fi
    ;;
  full)
    if [ ! -d "$TARGET_DIR/workspace" ]; then
      echo "错误: $TARGET_DIR/workspace 不存在"
      exit 1
    fi
    backup_dir "$TARGET_DIR/workspace"
    backup_dir "$TARGET_DIR/skills"
    if [ -d "$ABS_PACK_PATH/workspace" ]; then
      cp -R "$ABS_PACK_PATH/workspace/." "$TARGET_DIR/workspace/"
    fi
    if [ -d "$ABS_PACK_PATH/skills" ]; then
      cp -R "$ABS_PACK_PATH/skills/." "$TARGET_DIR/skills/"
    fi
    ;;
  *)
    echo "错误: 安装模式只能是 skills-only 或 full"
    exit 1
    ;;
esac

echo "安装完成: $PACK_PATH ($MODE)"
echo "注意: 行业包不会自动安装 core 基础技能层"
echo "如未安装，请先执行: ./core/scripts/install-core-skills.sh"
echo "建议接着执行: openclaw skills check"
