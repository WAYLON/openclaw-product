# 按 Agent 分配模型教程

> 这份文档解决的是一个真实交付问题：不同 Agent 的工作类型不同，不能所有 Agent 都硬用同一套大模型参数。平台级默认值可以统一，但每个 Agent 应该允许独立选择自己的模型、推理强度和回退链路。

## 1. 设计原则

### 1.1 平台默认值仍然保留

平台默认值仍然是：

- `provider: codex`
- `model: GPT-5.4`
- `reasoning_effort: medium`

这保证：

- 首次安装能跑
- 没有单独配置时不报错
- 培训和演示有统一口径

### 1.2 但 Agent 级必须允许覆盖

原因很直接：

- 股票、法务更偏深度分析
- 资讯、客服更偏快回复
- 修图 Agent 的主脑和图像处理外部技能不是一回事
- 教育 Agent 还会接语音、课件解析、课堂互动

所以推荐采用：

```text
平台默认模型
  -> 租户默认模型
    -> Agent 独立模型
      -> 渠道补充参数
```

## 2. 当前推荐分配

| Agent | 推荐主模型 | reasoning_effort | 推荐用途 |
|---|---|---:|---|
| `stock-agent` | `codex / GPT-5.4` | `medium` | 研究、分析、风险总结 |
| `education-agent` | `codex / GPT-5.4` | `medium` | 教学设计、课堂互动、资料生成 |
| `news-agent` | `codex / GPT-5.4` | `low` | 快速简报、热点汇总、定时报送 |
| `loan-agent` | `codex / GPT-5.4` | `medium` | 材料引导、合规说明、留资筛查 |
| `local-commerce-agent` | `codex / GPT-5.4` | `low` | 商品问答、活动话术、运营回复 |
| `photo-polisher` | `codex / GPT-5.4` | `low` | 修图流程编排、结果解释、任务分流 |
| `sales-agent` | `codex / GPT-5.4` | `low` | 快速对话、客户跟进、转化问答 |
| `legal-agent` | `codex / GPT-5.4` | `high` | 合同审阅、条款比较、风险提示 |

## 3. 关键理解

### 3.1 修图 Agent 不等于图像模型本体

`photo-polisher` 的大模型主要负责：

- 理解用户修图要求
- 安排使用哪个外部技能
- 解释前后差异
- 生成交付说明

真正做图像处理的是：

- `GFPGAN`
- `Real-ESRGAN`
- `rembg`

所以：

- 主脑模型可以偏快
- 图像重活由外部技能 / GPU 服务承担

### 3.2 教育 Agent 的语音能力不等于主模型变成语音模型

教育 Agent 需要：

- ASR：转写课堂录音
- TTS：生成讲解音频
- 口语反馈：对学生发音或回答点评

这些能力应通过：

- `OpenMAIC`
- 语音专用 API
- ASR/TTS 外部技能

来补齐，而不是要求主脑一个模型包打天下。

## 4. 配置顺序

推荐实际解析顺序：

1. 先读平台默认模型
2. 再读租户默认模型
3. 再读 Agent 的 `agent.yaml`
4. 最后读渠道实例补充参数

示意：

```text
platform.default_model
  -> tenant.default_agent_model
    -> agents/<agent>/agent.yaml:model
      -> channel_instance.model_override
```

## 5. Agent 级配置示例

示例：`stock-agent`

```yaml
model:
  provider: codex
  model: GPT-5.4
  reasoning_effort: medium
  profile: research_deep
  fallback_chain:
    - provider: codex
      model: GPT-5.4
      reasoning_effort: medium
    - provider: local-openai
      model: gpt-5.4
      reasoning_effort: low
```

示例：`news-agent`

```yaml
model:
  provider: codex
  model: GPT-5.4
  reasoning_effort: low
  profile: brief_fast
  fallback_chain:
    - provider: codex
      model: GPT-5.4
      reasoning_effort: low
    - provider: local-openai
      model: gpt-5.4
      reasoning_effort: low
```

示例：`legal-agent`

```yaml
model:
  provider: codex
  model: GPT-5.4
  reasoning_effort: high
  profile: contract_review
  fallback_chain:
    - provider: codex
      model: GPT-5.4
      reasoning_effort: high
    - provider: codex
      model: GPT-5.4
      reasoning_effort: medium
```

## 6. 渠道侧补充配置

如果某个飞书机器人就是给“快回复场景”用的，可以允许它在渠道层补一层：

```yaml
channel_instance:
  id: salesbot
  type: feishu
  bound_agent_id: sales-agent
  model_override:
    reasoning_effort: low
    response_style: concise
```

注意：

- 渠道层只能做补充
- 不要在渠道层把 Agent 完全换脑
- 主脑仍应由 Agent 自己定义

## 7. 今天这套本地安装法里怎么做

今天本地已经安装了多个 OpenClaw Agent，并通过飞书一只机器人对应一个 Agent。

在这种交付方式里，推荐：

1. 模型主配置写进每个 `agents/<agent>/agent.yaml`
2. 飞书机器人只绑定 Agent，不直接决定主模型
3. 如果某个 Agent 需要单独模型，再改它自己的 `agent.yaml`
4. 如果某个渠道要更快，再在渠道层只补 `reasoning_effort`

## 8. 模型推荐落地表

| Agent | 推荐 profile | 原因 |
|---|---|---|
| `stock-agent` | `research_deep` | 需要多步骤分析、研报摘要、风控总结 |
| `education-agent` | `teaching_multimodal` | 需要讲义、课堂、作业、语音协同 |
| `news-agent` | `brief_fast` | 更强调快、稳、日更周更 |
| `loan-agent` | `compliance_structured` | 要求表述稳健、结构化、合规 |
| `local-commerce-agent` | `conversion_fast` | 面向运营、咨询、活动话术，速度优先 |
| `photo-polisher` | `vision_orchestrator` | 主脑负责任务拆分，图像处理走外部技能 |
| `sales-agent` | `dialogue_conversion` | 要求回复快、追问强、转化明确 |
| `legal-agent` | `contract_review` | 更需要深度比对和风险表达 |

## 9. 首发阶段不建议做的事

首发不建议：

- 一个 Agent 同时动态切 5 种模型再做复杂路由
- 在渠道里临时决定业务脑子
- 把图像/GPU/语音外部技能和主脑模型混成一层

首发建议：

- 每个 Agent 先有一个明确主模型
- 再配一个简单 fallback
- 等真实使用数据出来，再收敛模型成本

## 10. 验证方法

### 10.1 看配置

```bash
sed -n '1,80p' agents/stock-agent/agent.yaml
sed -n '1,80p' agents/legal-agent/agent.yaml
```

### 10.2 看差异

重点看：

- `reasoning_effort`
- `profile`
- `fallback_chain`

### 10.3 联调时检查

联调时建议先问：

- 股票 Agent：`请帮我整理一份某只股票的研究摘要`
- 资讯 Agent：`请生成今日简报`
- 法务 Agent：`请列出这份合同的风险条款`

如果输出风格明显不同，说明模型分配已经起作用。

## 11. 推荐模板文件

推荐配合这个模板一起用：

- [agent-model-routing.example.yaml](/Users/waylon/Desktop/openclaw-product/docs/templates/agent-model-routing.example.yaml)

它用于集中查看：

- 平台默认模型
- 租户默认模型
- Agent 级覆盖
- 渠道级补充参数
