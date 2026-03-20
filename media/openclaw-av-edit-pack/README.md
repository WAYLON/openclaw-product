# OpenClaw 音视频剪辑包

这是面向音视频处理、素材整理、转码、剪辑协作的行业包。

它适合：

- 音视频转码
- 批量裁剪
- 封面抽帧
- 字幕处理
- 素材目录整理

注意：

- 这个目录是媒体行业包，不是基础层
- 正确安装顺序是先装 `core/`，再装这个包

## 当前结构

- `workspace/`
- `skills/av-edit-core/`
- `scripts/check_av_tools.sh`

## 推荐安装方式

### 方案 A：只安装技能

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh media/openclaw-av-edit-pack skills-only
```

### 方案 B：安装完整工作区

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh media/openclaw-av-edit-pack full
```

## 目标机器需要自己补的内容

- `ffmpeg`
- `ffprobe`
- 实际素材目录
- 目标输出目录
- 如需字幕识别或语音能力，对应 API 或本地模型

## 建议安装后立刻验证

```bash
./media/openclaw-av-edit-pack/scripts/check_av_tools.sh
openclaw skills check
```
