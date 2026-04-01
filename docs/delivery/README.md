# 交付与升级文档目录

这个目录主要给实施、交付、升级和版本维护使用。

## 推荐阅读顺序

1. [实施交付清单.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/实施交付清单.md)
2. [版本发布流程.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本发布流程.md)
3. [角色验收模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/角色验收模板.md)
4. [专有技能新增规范.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/专有技能新增规范.md)
5. [版本迁移模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/版本迁移模板.md)
6. [回滚模板.md](/Users/waylon/Desktop/openclaw-product/docs/delivery/回滚模板.md)

## 怎么用

- 要做首发交付：
  - 先看 `实施交付清单`
- 要发新版本：
  - 先看 `版本发布流程`
- 要按角色做最小场景验收：
  - 先看 `角色验收模板`
- 要给某个 Agent 新增专有技能：
  - 先看 `专有技能新增规范`
- 要给老客户升级：
  - 先看 `版本迁移模板`
- 要回滚新增 skill：
  - 看 `回滚模板`

## 当前原则

- 所有安装动作优先走官方文档
- 本项目只补当前 7 角色的交付结构
- 老客户升级走迁移，不走覆盖
- 新 skill 默认按可选启用处理

## 当前可执行检查入口

- `make delivery-check`
  - 仓库交付结构检查
- `make acceptance`
  - 本机 OpenClaw 最小验收
- `./agent-platform acceptance --scenario`
  - 按角色验收模板执行场景问题
- `./agent-platform acceptance --scenario --report <path>`
  - 按角色执行并把结果落成验收记录
- `./agent-platform agent cleanup`
  - 清理项目内已经失效的旧 Agent 安装记录
