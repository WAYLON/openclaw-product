# Agent 官方工作区文件说明

> 本页用于明确：客户现场的 Agent 工作区文件由 OpenClaw 官方命令生成，本项目不再自带或覆盖这些文件。

## 官方生成什么

在客户机器上执行官方 Agent 创建命令后，OpenClaw 会在工作区生成：

- `soul.yaml`
- `AGENTS.md`
- `IDENTITY.md`

这些文件属于客户现场运行时的一部分，不由本项目仓库维护。

## 本项目提供什么

本项目只提供两类内容：

1. `agents/<agent>/skills/`
说明：
- 对应 Agent 的专有技能

2. `packages/<agent>/...`
说明：
- 安装说明
- 交付说明
- 培训和验收文档

## 安装顺序

1. 先在客户机器上用官方命令创建 Agent
2. 让 OpenClaw 在 `~/.openclaw/workspaces/<agent>/` 中生成 `soul.yaml / AGENTS.md / IDENTITY.md`
3. 再由本项目把 `skills/` 同步进对应工作区

## 项目边界

- 本项目不再提供 `soul.yaml`
- 本项目不再提供 `AGENTS.md`
- 本项目不再提供 `IDENTITY.md`
- 本项目不覆盖客户现场已经由官方生成的工作区文件
- 本项目只补技能、文档、密钥规则和交付流程
