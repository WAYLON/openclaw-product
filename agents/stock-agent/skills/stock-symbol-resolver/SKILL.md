# stock-symbol-resolver

## 作用
把中文简称、代码、市场后缀统一解析为标准股票标识。

## 来源
TradingAgents-AShare / akshare-stock / Ashare

## 启用建议
建议首发

## 风险等级
中

## 是否需要 Key
否

## 运行要求
无

## 当前组织方式
该 skill 直接放在当前 Agent 的 `skills/` 目录下，不再通过 任何中间封装层引用。

## 使用原则
1. 只服务当前 Agent 的专业目标。
2. 首次命中需要 Key 的能力时，先给中文初始化提示。
3. 输出默认中文，便于交付和讲解。
