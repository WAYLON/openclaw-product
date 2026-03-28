# 助贷 Agent 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `lead-intake-form` | Formbricks | 建议首发 | 低 | 是 | 服务 / key | 创建意向表单与线索采集页。 |
| `loan-intent-capture` | Formbricks / EspoCRM | 建议首发 | 低 | 是 | 服务 / key | 采集贷款用途、金额、期限、地区。 |
| `eligibility-precheck` | Formbricks / n8n | 建议首发 | 中 | 是 | 服务 / key | 按预设规则做资格初筛。 |
| `material-checklist-guide` | Documenso / Formbricks | 建议首发 | 低 | 否 | 无 | 给出材料清单、拍摄要求、常见缺漏。 |
| `id-card-ocr-parse` | PaddleOCR | 建议首发 | 中 | 否 | OCR / 本地服务 | 解析身份证关键信息。 |
| `income-doc-parse` | PaddleOCR / MinerU | 建议首发 | 中 | 否 | OCR / 本地服务 | 解析收入证明、工资条。 |
| `bank-statement-parse` | MinerU / PaddleOCR | 建议首发 | 中 | 否 | OCR / 本地服务 | 抽取流水摘要。 |
| `application-form-filler` | n8n / Formbricks | 建议首发 | 中 | 是 | 服务 / key | 把用户输入转成申请表预填数据。 |
| `crm-lead-sync` | EspoCRM | 建议首发 | 低 | 是 | 服务 / key | 把线索同步进 CRM。 |
| `appointment-booking` | Cal.com | 建议首发 | 低 | 是 | 服务 / key | 预约顾问回访。 |
| `contract-sign-flow` | Documenso | 建议首发 | 中 | 是 | 服务 / key | 意向确认与签署流程。 |
| `compliance-reminder` | n8n / policies | 建议首发 | 中 | 否 | 无 | 中文合规提示、风险说明、禁止承诺模板。 |
