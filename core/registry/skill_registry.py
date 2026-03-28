from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SkillSpec:
    """Skill 注册描述。"""

    skill_id: str
    source: str
    needs_key: bool
    risk_level: str


class SkillRegistry:
    """统一登记共享 skill 与专业 skill。"""

    def __init__(self) -> None:
        self._skills: dict[str, SkillSpec] = {}

    def register(self, spec: SkillSpec) -> None:
        if not spec.skill_id:
            raise ValueError("skill_id 不能为空。")
        self._skills[spec.skill_id] = spec

    def get(self, skill_id: str) -> SkillSpec | None:
        return self._skills.get(skill_id)
