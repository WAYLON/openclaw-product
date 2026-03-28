# CLI 命令设计

> 当前仓库已提供一个可执行 MVP CLI：[`agent-platform`](/Users/waylon/Desktop/openclaw-product/agent-platform)
>
> 口径说明：
> - **OpenClaw 本体安装、Agent 注册、渠道绑定**：优先使用官方命令，例如 `openclaw onboard`、`openclaw agents add`、`openclaw agents bind`
> - **本文件描述的 `agent-platform`**：用于项目模板生成、工作区同步、密钥写入与辅助自动化，不替代 OpenClaw 官方主流程

## 1. 平台命令

### 初始化平台

```bash
./agent-platform init
```

### 启动平台

```bash
./agent-platform start
```

### 查看状态

```bash
./agent-platform status
```

### 自检

```bash
./agent-platform doctor
```

## 2. Agent 命令

### 安装 Agent

```bash
./agent-platform agent install <agent>
```

示例：

```bash
./agent-platform agent install education-agent
```

### 启用 Agent

```bash
./agent-platform agent enable <agent>
```

### 停用 Agent

```bash
./agent-platform agent disable <agent>
```

### 查看已安装 Agent

```bash
./agent-platform agent list
```

### 卸载 Agent

```bash
./agent-platform agent uninstall <agent>
```

### 同步到本机 OpenClaw 多 Agent 目录

```bash
./agent-platform openclaw export <agent>
```

示例：

```bash
./agent-platform openclaw export education-agent
```

## 3. 密钥命令

### 设置密钥

```bash
./agent-platform secret set <target> <key> --value "<value>" --scope <scope>
```

示例：

```bash
./agent-platform secret set education-agent openmaic_api_key --value "your-key" --scope agent
```

### 查看密钥

```bash
./agent-platform secret list <target> --scope <scope>
```

### 删除密钥

```bash
./agent-platform secret remove <target> <key> --scope <scope>
```

## 4. 建议命令组合

### 新平台首次安装

```bash
./agent-platform init
./agent-platform start
./agent-platform doctor
```

### 安装并同步一个教育 Agent

```bash
./agent-platform agent install education-agent
./agent-platform openclaw export education-agent
./agent-platform secret set education-agent openmaic_api_key --value "your-key" --scope agent
```

### 查看当前项目状态

```bash
./agent-platform agent list
./agent-platform status
```

### 导出到真实 OpenClaw

```bash
./agent-platform openclaw export education-agent
```

## 5. 当前命令边界

当前 CLI 已经可执行，但它是平台安装与交付 MVP：
- 能初始化平台状态
- 能安装 / 启停 / 卸载 Agent
- 能写入密钥
- 能同步 workspace 模板到本机 OpenClaw 多 Agent 目录
- 能做平台自检

当前还不是完整运行时：
- 不负责真正启动飞书 / 企微 / 钉钉消息监听服务
- 不负责真正调用外部 CRM / OCR / CMS / 签署系统
- 不负责真实业务执行链路

这部分后续会在真实运行时层继续补。
