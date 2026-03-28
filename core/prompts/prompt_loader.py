from __future__ import annotations

from pathlib import Path


class PromptLoader:
    """加载某个 Agent 的 prompt 文件。

    约定：
    - `system.prompt.md` 对应系统主提示词
    - `channel_reply.prompt.md` 对应渠道回复口径
    - 后续可以扩展更多 prompt 文件，但命名仍建议保持清晰
    """

    def __init__(self, agent_dir: Path) -> None:
        self.agent_dir = agent_dir

    def load(self) -> dict[str, str]:
        prompts_dir = self.agent_dir / "prompts"
        if not prompts_dir.exists():
            raise FileNotFoundError(f"未找到 prompts 目录：{prompts_dir}")
        result = {}
        for path in prompts_dir.glob("*.md"):
            result[path.stem] = path.read_text(encoding="utf-8")
        return result
