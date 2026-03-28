from __future__ import annotations

from dataclasses import dataclass

from core.secrets.credential_resolver import CredentialResolver
from core.secrets.first_run_init_prompt import build_first_run_init_prompt


@dataclass
class GuardResult:
    ok: bool
    init_prompt: str | None = None
    resolved_scope: str | None = None


class KeyInitGuard:
    """首次命中需要凭证的能力时，统一返回中文初始化提示。"""

    def __init__(self, resolver: CredentialResolver) -> None:
        self.resolver = resolver

    def ensure(self, credential_name: str, purpose: str, scopes: dict[str, dict]) -> GuardResult:
        scope, value = self.resolver.resolve(credential_name, scopes)
        if value:
            return GuardResult(ok=True, resolved_scope=scope)
        return GuardResult(
            ok=False,
            init_prompt=build_first_run_init_prompt(
                credential_name,
                purpose,
                [
                    "平台级默认配置",
                    "租户级配置",
                    "Agent 级配置",
                    "渠道级配置",
                    "当前账号覆盖配置",
                ],
            ),
        )
