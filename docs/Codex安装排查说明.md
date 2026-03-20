# Codex 安装排查说明

这个文档给内部技术安装人员使用。

目标是解决：

- Codex 命令装了但不能用
- Codex 能启动但认证失败
- Codex 环境和代理不一致
- Codex 本地配置损坏

## 一、先看最小前提

至少确认：

- `codex` 命令存在
- Node 版本正常
- 用户主目录可写
- `~/.codex/` 存在或可创建

推荐检查：

```bash
which codex
codex --help
node -v
```

## 二、配置目录检查

重点看：

- `~/.codex/config.toml`
- `~/.codex/auth.json`
- `~/.codex/accounts/`
- `~/.codex/sessions/`

常见问题：

- `auth.json` 损坏
- `accounts/` 下有旧认证残留
- `sessions/` 太脏
- 有 stale `.lock`

## 三、代理一致性检查

Codex 经常不是“装坏了”，而是：

- CLI 当前 shell 有代理
- GUI / App 进程没代理
- Node fetch 没读到环境变量

因此必须统一：

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `ALL_PROXY`
- `NO_PROXY`
- `NODE_USE_ENV_PROXY`

## 四、认证问题检查

常见表现：

- 浏览器能开
- 登录能过
- 回调能拿到
- 但最后拿 token 失败

这时不要死磕浏览器页面，优先检查：

- 本地代理
- 系统区域限制
- 账号风控
- 是否能复用本地已有认证

## 五、常见修复手段

### 1. 清理锁

查：

- `~/.codex/**/*.lock`

### 2. 备份并清理旧认证

先备份：

- `~/.codex/auth.json`
- `~/.codex/accounts/*.auth.json`

再决定是否重建认证。

### 3. 复用本地认证

如果当前机器已有有效官方客户端认证，可直接做认证复用，不必反复走网页登录。

## 六、安装人员推荐排查顺序

1. `codex --help` 是否正常
2. Node 版本是否正常
3. 代理是否统一
4. `~/.codex/auth.json` 是否存在
5. 是否有 stale lock
6. 是否能做最小请求

## 七、和 OpenClaw 的关系

Codex 排查时，很多网络和 OAuth 问题与 OpenClaw 共用一套根因：

- 代理不一致
- Node 环境没继承变量
- GUI 与 shell 环境不同
- 本地认证文件冲突

所以安装人员可以配合阅读：

- `OpenClaw-Codex-OAuth修复说明.md`

## 八、一句话总结

Codex 安装排查里最常见的误判不是“程序坏了”，而是：

**命令装好了，但代理、认证、运行时环境没统一。**
