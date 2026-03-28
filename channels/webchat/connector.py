from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class WebChatAdapter(ChannelAdapterBase):
    """Web Chat / H5 聊天入口适配器。"""

    channel_type = "webchat"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("widget_id", "")
        if not instance_id:
            raise ValueError("Web Chat 请求缺少 widget_id，无法确定绑定实例。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("visitor_id", ""),
            text=payload.get("text"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：可继续扩展为 WebSocket、SSE 或 REST 回包。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
