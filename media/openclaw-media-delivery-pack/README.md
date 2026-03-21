# OpenClaw 媒体发送包

这是面向图片、音频、视频、文件等媒体资源发送与分发的行业包。

它适合：

- 向飞书发送图片
- 向飞书发送音频
- 发送视频或文件附件
- 对媒体发送前做格式检查
- 沉淀各渠道的媒体发送规则

注意：

- 这个目录是媒体行业包，不是基础层
- 正确安装顺序是先装 `core/`，再装这个包

## 当前结构

- `workspace/`
  - `INIT_PROMPT.md`：首次初始化提示词，会要求主动提醒凭证和依赖
- `skills/media-delivery-core/`
- `scripts/check_media_delivery_env.sh`

## 推荐安装方式

### 方案 A：只安装技能

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh media/openclaw-media-delivery-pack skills-only
```

### 方案 B：安装完整工作区

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh media/openclaw-media-delivery-pack full
```

## 目标机器需要自己补的内容

- 已接入的消息渠道
- 本地媒体文件路径
- 如需语音气泡发送，`ffmpeg`
- 渠道鉴权信息

## 建议安装后立刻验证

```bash
./media/openclaw-media-delivery-pack/scripts/check_media_delivery_env.sh
openclaw skills check
```
