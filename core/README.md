# OpenClaw 公共底座

这个目录用于存放所有业务领域都会共用的 OpenClaw 基础安装、基础技能预设和初始化资料。

它不属于股票，也不属于教育，而是所有产品包都要依赖的公共层。

注意：

- OpenClaw 本体仍应先从官方渠道安装
- `core/` 只负责官方本体安装完成后的交付层动作
- 不要把 `core/` 误当成本体安装包

## 目录内容

- `安装-openclaw-本体.md`
  - 安装 OpenClaw 本体并初始化 `~/.openclaw` 的通用步骤
- `env.example`
  - 通用环境变量占位模板
- `skills/`
  - 默认基础技能层
- `scripts/install-core-skills.sh`
  - 按固定清单安装基础技能
- `scripts/check-core-skills.sh`
  - 检查基础技能预设
- `从零部署-openclaw-股票版.md`
  - 在完成本体安装后，继续部署股票产品包的完整步骤

## 使用顺序

如果客户机器上还没有 OpenClaw，请按这个顺序操作：

1. 阅读 `安装-openclaw-本体.md`
2. 先按 OpenClaw 官网 / 官方文档完成本体安装和初始化
3. 执行 `core/scripts/install-core-skills.sh`
4. 再根据业务场景选择具体产品包
5. 如果是股票场景，继续阅读 `从零部署-openclaw-股票版.md`

## 设计原则

- 本体安装与业务包分离
- 基础技能与行业技能分离
- 通用依赖集中管理
- 各业务目录只关心自己的能力和工作流
