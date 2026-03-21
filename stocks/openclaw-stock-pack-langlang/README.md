# OpenClaw 股票研究包 LangLang 专用版

这是面向 LangLang 的股票研究专用交付包。

它基于通用股票研究包扩展而来，但交付方式、工作区模板和客户占位信息按 LangLang 场景单独整理，便于你后续直接给 LangLang 安装和维护。

注意：

- 这个目录也是行业包，不是完整基础层
- 正确交付顺序是先装 `core/` 基础技能层，再装 LangLang 专用股票包

如果目标机器是从 0 开始部署，请先阅读：

- `../../core/README.md`
- `../../core/安装-openclaw-本体.md`
- `../../core/从零部署-openclaw-股票版.md`

## 这个专用版和通用版的区别

- 保留通用股票技能能力
- 工作区模板按 LangLang 单独占位
- 交付时优先作为 LangLang 的默认股票研究工作区
- 后续可以继续往这个目录内加入 LangLang 专属规则、脚本、字段映射和工作流

## LangLang 的真实工作流

LangLang 版的重点不是先给一支固定策略，而是先做“共性倒推”：

1. 先用 JQData / 聚宽输入特定条件
2. 反推某类股票在更早时点的共性
   例如：
   - “早盘 10:00 涨幅 5% 的股票，前一天下午 14:30 有什么共性”
   - 反推阶段允许同时开 3 条研究链路并行分析，再统一汇总交叉验证
3. 先输出研究结果和共性总结
4. 再根据这些共性生成聚宽回测代码
5. 你自己把代码粘贴到聚宽里跑回测
6. 如果你认可这个策略，再进入盘中选股阶段
7. 盘中选股阶段再调用 `qveris-official`，通过 `qveris.ai` 去调用同花顺工具能力

一句话：

- LangLang 版负责“研究共性 + 生成代码”
- 通用股票包负责“后续盘中选股与执行侧能力补充”

## 目录结构

- `workspace/`
  - `SOUL.md`：LangLang 使用时的股票研究人格模式
  - `AGENTS.md`：LangLang 股票任务路由规则
  - `TOOLS.md`：LangLang 机器上的工具与账户占位说明
  - `USER.md`：LangLang 用户偏好模板
  - `MEMORY.md`：LangLang 长期记忆模板
  - `INIT_PROMPT.md`：LangLang 初始化提示词
- `skills/`
  - `stock-research-core-langlang/`
  - `jqdata-playbook/`
  - `qveris-official/`
- `scripts/`
  - `check_jqdatasdk.py`
  - `check_jq_auth.py`
  - `check_min_get_price.py`

## 推荐安装方式

### 方案 A：只安装技能

适合 LangLang 机器已经有自己的 `workspace` 规则。

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh stocks/openclaw-stock-pack-langlang skills-only
```

### 方案 B：安装完整工作区

适合你希望 LangLang 直接采用这套股票研究工作区。

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh stocks/openclaw-stock-pack-langlang full
```

## LangLang 机器本地还要补什么

- OpenClaw 模型或 provider 配置
- 聚宽 / JQData 账号或环境变量
- `QVERIS_API_KEY`
- LangLang 本机脚本路径
- 是否通过 `qveris.ai` 调用同花顺工具能力

这些内容应只保留在 LangLang 机器本地。

## 建议安装后立刻验证

如果 LangLang 机器已准备好 Python 和聚宽环境，建议按顺序执行：

```bash
python3 stocks/openclaw-stock-pack-langlang/scripts/check_jqdatasdk.py
python3 stocks/openclaw-stock-pack-langlang/scripts/check_jq_auth.py
python3 stocks/openclaw-stock-pack-langlang/scripts/check_min_get_price.py
```

这样可以快速确认：

- SDK 是否可导入
- 聚宽认证是否通过
- 最小 `get_price` 链路是否可用

## LangLang 内置量化回测代码生成规范

当前 LangLang 专用版不是内置一支固定策略，而是内置了聚宽代码生成规范：

- `stocks/openclaw-stock-pack-langlang/skills/jqdata-playbook/references/jq-backtest-codegen-spec.md`

它的作用是：

- LangLang 在对话中直接生成完整的 JoinQuant / JQData 回测脚本
- 生成结果默认采用稳定的聚宽策略格式
- 便于你后续继续改写、调参和复用
- 在共性研究阶段，优先支持 3 条并行研究链路后再汇总生成代码

适合：

- 让 LangLang 先做共性研究，再现场写回测代码
- 把股票想法快速转成聚宽脚本
- 用统一格式沉淀 LangLang 自己的量化研究风格
