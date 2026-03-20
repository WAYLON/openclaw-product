# OpenMAIC 集成说明

来源：

- OpenMAIC 中文 README
- OpenClaw 集成章节
- GitHub 地址：`https://github.com/THU-MAIC/OpenMAIC/blob/main/README-zh.md#-openclaw-%E9%9B%86%E6%88%90`

## 已确认的关键信息

OpenMAIC 是一个多智能体互动课堂平台，可以把主题或文档转成：

- 幻灯片
- 测验
- 交互式模拟
- 项目制学习活动

并且 README 明确说明了 OpenClaw 集成方式：

1. 安装 `openmaic` skill
2. 选择托管模式或本地部署模式
3. 通过 OpenClaw 在聊天应用中直接发起课堂

## 对本仓库的意义

这说明 OpenMAIC 更适合被放在：

- `education/` 行业目录

而不是：

- `core/` 基础技能层

因为它本质上是教育行业能力，不是所有场景都需要的基础层。

## 本地部署前置要求

OpenMAIC README 中明确给出的环境要求包括：

- Node.js >= 20
- pnpm >= 10

并且至少需要一个可用的 LLM API Key。

## 技术交付建议

内部交付时建议按这三层理解：

1. `core`
   - 安装 OpenClaw 本体和基础技能
2. `education/openclaw-education-pack`
   - 安装教育行业规则与 OpenMAIC skill
3. 目标机器本地
   - 决定使用托管模式还是本地部署模式

## 不要混淆的点

- OpenMAIC 是教育行业能力，不是通用基础技能
- OpenMAIC 的 OpenClaw 集成，不等于已经完成 OpenMAIC 本地部署
- 如果目标机器没部署 OpenMAIC，本地只能做方案设计和接入说明，不能假装课堂已经成功生成
