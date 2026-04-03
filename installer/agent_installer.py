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
        self._write_workspace_files(request.target_agent_id, source_agent_dir, package_dir, workspace_dir)

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
        copy_dirs = ["skills"]
        for dirname in copy_dirs:
            source_dir = source_agent_dir / dirname
            if source_dir.exists():
                shutil.copytree(source_dir, workspace_dir / dirname, dirs_exist_ok=True)

        copy_files = ["soul.yaml", "AGENTS.md", "IDENTITY.md"]
        for filename in copy_files:
            source_file = source_agent_dir / filename
            if source_file.exists():
                shutil.copy2(source_file, workspace_dir / filename)

        shutil.copytree(package_dir, workspace_dir / "delivery-package", dirs_exist_ok=True)

    def _write_workspace_files(
        self,
        agent_id: str,
        source_agent_dir: Path,
        package_dir: Path,
        workspace_dir: Path,
    ) -> None:
        soul_text = (source_agent_dir / "soul.yaml").read_text(encoding="utf-8") if (source_agent_dir / "soul.yaml").exists() else ""

        workspace_files = {
            "SOUL.md": self._build_soul_md(agent_id, soul_text),
            "USER.md": self._build_user_md(agent_id),
            "TOOLS.md": self._build_tools_md(agent_id),
            "HEARTBEAT.md": self._build_heartbeat_md(agent_id),
            "MEMORY.md": self._build_memory_md(agent_id),
        }

        for filename, content in workspace_files.items():
            target = workspace_dir / filename
            if not target.exists():
                target.write_text(content, encoding="utf-8")

    def _build_soul_md(self, agent_id: str, soul_text: str) -> str:
        return f"""# {agent_id} 工作区配置

以下内容来自 `soul.yaml`，用于生成该 Agent 的默认工作方式、边界与风格：

```yaml
{soul_text.rstrip()}
```
"""

    def _build_identity_md(self, agent_id: str) -> str:
        return f"""# {agent_id} 身份说明

你是 `{agent_id}` 的独立专业 Agent。

要求：
- 只处理本专业范围内的问题
- 默认使用中文回答
- 不假装自己是总控调度器
- 不替其他 Agent 做专业判断
"""

    def _build_user_md(self, agent_id: str) -> str:
        return f"""# {agent_id} 用户上下文

这里用于补充该 Agent 的客户画像、使用场景和教学重点。

当前默认规则：
- 优先面向中文客户
- 回答尽量结构化
- 便于老师讲解与演示
"""

    def _build_tools_md(self, agent_id: str) -> str:
        return f"""# {agent_id} 工具与技能说明

## 使用顺序
1. 先用本工作区 `skills/` 里的专业技能
2. 再用本工作区 `skills/` 里的基础技能
3. 不通过独立封装层，第三方系统能力也直接放在当前 Agent 的 `skills/` 目录中

## 对外回答规则
- 当用户询问“你有哪些技能”“你的专业技能是什么”“你会什么”“你能做什么”时，必须先读取本工作区 `skills/` 目录。
- 回答时先列专有技能，再列共享技能，不要只做抽象能力概括。

## 约束
- 不直接把第三方系统当作业务脑子
- 不跨 Agent 共享默认工作方式和记忆
"""

    def _build_heartbeat_md(self, agent_id: str) -> str:
        return f"""# {agent_id} Heartbeat 检查清单

- 当前模型是否正确
- 当前渠道是否绑定正确
- 需要的 Key 是否已初始化
- 专业技能是否能正常调用
- 对外回复是否保持中文风格
"""

    def _build_memory_md(self, agent_id: str) -> str:
        return f"""# {agent_id} Memory 说明

- 记忆命名空间：`memory/{agent_id}`
- 不与其他 Agent 共用业务决策记忆
- 共享的是工具，不共享默认工作方式与结论
"""
