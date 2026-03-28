# education-agent 完整安装示例

> 当前推荐口径：**官方 OpenClaw 命令优先**。本示例中，`openclaw` 负责本体安装、Agent 注册与渠道绑定，`agent-platform` 只负责项目模板生成、工作区同步与交付自动化。

## 1. 前置条件

先按官方方式安装 OpenClaw：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw --version
openclaw status
```

预期结果：
- `openclaw --version` 有输出
- `openclaw status` 能看到 gateway 已启动

## 2. 注册 education-agent

先用官方命令注册 Agent：

```bash
openclaw agents add education-agent
openclaw agents list
```

预期看到：

```text
education-agent
```

## 3. 初始化项目模板状态

```bash
cd ~/Desktop/openclaw-product
./agent-platform init
./agent-platform start
./agent-platform doctor
```

## 4. 生成 education-agent 模板并导出

```bash
./agent-platform agent install education-agent
./agent-platform openclaw export education-agent
./agent-platform agent list
```

再检查项目内工作区模板：

```bash
find .platform/workspaces/education-agent -maxdepth 2 -type f | sort
```

## 5. 设置本机 OpenClaw 身份文件

```bash
openclaw agents set-identity \
  --agent education-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent/IDENTITY.md
```

## 6. 绑定飞书实例

如果飞书机器人已创建完成，优先用官方命令绑定：

```bash
openclaw agents bind --agent education-agent --channel feishu --account educationbot
openclaw agents bindings --json
```

## 7. 配置教育相关 Key

### OpenMAIC

```bash
./agent-platform secret set education-agent openmaic_api_key --value "replace-me" --scope agent
```

### OpenMAIC 语音能力

```bash
./agent-platform secret set education-agent openmaic_asr_api_key --value "replace-me" --scope agent
./agent-platform secret set education-agent openmaic_tts_api_key --value "replace-me" --scope agent
```

### Quizzle

```bash
./agent-platform secret set education-agent quizzle_api_key --value "replace-me" --scope agent
```

### Moodle

```bash
./agent-platform secret set education-agent moodle_token --value "replace-me" --scope agent
```

查看已配置：

```bash
./agent-platform secret list education-agent --scope agent
```

## 8. 检查交付文档

```bash
find packages/education-agent/docs -maxdepth 1 -type f | sort
find agents/education-agent/docs -maxdepth 1 -type f | sort
find .platform/workspaces/education-agent/docs -maxdepth 1 -type f | sort
```

重点文件：
- [quickstart.md](/Users/waylon/Desktop/openclaw-product/packages/education-agent/docs/quickstart.md)
- [user-guide.md](/Users/waylon/Desktop/openclaw-product/packages/education-agent/docs/user-guide.md)
- [trainer-guide.md](/Users/waylon/Desktop/openclaw-product/packages/education-agent/docs/trainer-guide.md)

## 9. 首次联调建议

建议先测试这类问题：
- 帮我设计一节关于函数图像的中文课堂大纲
- 帮我生成一份 10 题的课堂小测
- 帮我整理这份课件 PDF 的知识点
- 请把这段课堂录音整理成中文课堂纪要
- 请把这份课堂提纲改成老师可直接播报的语音串讲稿

最小验收：

```bash
openclaw agent --agent education-agent --message "请用一句话介绍你自己"
```

## 10. 失败排查

### 提示缺少 Key

说明对应 Skill 命中了初始化守卫，继续补齐：
- `openmaic_api_key`
- `openmaic_asr_api_key`
- `openmaic_tts_api_key`
- `quizzle_api_key`
- `moodle_token`

### 安装后找不到包

```bash
ls packages/education-agent
ls agents/education-agent
ls /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent
```

### 飞书绑定失败

先确认：

```bash
openclaw agents list
openclaw agents bindings --json
```

再检查 `educationbot` 是否已经创建成功。若未创建，请先按飞书官方插件流程完成扫码建机器人。
