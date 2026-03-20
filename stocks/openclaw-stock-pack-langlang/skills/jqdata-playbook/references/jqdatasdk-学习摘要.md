# jqdatasdk 学习摘要

本文档基于 JoinQuant 官方 GitHub 仓库整理，用于 LangLang 专用版中的本地 SDK 参考。

注意：

- 这份资料对应的是本地 `jqdatasdk` SDK
- 它和聚宽平台 / 策略 API 不是同一层东西
- 如果你要理解平台侧函数规则和复权 / 回测语义，还要结合 `JoinQuantAPI-学习摘要.md`

官方仓库：

- [JoinQuant/jqdatasdk](https://github.com/JoinQuant/jqdatasdk)

## 一、定位

官方仓库将 `jqdatasdk` 描述为：

- 简单易用的量化金融数据包
- 面向中国金融市场数据获取

从仓库 README 可以确认，它的定位是：

- 本地 Python 调用
- 面向研究与数据访问
- 适合在本地量化环境中接入聚宽数据

## 二、安装方式

官方仓库 README 给出的安装方法非常直接：

```bash
pip install jqdatasdk
pip install -U jqdatasdk
```

LangLang 版中的结论：

- 本地环境应优先确认 Python 与 pip 可用
- 如果客户机器没有 Python 环境，不要先谈 SDK 接入
- 安装完成后，再继续做认证与最小调用验证

## 三、最小使用方式

官方 README 展示的最小调用方式包括：

```python
import jqdatasdk
jqdatasdk.auth(username, password)
jqdatasdk.get_price("000001.XSHE", start_date="2017-01-01", end_date="2017-12-31")
```

从这段最小示例可以提炼出三个关键点：

1. 本地调用前先 `import jqdatasdk`
2. 使用官网账号密码做 `auth`
3. 最小可验证接口之一是 `get_price`

## 四、从仓库 README 提炼出的产品特征

仓库 README 强调了以下特点：

- 全平台兼容
- 本地化调用部署
- 覆盖中国市场多类数据
- 支持多频率量价数据
- 提供丰富 API 文档

对 LangLang 版的实际意义是：

- 它不是只适合云端策略平台
- 可以作为本地研究环境的数据接入层
- 适合配合本地脚本、研究工作流和 OpenClaw 技能一起使用

## 五、LangLang 版接入规则

在 LangLang 专用版中，使用 `jqdatasdk` 时默认遵守以下规则：

1. 先确认本机 Python 环境可用
2. 先确认账号认证能通过
3. 先用最小 `get_price` 调用做连通性验证
4. 再进入更复杂的选股、回测或研究逻辑
5. 不把“SDK 已安装”误认为“数据链路已可用”

## 六、建议的最小验证流程

建议按这个顺序验证：

1. `pip show jqdatasdk`
2. `python -c "import jqdatasdk; print('ok')"`
3. 执行认证
4. 调用一条最小 `get_price`

只有四步都通过，才能认为本地聚宽 SDK 已可用于研究工作流。

## 七、LangLang 版为什么要内置这个摘要

因为 LangLang 版不仅要“知道聚宽 API”，还要知道：

- 本地 SDK 怎么装
- 最小可用链路是什么
- 真实可用的判断标准是什么

所以这个摘要和 `JoinQuantAPI-学习摘要.md` 是互补关系：

- `JoinQuantAPI-学习摘要.md` 偏 API 规则与研究坑点
- `jqdatasdk-学习摘要.md` 偏本地 SDK 接入与最小调用链路
