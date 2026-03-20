# JoinQuant API 学习摘要

本文档基于聚宽官方 API PDF 文档整理，作为 LangLang 专用版中的聚宽使用摘要。

注意：

- 这份 PDF 更接近“聚宽平台 / 策略 API 文档”
- 它不是严格意义上的 `jqdatasdk` 本地 SDK 文档
- 因此它主要用于理解平台侧规则、回测 / 模拟盘逻辑、历史数据接口语义和常见坑点
- 本地 SDK 接入、认证和最小调用链路，应结合 `jqdatasdk-学习摘要.md` 一起看

官方 PDF 来源：

- [JoinQuant API 文档 PDF](https://cdn.joinquant.com/help/img/JoinQuantAPI.pdf)

## 一、这份文档适合解决什么问题

这份 PDF 更适合回答：

- `initialize`、定时函数、平台生命周期怎么理解
- 回测和模拟盘有哪些行为差异
- 基准、交易成本、复权、真实价格这些规则怎么理解
- `history` / `attribute_history` / `get_price` / `get_bars` 在研究中有哪些坑

它不适合单独回答：

- 本地 `jqdatasdk` 怎么安装
- 本地 SDK 怎么认证
- 本地 SDK 最小调用链路怎么验证

这些应查看：

- [jqdatasdk-学习摘要.md](jqdatasdk-学习摘要.md)

## 二、初始化与定时运行

### 1. `initialize(context)`

- 用于初始化策略
- 在模拟盘生命周期中只执行一次
- 模拟盘重启后不会再次执行
- 如果代码变化后需要修正状态，应使用 `after_code_changed`

结论：

- 不要误以为模拟盘每次启动都会重新执行 `initialize`
- 状态更新逻辑不能只寄托在 `initialize`

### 2. 定时函数

常见接口包括：

- `run_daily`
- `run_weekly`
- `run_monthly`

文档示例显示可以指定：

- `after_close`
- 固定时间如 `10:00`
- 分钟级场景中的 `every_bar`

结论：

- 盘中策略优先用定时函数明确节奏
- 不要把所有逻辑都塞进 `handle_data`

## 三、基准与交易成本

### 1. `set_benchmark`

官方文档说明：

- 默认基准为沪深 300
- 可通过 `set_benchmark(security)` 改为其他股票 / 指数 / ETF
- 这个函数只能在 `initialize` 中调用

结论：

- 每个回测都应显式设置基准
- 不要依赖默认值

### 2. `set_order_cost`

可以显式设置：

- 买入印花税
- 卖出印花税
- 买入佣金
- 卖出佣金
- 最低佣金

结论：

- 成本敏感策略必须显式建模
- 不要只看毛收益

## 四、历史数据接口重点

### 1. `get_price`

适合：

- 获取单只或多只标的历史行情
- 按日或按分钟取数
- 指定字段

文档版本显示：

- 单标的返回 DataFrame
- 多标的返回 Panel

结论：

- 文档版本较老，当前环境要再做实测
- 写脚本时不要死记旧返回结构

### 2. `get_bars`

适合：

- 按数量获取 bar 数据
- 支持不同周期
- 支持 `include_now`

结论：

- 盘中研究要明确当前 bar 是否纳入
- 默认先按“不要把未完成 bar 误算进信号”来设计

### 3. `history`

官方文档示例说明：

- 可取过去若干分钟或若干日的数据
- 分钟场景默认不包含当前分钟

结论：

- 写盘中逻辑时必须明确“是否包含当前分钟”
- 否则信号定义很容易和主观理解错位

### 4. `attribute_history`

与 `history` / `get_price` 一样，也会受到复权与当前日期视角影响。

## 五、复权与真实价格的核心坑

官方文档对 `set_option('use_real_price', True)` 的解释非常关键。

要点：

- 开启真实价格模式后，下单使用真实价格
- 但 `history` / `attribute_history` / `get_price` 返回的价格仍可能是基于“当前日期视角”的前复权价格
- 不同日期看到的前复权价格可能不同
- 因此不要跨日期缓存这些接口返回结果

结论：

- 不要跨日期缓存 `history` / `attribute_history` / `get_price`
- 否则跨日研究会产生错误理解

## 六、LangLang 版默认规则

在 LangLang 专用版中，使用聚宽时默认遵守：

1. 每个回测先明确写基准
2. 每个回测先明确写费用假设
3. 盘中逻辑明确是否包含当前 bar
4. 不跨日期缓存 `history` / `attribute_history` / `get_price`
5. 如果文档与当前环境行为不一致，以目标机器实测为准

## 七、为什么这份摘要重要

LangLang 版需要避免以下典型问题：

- 把默认基准当成理所当然
- 忽略交易成本
- 误用当前 bar
- 错把复权价格当交易价格
- 跨日期缓存历史结果

因此，这份摘要是 LangLang 版聚宽技能的基础约束说明。
