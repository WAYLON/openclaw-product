# 股票目录

这个目录用于存放所有股票相关的 OpenClaw 产品包。

## 设计原则

- 股票领域只关心股票产品，不承载本体安装说明
- 通用安装、初始化、环境模板统一放在 `core/`
- 每个股票产品包都必须自带 `README.md`
- 每个股票产品包都必须至少有 `workspace/` 和 `skills/`

## 当前产品

- `openclaw-stock-pack/`
  - 通用股票研究包
  - 不包含聚宽专用能力
  - 适合一般股票研究、选股、新闻判断与外部能力补充

- `openclaw-stock-pack-langlang/`
  - LangLang 专用股票研究包
  - 包含聚宽 / JQData 研究能力
  - 用于 LangLang 机器上的定制化交付

## 安装入口

如果目标机器还没有 OpenClaw，请先阅读：

- `../core/安装-openclaw-本体.md`

如果目标机器已经有 OpenClaw，请按目标包分别阅读：

- `openclaw-stock-pack/README.md`
- `openclaw-stock-pack-langlang/README.md`

## 建议扩展方向

后续可以继续新增股票子产品，例如：

- `openclaw-trader-pack/`
- `openclaw-fund-pack/`
- `openclaw-news-pack/`

它们应与现有产品包平行存在。
