from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ChannelEnvelope:
    """统一的渠道入站信封。

    约束：
    - 一个渠道实例只绑定一个 Agent。
    - 渠道层只负责接入和标准化，不做多业务 Agent 总控判断。
    """

    channel_type: str
    instance_id: str
    sender_id: str
    text: str | None = None
    attachments: list[dict[str, Any]] | None = None


class ChannelAdapterBase:
    """渠道适配层基类。

    子类只做三件事：
    1. 把渠道原始 payload 标准化为 `ChannelEnvelope`
    2. 把 Agent 回复包装成渠道可发送结构
    3. 解析当前实例绑定标识
    """

    channel_type = "base"

    def receive(self, payload: dict[str, Any]) -> ChannelEnvelope:
        raise NotImplementedError("子类必须实现 receive()，把渠道 payload 转成 ChannelEnvelope。")

    def reply(self, instance_id: str, message: str) -> dict[str, Any]:
        raise NotImplementedError("子类必须实现 reply()，把文本回复包装成渠道响应结构。")

    def resolve_instance_binding(self, instance_id: str) -> str:
        raise NotImplementedError("子类必须实现 resolve_instance_binding()，返回实例绑定键。")
