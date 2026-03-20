#!/usr/bin/env bash
set -euo pipefail

echo "检查音视频处理前置工具..."
echo ""

if command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg: $(ffmpeg -version | head -n 1)"
else
  echo "ffmpeg: 未安装"
fi

if command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe: 可用"
else
  echo "ffprobe: 未安装"
fi
