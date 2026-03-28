# stock-agent 完整安装示例

> 当前推荐口径：**官方 OpenClaw 命令优先**。本示例中，`openclaw` 负责本体安装、Agent 注册与渠道绑定，`agent-platform` 只负责项目模板生成、工作区同步与交付自动化。

## 1. 前置条件

先按官方方式安装 OpenClaw：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw --version
openclaw status
```

## 2. 注册 stock-agent

```bash
openclaw agents add stock-agent
openclaw agents list
```

## 3. 初始化项目模板状态

```bash
cd ~/Desktop/openclaw-product
./agent-platform init
./agent-platform start
./agent-platform doctor
```

## 4. 生成 stock-agent 模板并导出

```bash
./agent-platform agent install stock-agent
./agent-platform openclaw export stock-agent
./agent-platform agent list
```

再检查工作区模板：

```bash
find .platform/workspaces/stock-agent -maxdepth 2 -type f | sort
```

## 5. 设置本机 OpenClaw 身份文件

```bash
openclaw agents set-identity \
  --agent stock-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/stock-agent/IDENTITY.md
```

## 6. 绑定渠道

优先使用官方命令。企业微信示例：

```bash
openclaw agents bind --agent stock-agent --channel wecom --account wecom-stock-app
openclaw agents bindings --json
```

如果当前阶段先走飞书，也可以：

```bash
openclaw agents bind --agent stock-agent --channel feishu --account stockbot
```

## 7. 配置股票相关 Key

### Tavily 搜索

```bash
./agent-platform secret set stock-agent tavily_api_key --value "replace-me" --scope agent
```

### TradingAgents-AShare 接入点

```bash
./agent-platform secret set stock-agent tradingagents_endpoint --value "http://127.0.0.1:9001" --scope agent
```

### 可选 Qveris

```bash
./agent-platform secret set stock-agent qveris_api_key --value "replace-me" --scope agent
```

## 8. 检查交付包

```bash
find packages/stock-agent/docs -maxdepth 1 -type f | sort
sed -n '1,160p' agents/stock-agent/skills/catalog.yaml
sed -n '1,160p' .platform/workspaces/stock-agent/skills/catalog.yaml
```

## 9. 首次联调建议

建议先测试：
- 帮我解析一下宁德时代的股票代码和市场
- 帮我做一份最近 30 天的技术面摘要
- 帮我生成一份中文研究简报

最小验收：

```bash
openclaw agent --agent stock-agent --message "请用一句话介绍你自己"
```

## 10. 风险提醒

股票 Agent 首发定位是：
- 研究辅助
- 风险提示
- 信息归纳

不建议首发直接上线：
- 自动交易
- 直接荐股
- 自动执行买卖

## 11. 失败排查

### 查不到行情

优先检查：
- `tradingagents_endpoint`
- 外部行情数据技能底座是否可用

### 资讯分析不生效

优先检查：
- `tavily_api_key`

### 渠道绑定后无响应

先确认：

```bash
openclaw agents bindings --json
```

看是否存在：

```text
stock-agent <- wecom:wecom-stock-app
```

或：

```text
stock-agent <- feishu:stockbot
```
