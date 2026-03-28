# 电商 / 本地生活 Agent 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `product-catalog-query` | Medusa / Saleor | 建议首发 | 低 | 是 | 服务 / key | 查商品、SKU、库存、门店信息。 |
| `store-content-manager` | Strapi / Directus / Payload | 建议首发 | 低 | 是 | 服务 / key | 管理门店介绍、活动说明、FAQ。 |
| `product-faq-answerer` | Strapi / 本 Agent 本地问答技能 | 建议首发 | 低 | 否 | 无 | 回答商品和门店常见问题。 |
| `coupon-offer-guide` | Strapi / Formbricks | 建议首发 | 低 | 否 | 无 | 解释优惠、券、活动使用方式。 |
| `activity-copy-generator` | 本 Agent 本地生成技能 | 建议首发 | 低 | 否 | 无 | 生成促销文案与上新文案。 |
| `crm-customer-tagging` | EspoCRM | 建议首发 | 低 | 是 | 服务 / key | 打标签、沉淀潜客画像。 |
| `lead-capture-form` | Formbricks | 建议首发 | 低 | 是 | 服务 / key | 收集咨询信息。 |
| `booking-and-arrival-flow` | Cal.com / n8n | 建议首发 | 低 | 是 | 服务 / key | 预约到店、核销前提醒。 |
| `product-image-cleanup` | rembg / 图像外部技能 | 建议首发 | 低 | 否 | CPU / GPU | 处理商品展示图。 |
| `background-remove` | rembg | 建议首发 | 低 | 否 | CPU / GPU | 抠图与背景替换。 |
| `order-followup-note` | EspoCRM / Chatwoot | 建议首发 | 低 | 是 | 服务 / key | 记录客户意向与跟进备注。 |
| `promotion-performance-brief` | EspoCRM / summarize / excel-xlsx | 建议首发 | 低 | 是 | 服务 / 文档 | 输出活动成效简报。 |
