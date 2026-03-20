#!/usr/bin/env bash
set -euo pipefail

echo "应用 demo/open 默认预设..."

openclaw config set channels.feishu.streaming true

echo
echo "已设置："
echo "- channels.feishu.streaming = true"
echo
echo "建议在新会话中手动执行："
echo "/verbose"
echo "/reasoning"
echo
echo "说明："
echo "- 该脚本目前只自动设置已确认可用的配置项"
echo "- 其他“权限放开”项建议在工具管理界面按需开启"
echo "- 如果你要把高危权限也做成脚本化预设，需要先确认你当前 OpenClaw 版本的精确配置键"
