from __future__ import annotations

from channels.base.connector import ChannelAdapterBase, ChannelEnvelope


class FeishuAdapter(ChannelAdapterBase):
    """飞书渠道适配器。

    当前骨架只做标准字段映射：
    - `app_id` -> 渠道实例
    - `sender_id` -> 发送者
    - `text` -> 文本内容
    """

    channel_type = "feishu"

    def receive(self, payload: dict) -> ChannelEnvelope:
        instance_id = payload.get("app_id", "")
        if not instance_id:
            raise ValueError("飞书消息缺少 app_id，无法确定绑定到哪个 Agent。")
        return ChannelEnvelope(
            channel_type=self.channel_type,
            instance_id=instance_id,
            sender_id=payload.get("sender_id", ""),
            text=payload.get("text"),
        )

    def reply(self, instance_id: str, message: str) -> dict:
        return {
            "channel": self.channel_type,
            "instance_id": instance_id,
            "message": message,
            "note": "骨架模式：此处返回飞书发送载荷，后续可接真实 SDK。",
        }

    def resolve_instance_binding(self, instance_id: str) -> str:
        return instance_id
