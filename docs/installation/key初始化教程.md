# Key 初始化教程

> 这份文档只保留当前真实安装口径。

## 1. 统一规则

所有需要 key 的技能，都按下面两层写清：

1. `LaunchAgent`
   - 是否需要写进 `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
2. `环境变量`
   - 实际变量名是什么

如果某个技能不是走环境变量，而是走配置文件读取，则额外写：

3. `配置位置`
   - 在 `~/.openclaw/openclaw.json` 的哪个字段

## 2. 当前技能与 Key 对照

### TradingAgents

- 技能：`tradingagents-analysis`
- LaunchAgent：需要
- 环境变量：`TRADINGAGENTS_TOKEN`
- 配置位置：不使用
- 重启 gateway：需要

### QVeris

- 技能：`qveris`
- LaunchAgent：需要
- 环境变量：`QVERIS_API_KEY`
- 配置位置：插件配置仍可存在于 `openclaw.json`，但运行时 key 以 LaunchAgent 为准
- 重启 gateway：需要

### Gemini

- 技能：`nano-banana-pro` 等依赖 Gemini 的能力
- LaunchAgent：需要
- 环境变量：`GEMINI_API_KEY`
- 配置位置：不使用
- 重启 gateway：需要

### OpenMAIC

- 技能：`openmaic`
- LaunchAgent：不需要
- 环境变量：不使用
- 配置位置：`skills.entries.openmaic.config.accessCode`
- 重启 gateway：修改后建议重启

### SiliconFlow

- 用途 1：平台备用大模型
- 用途 2：`memory-lancedb-pro` 的 embedding
- LaunchAgent：建议写入
- 环境变量：`SILICONFLOW_API_KEY`
- 配置位置：模型和 embedding 的 `baseUrl / model / dimensions` 写 `openclaw.json`
- 重启 gateway：需要

## 3. 当前实际规则

- 后台运行时 key，不只写 shell
- 必须写 LaunchAgent
- 然后重启 gateway
- 配置型 key 再写 `openclaw.json`

## 4. 验证方法

### 验证 LaunchAgent

检查文件：

```bash
plutil -p ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

检查运行时：

```bash
launchctl print gui/$(id -u)/ai.openclaw.gateway
```

### 验证环境变量

重点查看这些变量是否已进入 gateway 运行时：

- `TRADINGAGENTS_TOKEN`
- `QVERIS_API_KEY`
- `GEMINI_API_KEY`
- `SILICONFLOW_API_KEY`

### 验证 OpenClaw 配置

```bash
jq '.skills.entries.openmaic' ~/.openclaw/openclaw.json
```
