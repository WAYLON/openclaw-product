from __future__ import annotations

from pathlib import Path

from installer.validate_package import validate_package


def build_package(root: Path, agent_id: str) -> Path:
    """构建某个 Agent 的交付包。

    当前版本先做“正式交付前检查”，目标不是压缩打包，而是保证：
    - 包目录存在
    - docs 交付物齐全
    - install-manifest 存在
    - 交付包达到可安装、可演示、可教学的最低标准

    后续可继续扩展：
    - zip / tar 产物生成
    - 校验和输出
    - 版本号写入
    - 发布仓库或对象存储上传
    """

    package_dir = root / "packages" / agent_id
    if not package_dir.exists():
        raise FileNotFoundError(f"未找到 Agent 包：{agent_id}")

    source_agent_dir = root / "agents" / agent_id
    missing = validate_package(package_dir, source_agent_dir)
    if missing:
        joined = "、".join(missing)
        raise ValueError(f"交付包校验未通过，缺少：{joined}")

    manifest = package_dir / "config" / "install-manifest.yaml"
    if not manifest.exists():
        raise FileNotFoundError(f"缺少安装清单：{manifest}")

    return package_dir
