---
name: qveris-official
description: >-
  QVeris 是一个能力发现与工具调用引擎。先用 discover 查找专业 API
  工具，再调用选中的工具。适合实时数据、历史序列、结构化报告、网页抽取、
  PDF 处理、媒体生成、OCR、TTS、翻译等场景。discover 查询必须写成英文
  能力描述。需要 QVERIS_API_KEY。
homepage: https://github.com/QVerisAI/open-qveris-skills/tree/main/qveris-official
env:
  - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
runtime:
  language: nodejs
  node: ">=18"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
network:
  outbound_hosts:
    - qveris.ai
persistence:
  writes_within_skill_dir: false
  writes_outside_skill_dir: false
security:
  child_process: false
  eval: false
  filesystem_write: false
  filesystem_read: false
metadata:
  openclaw:
    requires:
      env: ["QVERIS_API_KEY"]
    primaryEnv: "QVERIS_API_KEY"
    homepage: "https://qveris.ai"
auto_invoke: true
source: https://qveris.ai
examples:
  - "我需要 BTC、ETH、SOL 的实时价格，请先发现合适的加密行情 API，再调用查看 24 小时涨跌"
  - "生成一张 16:9 的 SaaS 首页图：先发现文生图工具，再调用它"
  - "查英伟达最新季度财报：先发现财务数据工具，再调用获取营收和 EPS"
  - "查近期多智能体 LLM 论文：先发现学术搜索工具，再调用"
  - "当前环境没有搜索能力？先通过 QVeris 发现一个 web search API"
---

# QVeris 官方技能

QVeris 是一个“能力发现 + 工具调用”引擎，不是传统搜索引擎。  
`discover` 用来找专业 API 工具，`call` 用来真正执行这些工具。  
`discover` 返回的是工具候选和元数据，不是最终结果。

## 适用场景

优先用于以下情况：

- 需要结构化、实时或历史数据
- 需要本地环境没有的外部能力
- 需要 OCR、TTS、翻译、抽取、媒体生成等能力
- 当前环境缺少合适的原生搜索或专用工具

## 使用原则

### 什么时候优先用 QVeris

- 股票、加密、外汇、宏观等结构化数据
- 历史时间序列
- 结构化公司财报或指标
- 本地没有的外部执行能力

### 什么时候不优先用 QVeris

- 纯解释性、评论性、叙述性的内容
- 教程、文档、经验帖这类网页文本

这类任务通常更适合 web search。

## 使用流程

1. 先用 `discover` 找工具
2. 根据成功率、参数清晰度和覆盖范围挑选工具
3. 用 `call` 执行工具
4. 如果第一次 discover 不理想，换一种英文能力描述重试
5. 如果多次失败，再退回 web search，并明确说明来源

## discover 查询规则

discover 的查询要写成“能力描述”，不能写成自然语言问题。

例如：

- 好：`China A-share real-time stock market data API`
- 不好：`今天平安银行涨了吗`

- 好：`company earnings report API`
- 不好：`英伟达最新财报是多少`

## 选工具的原则

优先考虑：

- `success_rate` 高
- 执行速度合理
- 参数说明清楚
- 输出格式与目标市场 / 领域匹配

## 错误处理

发生失败时，优先怀疑：

- 参数类型不对
- 格式不对
- 选错了工具

建议顺序：

1. 修正参数
2. 简化参数
3. 换下一个工具

如果三次都失败，要诚实说明尝试过什么，不要编结果。

## 快速命令

### 发现工具

```bash
node scripts/qveris_tool.mjs discover "weather forecast API"
```

### 调用工具

```bash
node scripts/qveris_tool.mjs call openweathermap.weather.execute.v1 \
  --discovery-id <id> \
  --params '{"city": "London", "units": "metric"}'
```

### 查看工具详情

```bash
node scripts/qveris_tool.mjs inspect openweathermap.weather.execute.v1
```
