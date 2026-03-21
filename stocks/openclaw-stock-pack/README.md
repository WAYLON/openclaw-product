# OpenClaw 通用股票研究包

这是一个可搬运的通用股票研究产品包。

它适合一般股票研究、选股、新闻判断与外部能力补充场景，但不默认包含聚宽 / JQData 专用能力。

注意：

- 这个目录不是完整基础版
- 正确交付顺序是先装 `core/` 基础技能层，再装这个股票行业包

如果目标机器是从 0 开始部署，请先阅读：

- `../../core/README.md`
- `../../core/安装-openclaw-本体.md`
- `../../core/从零部署-openclaw-股票版.md`

## 目录结构

- `workspace/`
  - `SOUL.md`：通用股票研究模式人格
  - `AGENTS.md`：通用股票任务路由规则
  - `TOOLS.md`：本机工具与账户占位说明
  - `USER.md`：用户偏好模板
  - `MEMORY.md`：长期记忆模板
  - `INIT_PROMPT.md`：首次初始化提示词，会要求主动提醒凭证和依赖
- `skills/`
  - `stock-research-core/`：股票研究总路由技能
  - `qveris-official/`：QVeris 官方技能

## 不包含的能力

这个通用版不包含：

- `jqdata-playbook`
- 聚宽专用文档层
- 对 `jqdata-research` 的默认依赖

如果客户需要聚宽 / JQData 研究能力，请改用：

- `../openclaw-stock-pack-langlang/`

## 推荐安装方式

### 方案 A：只安装技能

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh stocks/openclaw-stock-pack skills-only
```

### 方案 B：安装完整工作区

```bash
./core/scripts/install-core-skills.sh
./scripts/install-pack.sh stocks/openclaw-stock-pack full
```

## 目标机器需要自己补的内容

- OpenClaw 模型或 provider 配置
- `QVERIS_API_KEY`
- 本机脚本路径
- 同花顺或其他终端接入方式

这些内容应保留在目标机器本地，不建议随仓库一起分发。
