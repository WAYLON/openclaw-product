from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InitStatus:
    tenant_id: str
    agent_id: str
    channel_instance_id: str
    credential_name: str
    status: str


class InitStatusStore:
    """记录首次初始化提示状态。

    当前是内存实现，后续可替换为文件或数据库存储。
    """

    def __init__(self) -> None:
        self._store: dict[str, InitStatus] = {}

    def _key(self, tenant_id: str, agent_id: str, channel_instance_id: str, credential_name: str) -> str:
        return f"{tenant_id}:{agent_id}:{channel_instance_id}:{credential_name}"

    def set(self, item: InitStatus) -> None:
        self._store[self._key(item.tenant_id, item.agent_id, item.channel_instance_id, item.credential_name)] = item

    def get(self, tenant_id: str, agent_id: str, channel_instance_id: str, credential_name: str) -> InitStatus | None:
        return self._store.get(self._key(tenant_id, agent_id, channel_instance_id, credential_name))
