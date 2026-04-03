from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLATFORM_DIR = ROOT / ".platform"
AGENTS_DIR = PLATFORM_DIR / "agents"
WORKSPACES_DIR = PLATFORM_DIR / "workspaces"
SECRETS_DIR = PLATFORM_DIR / "secrets"
RUNTIME_FILE = PLATFORM_DIR / "runtime.json"
PLATFORM_FILE = PLATFORM_DIR / "platform.json"
EXPECTED_AGENT_COUNT = 6

REQUIRED_TOP_LEVEL_DIRS = [
    "core",
    "channels",
    "agents",
    "packages",
    "installer",
    "docs",
]

REQUIRED_ENGINEERING_FILES = [
    "pyproject.toml",
    ".gitignore",
    "Makefile",
    "agent-platform",
]

REQUIRED_PLATFORM_DOCS = [
    "docs/architecture/平台总体架构与交付设计.md",
    "docs/installation/平台安装教程.md",
    "docs/guides/老师讲解总提纲.md",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_runtime_dirs() -> None:
    for path in [
        PLATFORM_DIR,
        AGENTS_DIR,
        WORKSPACES_DIR,
        SECRETS_DIR / "platform",
        SECRETS_DIR / "tenant",
        SECRETS_DIR / "agent",
        SECRETS_DIR / "channel",
        SECRETS_DIR / "account",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def validate_project_structure() -> list[str]:
    issues: list[str] = []
    for dirname in REQUIRED_TOP_LEVEL_DIRS:
        if not (ROOT / dirname).exists():
            issues.append(f"缺少目录：{dirname}")
    for relpath in REQUIRED_ENGINEERING_FILES:
        if not (ROOT / relpath).exists():
            issues.append(f"缺少工程文件：{relpath}")
    for relpath in REQUIRED_PLATFORM_DOCS:
        if not (ROOT / relpath).exists():
            issues.append(f"缺少平台文档：{relpath}")
    agent_count = len(list((ROOT / "agents").glob("*/soul.yaml")))
    if agent_count < EXPECTED_AGENT_COUNT:
        issues.append(f"业务 Agent 模板数量不足 {EXPECTED_AGENT_COUNT} 个，当前仅有 {agent_count} 个")
    return issues


def default_platform_payload() -> dict:
    return {
        "initialized_at": now_iso(),
        "default_model": {
            "provider": "local-proxy",
            "model": "gpt-5.4",
            "reasoning_effort": "medium",
        },
        "permission_profile": "default_open_profile",
        "tools": {
            "profile": "full",
            "also_allow": ["exec"],
        },
        "locale": "zh-CN",
        "docs_language": "zh-CN",
        "notes": [
            "本平台采用平行 Agent 架构。",
            "当前推荐运行态为 7 个 Agent：1 个 main + 6 个业务 Agent。",
            "一个渠道实例只绑定一个 Agent。",
            "Soul、Prompt、文档与讲师资料默认中文。",
        ],
    }


def default_runtime_payload() -> dict:
    return {
        "started": False,
        "started_at": None,
        "mode": "delivery-skeleton",
        "message": "平台已完成初始化，待执行启动命令。",
    }


def ensure_platform_state(force: bool = False) -> None:
    ensure_runtime_dirs()
    if force or not PLATFORM_FILE.exists():
        write_json(PLATFORM_FILE, default_platform_payload())
    if force or not RUNTIME_FILE.exists():
        write_json(RUNTIME_FILE, default_runtime_payload())


def cmd_run(args: argparse.Namespace) -> int:
    issues = validate_project_structure()
    if issues:
        print("项目结构校验失败：")
        for issue in issues:
            print(f"- {issue}")
        return 1

    ensure_platform_state(force=args.force)
    source_agent_count = len(list((ROOT / "agents").glob("*/soul.yaml")))
    installed_agent_count = len(list(AGENTS_DIR.glob("*.json")))

    print("平台初始化脚本执行完成")
    print(f"- 项目根目录: {ROOT}")
    print(f"- 平台状态文件: {PLATFORM_FILE}")
    print(f"- 运行状态文件: {RUNTIME_FILE}")
    print(f"- 可安装 Agent 模板数: {source_agent_count}")
    print(f"- 当前已安装 Agent 数: {installed_agent_count}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    issues = validate_project_structure()
    if not PLATFORM_FILE.exists():
        issues.append("缺少 .platform/platform.json，请先执行 bootstrap")
    if not RUNTIME_FILE.exists():
        issues.append("缺少 .platform/runtime.json，请先执行 bootstrap")
    if issues:
        print("检查未通过：")
        for issue in issues:
            print(f"- {issue}")
        return 1

    agent_states = sorted(AGENTS_DIR.glob("*.json"))
    agent_sources = sorted((ROOT / "agents").glob("*/soul.yaml"))
    print("检查通过")
    print(f"- Agent 模板数: {len(agent_sources)}")
    print(f"- 已安装 Agent 数: {len(agent_states)}")
    print(f"- 平台状态文件: {PLATFORM_FILE.exists()}")
    print(f"- 运行状态文件: {RUNTIME_FILE.exists()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bootstrap_project.py",
        description="OpenClaw 平行 Agent 安装平台初始化脚本",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="初始化平台运行态目录，不预装 Agent")
    run_parser.add_argument("--force", action="store_true", help="覆盖重建平台运行态文件")
    run_parser.set_defaults(func=cmd_run)

    check_parser = subparsers.add_parser("check", help="检查平台目录与运行态文件")
    check_parser.set_defaults(func=cmd_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
