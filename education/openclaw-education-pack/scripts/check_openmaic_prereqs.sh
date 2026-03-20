#!/usr/bin/env bash
set -euo pipefail

echo "检查 OpenMAIC 本地前置环境..."
echo ""

if command -v node >/dev/null 2>&1; then
  echo "node: $(node --version)"
else
  echo "node: 未安装"
fi

if command -v pnpm >/dev/null 2>&1; then
  echo "pnpm: $(pnpm --version)"
else
  echo "pnpm: 未安装"
fi

if [ -n "${OPENAI_API_KEY:-}" ] || [ -n "${ANTHROPIC_API_KEY:-}" ] || [ -n "${GOOGLE_API_KEY:-}" ]; then
  echo "LLM API Key: 已检测到至少一个环境变量"
else
  echo "LLM API Key: 未检测到常见环境变量"
fi

echo ""
echo "建议继续检查:"
echo "- OpenMAIC 项目是否已 clone"
echo "- .env.local 是否已配置"
echo "- openclaw skills check"
