# 安装文档目录

这个目录只保留当前首发 7 个角色所需的安装与交付文档。

当前口径：

- `main`：默认入口 / 技能管理员
- `education-agent`
- `stock-agent`
- `loan-agent`
- `social-media-agent`
- `news-agent`
- `sales-agent`

当前默认模型：

- `local-proxy / gpt-5.4`

当前飞书口径：

- `7` 个 bot 对 `7` 个 Agent

## 文件清单

- [平台安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/平台安装教程.md)
- [重装与清理路径.md](/Users/waylon/Desktop/openclaw-product/docs/installation/重装与清理路径.md)
- [新机器安装路径.md](/Users/waylon/Desktop/openclaw-product/docs/installation/新机器安装路径.md)
- [老机器升级路径.md](/Users/waylon/Desktop/openclaw-product/docs/installation/老机器升级路径.md)
- [7个Agent完整安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/7个Agent完整安装教程.md)
- [7个Agent-渠道绑定与模型分配总表.md](/Users/waylon/Desktop/openclaw-product/docs/installation/7个Agent-渠道绑定与模型分配总表.md)
- [实际运行基线与重写说明.md](/Users/waylon/Desktop/openclaw-product/docs/installation/实际运行基线与重写说明.md)
- [../guides/Agent官方核心文件说明.md](/Users/waylon/Desktop/openclaw-product/docs/guides/Agent官方核心文件说明.md)
- [技能加载与会话可见性说明.md](/Users/waylon/Desktop/openclaw-product/docs/installation/技能加载与会话可见性说明.md)
- [key初始化教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/key初始化教程.md)
- [记忆插件安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/记忆插件安装教程.md)
- [CLI命令设计.md](/Users/waylon/Desktop/openclaw-product/docs/installation/CLI命令设计.md)
- [education-agent-安装示例.md](/Users/waylon/Desktop/openclaw-product/docs/installation/examples/education-agent-安装示例.md)
- [stock-agent-安装示例.md](/Users/waylon/Desktop/openclaw-product/docs/installation/examples/stock-agent-安装示例.md)
- [专有技能新增规范.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/专有技能新增规范.md)
- [版本迁移模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本迁移模板.md)
- [回滚模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/回滚模板.md)

## 建议阅读顺序

1. 平台安装教程
2. 重装与清理路径 / 新机器安装路径 / 老机器升级路径
3. 7个Agent完整安装教程
4. 7个Agent-渠道绑定与模型分配总表
5. 实际运行基线与重写说明
6. key初始化教程
7. 对应 Agent 的安装示例
8. 专有技能新增规范 / 迁移模板 / 回滚模板

## 说明

- OpenClaw 本体安装、Agent 创建、渠道绑定：优先走官方命令
- OpenClaw CLI / App 默认安装最新稳定版
- 飞书插件默认使用 `npx -y @larksuite/openclaw-lark install`
- `agent-platform`：只负责模板生成、同步与交付辅助
- 后台运行时 key：统一写 LaunchAgent
- 配置型 skill key：写 `openclaw.json`
- 交付结构检查：`make delivery-check`
- 本机最小验收：`./agent-platform acceptance --full --report <path>`
