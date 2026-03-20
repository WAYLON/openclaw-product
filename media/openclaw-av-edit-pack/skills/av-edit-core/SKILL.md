---
name: av-edit-core
description: 处理音视频转码、裁剪、抽帧、封装转换与素材整理的媒体技能。
allowed-tools: Read, Write, Edit, Exec
---

# 音视频剪辑核心技能

当任务属于以下类型时，使用这个技能：

- 视频裁剪
- 音频抽取
- 转码
- 抽帧
- 媒体目录整理

## 使用规则

1. 先确认输入文件存在
2. 再确认输出要求
3. 优先生成可复用命令或脚本
4. 如果会覆盖原文件，必须先提醒

## 前置依赖

- `ffmpeg`
- `ffprobe`

## 参考资料

- `references/av-edit-workflows.md`
