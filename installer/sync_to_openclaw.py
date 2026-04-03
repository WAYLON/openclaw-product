from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_WORKSPACES = ROOT / ".platform" / "workspaces"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="把项目内 Agent workspace 模板同步到本机 OpenClaw 运行目录")
    parser.add_argument("agent_id", help="要同步的 Agent ID")
    parser.add_argument("--openclaw-home", default=str(Path.home() / ".openclaw"), help="OpenClaw 根目录")
    return parser


def sync_workspace(agent_id: str, openclaw_home: Path) -> dict:
    source_workspace = STATE_WORKSPACES / agent_id
    if not source_workspace.exists():
        raise FileNotFoundError(f"未找到本地模板工作区: {source_workspace}")

    target_workspace = openclaw_home / "workspaces" / agent_id
    target_state_dir = openclaw_home / "agents" / agent_id / "agent"
    if not target_workspace.exists():
        raise FileNotFoundError(f"未找到目标 OpenClaw Agent 工作区：{target_workspace}。请先执行官方命令创建 Agent。")
    source_skills = source_workspace / "skills"
    target_skills = target_workspace / "skills"
    if target_skills.exists():
        shutil.rmtree(target_skills)
    if source_skills.exists():
        shutil.copytree(source_skills, target_skills)

    return {
        "agent_id": agent_id,
        "source_workspace": str(source_workspace),
        "target_workspace": str(target_workspace),
        "target_state_dir": str(target_state_dir),
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    openclaw_home = Path(args.openclaw_home).expanduser()
    result = sync_workspace(args.agent_id, openclaw_home)

    print("已把项目技能同步到 OpenClaw 运行目录")
    print(f"- agent_id: {result['agent_id']}")
    print(f"- source_workspace: {result['source_workspace']}")
    print(f"- target_workspace: {result['target_workspace']}")
    print(f"- target_state_dir: {result['target_state_dir']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
