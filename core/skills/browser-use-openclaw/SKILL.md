---
name: browser-use-openclaw
description: >-
  基于本机已安装的 browser-use CLI 提供浏览器自动化能力。适合打开网页、
  点击、输入、截图、抽取数据、连接真实 Chrome，以及执行表单填写和网页操作。
  默认优先使用本机真实浏览器模式。需要本机已安装 browser-use。
runtime:
  language: python
  python: ">=3.12"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
dependencies:
  bins:
    - browser-use
security:
  child_process: true
  eval: false
  filesystem_write: true
  filesystem_read: true
examples:
  - "打开 https://example.com，然后截图"
  - "连接真实 Chrome，打开 GitHub 并提取当前页面标题"
  - "帮我用浏览器访问一个页面，列出可点击元素"
---

# browser-use OpenClaw 技能

这个技能用于把本机的 `browser-use` CLI 接到 OpenClaw。

## 什么时候用

以下任务优先使用这个技能：

- 打开网页
- 浏览器自动化
- 表单填写
- 网页截图
- 页面元素观察
- 简单数据提取
- 希望连接真实 Chrome 复用已有登录态

## 前置要求

当前机器必须满足：

- 已安装 `browser-use`
- 建议使用 Python `3.12`
- 首次使用前，先确认 `browser-use doctor` 能通过本地基础检查

本机安装建议：

```bash
uv tool install --python 3.12 browser-use
browser-use doctor
```

## 默认执行方式

默认优先用真实浏览器模式：

```bash
browser-use --browser real open <url>
```

如果只是本地轻量测试，也可以直接用默认模式。

## 最小工作流

### 1. 打开页面

```bash
bash scripts/browser_use_open.sh https://example.com
```

### 2. 查看页面状态

```bash
bash scripts/browser_use_state.sh
```

### 3. 截图

```bash
bash scripts/browser_use_screenshot.sh
```

### 4. 抽取内容

```bash
bash scripts/browser_use_extract.sh "提取页面主要结论"
```

## 使用原则

- 默认中文输出说明
- 涉及登录态时，优先使用真实浏览器模式
- 如果 `browser-use` 缺失、版本异常或 `doctor` 失败，先说明依赖问题
- 不要假装网页操作已经成功，除非命令确实执行成功

## 常见坑

- `browser-use` 在 Python `3.14` 上可能出现兼容问题，优先用 `3.12`
- 全局参数要放在子命令前面，例如：

```bash
browser-use --browser real open https://example.com
```

而不是：

```bash
browser-use open https://example.com --browser real
```

## 建议搭配

- 如需标准 DevTools HTTP 接口，可先运行：

```bash
bash scripts/start_standard_devtools.sh
```

- 如需复杂网页状态提取，可先 `open`，再 `state`，最后 `extract`
