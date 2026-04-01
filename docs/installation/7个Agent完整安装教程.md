# 7 个首发 Agent 完整安装教程

> 目标：把当前首发的 7 个 Agent 安装到一台新的 OpenClaw 环境中，并完成最小验收。

## 0. 如果不是干净机器，先清理既有状态

如果这台机器之前装过 OpenClaw，不要直接覆盖安装，先走：

- [重装与清理路径.md](/Users/waylon/Desktop/openclaw-product/docs/installation/重装与清理路径.md)

固定顺序：

1. 备份
2. 清理既有状态
3. 重装
4. 验收

## 1. 先装 OpenClaw 本体

说明：

- OpenClaw 本体安装先以官方文档为准
- 飞书插件安装先以官方文档为准
- 下面保留的是当前项目已验证可用的官方命令入口
- `npm install -g openclaw` 只安装或更新 CLI，不会自动下载或更新 `OpenClaw.app`
- `npx -y @larksuite/openclaw-lark install` 只安装飞书插件，不会代替 App 安装或 App 更新
- `OpenClaw.app` 需要单独按官方文档下载或升级

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

工具权限基线：

- 当前 7 个 Agent 默认都是 `tools.profile = full`
- 当前项目文档口径的 `exec` 默认放权写法为：
  - `tools.exec.security = "full"`
  - `tools.exec.ask = "off"`
- 这样像 `excel-xlsx`、`word-docx` 这类需要本地命令落文件的 skill 才不会因为 allowlist miss 失败

Chrome 远程调试要求：

- `opencli`、`agent-browser` 依赖 Chrome 远程调试
- 需要开启后访问：
  - `chrome://inspect/#remote-debugging`
- 确认可见当前本机 Chrome 调试目标

## 5. 安装专有技能

- `stock-agent`
  - `tradingagents-analysis`
- `education-agent`
  - `openmaic`

## 6. 绑定飞书

说明：

- Agent 创建、渠道绑定优先走官方命令
- 本项目只补当前 7 bot 对 7 agent 的绑定表
- 主入口 bot 不是 `accounts` 里的普通账号，而是 `channels.feishu` 顶层默认账号
- 如果把 7 个 bot 全部都塞进 `accounts`，很容易出现看起来像 `6/7` 的错误状态

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

## 8. 最低验收

最低验收不要只看“插件装上了”和“status 能跑”，至少要覆盖：

1. Gateway probe
2. 7 个 Agent 最小回复
3. memory 健康检查
4. Feishu 配置健康检查

```bash
./agent-platform acceptance --full --report ./reports/install-acceptance.md
```

补充说明：

- `pairing required`
- memory 检索异常
- Feishu health 数量不对

这些都应该在这轮验收里尽早暴露，而不是等到客户真实用起来才发现。

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
