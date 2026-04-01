from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_WORKSPACES = ROOT / ".platform" / "workspaces"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_agent_name(soul_path: Path, fallback: str) -> str:
    if not soul_path.exists():
        return fallback
    for line in soul_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            return stripped.split(":", 1)[1].strip() or fallback
    return fallback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="把项目内 Agent workspace 模板同步到本机 OpenClaw 多 Agent 目录")
    parser.add_argument("agent_id", help="要同步的 Agent ID")
    parser.add_argument("--openclaw-home", default=str(Path.home() / ".openclaw"), help="OpenClaw 根目录")
    parser.add_argument("--parallel-root", default="", help="平行 Agent 根目录，默认使用 <openclaw-home>/parallel-agents")
    parser.add_argument("--execute", action="store_true", help="同步后尝试直接执行官方 openclaw agents add / set-identity")
    return parser


def sync_workspace(agent_id: str, openclaw_home: Path, parallel_root: Path) -> dict:
    source_workspace = STATE_WORKSPACES / agent_id
    if not source_workspace.exists():
        raise FileNotFoundError(f"未找到本地模板工作区: {source_workspace}")

    target_workspace = parallel_root / "workspaces" / agent_id
    target_state_dir = parallel_root / "state" / agent_id / "agent"
    target_package_dir = parallel_root / "packages" / agent_id
    registry_file = parallel_root / "registry.json"
    source_package_dir = ROOT / "packages" / agent_id
    source_agent_dir = ROOT / "agents" / agent_id

    if target_workspace.exists():
        shutil.rmtree(target_workspace)
    target_workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_workspace, target_workspace)
    target_state_dir.mkdir(parents=True, exist_ok=True)
    if target_package_dir.exists():
        shutil.rmtree(target_package_dir)
    target_package_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_package_dir, target_package_dir)

    registry = read_json(registry_file) or {}
    installed_at = registry.get("installed_at") or datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    agents = registry.get("agents")
    if not isinstance(agents, list):
        agents = []

    name = extract_agent_name(source_agent_dir / "soul.yaml", agent_id)

    entry = {
        "id": agent_id,
        "name": name,
        "workspace": str(target_workspace),
        "agent_dir": str(target_state_dir),
        "package_dir": str(target_package_dir),
        "synced_at": datetime.now().isoformat(timespec="seconds"),
        "source_workspace": str(source_workspace),
    }
    kept = [item for item in agents if item.get("id") != agent_id]
    kept.append(entry)
    registry = {
        "installed_at": installed_at,
        "agents": kept,
    }
    write_json(registry_file, registry)

    return {
        "agent_id": agent_id,
        "source_workspace": str(source_workspace),
        "target_workspace": str(target_workspace),
        "target_state_dir": str(target_state_dir),
        "target_package_dir": str(target_package_dir),
        "identity_file": str(target_workspace / "IDENTITY.md"),
        "registry_file": str(registry_file),
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
    parallel_root = Path(args.parallel_root).expanduser() if args.parallel_root else openclaw_home / "parallel-agents"
    result = sync_workspace(args.agent_id, openclaw_home, parallel_root)

    print("已把项目模板同步到 OpenClaw 平行 Agent 目录")
    print(f"- agent_id: {result['agent_id']}")
    print(f"- source_workspace: {result['source_workspace']}")
    print(f"- target_workspace: {result['target_workspace']}")
    print(f"- target_state_dir: {result['target_state_dir']}")
    print(f"- target_package_dir: {result['target_package_dir']}")
    print(f"- registry_file: {result['registry_file']}")

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
