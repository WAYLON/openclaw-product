# 从零部署 OpenClaw 股票版

本文档用于指导客户在一台全新的机器上，从 0 开始部署 OpenClaw，并导入本仓库中的股票研究产品包。

开始前，请先完成：

- `安装-openclaw-本体.md`

## 目标

完成后，目标机器应具备：

- 一个可正常工作的 OpenClaw 环境
- 已初始化的 `~/.openclaw`
- 已安装 core 基础技能预设
- 已导入的股票研究工作区和技能
- 已完成必要的本地密钥与账号配置

## 第 1 步：确认 OpenClaw 本体已安装并初始化

目标机器至少应满足：

- `openclaw --help` 可正常执行
- `~/.openclaw/openclaw.json` 存在
- `~/.openclaw/workspace/` 存在
- `~/.openclaw/skills/` 存在

执行：

```bash
openclaw --help
ls ~/.openclaw
```

如果还没做到这一步，请先回到 `安装-openclaw-本体.md`。

## 第 2 步：克隆产品仓库

在目标机器执行：

```bash
git clone git@github.com:WAYLON/openclaw-product.git
cd openclaw-product
```

如果目标机器不能使用 SSH，也可以改用 HTTPS 地址。

## 第 3 步：安装 core 基础技能层

在目标机器执行：

```bash
./core/scripts/install-core-skills.sh
./core/scripts/check-core-skills.sh
```

这一步安装的是所有行业都共用的基础技能，而不是股票专属技能。

## 第 4 步：决定导入方式

股票包支持两种方式：

### 方式 A：只导入技能

适用于：

- 客户已经有自己的 `SOUL.md`
- 客户已经有自己的 `AGENTS.md`
- 你只想给对方增加股票研究能力

执行：

```bash
cp -R stocks/openclaw-stock-pack/skills/. ~/.openclaw/skills/
openclaw skills check
```

### 方式 B：导入技能和工作区

适用于：

- 客户愿意采用这套股票研究工作流
- 你希望对方的工作区里带有股票研究模式和路由规则

先备份：

```bash
cp -R ~/.openclaw/workspace ~/.openclaw/workspace.bak.$(date +%Y%m%d_%H%M%S)
cp -R ~/.openclaw/skills ~/.openclaw/skills.bak.$(date +%Y%m%d_%H%M%S)
```

再导入：

```bash
cp -R stocks/openclaw-stock-pack/workspace/. ~/.openclaw/workspace/
cp -R stocks/openclaw-stock-pack/skills/. ~/.openclaw/skills/
openclaw skills check
```

## 第 5 步：补齐本地密钥和账号

导入完产品包，不代表已经具备真实执行能力。以下内容必须在目标机器本地自行补齐：

- OpenClaw 所需模型或 provider 配置
- 聚宽 / JQData 账号与环境变量
- `QVERIS_API_KEY`
- 本机脚本路径
- 同花顺本地接入方式

建议参考：

- `env.example`
- `../stocks/openclaw-stock-pack/workspace/TOOLS.md`

## 第 6 步：确认依赖能力

这个股票包叠加以下能力时效果最佳：

- core 基础技能预设
- `jqdata-research`
- `qveris-official`

其中：

- `qveris-official` 属于股票行业附加技能，已在本包中提供
- `jqdata-research` 需要目标机器另行安装或已有同等能力

如果没有 `jqdata-research`，系统仍可做研究设计和分析说明，但不能假装已跑过历史数据。

## 第 7 步：做安装检查

执行：

```bash
openclaw skills check
```

至少应确认：

- core 基础技能已按预期安装
- `stock-research-core` 已被识别
- `qveris-official` 已被识别

如果你部署的是 LangLang 版，还要确认：

- `jqdata-playbook` 已被识别

如果你还额外安装了 `jqdata-research`，也要确认它处于可用状态。

## 第 8 步：检查工作区文件

如果你采用的是“完整导入”模式，再检查这些文件是否已经进入目标机器：

```bash
ls ~/.openclaw/workspace
```

应至少看到：

- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- `USER.md`
- `MEMORY.md`

## 第 9 步：做一次最小验证

可以用下面这类问题做人工验证：

- “帮我从股票研究角度看一下这套工作区现在是干什么的”
- “帮我设计一个 A 股放量突破的研究框架”
- “如果我没有 jqdata-research，你现在能做什么，不能做什么”

验证重点：

- 是否进入股票研究模式
- 是否能正确说明路由规则
- 是否能诚实说明缺失依赖

## 第 10 步：交付给客户前的安全检查

提交或打包前，请确认没有带出这些内容：

- API Key
- 聚宽账号密码
- 本地路径中的隐私信息
- 客户专属敏感资料
- 含真实密钥的 `openclaw.json`

## 常用命令汇总

### 克隆仓库

```bash
git clone git@github.com:WAYLON/openclaw-product.git
cd openclaw-product
```

### 安装基础技能

```bash
./core/scripts/install-core-skills.sh
./core/scripts/check-core-skills.sh
```

### 只导入技能

```bash
cp -R stocks/openclaw-stock-pack/skills/. ~/.openclaw/skills/
openclaw skills check
```

### 完整导入

```bash
cp -R stocks/openclaw-stock-pack/workspace/. ~/.openclaw/workspace/
cp -R stocks/openclaw-stock-pack/skills/. ~/.openclaw/skills/
openclaw skills check
```

### 备份现有配置

```bash
cp -R ~/.openclaw/workspace ~/.openclaw/workspace.bak.$(date +%Y%m%d_%H%M%S)
cp -R ~/.openclaw/skills ~/.openclaw/skills.bak.$(date +%Y%m%d_%H%M%S)
```

## 一句话总结

从 0 部署时，顺序必须是：

1. 安装 OpenClaw 本体
2. 初始化 `~/.openclaw`
3. 克隆本仓库
4. 安装 core 基础技能并导入股票产品包
5. 填写本地密钥和账号
6. 运行检查
