# 像素修图师 技能矩阵

    | 技能 | 来源底座 | 首发建议 | 风险等级 | 需要 Key | 运行要求 | 中文说明 |
    |---|---|---|---|---|---|---|
    | `face-restore` | GFPGAN | 建议首发 | 低 | 否 | CPU / GPU / Docker / API | 做人脸修复。 |
| `image-upscale` | Real-ESRGAN | 建议首发 | 低 | 否 | CPU / GPU / Docker / API | 做超分放大。 |
| `old-photo-repair` | GFPGAN / Real-ESRGAN | 建议首发 | 低 | 否 | CPU / GPU | 修复老照片。 |
| `portrait-enhance` | GFPGAN | 建议首发 | 低 | 否 | CPU / GPU | 优化人像细节。 |
| `product-photo-cleanup` | rembg / Real-ESRGAN | 建议首发 | 低 | 否 | CPU / GPU | 处理商品图。 |
| `background-remove` | rembg | 建议首发 | 低 | 否 | CPU / GPU / API | 移除背景。 |
| `id-photo-standardize` | PaddleOCR / rembg | 建议首发 | 中 | 否 | CPU / OCR | 做证件照规范化预处理。 |
| `image-batch-enhance` | GFPGAN / Real-ESRGAN / rembg | 建议首发 | 中 | 否 | CPU / GPU / Docker | 批量处理图片。 |
| `low-light-fix` | Real-ESRGAN / custom pipeline | 建议首发 | 中 | 否 | GPU 建议 | 修复低光图。 |
| `blur-recovery` | Real-ESRGAN | 建议首发 | 中 | 否 | GPU 建议 | 对模糊图做增强。 |
| `image-precheck` | PaddleOCR / metadata | 建议首发 | 低 | 否 | CPU | 预检分辨率、噪声、清晰度。 |
| `before-after-packager` | 本 Agent 本地图文打包技能 | 建议首发 | 低 | 否 | 文档 | 输出前后对比包。 |
