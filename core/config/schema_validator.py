from __future__ import annotations

from pathlib import Path


class SchemaValidationError(ValueError):
    """配置结构不满足平台最低要求。"""


def validate_agent_config(payload: dict, source: Path | None = None) -> None:
    location = str(source) if source else "agent.yaml"
    required_top_keys = ["id", "name", "model", "runtime", "skills", "docs"]
    missing = [key for key in required_top_keys if key not in payload]
    if missing:
        raise SchemaValidationError(f"{location} 缺少顶层字段：{', '.join(missing)}")

    model = payload.get("model") or {}
    for key in ["provider", "model", "reasoning_effort"]:
        if key not in model:
            raise SchemaValidationError(f"{location} 的 model 缺少字段：{key}")

    runtime = payload.get("runtime") or {}
    for key in ["memory_namespace", "permission_profile"]:
        if key not in runtime:
            raise SchemaValidationError(f"{location} 的 runtime 缺少字段：{key}")

    skills = payload.get("skills") or {}
    for key in ["layout", "catalog", "entries"]:
        if key not in skills:
            raise SchemaValidationError(f"{location} 的 skills 缺少字段：{key}")

    docs = payload.get("docs") or {}
    for key in ["quickstart", "user_guide", "trainer_guide", "faq", "examples"]:
        if key not in docs:
            raise SchemaValidationError(f"{location} 的 docs 缺少字段：{key}")


def validate_install_manifest(payload: dict, source: Path | None = None) -> None:
    location = str(source) if source else "install-manifest.yaml"
    if "package" not in payload:
        raise SchemaValidationError(f"{location} 缺少顶层字段：package")
    package = payload.get("package") or {}
    for key in ["id", "display_name", "language", "install_mode", "includes", "supports"]:
        if key not in package:
            raise SchemaValidationError(f"{location} 的 package 缺少字段：{key}")
