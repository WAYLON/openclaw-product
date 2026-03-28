# 安装文档目录

这个目录用于正式交付 OpenClaw 官方安装、Agent 内容同步、渠道绑定、Key 初始化与单 Agent 安装示例。

## 文件清单
- [按需安装机器人教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/按需安装机器人教程.md)
- [8个机器人完整安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/8个机器人完整安装教程.md)
- [平台安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/平台安装教程.md)
- [agent安装教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/agent安装教程.md)
- [渠道绑定教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/渠道绑定教程.md)
- [OpenClaw-本地实操安装沉淀.md](/Users/waylon/Desktop/openclaw-product/docs/installation/OpenClaw-本地实操安装沉淀.md)
- [8个Agent-渠道绑定与模型分配总表.md](/Users/waylon/Desktop/openclaw-product/docs/installation/8个Agent-渠道绑定与模型分配总表.md)
- [按Agent分配模型教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/按Agent分配模型教程.md)
- [key初始化教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/key初始化教程.md)
- [CLI命令设计.md](/Users/waylon/Desktop/openclaw-product/docs/installation/CLI命令设计.md)
- [education-agent-安装示例.md](/Users/waylon/Desktop/openclaw-product/docs/installation/examples/education-agent-安装示例.md)
- [stock-agent-安装示例.md](/Users/waylon/Desktop/openclaw-product/docs/installation/examples/stock-agent-安装示例.md)
- [photo-polisher-安装示例.md](/Users/waylon/Desktop/openclaw-product/docs/installation/examples/photo-polisher-安装示例.md)

## 建议阅读顺序
1. 按需安装机器人教程
2. 平台安装教程
3. agent 安装教程
4. 渠道绑定教程
5. 8个机器人完整安装教程
6. OpenClaw-本地实操安装沉淀
7. 8 个 Agent 的渠道绑定与模型分配总表
8. CLI 命令设计
9. 按 Agent 分配模型教程
10. key 初始化教程
11. 对应 Agent 的完整安装示例

## 说明
- OpenClaw 本体安装、Agent 注册、渠道绑定：优先走官方命令
- `agent-platform`：定位为模板生成、工作区同步、交付自动化补充
- 客户不需要 8 个机器人全装时，请优先阅读 [按需安装机器人教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/按需安装机器人教程.md)
- 不再单独维护“渠道配置文件夹”
- 渠道代码层 `channels/` 仍然保留，它是接入适配层，不是配置目录
- 项目侧完成模板安装后，可使用 `./agent-platform openclaw export <agent>` 把工作区模板同步到本机 OpenClaw
- 如果按今天的本地实操方式交付，请优先阅读 [OpenClaw-本地实操安装沉淀.md](/Users/waylon/Desktop/openclaw-product/docs/installation/OpenClaw-本地实操安装沉淀.md)
- 如果一个 Agent 要接一个独立大模型，请优先阅读 [按Agent分配模型教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/按Agent分配模型教程.md)
