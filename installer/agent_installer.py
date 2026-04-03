from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from installer.validate_package import validate_package


@dataclass
class InstallRequest:
    """一次安装请求。

    设计目标：
    - 安装动作只处理目标 Agent，自身不顺带改其他 Agent。
    - 安装结果尽量贴近 OpenClaw 原生多 Agent workspace 形态。
    """

    package_id: str
    tenant_id: str
    channel_instance_id: str
    target_agent_id: str


@dataclass
class InstallResult:
    agent_id: str
    package_dir: Path
    source_agent_dir: Path
    workspace_dir: Path


class AgentInstaller:
    """把一个 Agent 源目录装配成可同步到 OpenClaw 的 workspace 模板。"""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.platform_dir = root / ".platform"
        self.workspaces_dir = self.platform_dir / "workspaces"

    def install(self, request: InstallRequest) -> InstallResult:
        package_dir = self.root / "packages" / request.package_id
        source_agent_dir = self.root / "agents" / request.target_agent_id
        if not package_dir.exists():
            raise FileNotFoundError(f"未找到包目录: {package_dir}")
        if not source_agent_dir.exists():
            raise FileNotFoundError(f"未找到 Agent 源目录: {source_agent_dir}")
        if request.package_id != request.target_agent_id:
            raise ValueError("安装请求不合法：package_id 与 target_agent_id 必须一致。")
        validation_errors = validate_package(package_dir, source_agent_dir)
        if validation_errors:
            joined = "\n- ".join(validation_errors)
            raise ValueError(f"Agent 安装前校验未通过：\n- {joined}")

        workspace_dir = self.workspaces_dir / request.target_agent_id
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)
        workspace_dir.mkdir(parents=True, exist_ok=True)

        self._copy_workspace_assets(source_agent_dir, package_dir, workspace_dir)

        return InstallResult(
            agent_id=request.target_agent_id,
            package_dir=package_dir,
            source_agent_dir=source_agent_dir,
            workspace_dir=workspace_dir,
        )

    def uninstall_workspace(self, agent_id: str) -> Path:
        workspace_dir = self.workspaces_dir / agent_id
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)
        return workspace_dir

    def _copy_workspace_assets(self, source_agent_dir: Path, package_dir: Path, workspace_dir: Path) -> None:
        source_dir = source_agent_dir / "skills"
        if source_dir.exists():
            shutil.copytree(source_dir, workspace_dir / "skills", dirs_exist_ok=True)

        shutil.copytree(package_dir, workspace_dir / "delivery-package", dirs_exist_ok=True)
