from __future__ import annotations

from pathlib import Path

from core.config.schema_validator import validate_agent_config


class ConfigLoader:
    """统一读取 YAML 配置。

    当前只做最小读取，后续可扩展：
    - schema 校验
    - 环境变量覆盖
    - tenant / channel / agent merge
    """

    def __init__(self, root: Path) -> None:
        self.root = root

    def load_yaml(self, relative_path: str) -> dict:
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "缺少 PyYAML，请先执行 `python3 -m pip install -r requirements.txt` 或安装项目依赖。"
            ) from exc
        target = self.root / relative_path
        if not target.exists():
            raise FileNotFoundError(f"配置文件不存在：{target}")
        return yaml.safe_load(target.read_text(encoding="utf-8")) or {}

    def load_agent_config(self, relative_path: str) -> dict:
        payload = self.load_yaml(relative_path)
        validate_agent_config(payload, self.root / relative_path)
        return payload
