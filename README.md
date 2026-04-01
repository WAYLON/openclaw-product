# OpenClaw 实战交付工程

这是一个基于 OpenClaw 的多 Agent 实战交付仓库。

这次重写后的口径，不再以早期概念模板为准，而是以当前这台 macOS 机器上已经实际跑通的环境为基线，并按当前首发的 `7` 个角色收敛：

- OpenClaw CLI / App：安装时以最新稳定版为准
- `npm install -g openclaw` 默认只更新 CLI，不会自动下载或更新 `OpenClaw.app`
- 飞书官方插件安装命令不会代替 App 安装或 App 更新
- Gateway：`~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- 默认模型：`local-proxy/gpt-5.4`
- 备用大模型：`siliconflow/Qwen/Qwen3.5-122B-A10B`
- 运行模式：本机 `local` + LaunchAgent 守护
- 当前首发 Agent 总数：`7`
  - `main`（默认入口 / 技能管理员）
  - `education-agent`
  - `stock-agent`
  - `loan-agent`
  - `social-media-agent`
  - `news-agent`
  - `sales-agent`
- 渠道：飞书 `7` 个机器人，对应 `7` 个 Agent
- 长期记忆插件：`memory-lancedb-pro`
- 上下文压缩插件：`lossless-claw`

## 当前项目目标

这个仓库现在承担 4 件事：

1. 固化这套已经跑通的 OpenClaw 生产口径
2. 管理当前首发 7 个 Agent 的模板、专有 skill 和交付资料
3. 管理共享基础 skill 的分配规则
4. 给新机器复刻出相同的安装、配置和交付结构

## 当前运行基线

真实运行态现在直接是：

- `local-proxy / gpt-5.4`
- `baseUrl = http://127.0.0.1:8080/v1`
- `apiKey = pwd`

当前同时补充了一个可选大模型：

- `siliconflow / Qwen/Qwen3.5-122B-A10B`
- `baseUrl = https://api.siliconflow.cn/v1`

这套链路是当前机器上已经验证过稳定且明显快于 `openai-codex` OAuth 的方案。

## 核心设计原则

- 所有安装动作优先走官方文档与官方命令
- 不设业务总控 Agent，业务 Agent 平行独立
- `main` 只做默认入口与技能管理员，不做业务总控分发
- 一个飞书机器人只绑定一个 Agent
- 共享 skill 放在 `~/.openclaw/skills`
- 专有 skill 放在 `~/.openclaw/workspaces/<agent>/skills`
- 当前项目文档口径的 `exec` 默认放权写法为：
  - `tools.profile = "full"`
  - `tools.exec.security = "full"`
  - `tools.exec.ask = "off"`
- 后台运行时用到的 key，统一写入 LaunchAgent 环境变量并重启 gateway
- skill 明确要求写配置文件的，再写进 `openclaw.json`

## 当前共享技能基线

当前已纳入全局共享基础技能的有：

- `web-access`
- `opencli`
- `self-improving-agent`
- `skill-vetter`
- `skill-creator`
- `summarize`
- `agent-browser`
- `ontology`
- `weather`
- `document-pro`
- `github`
- `proactive-agent`
- `mcporter`
- `multi-search-engine`
- `nano-pdf`
- `nano-banana-pro`
- `excel-xlsx`
- `word-docx`
- `desktop-control`

其中：

- `main` 额外显式挂了 `skill-creator`
- 所有 Agent 当前都使用 `tools.profile = full`
- `opencli`、`agent-browser` 依赖 Chrome 远程调试
- 安装后需要在 `chrome://inspect/#remote-debugging` 确认调试目标可见

## 当前专有技能

- `stock-agent`
  - `tradingagents-analysis`
- `education-agent`
  - `openmaic`
- `social-media-agent`
  - 当前首发先依赖共享技能，不额外挂专有 skill

## 目录说明

- `agents/`
  - 各业务 Agent 的核心模板定义
- `packages/`
  - 面向交付的专业包说明与安装清单
- `channels/`
  - 渠道接入 connector 模板
- `core/`
  - 底层装配、配置、注册与密钥处理逻辑
- `installer/`
  - 模板同步、导出、安装校验
- `docs/`
  - 架构、安装、交付、讲解文档

## 安装后运行目录

按本项目安装完成后，最终生效的现场目录以 `~/.openclaw` 为准，结构应直接落成：

- `~/.openclaw/workspaces/<agent>/`
- `~/.openclaw/agents/<agent>/agent/`
- `~/.openclaw/skills/`
- `~/.openclaw/extensions/`
- `~/.openclaw/memory/`
- `~/.openclaw/logs/`

项目仓库 `openclaw-product/` 只是模板、安装器和文档来源，不是最终运行现场。

## 文档入口

- [docs/architecture/平台总体架构与交付设计.md](/Users/waylon/Desktop/openclaw-product/docs/architecture/平台总体架构与交付设计.md)
  - 当前项目的真实运行架构、技能分层、Key 规则、飞书绑定策略
- [docs/installation/实际运行基线与重写说明.md](/Users/waylon/Desktop/openclaw-product/docs/installation/实际运行基线与重写说明.md)
  - 按当前机器实际跑通的方式复刻
- [docs/templates/agent-model-routing.example.yaml](/Users/waylon/Desktop/openclaw-product/docs/templates/agent-model-routing.example.yaml)
  - 当前推荐模型路由模板
- [docs/templates/channel-binding.example.yaml](/Users/waylon/Desktop/openclaw-product/docs/templates/channel-binding.example.yaml)
  - 当前推荐飞书绑定模板
- [docs/installation/记忆插件安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/记忆插件安装教程.md)
  - `memory-lancedb-pro` 与 `lossless-claw` 的正式安装说明
- [docs/delivery/专有技能新增规范.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/专有技能新增规范.md)
  - 后续给某个 Agent 增加专有技能时的统一规则
- [docs/delivery/版本迁移模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本迁移模板.md)
  - 老客户增量升级模板
- [docs/delivery/回滚模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/回滚模板.md)
  - 新技能上线失败时的标准回滚模板
- [docs/guides/README.md](/Users/waylon/Desktop/openclaw-product/docs/guides/README.md)
  - 使用、培训、人格审阅入口
- [docs/guides/Agent官方核心文件说明.md](/Users/waylon/Desktop/openclaw-product/docs/guides/Agent官方核心文件说明.md)
  - 当前项目里 Agent 官方核心文件与交付文档的分层说明
- [docs/delivery/README.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/README.md)
  - 交付、升级、回滚入口

## 推荐落地顺序

1. 先按官方文档安装 OpenClaw CLI / App
2. 用 CLI 初始化本机 OpenClaw
3. 按官方文档安装并启用飞书官方插件
4. 配置 `local-proxy/gpt-5.4`
5. 配置 7 个飞书机器人与 7 个 Agent 的绑定
6. 启用 `memory-lancedb-pro` 和 `lossless-claw`
7. 安装共享基础 skill
8. 再给 `stock-agent` / `education-agent` 等加专有 skill

## 后续新增专有技能的默认策略

- 只做增量，不做覆盖
- 先改模板和文档，再迁移客户现场
- 不直接覆盖客户已运行一段时间的 `openclaw.json`
- 不改已有 `agent id`、渠道绑定、记忆命名空间
- 新 skill 默认按“可选启用”处理

具体执行时，统一参考这三份文档：

- [docs/delivery/专有技能新增规范.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/专有技能新增规范.md)
- [docs/delivery/版本迁移模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本迁移模板.md)
- [docs/delivery/回滚模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/回滚模板.md)

其中已经补清楚：

- 每个业务 Agent 分别适合新增什么类型的专有技能
- 每个 Agent 应该改哪些文件
- 老客户现场升级顺序
- 哪些动作不能做
- 出问题后如何只回滚目标 skill，而不影响已稳定运行的人

## 推荐命令

```bash
npm install -g openclaw
openclaw onboard --mode local --flow quickstart --non-interactive --accept-risk --install-daemon --skip-channels --skip-search --skip-ui --skip-health --auth-choice skip
npx -y @larksuite/openclaw-lark install

make venv
make bootstrap
make doctor
make quality
make check-packages
make delivery-check
make acceptance
```

补充：

- `make delivery-check`
  - 校验当前仓库是否具备可交付的 7 角色文档、模板和交付包结构
- `make acceptance`
  - 对本机 OpenClaw 环境执行最小只读验收
  - 默认不跑 `channels --probe`
  - 如需附加渠道探测或最小回复测试，可直接运行 `scripts/acceptance_check.py` 的参数版

## 说明

桌面上已经有两份真实安装文档：

- `/Users/waylon/Desktop/OpenClaw-安装部署指南-精简版.md`
- `/Users/waylon/Desktop/OpenClaw-安装与排障记录.md`

本仓库现在默认以那两份文档为最终安装基线。

补充：

- OpenClaw 本体安装、飞书插件安装、Agent 创建与渠道绑定，默认都先遵循官方文档
- 本仓库主要补充的是：7 角色交付结构、共享技能、专有技能、记忆插件、Key 规则和迁移回滚规范
