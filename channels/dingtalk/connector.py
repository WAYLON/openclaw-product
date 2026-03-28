from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class DingtalkAdapter(ChannelAdapterBase):
    """钉钉渠道适配器。"""

    channel_type = "dingtalk"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("robot_code", "")
        if not instance_id:
            raise ValueError("钉钉消息缺少 robot_code，无法确定绑定实例。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("sender_staff_id", ""),
            text=payload.get("text", {}).get("content"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：后续可接钉钉机器人或应用发送接口。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
