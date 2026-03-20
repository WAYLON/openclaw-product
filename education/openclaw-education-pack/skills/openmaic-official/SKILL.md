---
name: openmaic-official
description: 使用 OpenMAIC 进行互动课堂生成、课程结构编排和教育场景内容组织的技能。
allowed-tools: Read, Write, Edit, WebSearch, Browser, Exec
---

# OpenMAIC 官方教育技能

当任务属于教育、课堂、课程设计、教学材料转化时，使用这个技能。

这个技能围绕 OpenMAIC 的 OpenClaw 集成方式组织，不是简单的内容总结器。

官方参考：

- https://github.com/THU-MAIC/OpenMAIC/blob/main/README-zh.md#-openclaw-%E9%9B%86%E6%88%90

## 适用场景

- “帮我把这份文档做成一堂课”
- “给我生成一个互动课堂”
- “把这个主题讲成一套有测验和活动的教学流程”
- “如何在飞书里直接发起一个课堂”

## 核心能力

- 将主题或文档转成课堂
- 组织课堂结构
- 生成幻灯片、测验、互动活动思路
- 说明 OpenMAIC 的接入和部署前提

## 使用规则

1. 先确认输入材料是什么
2. 再确认受众是谁
3. 再确认课堂目标和时长
4. 最后决定是否需要依赖 OpenMAIC 本地环境

## 不能做什么

- 不能假装本地已经完成 OpenMAIC 部署
- 不能编造 API Key、模型配置或运行状态
- 不能把普通教育讲解误说成已生成完整互动课堂

## 参考资料

优先阅读：

- `references/openmaic-integration-notes.md`
