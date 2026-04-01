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

## 5. 最小验收

```bash
openclaw agent --agent education-agent --message "请只回复ok"
```
