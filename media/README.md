# 媒体目录

这个目录用于存放所有音视频与媒体分发相关的 OpenClaw 产品包。

## 设计原则

- 媒体领域只放媒体相关产品
- 本体安装与基础技能不放在这里，统一放在 `core/`
- 每个媒体产品包都必须自带 `README.md`
- 每个媒体产品包都必须至少有 `workspace/` 和 `skills/`

## 当前产品

- `openclaw-av-edit-pack/`
  - 音视频剪辑行业包
- `openclaw-media-delivery-pack/`
  - 发送媒体资源行业包

## 安装入口

如果目标机器还没有 OpenClaw，请先阅读：

- `../core/安装-openclaw-本体.md`

如果目标机器已完成 `core` 安装，再进入具体产品包按包内说明安装。
