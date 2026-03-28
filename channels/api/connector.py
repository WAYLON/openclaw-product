from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class ApiAdapter(ChannelAdapterBase):
    """API 调用入口适配器。"""

    channel_type = "api"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("api_client_id", "")
        if not instance_id:
            raise ValueError("API 请求缺少 api_client_id，无法确定绑定实例。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("caller_id", ""),
            text=payload.get("text"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：后续可扩展 trace_id、usage、debug 元数据。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
