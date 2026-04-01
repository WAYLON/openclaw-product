# education-agent 安装示例

## 1. 注册 Agent

```bash
openclaw agents add education-agent
```

## 2. 安装模板

```bash
cd ~/Desktop/openclaw-product
./agent-platform agent install education-agent
./agent-platform openclaw export education-agent
```

## 3. 绑定飞书

```bash
openclaw agents bind --agent education-agent --channel feishu --account educationbot
```

## 4. 配置 OpenMAIC hosted access code

写入：

- `~/.openclaw/openclaw.json`

配置路径：

- `skills.entries.openmaic.config.accessCode`

## 4.1 OpenMAIC 作为专有技能的可见性要求

如果现场是把 `openmaic` 按教育 Agent 私有 skill 方式接入，需要额外确认：

1. skill 放在：
   - `~/.openclaw/parallel-agents/workspaces/education-agent/skills/openmaic/`
2. `SKILL.md` 带合法 frontmatter
3. 拷贝后已重启 gateway
4. 用新会话验证，不用旧线程结果代替
5. 如果仍沿用旧技能清单，直接重建 `education-agent` 的 session snapshot

当前项目已经有一条真实跑通的现场事实：

- 私有 skill 路径按下面这条实际运行：
  - `~/.openclaw/parallel-agents/workspaces/education-agent/skills/openmaic/SKILL.md`
- `references/hosted-mode.md` 已补齐
- `references/generate-flow.md` 已补齐
- `accessCode` 已通过：
  - `https://open.maic.chat/api/health`
- `education-agent` 已成功提交真实课堂生成任务，不是只回大纲

现场实测任务示例：

- `Job ID: 4iOKux0RvQ`
- 运行状态：`running / generating_scenes`
- 说明：已经进入真实生成链路

## 5. 最小验收

```bash
openclaw agent --agent education-agent --message "请只回复ok"
```

如果刚接入或刚修过 `openmaic`，建议直接开新会话再测：

```bash
openclaw agent --agent education-agent --message "帮我把这份讲义整理成课堂重点"
```

当前项目建议作为标准演示语句使用：

```text
用 openmaic 生成一个互动课堂：零基础文科生，30 分钟学会 Python。生成完成后直接把 classroom URL 发我。
```
