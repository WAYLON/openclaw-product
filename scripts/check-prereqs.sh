#!/usr/bin/env bash
set -euo pipefail

echo "检查基础命令..."
for cmd in git node npm; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "OK  $cmd"
  else
    echo "MISS $cmd"
  fi
done

echo
echo "检查 OpenClaw 基础目录..."
if [ -d "$HOME/.openclaw" ]; then
  echo "OK  ~/.openclaw"
else
  echo "MISS ~/.openclaw"
fi

if [ -f "$HOME/.openclaw/openclaw.json" ]; then
  echo "OK  ~/.openclaw/openclaw.json"
else
  echo "MISS ~/.openclaw/openclaw.json"
fi

if [ -d "$HOME/.openclaw/workspace" ]; then
  echo "OK  ~/.openclaw/workspace"
else
  echo "MISS ~/.openclaw/workspace"
fi

if [ -d "$HOME/.openclaw/skills" ]; then
  echo "OK  ~/.openclaw/skills"
else
  echo "MISS ~/.openclaw/skills"
fi
