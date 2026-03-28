from __future__ import annotations


class SecretScopePolicy:
    """定义平台中凭证查找、覆盖和回退的统一顺序。

    设计目标：
    - 先允许更细粒度范围覆盖更粗粒度范围
    - 保持平台默认值可作为首发演示兜底
    - 允许某个 Agent、渠道或账号在不改全局配置的前提下单独覆写
    """

    default_order = ["account", "channel", "agent", "tenant", "platform"]

    def resolve_order(self, custom_order: list[str] | None = None) -> list[str]:
        order = custom_order or self.default_order
        allowed = set(self.default_order)
        invalid = [scope for scope in order if scope not in allowed]
        if invalid:
            joined = "、".join(invalid)
            raise ValueError(f"存在不支持的 secret scope：{joined}")
        return order

    def explain_order(self, custom_order: list[str] | None = None) -> list[str]:
        order = self.resolve_order(custom_order)
        mapping = {
            "account": "账号级覆盖，适合某个具体用户或座席的专属凭证。",
            "channel": "渠道级覆盖，适合同一个 Agent 在不同渠道使用不同密钥。",
            "agent": "Agent 级覆盖，适合某个专业 Agent 单独配置第三方能力。",
            "tenant": "租户级覆盖，适合同一客户组织范围内统一配置。",
            "platform": "平台级默认值，适合作为首发演示或公共兜底配置。",
        }
        return [f"{scope}: {mapping[scope]}" for scope in order]
