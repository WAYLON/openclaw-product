from __future__ import annotations

from typing import Any


class CredentialResolver:
    """按作用域优先级解析凭证。

    默认顺序：
    account -> channel -> agent -> tenant -> platform
    """

    scope_order = ["account", "channel", "agent", "tenant", "platform"]

    def resolve(self, credential_name: str, scopes: dict[str, dict[str, Any]]) -> tuple[str | None, str | None]:
        for scope in self.scope_order:
            value = scopes.get(scope, {}).get(credential_name)
            if value:
                return scope, value
        return None, None
