from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """当前调用上下文。

    每个 Agent 只看到自己这一条调用链上下文，不共享默认工作方式与决策。
    """

    tenant_id: str
    agent_id: str
    channel_instance_id: str
    user_id: str | None = None
    memory_namespace: str | None = None
    config: dict[str, Any] = field(default_factory=dict)


class AgentBase:
    """平行 Agent 基类，只承载当前 Agent 自己的脑子。"""

    agent_id: str = ""
    zh_name: str = ""

    def __init__(self, soul: dict[str, Any], prompts: dict[str, str], skills: list[str]) -> None:
        self.soul = soul
        self.prompts = prompts
        self.skills = skills

    def can_handle(self, task_type: str) -> bool:
        return True

    def build_system_prompt(self, context: AgentContext) -> str:
        return self.prompts.get("system", "")

    def invoke(self, context: AgentContext, message: str) -> dict[str, Any]:
        """骨架调用入口。

        当前先回显 Agent 已收到请求，后续可在各专业 Agent 子类里覆盖。
        """

        return {
            "agent_id": self.agent_id,
            "reply": f"{self.zh_name} 已收到请求：{message}",
            "context": context.memory_namespace,
        }
