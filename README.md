# OpenClaw 交付仓库

这个仓库是给内部技术人员、实施人员、交付人员使用的。

它的用途不是给客户阅读，而是帮助技术人员：

- 安装 OpenClaw 本体
- 安装基础技能层
- 叠加行业包
- 叠加客户定制包
- 做本地验证和交付验收

## 本体安装前提

这个仓库不是 OpenClaw 本体安装源。

正确顺序是：

1. 先从 OpenClaw 官网或官方文档完成本体安装
2. 先完成 `~/.openclaw` 初始化
3. 再使用本仓库安装 `core`
4. 再安装行业包或客户专版

## 语言默认规则

这个仓库默认全部使用中文。

例外只包括：

- 命令
- 路径
- 环境变量
- 外部仓库名
- 外部技能名
- API 字段名

也就是说：

- 文档默认中文
- 工作区默认中文
- 输出模板默认中文
- 安装说明默认中文

不要再额外混入英文说明。

设计目标只有三个：

1. 技术人员知道先装什么、再装什么
2. 不同行业可以平行扩展，互不污染
3. 每个产品包都能独立交付，不依赖口头记忆

## 安装人员入口

内部技术安装人员优先看：

- `docs/技术交付SOP.md`
- `core/README.md`
- `core/安装-openclaw-本体.md`

## 仓库结构

- `core/`
  - OpenClaw 公共底座
  - 放本体安装、基础技能预设、初始化、通用环境变量模板、从 0 部署说明
- `stocks/`
  - 股票相关产品包
- `education/`
  - 教育相关产品包
- `media/`
  - 音视频与媒体发送相关产品包
- `docs/`
  - 项目结构、命名规范、交付规范
- `scripts/`
  - 安装脚本、检查脚本

## 技术人员怎么用这个仓库

### 情况 1：目标机器还没有 OpenClaw

顺序如下：

1. 阅读 `core/安装-openclaw-本体.md`
2. 先按 OpenClaw 官网 / 官方文档完成本体安装和 `~/.openclaw` 初始化
3. 安装 `core/skills` 对应的基础技能预设
4. 阅读具体行业目录下的产品包说明
5. 使用 `scripts/install-pack.sh` 安装目标包

### 情况 2：目标机器已经有 OpenClaw

顺序如下：

1. 进入目标行业目录
2. 阅读对应产品包 `README.md`
3. 使用 `scripts/install-pack.sh` 选择安装模式

## 当前已有产品

### 股票

- `stocks/openclaw-stock-pack/`
  - 股票研究行业包
  - 叠加在 core 基础技能之上

### 教育

- `education/openclaw-education-pack/`
  - 教育行业基础包
  - 当前以 OpenMAIC 集成为核心教育能力

### 媒体

- `media/openclaw-av-edit-pack/`
  - 音视频剪辑行业包
- `media/openclaw-media-delivery-pack/`
  - 媒体发送行业包

## 安装原则

所有交付默认分两层：

1. `core`
2. 行业包 / 客户包

含义：

- `core`
  - 安装 OpenClaw 本体
  - 安装基础技能预设
- 行业包 / 客户包
  - 安装行业工作区
  - 安装行业附加技能

这意味着：

- 这个仓库主要是交付侧使用
- 客户通常只会接触被安装后的 OpenClaw 环境
- 技术人员不应把整个仓库原样当作客户阅读材料发出去

每个产品包统一支持两种模式：

1. `skills-only`
2. `full`

含义：

- `skills-only`
  - 只安装技能
  - 不改客户现有 `workspace` 个性与规则
- `full`
  - 同时安装 `workspace + skills`
  - 适合客户愿意采用整套工作流

## 安全原则

- 不提交真实 API Key
- 不提交真实账号密码
- 不提交客户专属隐私信息
- 只提交模板、规则、脚本、说明文档

## 先看哪些文档

- `docs/项目结构设计.md`
- `docs/技术交付说明.md`
- `docs/产品包规范.md`
- `docs/默认运行规范.md`
- `docs/默认交付预设.md`
- `docs/初始化与人格塑造.md`
- `docs/接入飞书.md`
- `docs/接入微信.md`
- `docs/接入国外模型说明.md`
- `docs/迁移与常见坑说明.md`
- `docs/模型配置与切换.md`
- `docs/OpenClaw-Codex-OAuth修复说明.md`
- `docs/Codex安装排查说明.md`
- `core/README.md`

## 后续扩展方式

以后如果要新增行业，直接新增一个平行目录即可，例如：

- `finance/`
- `sales/`
- `operations/`

每个行业目录内部继续按“产品包”组织，不要把所有内容堆在根目录。
