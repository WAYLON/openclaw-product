# photo-polisher 完整安装示例

> 当前推荐口径：**官方 OpenClaw 命令优先**。本示例中，`openclaw` 负责本体安装、Agent 注册与渠道绑定，`agent-platform` 只负责项目模板生成、工作区同步与交付自动化。

## 1. 前置条件

先按官方方式安装 OpenClaw：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw --version
openclaw status
```

## 2. 注册 photo-polisher

```bash
openclaw agents add photo-polisher
openclaw agents list
```

## 3. 初始化项目模板状态

```bash
cd ~/Desktop/openclaw-product
./agent-platform init
./agent-platform start
./agent-platform doctor
```

## 4. 生成 photo-polisher 模板并导出

```bash
./agent-platform agent install photo-polisher
./agent-platform openclaw export photo-polisher
./agent-platform agent list
```

再检查工作区模板：

```bash
find .platform/workspaces/photo-polisher -maxdepth 2 -type f | sort
```

## 5. 设置本机 OpenClaw 身份文件

```bash
openclaw agents set-identity \
  --agent photo-polisher \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/photo-polisher/IDENTITY.md
```

## 6. 绑定渠道

如果当前本机已经是飞书全量落地，优先使用飞书绑定：

```bash
openclaw agents bind --agent photo-polisher --channel feishu --account photobot
openclaw agents bindings --json
```

如果客户后续要求 API 化图片入口，再补 Webhook：

```bash
openclaw agents bind --agent photo-polisher --channel webhook --account photo-webhook
openclaw agents bindings --json
```

如果后续要接飞书机器人，也可以单独再绑定飞书实例。

## 7. 配置修图相关服务

### GFPGAN 服务地址

```bash
./agent-platform secret set photo-polisher gfpgan_endpoint --value "http://127.0.0.1:7861" --scope agent
```

### Real-ESRGAN 服务地址

```bash
./agent-platform secret set photo-polisher realesrgan_endpoint --value "http://127.0.0.1:7862" --scope agent
```

### rembg 服务地址

```bash
./agent-platform secret set photo-polisher rembg_endpoint --value "http://127.0.0.1:7863" --scope agent
```

### 可选 OCR

```bash
./agent-platform secret set photo-polisher paddleocr_endpoint --value "http://127.0.0.1:7864" --scope agent
```

查看已配置：

```bash
./agent-platform secret list photo-polisher --scope agent
```

## 8. 检查修图包交付物

```bash
find packages/photo-polisher/docs -maxdepth 1 -type f | sort
find packages/photo-polisher/assets -maxdepth 1 -type f | sort
find .platform/workspaces/photo-polisher/docs -maxdepth 1 -type f | sort
```

重点文件：
- [quickstart.md](/Users/waylon/Desktop/openclaw-product/packages/photo-polisher/docs/quickstart.md)
- [trainer-guide.md](/Users/waylon/Desktop/openclaw-product/packages/photo-polisher/docs/trainer-guide.md)
- [image-plan.md](/Users/waylon/Desktop/openclaw-product/packages/photo-polisher/docs/image-plan.md)

## 9. 首次联调建议

建议先测试：
- 帮我修复这张老照片
- 帮我把这张图片做 2 倍放大
- 帮我去掉商品图背景

最小验收：

```bash
openclaw agent --agent photo-polisher --message "请用一句话介绍你自己"
```

## 10. CPU / GPU / Docker / API 说明

### CPU
- 适合演示
- 速度较慢

### GPU
- 适合正式批量交付
- 推荐用于超分和复杂修复

### Docker
- 适合统一部署
- 便于环境标准化

### API
- 适合已有图像服务底座
- 便于渠道侧统一接入

## 11. 失败排查

### 没有结果输出

先检查对应 Endpoint：

```bash
./agent-platform secret list photo-polisher --scope agent
```

### 想先演示，不想接 GPU

可以先只配置：
- `rembg_endpoint`
- `gfpgan_endpoint`

把 Real-ESRGAN 留到第二阶段。
