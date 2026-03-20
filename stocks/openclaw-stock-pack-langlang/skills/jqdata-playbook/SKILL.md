---
name: jqdata-playbook
description: >-
  用于 JoinQuant / JQData 方向的 A 股研究工作流，包括历史筛选、
  回测规划、因子研究、分钟级形态分析，以及把用户的股票想法转成可重复
  执行的量化任务。
metadata:
  short-description: 聚宽研究工作流与参考技能
---

# 聚宽研究流程技能

这个技能是围绕 JoinQuant / JQData 的工作流层。  
当用户要做 A 股历史分析、因子研究或可复用选股流程时，使用它。

## 适用场景

适用于以下任务：

- A 股历史数据分析
- 量化式筛选
- 分钟级或日级形态研究
- 事件研究
- 回测规划
- 把主观想法改造成脚本化规则

## 工作流程

1. 把用户需求翻译成明确规则
2. 判断现有本地脚本是否足够
3. 如有需要，在已安装时路由给 `jqdata-research`
4. 报告假设、股票池、时间窗口和限制条件
5. 把有价值的规则沉淀下来复用

## 规则翻译

把模糊语言转成可量化定义。

例如：

- “放量” -> 用量比或滚动分位数定义
- “突破” -> 用前高、均线或区间突破定义
- “强势” -> 用涨幅排名、换手、广度或相对强度定义
- “低吸” -> 用回撤深度、支撑位和反弹确认定义

## 输出要求

每个聚宽风格研究都应明确写出：

- 股票池
- 时间区间
- 数据频率
- 信号公式
- 排除条件
- 评估方式

## 参考资料

- 阅读 [references/jq-research-rules.md](references/jq-research-rules.md) 获取标准研究约定
- 在继续导入更多聚宽文档前，先阅读 [references/jq-doc-ingest-guide.md](references/jq-doc-ingest-guide.md)
- 阅读 [references/JoinQuantAPI-学习摘要.md](references/JoinQuantAPI-学习摘要.md) 获取基于官方 PDF 的关键规则摘要
- 阅读 [references/jqdatasdk-学习摘要.md](references/jqdatasdk-学习摘要.md) 获取基于官方 GitHub 仓库的本地 SDK 接入摘要

## 备注

- 这个技能是流程和文档层，不直接等于执行器
- 真实执行可以交给 `jqdata-research` 或本地脚本
- 如果没有 `jqdata-research`，就停留在研究设计与分析说明模式，并明确告知限制
- 写盘中和跨日逻辑时，必须特别注意 `get_price` / `get_bars` / `history` / `attribute_history` 与复权逻辑
