from __future__ import annotations

from pathlib import Path
import yaml


class SoulLoader:
    """加载某个 Agent 的 soul.yaml。"""

    def __init__(self, agent_dir: Path) -> None:
        self.agent_dir = agent_dir

    def load(self) -> dict:
        soul_path = self.agent_dir / "soul.yaml"
        if not soul_path.exists():
            raise FileNotFoundError(f"未找到 soul 文件：{soul_path}")
        return yaml.safe_load(soul_path.read_text(encoding="utf-8")) or {}
