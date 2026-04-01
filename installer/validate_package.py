from __future__ import annotations

from pathlib import Path

from core.config.schema_validator import validate_install_manifest, SchemaValidationError
from core.config.config_loader import ConfigLoader


REQUIRED_SUPPORT_FILES = [
    "README.md",
    "config/install-manifest.yaml",
    "examples/trainer-demo-script.md",
]

REQUIRED_AGENT_FILES = [
    "soul.yaml",
    "AGENTS.md",
    "IDENTITY.md",
]


def validate_package(package_dir: Path, source_agent_dir: Path | None = None) -> list[str]:
    """校验专业包是否满足正式交付最低要求。

    这里校验的不是业务效果，而是交付完整性：
    - 包级 README
    - 安装清单
    - 讲师演示脚本
    - 五份核心交付文档
    """

    if not package_dir.exists():
        return [f"包目录不存在：{package_dir}"]
    missing = []

    for relpath in REQUIRED_SUPPORT_FILES:
        if not (package_dir / relpath).exists():
            missing.append(relpath)

    required_package_docs = ["quickstart.md", "user-guide.md", "trainer-guide.md", "faq.md", "examples.md"]
    for name in required_package_docs:
        if not (package_dir / "docs" / name).exists():
            missing.append(f"docs/{name}")

    if source_agent_dir is not None:
        if not source_agent_dir.exists():
            missing.append(f"Agent 源目录不存在：{source_agent_dir}")
        else:
            for relpath in REQUIRED_AGENT_FILES:
                if not (source_agent_dir / relpath).exists():
                    missing.append(f"agent/{relpath}")

    if missing:
        return missing

    try:
        manifest_loader = ConfigLoader(package_dir.parent.parent)
        manifest_payload = manifest_loader.load_yaml(str(package_dir.relative_to(manifest_loader.root) / "config" / "install-manifest.yaml"))
        validate_install_manifest(manifest_payload, package_dir / "config" / "install-manifest.yaml")
    except (SchemaValidationError, RuntimeError, FileNotFoundError) as exc:
        missing.append(str(exc))
    return missing
