---
name: media-delivery-core
description: 处理图片、音频、视频和文件发送前校验与发送规则的媒体分发技能。
allowed-tools: Read, Write, Edit, Exec
---

# 媒体发送核心技能

当任务属于以下内容时，使用这个技能：

- 图片发送
- 音频发送
- 视频发送
- 文件发送
- 发送前格式转换

## 使用规则

1. 先确认目标渠道
2. 再确认媒体类型
3. 再确认路径和格式
4. 如果渠道要求特殊扩展名或编码格式，先转换

## 前置依赖

- 已接入目标渠道
- 本地存在待发送文件

## 参考资料

- `references/media-delivery-rules.md`
