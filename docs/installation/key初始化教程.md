# Key 初始化教程

> 这份文档只保留当前真实安装口径。

## 1. 两类 Key

### 1.1 后台运行时 Key

这类 key 要写到：

- `~/Library/LaunchAgents/ai.openclaw.gateway.plist`

然后 reload / restart gateway。

当前例子：

- `TRADINGAGENTS_TOKEN`
- `GEMINI_API_KEY`
- `QVERIS_API_KEY`

### 1.2 配置型 Key

这类 key 写到：

- `~/.openclaw/openclaw.json`

当前例子：

- `openmaic`
  - `skills.entries.openmaic.config.accessCode`

## 2. 当前实际规则

- 后台 runtime 用的 key，不只写 shell
- 必须写 LaunchAgent
- 然后重启 gateway

如果某个 skill 明确要求走配置读取，就写 `openclaw.json`

## 3. 当前真实示例

### TradingAgents

- key 名：`TRADINGAGENTS_TOKEN`
- 写入位置：LaunchAgent

### OpenMAIC

- key 名：`OPENMAIC_ACCESS_CODE`
- 实际落点：`openclaw.json`

### Gemini

- key 名：`GEMINI_API_KEY`
- 写入位置：LaunchAgent

## 4. 验证方法

### 验证 LaunchAgent 环境变量

```bash
launchctl print gui/$(id -u)/ai.openclaw.gateway
```

### 验证 OpenClaw 配置

```bash
jq '.skills.entries.openmaic' ~/.openclaw/openclaw.json
```
