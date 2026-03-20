# 安装 OpenClaw 本体

本文档说明如何在一台新机器上安装 OpenClaw 本体，并初始化基础目录。

重要前提：

- OpenClaw 本体应优先从官网或官方文档安装
- 本文档不是替代官方安装源
- 本文档用于帮助安装人员在官方安装完成后做检查与衔接

这一步是所有业务包的前置条件。  
无论后面要装股票版、教育版还是其他领域版本，都要先完成这里的步骤。

## 目标

完成后，目标机器应具备：

- 可正常调用的 OpenClaw 命令
- 已初始化的 `~/.openclaw`
- 基础工作区目录
- 可继续导入业务产品包的环境

## 第 1 步：确认基础命令

先检查目标机器是否具备以下能力：

- `git`
- `node`
- `npm`

执行：

```bash
git --version
node -v
npm -v
```

如果这些命令不可用，先补齐基础开发环境。

## 第 2 步：安装 OpenClaw

按 OpenClaw 官网 / 官方文档方式完成安装。

安装完成后，请确认目标机器可以执行：

```bash
openclaw --help
```

如果这一步失败，先不要继续导入任何产品包。

## 第 3 步：初始化 OpenClaw

目标是让系统生成基础目录：

```text
~/.openclaw/
  openclaw.json
  workspace/
  skills/
```

如目标机器尚未初始化，请先完成 OpenClaw 的初始化流程。

完成后检查：

```bash
ls ~/.openclaw
```

至少应看到：

- `openclaw.json`
- `workspace`
- `skills`

## 第 4 步：补齐基础模型配置

OpenClaw 本体安装完成后，还需要目标机器本地配置自己的模型或 provider。

这一步至少要保证：

- 有可用的模型提供方
- 有可用的 API Key 或授权方式
- OpenClaw 可以正常启动会话

## 第 5 步：基础健康检查

执行：

```bash
openclaw skills check
```

这一步的目标不是要求所有技能都 ready，而是确认：

- OpenClaw 命令可用
- 技能系统可以扫描
- `~/.openclaw` 结构没有问题

## 完成标准

只有当下面三件事都成立时，才算完成了本体安装：

1. `openclaw --help` 可正常执行
2. `~/.openclaw` 已生成
3. `openclaw skills check` 可运行

## 下一步

完成本体安装后，再根据业务场景继续：

- 股票场景：阅读 `从零部署-openclaw-股票版.md`
- 教育场景：后续阅读教育目录对应文档
