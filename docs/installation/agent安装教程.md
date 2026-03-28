# Agent 安装教程

> 目标：先用官方 `openclaw agents` 完成 Agent 注册，再用本仓库把专业内容同步进去。  
> 当前推荐口径：**官方 `openclaw agents` 命令优先**，`agent-platform` 只负责模板生成、工作区同步和交付辅助。
>
> 如果客户只需要其中 1 到 3 个机器人，请先看：
> [按需安装机器人教程.md](/Users/waylon/Desktop/openclaw-product/docs/installation/按需安装机器人教程.md)

## 1. 安装某个 Agent

### 1.1 官方主流程

例如安装教育 Agent：

```bash
openclaw agents add education-agent
```

再补 identity：

```bash
openclaw agents set-identity \
  --agent education-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent/IDENTITY.md
```

### 1.2 项目模板补充方式

例如安装教育 Agent：

```bash
cd ~/Desktop/openclaw-product
./agent-platform agent install education-agent
```

再例如安装股票 Agent：

```bash
./agent-platform agent install stock-agent
```

安装成功后，会写入：

```text
.platform/agents/<agent>.json
.platform/workspaces/<agent>/
```

其中 `.platform/workspaces/<agent>/` 会生成更贴近 OpenClaw 原生的工作区模板，至少包含：

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `MEMORY.md`
- `skills/`
- `prompts/`
- `knowledge/`
- `docs/`
- `examples/`
- `delivery-package/`

## 2. 项目侧启用某个 Agent 模板

```bash
./agent-platform agent enable education-agent
```

## 3. 项目侧停用某个 Agent 模板

```bash
./agent-platform agent disable education-agent
```

## 4. 查看项目侧已安装模板

```bash
./agent-platform agent list
```

预期输出示例：

```text
education-agent  enabled  /你的路径/openclaw-product/.platform/workspaces/education-agent
stock-agent  enabled  /你的路径/openclaw-product/.platform/workspaces/stock-agent
photo-polisher  disabled  /你的路径/openclaw-product/.platform/workspaces/photo-polisher
```

## 5. 卸载项目侧模板

```bash
./agent-platform agent uninstall education-agent
```

说明：
- 当前 CLI 的卸载只会删除项目侧模板状态：
  - `.platform/agents/education-agent.json`
  - `.platform/workspaces/education-agent/`
- 不会删除仓库里 `agents/education-agent` 和 `packages/education-agent` 源文件
- 也不会调用官方 `openclaw agents delete`

## 6. 检查 Agent 是否安装成功

### 6.1 检查状态文件

```bash
cat .platform/agents/education-agent.json
```

重点看：
- `installed = true`
- `workspace_dir` 是否存在
- `install_mode = openclaw-workspace-template`

### 6.2 检查工作区模板

```bash
find .platform/workspaces/education-agent -maxdepth 2 -type f | sort
```

### 6.3 检查交付包是否存在

```bash
find packages/education-agent -maxdepth 2 -type f | sort
```

### 6.4 检查源目录配置是否存在

```bash
find agents/education-agent -maxdepth 2 -type f | sort
```

## 7. 典型安装流程

### 7.1 官方优先推荐

```bash
openclaw agents add education-agent
openclaw agents set-identity \
  --agent education-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent/IDENTITY.md
openclaw agents list
```

### 7.2 项目模板补充方式

```bash
./agent-platform init
./agent-platform agent install education-agent
./agent-platform agent list
find .platform/workspaces/education-agent -maxdepth 1 -type f | sort
```

### 7.3 同步到本机真实 OpenClaw

```bash
./agent-platform openclaw export education-agent
openclaw agents set-identity \
  --agent education-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent/IDENTITY.md
```

## 8. 常见报错排查

### 报错：`未找到 Agent 包`

检查：

```bash
ls packages
ls agents
```

### 报错：`Agent 未安装`

说明你先执行了 `enable/disable/uninstall`，但没有先 `install`。

### Agent 装了但不想立刻用

执行：

```bash
./agent-platform agent disable <agent>
```

### 安装后发现模板工作区内容不对

重新安装即可覆盖工作区模板：

```bash
./agent-platform agent install <agent>
```

## 9. 推荐操作顺序

1. 优先执行官方 `openclaw agents add`
2. 再补 `openclaw agents set-identity`
3. 再执行 `./agent-platform agent install`
4. 再执行 `./agent-platform openclaw export`
5. 绑定渠道
6. 配置必要 Key
7. 做第一次中文问答测试
