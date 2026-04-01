# 7 个首发 Agent 完整安装教程

> 目标：把当前首发的 7 个 Agent 安装到一台新的 OpenClaw 环境中，并完成最小验收。

## 1. 先装 OpenClaw 本体

说明：

- OpenClaw 本体安装先以官方文档为准
- 飞书插件安装先以官方文档为准
- 下面保留的是当前项目已验证可用的官方命令入口

```bash
npm install -g openclaw
openclaw onboard --mode local --flow quickstart --non-interactive --accept-risk --install-daemon --skip-channels --skip-search --skip-ui --skip-health --auth-choice skip
npx -y @larksuite/openclaw-lark install
```

然后确认：

```bash
openclaw --version
openclaw status --deep
```

## 2. 配默认模型

默认模型以实际运行基线为准：

- `local-proxy/gpt-5.4`
- `baseUrl = http://127.0.0.1:8080/v1`
- `apiKey = pwd`

## 3. 注册 7 个 Agent

```bash
for agent in \
  education-agent \
  stock-agent \
  loan-agent \
  social-media-agent \
  news-agent \
  sales-agent
do
  openclaw agents add "$agent"
done
```

说明：

- `main` 是默认入口，不需要额外创建

## 4. 安装共享技能

当前共享技能目录：

- `~/.openclaw/skills`

当前共享技能基线：

- `web-access`
- `opencli`
- `self-improving-agent`
- `skill-vetter`
- `skill-creator`
- `summarize`
- `agent-browser`
- `nano-pdf`
- `nano-banana-pro`
- `excel-xlsx`
- `word-docx`
- `desktop-control`

## 5. 安装专有技能

- `stock-agent`
  - `tradingagents-analysis`
- `education-agent`
  - `openmaic`

## 6. 绑定飞书

说明：

- Agent 创建、渠道绑定优先走官方命令
- 本项目只补当前 7 bot 对 7 agent 的绑定表

```bash
openclaw agents bind --agent main --channel feishu --account default
openclaw agents bind --agent education-agent --channel feishu --account educationbot
openclaw agents bind --agent stock-agent --channel feishu --account stockbot
openclaw agents bind --agent loan-agent --channel feishu --account loanbot
openclaw agents bind --agent social-media-agent --channel feishu --account socialbot
openclaw agents bind --agent news-agent --channel feishu --account newsbot
openclaw agents bind --agent sales-agent --channel feishu --account salesbot
```

## 7. 插件与 Key

插件：

- `memory-lancedb-pro`
- `lossless-claw`

插件安装细节见：

- [记忆插件安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/记忆插件安装教程.md)

运行时 key：

- `TRADINGAGENTS_TOKEN`
- `GEMINI_API_KEY`
- `QVERIS_API_KEY`

这些运行时 key 都要写到：

- `~/Library/LaunchAgents/ai.openclaw.gateway.plist`

然后重启 gateway。

配置型 key：

- `openmaic` 的 `accessCode`

写到：

- `~/.openclaw/openclaw.json`

## 8. 最小验收

```bash
openclaw agent --agent education-agent --message "请只回复ok"
openclaw agent --agent stock-agent --message "请只回复ok"
openclaw agent --agent loan-agent --message "请只回复ok"
openclaw agent --agent social-media-agent --message "请只回复ok"
openclaw agent --agent news-agent --message "请只回复ok"
openclaw agent --agent sales-agent --message "请只回复ok"
```

## 9. 后续新增专有技能怎么升级

如果后续要给某个 Agent 新增专有技能，不要直接覆盖已经运行一段时间的客户环境。

统一按下面规则做：

1. 先改项目模板和文档
2. 先补 key / token / access code
3. 先把 skill 拷到目标 Agent
4. 先做单 Agent 验证
5. 再启用 skill
6. 再重启 gateway
7. 再做真实场景验证

不要直接做：

- 不要直接覆盖客户整个 `openclaw.json`
- 不要直接替换客户整个 workspace
- 不要顺手修改其他 Agent 的模型、权限、记忆命名空间或渠道绑定

详细规范见：

- [专有技能新增规范.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/专有技能新增规范.md)
- [版本迁移模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本迁移模板.md)
- [回滚模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/回滚模板.md)
