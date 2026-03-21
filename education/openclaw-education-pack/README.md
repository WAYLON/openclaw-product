# OpenClaw 教育产品包

这是教育方向的行业基础包。

当前这版的核心教育能力来源于 OpenMAIC 的 OpenClaw 集成方案：

- [THU-MAIC/OpenMAIC README-zh](https://github.com/THU-MAIC/OpenMAIC/blob/main/README-zh.md#-openclaw-%E9%9B%86%E6%88%90)

它适合：

- 课程生成
- 互动课堂
- 教学材料转课堂
- 在飞书、Slack、Telegram 等渠道中发起课堂

注意：

- 这个目录是教育行业包，不是基础层
- 正确安装顺序是先装 `core/`，再装这个教育包

## 当前结构

- `workspace/`
  - 教育模式的人格和路由规则
  - `INIT_PROMPT.md`：首次初始化提示词，会要求主动提醒凭证和依赖
- `skills/openmaic-official/`
  - OpenMAIC 教育技能
- `scripts/check_openmaic_prereqs.sh`
  - 最小环境检查脚本

## 推荐安装方式

### 方案 A：只安装技能

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh education/openclaw-education-pack skills-only
```

### 方案 B：安装完整工作区

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh education/openclaw-education-pack full
```

## 目标机器需要自己补的内容

- OpenClaw 模型或 provider 配置
- OpenMAIC 运行环境
- 至少一个可用 LLM API Key
- 如需增强 PDF 解析，可选配置 MinerU

## 建议安装后立刻验证

```bash
./education/openclaw-education-pack/scripts/check_openmaic_prereqs.sh
openclaw skills check
```
