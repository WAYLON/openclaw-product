# 7 个首发 Agent 能力总览

> 这份文档用于对外介绍当前首发的 7 个 Agent 的能力边界、适用场景和演示重点。

| Agent | 专业定位 | 核心能力 | 最适合问什么 | 首发最能演示的能力 |
|---|---|---|---|---|
| `main` | 默认入口 / 技能管理员 | 共享 skill 安装、审查、分发、通用协调 | “给全部 agent 安装一个 skill” “这个 skill 安全不安全” | skill 安装、skill 审查、全员分发 |
| `education-agent` | 教学资料整理与讲解辅助 | `openmaic` + 共享技能 | “帮我把这份讲义整理成课堂重点” | 资料摘要、结构化讲解、备课整理 |
| `stock-agent` | 股票研究与风险提示 | `tradingagents-analysis` + 共享技能 | “分析这个股票的风险和观察点” | 股票分析、风险总结、研究整理 |
| `loan-agent` | 助贷方向通用辅助 | 共享技能 | “帮我整理这段材料说明” | 材料整理、说明归纳、文本辅助 |
| `social-media-agent` | 社交媒体浏览与内容运营辅助 | `opencli`、`web-access`、`summarize` | “帮我整理今天的社媒热点” | 热点整理、内容摘要、分发建议 |
| `news-agent` | 新闻动态整理与简报输出 | 共享技能 | “把今天几条新闻整理成摘要” | 新闻摘要、简报底稿、重点提炼 |
| `sales-agent` | 销售跟进与转化辅助 | 共享技能 | “总结这段客户对话，给我下一步建议” | 对话摘要、跟进建议、销售口径整理 |

## 统一共享技能

当前 7 个首发 Agent 共用的基础技能：

- `web-access`
- `opencli`
- `self-improving-agent`
- `skill-vetter`
- `summarize`
- `agent-browser`
- `ontology`
- `weather`
- `document-pro`
- `github`
- `proactive-agent`
- `mcporter`
- `multi-search-engine`
- `nano-pdf`
- `nano-banana-pro`
- `excel-xlsx`
- `word-docx`
- `desktop-control`

补充：

- `main` 额外挂 `skill-creator`

## 一句话讲法

- `main`：默认入口和技能管理员
- `education-agent`：偏教学资料整理和讲解辅助
- `stock-agent`：偏股票研究和风险提示
- `loan-agent`：偏材料整理和文本辅助
- `social-media-agent`：偏社媒浏览、热点、内容运营
- `news-agent`：偏新闻动态和摘要简报
- `sales-agent`：偏销售跟进和转化建议
