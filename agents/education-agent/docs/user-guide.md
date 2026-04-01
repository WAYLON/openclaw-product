# 教育 Agent 内部用户指南

## 核心定位
教育 Agent 主要面向交付后的终端用户，但这份内部版是给实施同学、开发同学、培训老师做实施和交付校验用的。

## 用户真正会用到的能力
- 教学资料整理
- 讲义 / PDF 内容摘要
- 课堂重点提炼
- 结合 OpenMAIC 的教学辅助

## 用户成功标准
- 知道这个 Agent 能做什么。
- 知道第一次怎么配置。
- 知道如何正确提问。
- 知道风险边界在哪里。

## 初始化关注点
- `openmaic` 的 `accessCode`

## 当前真实接通能力
- `openmaic` 当前按 hosted mode 接入
- 私有 skill 路径以实际运行现场为准：
  - `~/.openclaw/parallel-agents/workspaces/education-agent/skills/openmaic/`
- 当前已经跑过真实课堂生成任务，不只是大纲回复

## 推荐提问方式
- “帮我把这份讲义整理成课堂重点”
- “用 openmaic 生成一个互动课堂：零基础文科生，30 分钟学会 Python。生成完成后直接把 classroom URL 发我。”

## 内部交付提醒
- 不替代正式评分
- 不替代老师做高风险判断
