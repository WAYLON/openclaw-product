# OpenClaw/Codex OAuth 修复说明

这个文档给内部技术安装人员使用。

适用场景：

- OpenClaw OAuth 登录卡住
- Codex OAuth 登录卡住
- 网页授权成功但回调或换 token 失败
- 已有官方客户端本地认证，希望复用到目标应用

## 一、目标

修复分成两层：

1. 网络与运行时层
2. 认证与运行阻塞层

不要上来就死磕浏览器授权页面。

## 二、代理统一要求

统一使用：

- `HTTP_PROXY=http://127.0.0.1:7897`
- `HTTPS_PROXY=http://127.0.0.1:7897`
- `ALL_PROXY=http://127.0.0.1:7897`
- `NO_PROXY=localhost,127.0.0.1,::1`
- `NODE_USE_ENV_PROXY=1`

当前内部默认代理软件建议：

- Clash Verge

当前内部默认参考网络服务入口：

- [WgetCloud 官网](https://b8cfff2a4jquxdbmwbaj.wgetcloud.org/)
- [WgetCloud 用户消息页](https://b8cfff2a4jquxdbmwbaj.wgetcloud.org/user/message)

必须同时写到：

- 当前会话
- `~/.profile`
- 对应 shell 配置
- 应用运行时环境

## 三、平台兼容要求

### macOS

要检查：

- `launchctl setenv`
- LaunchAgent 的 `EnvironmentVariables`

### Linux

要检查：

- `systemd --user show-environment`
- `~/.config/environment.d/*.conf`
- `systemd --user` service override

## 四、代理验证要求

必须至少验证三件事：

1. `curl` 访问 https 目标能通
2. Node `fetch` 能通
3. `localhost` / `127.0.0.1` 不走代理

## 五、OAuth 排查顺序

OAuth 要分四段排查：

1. 授权页能否打开
2. 登录页能否成功
3. 本地回调能否拿到 `code`
4. `code` 能否换到 token

如果前三步都成功，但第四步报：

- `forbidden`
- `region`
- `risk`

就不要继续死磕网页登录链路，直接切换到：

- 本地认证复用

## 六、认证复用绕过

可从官方客户端本地认证文件中提取：

- `access_token`
- `refresh_token`
- `expires`
- `account_id` 或 `user_id`

再写入目标应用的 auth profile。

当前机器上可参考的文件：

- `~/.codex/auth.json`
- `~/.openclaw/identity/device-auth.json`

注意：

- 不要在日志中打印 token 明文
- 只做结构迁移

## 七、运行阻塞清理

修复前通常要清理：

- 僵尸进程
- `*.lock`
- `session.lock`
- stale gateway 状态

然后重启：

- gateway
- app
- service

## 八、仓库内置脚本

当前仓库已收编修复脚本：

- `scripts/openclaw-codex-oauth-repair.sh`

用途：

- 持久化代理环境
- 做 curl / Node / no_proxy 测试
- 清理锁和阻塞进程
- 重启 OpenClaw gateway
- 做最小请求验证

## 九、建议执行方式

```bash
chmod +x ./scripts/openclaw-codex-oauth-repair.sh
./scripts/openclaw-codex-oauth-repair.sh
```

如果要复用已有认证文件：

```bash
./scripts/openclaw-codex-oauth-repair.sh /path/to/auth-profiles.json
```

## 十、最终验收

以最小请求为准：

- `Reply with OK only.`

如果返回 `OK`，则视为链路恢复。
