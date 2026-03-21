# 技术交付 SOP

这份 SOP 面向内部技术安装人员，目标是把 OpenClaw 从本体安装、基础层部署、行业包安装、账号配置、最小验证到交付验收串成一套固定流程。

## 一、适用范围

适用于：

- 通用股票版
- LangLang 股票专用版
- 教育版
- 媒体类产品包

不适用于：

- 直接替代 OpenClaw 官方安装
- 跳过基础层直接发客户运行

## 二、总原则

1. 先装 OpenClaw 官方本体
2. 再装 `core/` 基础层
3. 再装行业包
4. 再补账号、密码、API Key、环境变量
5. 再做最小验证
6. 最后才算交付完成

## 三、标准交付顺序

### 第 1 步：确认客户机器前置条件

至少确认：

- `git`
- `node`
- `npm`
- `python3`
- `openclaw`

可直接检查：

```bash
git --version
node --version
npm --version
python3 --version
openclaw --help
```

### 第 2 步：先按官方方式安装 OpenClaw 本体

不要用本仓库代替本体安装。

先阅读：

- `core/安装-openclaw-本体.md`

完成后至少确认：

- `~/.openclaw` 已生成
- `~/.openclaw/openclaw.json` 存在
- `~/.openclaw/workspace/` 存在
- `~/.openclaw/skills/` 存在

### 第 3 步：安装 core 基础层

执行：

```bash
./core/scripts/install-core-skills.sh
./core/scripts/check-core-skills.sh
```

注意：

- `find-skills` 属于内部预装能力，不代表客户正式运行态默认启用
- 必装项应以 `check-core-skills.sh` 的结果为准

### 第 4 步：选择行业包

#### 通用股票版

适合：

- 盘中选股
- 盘中筛选
- 策略已认可后的执行侧工作流
- 通过 `qveris.ai` 调用同花顺工具能力

安装：

```bash
./scripts/install-pack.sh stocks/openclaw-stock-pack full
```

或：

```bash
./scripts/install-pack.sh stocks/openclaw-stock-pack skills-only
```

#### LangLang 股票专用版

适合：

- 先做 JQData 共性倒推
- 同时开 3 条研究链路并行分析
- 输出研究结论后生成 JoinQuant / JQData 回测代码
- 用户自己把代码粘贴去聚宽回测

安装：

```bash
./scripts/install-pack.sh stocks/openclaw-stock-pack-langlang full
```

或：

```bash
./scripts/install-pack.sh stocks/openclaw-stock-pack-langlang skills-only
```

注意：

- LangLang 版的总控 skill 名称是 `stock-research-core-langlang`
- 通用股票版的总控 skill 名称是 `stock-research-core`
- 两者不再共用同名目录，避免后装覆盖前装

### 第 5 步：补凭证和本地配置

不要等执行失败才补。

至少确认：

- 模型或 provider 配置
- `QVERIS_API_KEY`
- 聚宽环境变量（如适用）
- 本地脚本路径
- 代理或网络条件（如适用）

LangLang 版额外确认：

- `JQ_USER`
- `JQ_PASS`
- `jqdatasdk`
- 聚宽账号可认证

### 第 6 步：执行最小验证

通用股票版至少确认：

- `stock-research-core` 已识别
- `qveris-official` 已识别

LangLang 版至少确认：

- `stock-research-core-langlang` 已识别
- `jqdata-playbook` 已识别
- `qveris-official` 已识别

执行：

```bash
openclaw skills check
```

LangLang 版还要执行：

```bash
python3 stocks/openclaw-stock-pack-langlang/scripts/check_jqdatasdk.py
python3 stocks/openclaw-stock-pack-langlang/scripts/check_jq_auth.py
python3 stocks/openclaw-stock-pack-langlang/scripts/check_min_get_price.py
```

### 第 7 步：做业务语义验证

#### 通用股票版问法

- “你现在是做什么的”
- “盘中选股应该优先用什么能力”
- “如果策略已经认可，你会怎么做盘中筛选”

#### LangLang 版问法

- “早盘 10:00 涨幅 5% 的股票，前一天下午 14:30 有什么共性”
- “你应该先做什么，再做什么”
- “请按聚宽格式为这个研究结果生成回测代码”

期望行为：

- LangLang 先研究，再生成代码
- 通用股票版先走执行侧与盘中筛选
- 两者都不能假装已经跑过不存在的数据链路

### 第 8 步：初始化人格

安装完成后，把对应行业包的 `workspace/INIT_PROMPT.md` 发给龙虾执行初始化。

重点观察：

- 是否主动提醒缺少的凭证和依赖
- 是否默认中文输出
- 是否能正确说明自己的工作模式

### 第 9 步：安全检查

交付前确认：

- 没有把真实密钥提交进仓库
- 没有把客户账号密码留在示例文件中
- 没有默认放开高危外部安装能力
- 没有把 OpenClaw 直接暴露到公网

### 第 10 步：交付完成标准

下面 4 条同时满足，才算交付完成：

1. 能安装
2. 能识别技能
3. 能跑最小验证
4. 能正确说出自己的工作模式和边界

## 四、LangLang 股票版专项 SOP

LangLang 的固定顺序必须是：

1. 用户给结果条件
2. LangLang 把结果条件改写成研究问题
3. LangLang 同时开 3 条研究链路
4. LangLang 汇总共性和冲突项
5. LangLang 生成 JoinQuant / JQData 回测代码
6. 用户自己粘贴到聚宽回测
7. 用户认可策略后，再进入通用股票包的盘中选股阶段

三条研究链路优先建议：

- 不同时间窗口
- 不同过滤条件
- 不同市场环境分组

注意：

- LangLang 不是盘中执行器
- 它首先是研究和代码生成器
- 盘中执行和实时筛选主要交给 `qveris-official`

## 五、常见踩坑

### 1. 只装行业包，没装 core

结果：

- 技能不全
- 浏览器、搜索、定时等基础能力缺失

### 2. 把 LangLang 当成直接盘中选股器

结果：

- 研究阶段和执行阶段混在一起
- 很容易跳过回测验证

### 3. `jqdatasdk` 已安装，但没配 `JQ_USER / JQ_PASS`

结果：

- 导入成功
- 认证失败

### 4. `QVERIS_API_KEY` 没配

结果：

- `qveris-official` 可识别
- 但真实调用能力打不通

### 5. 技能被识别，不等于能力已打通

结果：

- 安装人员误判为“已经可用”
- 实际运行时才发现缺账号、缺 Key、缺环境

## 六、一句话总结

这套 SOP 的核心不是“把文件拷过去”，而是：

先装官方本体，再装基础层，再装行业包，再补凭证，再验收能力。
