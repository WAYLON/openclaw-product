# 教育 Agent 技能矩阵

| 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
|---|---|---|---|---|---|---|
| `lesson-topic-planner` | OpenMAIC | 建议首发 | 低 | 否 | 无 | 按教学目标拆解课题与课时。 |
| `lesson-outline-generator` | OpenMAIC | 建议首发 | 低 | 否 | 无 | 生成章节、重点、难点、互动节点。 |
| `slide-class-generator` | OpenMAIC / word-docx | 建议首发 | 低 | 否 | 文档导出 | 产出可讲授的中文课件草稿。 |
| `quiz-generator` | Quizzle / OpenMAIC | 建议首发 | 低 | 否 | 无 | 生成单选、多选、判断、问答题。 |
| `live-quiz-runtime` | Quizzle | 建议首发 | 中 | 是 | 服务 / key | 课堂实时答题、抢答、排名。 |
| `practice-exam-engine` | Quizzle / Moodle | 建议首发 | 低 | 是 | 服务 / key | 构建练习卷、章节测、模拟测。 |
| `interactive-classroom-builder` | OpenMAIC | 建议首发 | 中 | 是 | 浏览器 / 服务 | 构建互动课堂活动流程。 |
| `teaching-material-parser` | MinerU / PaddleOCR | 建议首发 | 低 | 否 | OCR / 本地服务 | 解析课件、讲义、试卷 PDF。 |
| `study-path-advisor` | OpenMAIC / Moodle | 建议首发 | 低 | 否 | 无 | 按学生目标推荐学习路径。 |
| `assignment-generator` | OpenMAIC / Moodle | 建议首发 | 低 | 是 | 服务 / key | 生成作业与提交说明。 |
| `teacher-ta-mode` | OpenMAIC | 建议首发 | 低 | 否 | 无 | 老师视角的课堂助手与课后总结助手。 |
| `class-exporter` | Moodle / word-docx / excel-xlsx | 建议首发 | 低 | 是 | 服务 / 文档 | 导出课件、题库、作业、课堂记录。 |
| `classroom-speech-transcriber` | OpenMAIC / PaddleOCR | 建议首发 | 中 | 是 | ASR 服务 / 音频输入 | 将课堂语音、老师串讲、学生口语转为可检索的中文课堂记录。 |
| `lesson-voice-narrator` | OpenMAIC | 建议首发 | 低 | 是 | TTS 服务 / 音频输出 | 将讲义、提纲、提示词转成可播报的中文课堂语音稿。 |
| `oral-practice-coach` | OpenMAIC / Quizzle | 建议首发 | 中 | 是 | ASR / TTS / 音频输入 | 对学生口语作答进行转写、点评和下一轮练习提示。 |
