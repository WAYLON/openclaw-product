# 法务 / 合同流程 Agent 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `contract-upload-parse` | Documenso / MinerU | 建议首发 | 低 | 是 | 服务 / OCR | 上传并解析合同文件。 |
| `clause-risk-highlight` | MinerU / policies | 建议首发 | 中 | 否 | OCR / 规则 | 标出重点条款与风险提示。 |
| `document-ocr-parse` | PaddleOCR | 建议首发 | 低 | 否 | OCR / 本地服务 | 识别扫描件。 |
| `table-and-figure-extract` | MinerU | 建议首发 | 低 | 否 | OCR / 本地服务 | 抽取表格与图示。 |
| `approval-form-collect` | Formbricks | 建议首发 | 低 | 是 | 服务 / key | 收集审批意见。 |
| `sign-request-create` | Documenso | 建议首发 | 中 | 是 | 服务 / key | 创建签署请求。 |
| `sign-status-track` | Documenso / n8n | 建议首发 | 低 | 是 | 服务 / key | 跟踪签署状态。 |
| `legal-faq-answerer` | 本 Agent 本地知识技能 | 建议首发 | 中 | 否 | 无 | 回答流程类常见问题。 |
| `case-material-checklist` | Formbricks / PaddleOCR | 建议首发 | 低 | 否 | OCR | 列案件材料清单。 |
| `contract-version-compare` | MinerU / summarize | 建议首发 | 中 | 否 | OCR / 文本比较 | 比对版本差异。 |
| `contract-summary` | MinerU / summarize / word-docx | 建议首发 | 低 | 否 | 文档 | 输出合同摘要。 |
| `evidence-package-export` | Documenso / word-docx / excel-xlsx | 建议首发 | 中 | 是 | 服务 / 文档 | 导出证据包与流程记录。 |
