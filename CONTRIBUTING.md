# 贡献说明

## 1. 基本要求

- 所有新增文档默认中文
- 不新增业务总控 Agent
- 一个渠道实例只绑定一个 Agent
- 所有技能直接放进对应 Agent 的 `skills/` 目录
- 不重新引入独立 `adapters/` 层

## 2. 提交前必须执行

```bash
make venv
make quality
make check-packages
```

## 3. 改动约束

- 改 `agents/<agent>/AGENTS.md`、`IDENTITY.md` 或 `soul.yaml` 时，要同步检查：
  - `docs/`
  - `packages/<agent>/config/install-manifest.yaml`
  - `skills/`
- 改安装流程时，要同步检查：
  - `installer/`
  - `docs/installation/`
- 改渠道层时，要保持：
  - `channels/*/connector.py`
  - 单实例单 Agent 绑定原则

## 4. 文档要求

- Quickstart、User Guide、Trainer Guide、FAQ、Examples 必须保持齐全
- Trainer Guide 必须可直接用于老师讲课
- 新增配置项时，要同步补模板和安装文档

## 5. 评审重点

- 是否破坏平行 Agent 原则
- 是否引入隐式总控逻辑
- 是否让渠道层承担业务脑子
- 是否降低了安装、培训、交付可执行性
