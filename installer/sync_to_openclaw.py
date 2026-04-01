from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_WORKSPACES = ROOT / ".platform" / "workspaces"


def extract_agent_name(soul_path: Path, fallback: str) -> str:
    if not soul_path.exists():
        return fallback
    for line in soul_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            return stripped.split(":", 1)[1].strip() or fallback
    return fallback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="把项目内 Agent workspace 模板同步到本机 OpenClaw 运行目录")
    parser.add_argument("agent_id", help="要同步的 Agent ID")
    parser.add_argument("--openclaw-home", default=str(Path.home() / ".openclaw"), help="OpenClaw 根目录")
    parser.add_argument("--execute", action="store_true", help="同步后尝试直接执行官方 openclaw agents add / set-identity")
    return parser


def sync_workspace(agent_id: str, openclaw_home: Path) -> dict:
    source_workspace = STATE_WORKSPACES / agent_id
    if not source_workspace.exists():
        raise FileNotFoundError(f"未找到本地模板工作区: {source_workspace}")

    target_workspace = openclaw_home / "workspaces" / agent_id
    target_state_dir = openclaw_home / "agents" / agent_id / "agent"
    source_agent_dir = ROOT / "agents" / agent_id

    if target_workspace.exists():
        shutil.rmtree(target_workspace)
    target_workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_workspace, target_workspace)
    target_state_dir.mkdir(parents=True, exist_ok=True)

    name = extract_agent_name(source_agent_dir / "soul.yaml", agent_id)

    return {
        "agent_id": agent_id,
        "agent_name": name,
        "source_workspace": str(source_workspace),
        "target_workspace": str(target_workspace),
        "target_state_dir": str(target_state_dir),
        "identity_file": str(target_workspace / "IDENTITY.md"),
    }


def run_openclaw_commands(agent_id: str, target_workspace: str, target_state_dir: str, identity_file: str) -> None:
    subprocess.run(
        [
            "openclaw",
            "agents",
            "add",
            "--agent",
            agent_id,
            "--workspace",
            target_workspace,
            "--agent-dir",
            target_state_dir,
        ],
        check=True,
    )
    subprocess.run(
        [
            "openclaw",
            "agents",
            "set-identity",
            "--agent",
            agent_id,
            "--identity-file",
            identity_file,
        ],
        check=True,
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    openclaw_home = Path(args.openclaw_home).expanduser()
    result = sync_workspace(args.agent_id, openclaw_home)

    print("已把项目模板同步到 OpenClaw 运行目录")
    print(f"- agent_id: {result['agent_id']}")
    print(f"- agent_name: {result['agent_name']}")
    print(f"- source_workspace: {result['source_workspace']}")
    print(f"- target_workspace: {result['target_workspace']}")
    print(f"- target_state_dir: {result['target_state_dir']}")

    add_cmd = (
        f"openclaw agents add --agent {result['agent_id']} "
        f"--workspace {result['target_workspace']} --agent-dir {result['target_state_dir']}"
    )
    identity_cmd = (
        f"openclaw agents set-identity --agent {result['agent_id']} "
        f"--identity-file {result['identity_file']}"
    )
    print("- 推荐下一步官方命令:")
    print(f"  {add_cmd}")
    print(f"  {identity_cmd}")

    if args.execute:
        run_openclaw_commands(
            args.agent_id,
            result["target_workspace"],
            result["target_state_dir"],
            result["identity_file"],
        )
        print("已执行 OpenClaw agents add / set-identity")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
