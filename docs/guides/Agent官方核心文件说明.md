# Agent 官方核心文件说明

> 本页用于明确：当前项目里，一个 Agent 最终只保留哪些偏官方核心的文件，哪些属于交付文档与配套资料。

## 当前保留的官方核心文件

每个业务 Agent 现在统一保留这几类核心文件：

1. `soul.yaml`
2. `AGENTS.md`
3. `IDENTITY.md`
4. `skills/`

这四类文件共同构成当前项目里的 Agent 主体定义。

## 每个文件分别负责什么

### `soul.yaml`

- 定义官方 `soul` 配置、定位、边界、风格、任务目标
- 回答“这个 Agent 是谁、做什么、不该做什么”

### `AGENTS.md`

- 定义工作规则、技能使用顺序、专有能力与共享能力基线
- 回答“这个 Agent 该怎么工作、优先用什么能力”

### `IDENTITY.md`

- 定义运行时身份说明
- 回答“这个 Agent 在现场应该被如何识别和介绍”

### `skills/`

- 放该 Agent 的专有技能
- 共享技能由平台统一安装，但运行时仍按会话可见性做验证
- 当前项目仓库默认只保留 `skills/` 这个官方目录本身
- 不再在仓库里长期堆放共享技能副本、旧专有 skill 残留或历史模板 skill

## 当前项目中不再作为主定义文件的内容

以下内容已经从 Agent 主定义层移除：

- `agent.yaml`
- `prompts/system.prompt.md`
- `prompts/channel_reply.prompt.md`
- `skills/catalog.yaml`

原因：

- 它们不是 OpenClaw 官方核心文件
- 容易把运行时、交付层和 Agent 配置层混在一起
- 长期会增加模板维护成本

## 当前项目的分层方式

### Agent 核心定义

- `soul.yaml`
- `AGENTS.md`
- `IDENTITY.md`
- `skills/`

### 交付包说明

- `packages/<agent>/config/install-manifest.yaml`
- `packages/<agent>/docs/...`

## 当前 6 个业务 Agent 的核心文件位置

`main` 目前不作为业务 Agent 单独放在 `agents/main/`，而是保留为模板：

- [主入口 Agent soul 模板](/Users/waylon/Desktop/openclaw-product/docs/templates/main-soul.example.yaml)
- [主入口 Agent AGENTS 模板](/Users/waylon/Desktop/openclaw-product/docs/templates/main-AGENTS.example.md)
- [主入口 Agent IDENTITY 模板](/Users/waylon/Desktop/openclaw-product/docs/templates/main-IDENTITY.example.md)

- [教育 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/education-agent/soul.yaml)
- [教育 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/education-agent/AGENTS.md)
- [教育 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/education-agent/IDENTITY.md)

- [股票 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/stock-agent/soul.yaml)
- [股票 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/stock-agent/AGENTS.md)
- [股票 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/stock-agent/IDENTITY.md)

- [助贷 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/loan-agent/soul.yaml)
- [助贷 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/loan-agent/AGENTS.md)
- [助贷 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/loan-agent/IDENTITY.md)

- [社媒 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/social-media-agent/soul.yaml)
- [社媒 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/social-media-agent/AGENTS.md)
- [社媒 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/social-media-agent/IDENTITY.md)

- [新闻 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/news-agent/soul.yaml)
- [新闻 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/news-agent/AGENTS.md)
- [新闻 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/news-agent/IDENTITY.md)

- [销售 Agent soul.yaml](/Users/waylon/Desktop/openclaw-product/agents/sales-agent/soul.yaml)
- [销售 Agent AGENTS.md](/Users/waylon/Desktop/openclaw-product/agents/sales-agent/AGENTS.md)
- [销售 Agent IDENTITY.md](/Users/waylon/Desktop/openclaw-product/agents/sales-agent/IDENTITY.md)

## 维护原则

- 改 Agent 的默认工作方式，优先改 `soul.yaml`
- 改工作规则，优先改 `AGENTS.md`
- 改身份说明，优先改 `IDENTITY.md`
- 改专有能力，优先改 `skills/`
- 不重新引入 `agent.yaml / prompts / skills/catalog.yaml` 作为主定义层
