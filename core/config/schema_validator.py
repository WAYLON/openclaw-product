from __future__ import annotations

from pathlib import Path


class SchemaValidationError(ValueError):
    """配置结构不满足平台最低要求。"""


def validate_install_manifest(payload: dict, source: Path | None = None) -> None:
    location = str(source) if source else "install-manifest.yaml"
    if "package" not in payload:
        raise SchemaValidationError(f"{location} 缺少顶层字段：package")
    package = payload.get("package") or {}
    for key in ["id", "display_name", "language", "install_mode", "includes", "supports"]:
        if key not in package:
            raise SchemaValidationError(f"{location} 的 package 缺少字段：{key}")
