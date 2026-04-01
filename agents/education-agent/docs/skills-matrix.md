# 教育 Agent 技能矩阵

## 共享技能基线

- `web-access`
- `opencli`
- `self-improving-agent`
- `skill-vetter`
- `summarize`
- `agent-browser`
- `ontology`
- `weather`
- `document-pro`
- `github`
- `proactive-agent`
- `mcporter`
- `multi-search-engine`
- `nano-pdf`
- `nano-banana-pro`
- `excel-xlsx`
- `word-docx`
- `desktop-control`

## 专有技能

| 技能 | 当前状态 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
|---|---|---|---|---|---|
| `openmaic` | 已接入 | 中 | 是 | hosted access code | 教学资料理解、课堂整理、教学辅助。 |

## 现场已验证事实

- `openmaic` 当前按教育 Agent 私有 skill 运行
- 私有 skill 实际路径：
  - `~/.openclaw/parallel-agents/workspaces/education-agent/skills/openmaic/`
- `accessCode` 已通过健康检查：
  - `https://open.maic.chat/api/health`
- 已真实提交课堂生成任务，不是只返回大纲
