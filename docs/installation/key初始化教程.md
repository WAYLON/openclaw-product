# Key 初始化教程

> 规则：第一次命中需要凭证的技能或第三方能力时，如果没配置，不允许直接报错，必须先返回中文初始化提示。

## 1. 哪些技能或第三方能力需要 Key

常见需要 Key 的能力包括：
- `openclaw-tavily-search`
- `qveris-official`
- `OpenMAIC`
- `OpenMAIC ASR`
- `OpenMAIC TTS`
- `Quizzle`
- `Moodle`
- `EspoCRM`
- `Formbricks`
- `n8n`
- `Cal.com`
- `Documenso`
- `Chatwoot`
- `UVdesk`
- `Strapi`
- `Directus`
- `Payload`
- `RSSHub` 某些私有接入

## 2. 第一次触发时如何提示

统一由以下组件处理：
- `key_init_guard`
- `credential_resolver`
- `secret_scope_policy`
- `first_run_init_prompt`
- `init_status_store`

提示示例：

```text
当前还不能继续执行，因为缺少必要凭证：openmaic_api_key

这个 Key 的用途：
用于访问 OpenMAIC 课程生成与互动课堂能力。

你可以在以下位置配置：
1. 平台级默认配置
2. 租户级配置
3. Agent 级配置
4. 渠道级配置
5. 当前账号覆盖配置

配置完成后，请回复：
已配置 openmaic_api_key
```

语音场景提示示例：

```text
当前还不能继续执行，因为缺少必要凭证：openmaic_tts_api_key

这个 Key 的用途：
用于把讲义、提纲、课堂提示词转换成中文语音播报内容。

你可以在以下位置配置：
1. 平台级默认配置
2. 租户级配置
3. Agent 级配置
4. 渠道级配置
5. 当前账号覆盖配置

配置完成后，请回复：
已配置 openmaic_tts_api_key
```

## 3. 如何配置 Key

### 3.1 推荐命令

按 Agent 级写入：

```bash
./agent-platform secret set education-agent openmaic_api_key --value "your-key" --scope agent
./agent-platform secret set education-agent openmaic_asr_api_key --value "your-key" --scope agent
./agent-platform secret set education-agent openmaic_tts_api_key --value "your-key" --scope agent
```

按租户级写入：

```bash
./agent-platform secret set demo-tenant tavily_api_key --value "your-key" --scope tenant
```

按渠道级写入：

```bash
./agent-platform secret set feishu-edu-bot app_secret --value "your-secret" --scope channel
```

### 3.2 查看已配置 Key

```bash
./agent-platform secret list education-agent --scope agent
```

输出示例：

```text
openmaic_api_key=***
```

### 3.3 删除 Key

```bash
./agent-platform secret remove education-agent openmaic_api_key --scope agent
```

## 4. 如何验证 Key 生效

### 4.1 看是否已写入状态目录

```bash
find .platform/secrets -maxdepth 3 -type f | sort
cat .platform/secrets/agent/education-agent.json
```

### 4.2 看命令行输出

如果成功，CLI 会输出：

```text
已写入密钥：scope=agent target=education-agent key=openmaic_api_key
```

### 4.3 看业务侧行为

后续当 Agent 再次命中对应技能或第三方能力时：
- 不应再提示缺少 Key
- 应进入下一步执行流程

## 5. 配置层次说明

当前优先级顺序：
1. `account`
2. `channel`
3. `agent`
4. `tenant`
5. `platform`

也就是：
- 当前账号配置会覆盖渠道配置
- 渠道配置会覆盖 Agent 配置
- Agent 配置会覆盖租户配置
- 租户配置会覆盖平台默认值

## 6. 常见报错排查

### 我已经配了 Key，还是提示缺失

先检查作用域是不是配错了：

```bash
./agent-platform secret list education-agent --scope agent
./agent-platform secret list demo-tenant --scope tenant
```

### Key 配到了 tenant，但当前 Agent 还是不生效

先确认后续实现里是否允许从 tenant scope 继承；当前骨架已经预留了这套顺序。

### 我不想把 Key 配在 Agent 级

可以配在：
- `platform`
- `tenant`
- `channel`
- `account`

## 7. 建议实践

- 通用服务放 `tenant` 或 `platform`
- 特定业务服务放 `agent`
- 特定机器人实例放 `channel`
- 特定老师 / 账号覆盖放 `account`
