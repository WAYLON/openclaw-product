# Installer 说明

`installer/` 目录不是临时脚本堆放区，而是平台交付与落地实施的模板同步层。

## 这一层负责什么

- 初始化项目模板状态目录与默认状态文件
- 安装、启用、停用、卸载专业 Agent 模板
- 校验交付包结构是否满足正式交付标准
- 同步 Agent workspace 模板到本机 OpenClaw
- 打包交付文档、示例和安装清单
- 为后续升级、回滚、下线预留统一入口

## 主要文件

- `bootstrap_project.py`
  平台初始化脚本。用于准备 `.platform/` 运行态、Agent 注册表和基础状态文件。
- `agent_installer.py`
  Agent 安装逻辑。负责安装状态写入、启停控制和目录校验。
- `validate_package.py`
  交付包校验工具。检查包级文档、配置和安装清单是否齐备。
- `build_package.py`
  交付包构建入口。当前版本先做目录级校验和清单确认，后续可扩展 zip、校验和和版本签名。
- `docs_packager.py`
  文档打包工具。将 quickstart、user-guide、trainer-guide、faq、examples 打包为交付资料。
- `sync_to_openclaw.py`
  模板同步工具。把项目内 Agent workspace 模板同步到本机 OpenClaw 多 Agent 目录。

## 推荐使用顺序

1. 先执行项目模板初始化
2. 再安装 Agent 模板
3. 再同步到本机 OpenClaw
4. 再写入凭证
5. 最后用官方命令做渠道绑定和联调验证

对应命令见：
- `/Users/waylon/Desktop/openclaw-product/docs/installation/平台安装教程.md`
- `/Users/waylon/Desktop/openclaw-product/docs/installation/agent安装教程.md`
- `/Users/waylon/Desktop/openclaw-product/docs/installation/渠道绑定教程.md`
