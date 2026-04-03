# 7 个首发 Agent 的渠道绑定与模型分配总表

> 这份文档用于实施时直接照着配置当前首发 7 个 Agent。

## 1. 总原则

- 一个飞书机器人只绑定一个 Agent
- 平台默认模型统一为 `local-proxy/gpt-5.4`
- 平台当前同时保留一个备用大模型：`siliconflow/Qwen/Qwen3.5-122B-A10B`
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

## 3.1 Feishu 最终 JSON 结构

主入口 bot 不是普通 `accounts` 之一，而是 `channels.feishu` 顶层默认账号。推荐结构直接按下面写，不要自行猜结构：

```json
{
  "channels": {
    "feishu": {
      "appId": "<主入口 Agent 的 appId>",
      "appSecret": "<主入口 Agent 的 appSecret>",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "requireMention": true,
      "allowFrom": ["*"],
      "accounts": {
        "educationbot": {
          "appId": "<教育 Agent 的 appId>",
          "appSecret": "<教育 Agent 的 appSecret>"
        },
        "stockbot": {
          "appId": "<股票 Agent 的 appId>",
          "appSecret": "<股票 Agent 的 appSecret>"
        },
        "loanbot": {
          "appId": "<助贷 Agent 的 appId>",
          "appSecret": "<助贷 Agent 的 appSecret>"
        },
        "socialbot": {
          "appId": "<社媒 Agent 的 appId>",
          "appSecret": "<社媒 Agent 的 appSecret>"
        },
        "newsbot": {
          "appId": "<新闻 Agent 的 appId>",
          "appSecret": "<新闻 Agent 的 appSecret>"
        },
        "salesbot": {
          "appId": "<销售 Agent 的 appId>",
          "appSecret": "<销售 Agent 的 appSecret>"
        }
      }
    }
  }
}
```

如果把主入口 bot 也塞进 `accounts`，状态探针和绑定结果很容易变成看起来像 `6/7`。

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

## 6. 当前备用大模型

平台当前额外保留一个可选大模型：

- `siliconflow/Qwen/Qwen3.5-122B-A10B`
- `baseUrl = https://api.siliconflow.cn/v1`
- 需要 `SILICONFLOW_API_KEY`

说明：

- 当前它不是平台主默认
- 默认仍然是 `local-proxy/gpt-5.4`
- 如果后续某个 Agent 需要更大模型，再按 Agent 单独覆盖
