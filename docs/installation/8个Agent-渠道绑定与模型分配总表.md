# 8 个 Agent 的渠道绑定与模型分配总表

> 这份文档不是概念稿，而是实施交付时直接照着配置的总表。目标是解决两个真实问题：
>
> 1. 每个 Agent 该绑定什么渠道实例
> 2. 每个 Agent 默认该走什么模型和推理强度

## 1. 总原则

### 1.1 渠道绑定原则

- 一个渠道实例只绑定一个 Agent
- 不做“一个机器人里再判断 8 个业务 Agent”的总控分发
- 同一个 Agent 可以有多个渠道实例，但每个实例仍然只指向这个 Agent
- 首发优先飞书；企微、钉钉、Webhook 作为并行可选入口

### 1.2 模型分配原则

- 平台默认值仍然是：
  - `provider: codex`
  - `model: GPT-5.4`
  - `reasoning_effort: medium`
- 但每个 Agent 按业务特性覆盖自己的 `reasoning_effort`
- 渠道层只做补充，不重写业务脑子
- fallback 统一允许回退到：
  - `local-openai / gpt-5.4 / low`

## 2. 8 个 Agent 的推荐落地表

| Agent | 推荐主渠道 | 首发渠道实例命名 | 推荐主模型 | reasoning_effort | fallback | 适合的对外风格 |
|---|---|---|---|---:|---|---|
| `stock-agent` | 飞书 / Webhook | `stockbot` | `codex / GPT-5.4` | `medium` | `local-openai / gpt-5.4 / low` | 稳健、研究型、带风险提醒 |
| `education-agent` | 飞书 / Web Chat | `educationbot` | `codex / GPT-5.4` | `medium` | `local-openai / gpt-5.4 / low` | 教学式、结构化、耐心讲解 |
| `news-agent` | 飞书 / 钉钉 / Webhook | `newsbot` | `codex / GPT-5.4` | `low` | `local-openai / gpt-5.4 / low` | 快、短、日报风格 |
| `loan-agent` | 飞书 / 企业微信 | `loanbot` | `codex / GPT-5.4` | `medium` | `local-openai / gpt-5.4 / low` | 合规、谨慎、引导式 |
| `local-commerce-agent` | 飞书 / 企业微信 / Web Chat | `commercebot` | `codex / GPT-5.4` | `low` | `local-openai / gpt-5.4 / low` | 转化导向、口语化、快回复 |
| `photo-polisher` | Webhook / Web Chat / 飞书 | `photobot` | `codex / GPT-5.4` | `low` | `local-openai / gpt-5.4 / low` | 任务编排式、结果说明式 |
| `sales-agent` | 企业微信 / 飞书 / Chat 台入口 | `salesbot` | `codex / GPT-5.4` | `low` | `local-openai / gpt-5.4 / low` | 快速转化、追问明确 |
| `legal-agent` | 飞书 / 企业微信 / Webhook | `legalbot` | `codex / GPT-5.4` | `high` | `local-openai / gpt-5.4 / low` | 审慎、专业、边界清晰 |

## 3. 每个 Agent 的推荐绑定说明

### 3.1 股票 Agent

- 首发推荐：
  - 飞书机器人：`stockbot`
  - Webhook：`stock-webhook`
- 推荐原因：
  - 飞书适合研究结论、日报、风控提醒
  - Webhook 适合接投研后台、告警系统、定时任务
- 不建议首发直接上高风险自动交易入口

### 3.2 教育 Agent

- 首发推荐：
  - 飞书机器人：`educationbot`
  - Web Chat：`education-web`
- 推荐原因：
  - 飞书适合老师演示、校内协作、文档能力
  - Web Chat 适合试听课、公开课、体验页
- 语音相关能力通过外部技能补，不要求渠道本身承载语音模型

### 3.3 资讯 Agent

- 首发推荐：
  - 飞书机器人：`newsbot`
  - 钉钉机器人：`news-dingtalk`
  - Webhook：`news-webhook`
- 推荐原因：
  - 资讯场景强调快推送、快汇总
  - 适合日报、周报、热点提醒

### 3.4 助贷 Agent

- 首发推荐：
  - 飞书机器人：`loanbot`
- 推荐原因：
  - 便于顾问跟进、材料提醒、预约排期
- 首发只做引导和初筛，不做授信判断自动化

### 3.5 电商 / 本地生活 Agent

- 首发推荐：
  - 飞书机器人：`commercebot`
  - 企业微信：`commerce-wecom`
  - Web Chat：`commerce-web`
- 推荐原因：
  - 咨询和转化场景强调短平快
  - Web Chat 可以直接接活动落地页

### 3.6 像素修图师

- 首发推荐：
  - 飞书机器人：`photobot`
  - Webhook：`photo-webhook`
  - Web Chat：`photo-web`
- 推荐原因：
  - 修图交付更适合接 API / Web 表单 / 上传入口
  - 飞书更适合内部演示与老师讲解

### 3.7 客服 / 销售转化 Agent

- 首发推荐：
  - 飞书机器人：`salesbot`
  - 企业微信：`sales-wecom`
- 推荐原因：
  - 快速对话和线索推进适合 IM 渠道
  - 后续可以接客服台，但首发先不复杂化

### 3.8 法务 / 合同流程 Agent

- 首发推荐：
  - 飞书机器人：`legalbot`
  - 企业微信：`legal-wecom`
  - Webhook：`legal-webhook`
- 推荐原因：
  - 文档、审批、合同流更适合企业内部协作渠道
  - Webhook 可接合同系统或表单系统

## 4. 当前项目中的默认模型配置

当前项目源码里，每个 Agent 的 `agent.yaml` 已经写入了推荐 profile：

| Agent | profile | 当前值 |
|---|---|---|
| `stock-agent` | `research_deep` | `medium` |
| `education-agent` | `teaching_multimodal` | `medium` |
| `news-agent` | `brief_fast` | `low` |
| `loan-agent` | `compliance_structured` | `medium` |
| `local-commerce-agent` | `conversion_fast` | `low` |
| `photo-polisher` | `vision_orchestrator` | `low` |
| `sales-agent` | `dialogue_conversion` | `low` |
| `legal-agent` | `contract_review` | `high` |

## 5. 渠道层允许补充但不允许改脑子

渠道实例层允许补的只有：

- `reasoning_effort`
- `response_style`
- `delivery_timeout`
- `channel_prompt_variant`

不建议在渠道层直接改：

- `provider`
- `model`
- Agent 的专业 role
- Agent 的 memory namespace

## 6. 推荐的首发绑定清单

首发如果只做 8 个飞书机器人，建议这样命名：

| 飞书实例 | 绑定 Agent |
|---|---|
| `stockbot` | `stock-agent` |
| `educationbot` | `education-agent` |
| `newsbot` | `news-agent` |
| `loanbot` | `loan-agent` |
| `commercebot` | `local-commerce-agent` |
| `photobot` | `photo-polisher` |
| `salesbot` | `sales-agent` |
| `legalbot` | `legal-agent` |

## 7. 推荐的本地命令

### 7.1 绑定渠道实例

```bash
openclaw agents bind --agent stock-agent --channel feishu --account stockbot
openclaw agents bind --agent education-agent --channel feishu --account educationbot
openclaw agents bind --agent news-agent --channel feishu --account newsbot
openclaw agents bind --agent loan-agent --channel feishu --account loanbot
openclaw agents bind --agent local-commerce-agent --channel feishu --account commercebot
openclaw agents bind --agent photo-polisher --channel feishu --account photobot
openclaw agents bind --agent sales-agent --channel feishu --account salesbot
openclaw agents bind --agent legal-agent --channel feishu --account legalbot
```

### 7.2 查看当前绑定

```bash
openclaw agents bindings --json
```

## 8. 实施时的检查顺序

1. 先确认 Agent 已安装
2. 再确认 Agent 已同步到本机 OpenClaw
3. 再绑定渠道实例
4. 再做 Key 初始化
5. 最后做最小对话测试

## 9. 推荐实施动作

如果你现在要开始落地，顺序建议是：

1. 先完成 8 个飞书实例的创建与沉淀
2. 先把 8 个飞书实例全部跑通
3. 后续客户有明确要求时，再补企业微信或 Webhook

这样最贴近你当前本机的真实落地方式。
