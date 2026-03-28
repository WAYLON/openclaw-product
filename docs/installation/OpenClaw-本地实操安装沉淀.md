# OpenClaw-本地实操安装沉淀

> 这份文档不是概念稿，而是按今天已经在本机跑通的方式沉淀出来的真实安装手册。  
> 当前推荐口径：**官方 OpenClaw 命令优先**，项目里的 `agent-platform` 和飞书辅助脚本只作为交付自动化补充。

## 1. 适用场景

适用于以下交付方式：

- 本机已经安装 OpenClaw
- 需要在同一台机器上安装多个独立 Agent
- 每个 Agent 都要绑定自己的飞书机器人
- 不希望新建机器人时把旧 `default` 永久覆盖
- 需要把“扫码创建出来的新机器人”沉淀成独立 `accountId`

## 2. 今天已经跑通的核心结论

### 2.0 官方优先主路径

如果你要尽量贴官方推荐方式，主路径应该是：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw agents add <agent>
openclaw agents set-identity --agent <agent> --identity-file <IDENTITY.md>
openclaw agents bind --agent <agent> --channel feishu --account <account-id>
```

也就是说：

- `openclaw onboard`：负责本体初始化
- `openclaw agents add`：负责注册 Agent
- `openclaw agents bind`：负责渠道绑定

我们自己的保留项：

- `./agent-platform`
- `feishu_capture_new_bot.py`
- `feishu_create_and_bind_bot.py`

只负责把项目模板、扫码恢复 `default`、沉淀新 `accountId` 这些动作自动化。

### 2.1 本机当前实际结果

截至今天这次安装验收，本机 `openclaw agents list` 已经能看到：

- `main`
- `stock-agent`
- `education-agent`
- `news-agent`
- `loan-agent`
- `local-commerce-agent`
- `photo-polisher`
- `sales-agent`
- `legal-agent`

其中新增的 8 个专业 Agent 都已完成最小调用验收，实际执行的是：

```bash
openclaw agent --agent <agent> --message "回复 OK" --json
```

本机今天实际通过的 8 个 Agent：

- `stock-agent`
- `education-agent`
- `news-agent`
- `loan-agent`
- `local-commerce-agent`
- `photo-polisher`
- `sales-agent`
- `legal-agent`

本机当前验收时的实际模型链路：

- `provider: local-openai`
- `model: gpt-5.4`

因此，今天这台机器的状态不是“待安装”，而是：

- 项目侧已安装 8 个 Agent 模板
- 本机 OpenClaw 侧已注册 8 个平行 Agent
- 8 个 Agent 最小调用已通过
- 可继续做渠道绑定和 Key 初始化

### 2.2 Agent 安装方式

今天实际沉淀出来的做法是：

1. 官方主路径：`openclaw agents add`
2. 项目补充路径：先在项目内安装模板，再同步到本机 OpenClaw

项目补充命令如下：

```bash
cd /Users/waylon/Desktop/openclaw-product
./agent-platform agent install stock-agent
./agent-platform openclaw export stock-agent
```

这条导出命令会把：

- `.platform/workspaces/stock-agent/`
- `packages/stock-agent/`

同步到：

- `~/.openclaw/parallel-agents/workspaces/stock-agent/`
- `~/.openclaw/parallel-agents/packages/stock-agent/`

并更新：

- `~/.openclaw/parallel-agents/registry.json`

如果目标机器上还没有这个 Agent，再补两条原生命令即可：

```bash
openclaw agents add \
  --agent stock-agent \
  --workspace /Users/waylon/.openclaw/parallel-agents/workspaces/stock-agent \
  --agent-dir /Users/waylon/.openclaw/parallel-agents/state/stock-agent/agent

openclaw agents set-identity \
  --agent stock-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/stock-agent/IDENTITY.md
```

### 2.3 飞书机器人创建方式

今天实际跑通的是飞书官方插件安装器：

```bash
npx -y @larksuite/openclaw-lark install
```

并且要选：

- 不复用现有机器人
- 进入“新建机器人”
- 用飞书扫码

### 2.4 一个关键坑

飞书官方安装器每次新建机器人时，默认会把当前飞书 `default` 配置覆盖成新机器人。

所以今天真正可交付的做法不是“直接新建完就结束”，而是：

1. 新建机器人
2. 读取当前被覆盖后的 `default`
3. 把这个新机器人沉淀成新的 `accountId`
4. 把旧 `default` 恢复回来
5. 再把新 `accountId` 绑定到指定 Agent

也就是说：

- 官方插件负责创建机器人
- 我们的脚本负责沉淀新账号并恢复旧 `default`
- 这两个脚本必须保留，不建议删除

## 3. 本地目录约定

今天本机实际使用了这些目录：

```text
~/.openclaw/parallel-agents/
├── registry.json
├── state/
│   ├── stock-agent/
│   ├── education-agent/
│   └── ...
└── workspaces/
    ├── stock-agent/
    ├── education-agent/
    └── ...
```

每个 workspace 里至少放：

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `MEMORY.md`
- `agent-package/`
- `delivery-package/`

## 4. 安装 8 个平行 Agent 的实际流程

推荐顺序：

1. 先用官方命令安装 OpenClaw 本体
2. 再用官方命令注册 Agent
3. 如需模板化交付，再用 `agent-platform openclaw export`
4. 最后用官方飞书插件装机器人，并用脚本做账号沉淀

### 4.1 先在项目内安装 Agent 模板

示例：安装教育 Agent

```bash
cd /Users/waylon/Desktop/openclaw-product
./agent-platform agent install education-agent
```

### 4.2 同步到本机 OpenClaw

```bash
./agent-platform openclaw export education-agent
```

### 4.3 首次导出后补原生命令

如果这是第一次把这个 Agent 加进本机 OpenClaw，再执行：

```bash
openclaw agents add \
  --agent education-agent \
  --workspace /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent \
  --agent-dir /Users/waylon/.openclaw/parallel-agents/state/education-agent/agent

openclaw agents set-identity \
  --agent education-agent \
  --identity-file /Users/waylon/.openclaw/parallel-agents/workspaces/education-agent/IDENTITY.md
```

### 4.4 检查是否安装成功

```bash
openclaw agents list
```

成功标志：

- 能看到 `stock-agent`
- 能看到 `education-agent`
- 能看到其他 6 个专业 Agent
- `Workspace` 指向 `~/.openclaw/parallel-agents/workspaces/<agent>`

### 4.5 本机今天的实际验收命令

今天本机是这样做安装验收的：

```bash
for agent in stock-agent education-agent news-agent loan-agent local-commerce-agent photo-polisher sales-agent legal-agent; do
  openclaw agent --agent "$agent" --message "回复 OK" --json
done
```

验收标准：

- 返回 `status = ok`
- 返回文本为 `OK`
- `provider` 和 `model` 可正常解析

今天本机实际验收结果：

- 8 个 Agent 全部通过
- 实际 provider：`local-openai`
- 实际 model：`gpt-5.4`

## 5. 飞书机器人一只一只安装的真实流程

### 5.1 启动官方安装器

```bash
npx -y @larksuite/openclaw-lark install --verbose
```

### 5.2 看到已有机器人提示时

如果出现：

```text
Found Feishu bot with App ID ...
Use it for this setup?
```

必须选：

```text
n
```

否则会复用旧机器人，不会创建新的。

### 5.3 扫码创建

安装器会给出一条链接，格式类似：

```text
https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=onboard
```

建议做法：

- 不要直接扫终端小二维码
- 把这条链接打开成网页大图再扫

### 5.4 创建成功后的正确处理

创建成功后，不要直接结束。

必须继续执行“沉淀新机器人”的步骤，否则：

- 新机器人会占掉 `default`
- 旧 `default` 会丢
- 后续绑定会越来越乱

创建完之后，官方侧检查命令建议立刻执行：

```bash
openclaw agents bindings --json
openclaw channels status --probe --json
```

## 6. 沉淀新飞书机器人的脚本

今天本机已经补了这个脚本：

- [feishu_capture_new_bot.py](/Users/waylon/.openclaw/workspace/feishu_capture_new_bot.py)
- [feishu_create_and_bind_bot.py](/Users/waylon/.openclaw/workspace/feishu_create_and_bind_bot.py)

以及一份稳定恢复基线：

- [feishu-default-baseline.json](/Users/waylon/.openclaw/feishu-default-baseline.json)

### 6.1 脚本用途

这个脚本负责：

1. 读取当前被安装器覆盖后的 `default`
2. 把它保存成新的独立 `accountId`
3. 恢复旧 `default`
4. 给指定 Agent 增加绑定
5. 重启 gateway

### 6.2 用法

#### 方式 A：分两步执行

示例：把刚创建的飞书机器人沉淀成 `educationbot`，绑定给 `education-agent`

```bash
python3 /Users/waylon/.openclaw/workspace/feishu_capture_new_bot.py \
  --account-id educationbot \
  --name 教育机器人 \
  --agent education-agent
```

示例：沉淀成 `newsbot` 并绑定 `news-agent`

```bash
python3 /Users/waylon/.openclaw/workspace/feishu_capture_new_bot.py \
  --account-id newsbot \
  --name 资讯机器人 \
  --agent news-agent
```

#### 方式 B：一条命令执行，扫码之外全自动

今天已经补了简化脚本，推荐以后优先用它：

```bash
python3 /Users/waylon/.openclaw/workspace/feishu_create_and_bind_bot.py \
  --account-id newsbot \
  --name 资讯机器人 \
  --agent news-agent
```

这条命令会自动完成：

1. 启动飞书官方安装器
2. 自动选择“不复用现有机器人”
3. 自动打开扫码页面
4. 等你扫码完成
5. 自动把新机器人沉淀成独立 `accountId`
6. 自动恢复旧 `default`
7. 自动绑定到目标 Agent
8. 自动重启 gateway

也就是说，后续真正需要人工做的只剩：

- 扫一次码

## 7. 今天已经跑通的最终绑定结果

截至今天本机实操结束，已经跑通的完整绑定形态是：

```text
main <- feishu:default
stock-agent <- feishu:stockbot
education-agent <- feishu:educationbot
news-agent <- feishu:newsbot
loan-agent <- feishu:loanbot
local-commerce-agent <- feishu:commercebot
photo-polisher <- feishu:photobot
sales-agent <- feishu:salesbot
legal-agent <- feishu:legalbot
```

也就是说，截至今天本机的实际绑定状态是：

- 原有主机器人保留：
  - `main <- feishu:default`
- 8 个专业 Agent 的独立飞书机器人全部已创建并绑定：
  - `stock-agent <- feishu:stockbot`
  - `education-agent <- feishu:educationbot`
  - `news-agent <- feishu:newsbot`
  - `loan-agent <- feishu:loanbot`
  - `local-commerce-agent <- feishu:commercebot`
  - `photo-polisher <- feishu:photobot`
  - `sales-agent <- feishu:salesbot`
  - `legal-agent <- feishu:legalbot`

今天本机 `openclaw channels status --probe --json` 已确认以上 9 个飞书实例全部：

- `configured = true`
- `running = true`
- `probe.ok = true`

也就是说：

- `default` 一直保留给原主机器人
- 每新建一只，就沉淀为一个新的独立 `accountId`
- 8 个专业 Agent 已全部拥有自己的独立飞书实例

## 8. 查看当前飞书实例和绑定

### 8.1 查看飞书实例

```bash
openclaw channels status --probe --json
```

### 8.2 查看 Agent 绑定

```bash
openclaw agents bindings --json
```

## 9. 推荐命名规范

建议统一用这套：

```text
stockbot          -> stock-agent
educationbot      -> education-agent
newsbot           -> news-agent
loanbot           -> loan-agent
commercebot       -> local-commerce-agent
photobot          -> photo-polisher
salesbot          -> sales-agent
legalbot          -> legal-agent
```

机器人中文名建议：

- 股票机器人
- 教育机器人
- 资讯机器人
- 助贷机器人
- 电商机器人
- 修图机器人
- 销售机器人
- 法务机器人

## 10. 典型完整操作顺序

推荐以后统一使用“一条命令 + 扫码”的方式。

以 `news-agent` 为例：

1. 执行：

```bash
python3 /Users/waylon/.openclaw/workspace/feishu_create_and_bind_bot.py \
  --account-id newsbot \
  --name 资讯机器人 \
  --agent news-agent
```

2. 用飞书扫码创建机器人
3. 其余步骤自动完成：
   - 不复用旧 `default`
   - 创建新机器人
   - 沉淀为 `newsbot`
   - 恢复旧 `default`
   - 绑定 `news-agent`
   - 重启 gateway

4. 验证：

```bash
openclaw channels status --probe --json
openclaw agents bindings --json
```

## 11. 常见问题排查

### 11.1 扫码后没有新增第三个实例

先看：

```bash
openclaw channels status --probe --json
```

如果还只有 `default`：

- 说明扫码创建没有真正成功
- 或飞书侧还没确认完成

### 11.2 新机器人把 `default` 覆盖了

这是官方安装器默认行为，不是异常。

正确处理不是手改配置，而是马上运行：

```bash
python3 /Users/waylon/.openclaw/workspace/feishu_capture_new_bot.py \
  --account-id <new-account-id> \
  --name <中文名> \
  --agent <agent-id>
```

### 11.3 为什么不用一个飞书实例绑定多个 Agent

因为这套平台的原则就是：

- 一个渠道实例只绑定一个 Agent
- 不做业务总控分发
- 每个 Agent 独立人格、独立记忆、独立决策

## 12. 安装成功判定标准

满足以下条件，才算今天这套本地安装方式真正完成：

- 8 个 Agent 已通过 `openclaw agents add` 安装
- 每个 Agent 有自己的 workspace 和 identity
- 飞书每新建一只机器人，都被沉淀成新的 `accountId`
- 旧 `default` 不丢
- `openclaw agents bindings --json` 能看到“一只机器人对应一个 Agent”
