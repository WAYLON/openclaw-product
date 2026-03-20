#!/usr/bin/env bash
set -euo pipefail

echo "检查媒体发送前置环境..."
echo ""

if command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg: 可用"
else
  echo "ffmpeg: 未安装"
fi

echo "请额外人工确认："
echo "- 目标渠道是否已接入"
echo "- 媒体文件路径是否存在"
echo "- 是否需要音频转 opus"
