from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class WebhookAdapter(ChannelAdapterBase):
    """通用 webhook 渠道适配器。"""

    channel_type = "webhook"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("instance_id", "")
        if not instance_id:
            raise ValueError("Webhook 请求缺少 instance_id，无法路由到绑定 Agent。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("sender_id", ""),
            text=payload.get("text"),
            attachments=payload.get("attachments"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：此结构可直接作为 webhook 响应体或交给上层发送器。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
