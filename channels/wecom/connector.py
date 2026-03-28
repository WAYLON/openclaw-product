from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class WecomAdapter(ChannelAdapterBase):
    """企业微信渠道适配器。"""

    channel_type = "wecom"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("agent_id", "")
        if not instance_id:
            raise ValueError("企业微信消息缺少 agent_id，无法确定绑定实例。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("from_user", ""),
            text=payload.get("content"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：后续可替换为企业微信机器人或应用回包结构。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
