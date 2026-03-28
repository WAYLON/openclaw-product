# 股票 Agent 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `stock-symbol-resolver` | TradingAgents-AShare / akshare-stock / Ashare | 建议首发 | 中 | 否 | 无 | 把中文简称、代码、市场后缀统一解析为标准股票标识。 |
| `stock-realtime-quote` | Ashare / akshare-stock | 建议首发 | 低 | 否 | 网络 | 查询实时行情、涨跌幅、盘口摘要。 |
| `stock-historical-kline` | Ashare / akshare-stock | 建议首发 | 低 | 否 | 网络 | 拉取日线、周线、分钟线并生成研究输入。 |
| `stock-fundamental-analysis` | TradingAgents-AShare / stock-analysis | 建议首发 | 中 | 否 | 网络 | 输出财务指标、估值区间、业务结构摘要。 |
| `stock-technical-analysis` | TradingAgents-AShare / stock-analysis | 建议首发 | 中 | 否 | 网络 | 做均线、量能、趋势、支撑阻力位分析。 |
| `stock-news-impact-analysis` | TradingAgents-AShare / openclaw-tavily-search | 建议首发 | 中 | 是 | 网络 / key | 结合资讯判断事件冲击方向与时效。 |
| `stock-sentiment-analysis` | TradingAgents-AShare / summarize | 建议首发 | 中 | 是 | 网络 / key | 抽取舆情情绪，输出乐观、中性、谨慎标签。 |
| `stock-watchlist-manager` | stock-watcher | 建议首发 | 低 | 否 | 本地存储 | 维护观察池、标签、备注和优先级。 |
| `stock-price-alert` | stock-monitor | 建议首发 | 中 | 否 | 调度 / 通知 | 对价格、涨跌幅、成交量设置提醒。 |
| `stock-strategy-backtest` | stock-strategy-backtester | 建议首发 | 中 | 否 | 本地计算 | 回测简单策略并输出收益、回撤、胜率。 |
| `stock-risk-summary` | TradingAgents-AShare | 建议首发 | 中 | 否 | 无 | 生成仓位、波动、事件、流动性风险摘要。 |
| `stock-research-report-generator` | TradingAgents-AShare / summarize / word-docx / excel-xlsx | 建议首发 | 中 | 否 | 文档导出 | 输出中文研究简报与讲解提纲。 |
