# OpenClaw Parallel Agent Platform

这是一个基于 OpenClaw 的平行 Agent 内容模板与交付工程，不再只是概念骨架。

当前安装口径：
- OpenClaw 本体、Agent 注册、渠道绑定：优先使用官方命令
- `agent-platform`：仅用于模板生成、工作区同步和交付自动化，不替代官方安装流程

## 设计原则
- 不设业务总控 Agent
- 所有业务 Agent 平行独立
- 一个渠道实例只绑定一个 Agent
- 基础 skill 共享，灵魂、策略、记忆、文档独立
- 所有对外文档、Soul、Prompt、教程默认中文

## 目录说明

### 顶层关键文档
- [docs/architecture/平台总体架构与交付设计.md](/Users/waylon/Desktop/openclaw-product/docs/architecture/平台总体架构与交付设计.md)：总设计文档，讲架构原则、分层边界、8 个 Agent 的总体设计。
- [docs/guides/老师讲解总提纲.md](/Users/waylon/Desktop/openclaw-product/docs/guides/老师讲解总提纲.md)：给老师和实施同学的讲解顺序总提纲。

### 顶层目录作用
- `core/`
  - 放运行底座和公共能力。
  - 主要包括配置加载、注册表、运行时基础类、密钥初始化守卫等。
  - 这里解决“怎么跑”，不放业务人格和业务判断。

- `channels/`
  - 放渠道接入代码。
  - 当前是飞书、企微、钉钉、webhook、webchat、api 等 connector。
  - 它们只负责接入和转发，不负责判断该用哪个业务 Agent。

- `agents/`
  - 放 8 个专业 Agent 的源模板。
  - 每个 Agent 目录里都有：
    - `agent.yaml`
    - `soul.yaml`
    - `prompts/`
    - `skills/`
    - `policies/`
    - `knowledge/`
    - `docs/`
    - `examples/`
  - 这是“专业脑子”的主目录。

- `agents/<agent>/skills/`
  - 放这个 Agent 自己的全部技能。
  - 现在不再单独做 adapter 层，也不再保留共享技能目录抽象。
  - 每个 skill 都直接放在对应 Agent 里，方便客户理解、方便独立交付。

- `packages/`
  - 放最终交付包。
  - 每个专业包目录对应一个 Agent，里面有：
    - `README.md`
    - `config/install-manifest.yaml`
    - `docs/quickstart.md`
    - `docs/user-guide.md`
    - `docs/trainer-guide.md`
    - `docs/faq.md`
    - `docs/examples.md`
  - 这是给客户交付的正式资料入口。

- `installer/`
  - 放模板同步、导出、校验、打包相关脚本。
  - 这些脚本不替代官方 OpenClaw 安装，只负责：
    - 生成模板
    - 同步到本机 OpenClaw workspace
    - 校验包结构
    - 辅助交付

- `docs/`
  - 放平台级文档。
  - 主要包括：
    - `installation/` 安装与绑定教程
    - `architecture/` 架构设计说明
    - `guides/` 老师讲解资料
    - `delivery/` 交付、版本、实施说明

- `scripts/`
  - 放项目级检查脚本。
  - 当前主要是质量检查和全包校验，不承载业务逻辑。

- `.github/`
  - 放仓库协作与 CI 配置。
  - 主要包括 GitHub Actions 和 `CODEOWNERS`。

- `.platform/`
  - 放项目运行时状态和模板安装后的内部产物。
  - 例如：
    - 已安装 Agent 状态
    - 模板工作区
    - 运行状态文件
  - 这不是 OpenClaw 官方运行目录，而是本项目自己的模板/同步状态目录。

- `examples/`
  - 放平台级示例材料和演示脚本。
  - 适合实施、销售、老师讲解时快速调用。

## 企业级工程能力
- [pyproject.toml](/Users/waylon/Desktop/openclaw-product/pyproject.toml)：项目元数据与依赖声明
- [requirements.txt](/Users/waylon/Desktop/openclaw-product/requirements.txt)：运行依赖
- [Makefile](/Users/waylon/Desktop/openclaw-product/Makefile)：统一命令入口
- [scripts/quality_check.py](/Users/waylon/Desktop/openclaw-product/scripts/quality_check.py)：质量检查
- [scripts/check_all_packages.py](/Users/waylon/Desktop/openclaw-product/scripts/check_all_packages.py)：全包安装校验
- [.github/workflows/ci.yml](/Users/waylon/Desktop/openclaw-product/.github/workflows/ci.yml)：持续集成
- [CONTRIBUTING.md](/Users/waylon/Desktop/openclaw-product/CONTRIBUTING.md)：协作规范
- [企业级优化说明.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/企业级优化说明.md)：本轮工程化升级说明
- [版本发布流程.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本发布流程.md)：发布前检查流程

## 推荐命令
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw agents add stock-agent

make venv
make bootstrap
make doctor
make quality
make check-packages
make ci
```

推荐顺序：
1. 先用官方 `openclaw onboard`
2. 再用官方 `openclaw agents add / set-identity / bind`
3. 最后用本仓库把专业内容同步进各 Agent workspace
