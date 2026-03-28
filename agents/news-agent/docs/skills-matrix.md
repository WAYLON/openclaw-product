# 资讯 Agent 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `rss-source-router` | RSSHub | 建议首发 | 低 | 否 | 网络 | 统一配置订阅源和平台 feed 路由。 |
| `feed-subscription-manager` | RSSHub | 建议首发 | 低 | 否 | 网络 | 管理订阅、标签、更新频率。 |
| `topic-monitor` | RSSHub / openclaw-tavily-search | 建议首发 | 低 | 是 | 网络 / key | 围绕主题持续监测新内容。 |
| `keyword-watch` | RSSHub / opencli | 建议首发 | 低 | 是 | 网络 / 浏览器 | 按关键词追踪平台与站点动态。 |
| `platform-content-reader` | opencli / web-access | 建议首发 | 低 | 否 | 浏览器 | 读取公众号、微博、知乎、B 站等内容。 |
| `news-cluster-summarizer` | summarize | 建议首发 | 低 | 否 | 无 | 把多篇相关内容聚类并生成中文摘要。 |
| `daily-brief-generator` | summarize / word-docx | 建议首发 | 低 | 否 | 文档 | 生成日报。 |
| `weekly-brief-generator` | summarize / word-docx | 建议首发 | 低 | 否 | 文档 | 生成周报。 |
| `competitor-content-scan` | opencli / web-access | 建议首发 | 低 | 否 | 浏览器 | 扫描竞品账号、栏目和站点内容。 |
| `content-publish-pipeline` | Strapi / Directus / Payload / n8n | 建议首发 | 中 | 是 | 服务 / key | 把稿件投递到内容后台或自动工作流。 |
| `article-knowledge-base-sync` | Strapi / Directus / Payload | 建议首发 | 低 | 是 | 服务 / key | 将精选资讯同步到知识库。 |
| `multi-source-merge` | RSSHub / summarize / opencli | 建议首发 | 低 | 否 | 网络 | 把相同主题的多源信息合并去重。 |
