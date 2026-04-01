# 7 个首发 Agent 的渠道绑定与模型分配总表

> 这份文档用于实施时直接照着配置当前首发 7 个角色。

## 1. 总原则

- 一个飞书机器人只绑定一个 Agent
- 平台默认模型统一为 `local-proxy/gpt-5.4`
- 当前首发不做按 Agent 的模型 provider 分裂
- 所有 Agent 当前统一走共享技能基线

## 2. 绑定总表

| Agent | 飞书账号 | 默认模型 | reasoning_effort | 对外风格 |
|---|---|---|---:|---|
| `main` | `default` | `local-proxy/gpt-5.4` | `medium` | 默认入口、安装协调、技能管理员 |
| `education-agent` | `educationbot` | `local-proxy/gpt-5.4` | `medium` | 教学式、结构化、耐心讲解 |
| `stock-agent` | `stockbot` | `local-proxy/gpt-5.4` | `medium` | 稳健、研究型、风险提醒 |
| `loan-agent` | `loanbot` | `local-proxy/gpt-5.4` | `medium` | 合规、谨慎、引导式 |
| `social-media-agent` | `socialbot` | `local-proxy/gpt-5.4` | `low` | 快、清楚、内容运营导向 |
| `news-agent` | `newsbot` | `local-proxy/gpt-5.4` | `low` | 快、短、日报风格 |
| `sales-agent` | `salesbot` | `local-proxy/gpt-5.4` | `low` | 快速转化、推进明确 |

## 3. 推荐绑定命令

```bash
openclaw agents bind --agent main --channel feishu --account default
openclaw agents bind --agent education-agent --channel feishu --account educationbot
openclaw agents bind --agent stock-agent --channel feishu --account stockbot
openclaw agents bind --agent loan-agent --channel feishu --account loanbot
openclaw agents bind --agent social-media-agent --channel feishu --account socialbot
openclaw agents bind --agent news-agent --channel feishu --account newsbot
openclaw agents bind --agent sales-agent --channel feishu --account salesbot
```

## 4. 飞书策略

- `dmPolicy = open`
- `groupPolicy = open`
- `requireMention = true`
- `allowFrom = ["*"]`

## 5. 检查顺序

1. 确认 Agent 已创建
2. 确认共享技能已分配
3. 确认模型默认值是 `local-proxy/gpt-5.4`
4. 绑定飞书账号
5. 做最小对话测试
