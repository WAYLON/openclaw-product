# LangLang 聚宽回测代码生成规范

这个文件不是固定策略成品，而是 LangLang 在对话中生成聚宽回测代码时必须遵守的格式规范。

目标：

- 让 LangLang 在用户提出回测需求时，直接生成完整的 JoinQuant / JQData 策略脚本
- 生成结果尽量贴近聚宽研究和回测的真实可运行格式
- 风格稳定，便于后续继续改造和复用

## 一、生成代码时必须满足的结构

生成的聚宽脚本，默认优先采用下面这种结构：

1. 文件头：
   - `# -*- coding: utf-8 -*-`
   - `import pandas as pd`
   - `import numpy as np`
   - `from jqdata import *`

2. 文件顶部先写策略说明注释：
   - 触发条件
   - 买入逻辑
   - 卖出逻辑
   - 输出内容

3. 必须包含 `initialize(context)`：
   - `set_benchmark(...)`
   - `set_option('use_real_price', True)`
   - 必要时 `set_option('order_volume_ratio', 1)`
   - `set_order_cost(...)`
   - 初始化 `g.xxx`
   - `run_daily(...)`

4. 核心逻辑函数拆开写：
   - 信号判定函数
   - 买入函数
   - 卖出函数
   - 统计输出函数

5. 最后要有统计输出逻辑：
   - 总体收益统计
   - 分组收益统计
   - 胜率
   - 盈亏比

## 二、默认代码风格

LangLang 生成代码时，默认遵守：

- 注释用中文
- 变量名、函数名、API 名保留 Python / 聚宽原生风格
- 条件拆开写，不要压成一大坨布尔表达式
- 尽量把每个条件命名成 `cond1`、`cond2` 或具名条件变量
- 统计逻辑单独封装，避免主流程过长

## 三、默认策略骨架

当用户要求“给我一份聚宽回测代码”时，如果没有特别指定框架，默认按下面骨架生成：

```python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from jqdata import *

'''
策略说明
1. ...
2. 买入逻辑
3. 卖出逻辑
4. 输出内容
'''

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    set_option('order_volume_ratio', 1)

    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        close_today_commission=0,
        min_commission=5
    ), type='stock')

    g.position_info = {}
    g.trade_records = []

    run_daily(buy_signal_xxx, time='14:30')
    run_daily(sell_signal_xxx, time='10:00')
    run_daily(report_result, time='after_close')


def buy_signal_xxx(context):
    pass


def sell_signal_xxx(context):
    pass


def report_group_stats(df, group_name):
    pass


def report_result(context):
    pass
```

## 四、生成时必须补全的要素

如果用户描述了策略条件，生成代码时必须把这些要素落实成代码，而不是停留在自然语言：

- 股票池
- 时间窗口
- 频率
- 条件定义
- 排除条件
- 买卖时点
- 统计维度

例如用户说：

- “14:30 买，次日 10:00 卖”
- “按上证 14:30 涨跌幅分组”

那生成代码时必须真的体现：

- `run_daily(..., time='14:30')`
- `run_daily(..., time='10:00')`
- 指数环境分组函数

## 五、不能偷懒的地方

LangLang 生成聚宽脚本时，不允许：

- 只给伪代码
- 只给函数名不写实现
- 把关键条件写成“这里自行补充”
- 假装聚宽 API 名称正确但实际乱写

如果某个 API 是否可用存在不确定性，必须在代码前或代码后明确说明风险点。

## 六、聚宽特有注意事项

生成代码时，必须默认注意：

- 盘中和跨日逻辑要特别谨慎
- `get_price` / `get_bars` / `history` / `attribute_history` 的使用口径要统一
- 复权逻辑要显式说明
- 成本建模不要省略
- `initialize` 和 `run_daily` 的时点要与策略口径一致

## 七、LangLang 专用要求

对于 LangLang，生成聚宽脚本时优先做到：

- 可以直接复制到聚宽研究环境中继续改
- 结构清楚，便于人工复核
- 注释足够让人快速懂逻辑
- 输出统计对复盘有用，不只是算一个总收益

## 八、什么时候要生成代码

当用户提出以下任务时，优先生成完整聚宽脚本：

- “给我一份聚宽回测代码”
- “把这个选股思路写成 JoinQuant 策略”
- “按这个规则生成可回测脚本”
- “把这个想法改成能在聚宽跑的代码”

## 九、什么时候不要直接生成代码

以下情况先补定义，再写代码：

- 买入条件不清楚
- 卖出条件不清楚
- 股票池不清楚
- 时间频率不清楚
- 输出目标不清楚

这时应该先问清楚或先把规则结构化，再生成脚本。
