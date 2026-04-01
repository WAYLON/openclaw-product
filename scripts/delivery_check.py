from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_BUSINESS_AGENTS = {
    "education-agent",
    "stock-agent",
    "loan-agent",
    "social-media-agent",
    "news-agent",
    "sales-agent",
}


def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        return False, f"命令不存在: {' '.join(cmd)}"
    except subprocess.TimeoutExpired:
        return False, f"命令超时: {' '.join(cmd)}"
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit={result.returncode}"
        return False, detail
    return True, result.stdout.strip()


def check_file(path: Path) -> tuple[bool, str]:
    if path.exists():
        return True, str(path.relative_to(ROOT))
    return False, f"缺少文件: {path.relative_to(ROOT)}"


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    required_files = [
        ROOT / "README.md",
        ROOT / "docs" / "guides" / "README.md",
        ROOT / "docs" / "delivery" / "README.md",
        ROOT / "docs" / "installation" / "README.md",
        ROOT / "docs" / "installation" / "重装与清理路径.md",
        ROOT / "docs" / "installation" / "记忆插件安装教程.md",
        ROOT / "docs" / "delivery" / "专有技能新增规范.md",
        ROOT / "docs" / "delivery" / "版本迁移模板.md",
        ROOT / "docs" / "delivery" / "回滚模板.md",
    ]
    for path in required_files:
        ok, detail = check_file(path)
        checks.append((f"文件存在: {path.relative_to(ROOT)}", ok, detail))

    agent_dirs = {path.name for path in (ROOT / "agents").iterdir() if path.is_dir()}
    checks.append(
        (
            "6 个业务 Agent 目录齐全",
            EXPECTED_BUSINESS_AGENTS.issubset(agent_dirs),
            f"当前目录: {sorted(agent_dirs)}",
        )
    )

    package_dirs = {path.name for path in (ROOT / "packages").iterdir() if path.is_dir()}
    checks.append(
        (
            "6 个业务包目录齐全",
            EXPECTED_BUSINESS_AGENTS.issubset(package_dirs),
            f"当前目录: {sorted(package_dirs)}",
        )
    )

    for agent_id in sorted(EXPECTED_BUSINESS_AGENTS):
        checks.append(
            (
                f"{agent_id} 模板存在",
                (ROOT / "agents" / agent_id / "soul.yaml").exists(),
                str(ROOT / "agents" / agent_id / "soul.yaml"),
            )
        )
        checks.append(
            (
                f"{agent_id} AGENTS.md 存在",
                (ROOT / "agents" / agent_id / "AGENTS.md").exists(),
                str(ROOT / "agents" / agent_id / "AGENTS.md"),
            )
        )
        checks.append(
            (
                f"{agent_id} IDENTITY.md 存在",
                (ROOT / "agents" / agent_id / "IDENTITY.md").exists(),
                str(ROOT / "agents" / agent_id / "IDENTITY.md"),
            )
        )
        checks.append(
            (
                f"{agent_id} 交付清单存在",
                (ROOT / "packages" / agent_id / "config" / "install-manifest.yaml").exists(),
                str(ROOT / "packages" / agent_id / "config" / "install-manifest.yaml"),
            )
        )
        checks.append(
            (
                f"{agent_id} trainer-guide 存在",
                (ROOT / "packages" / agent_id / "docs" / "trainer-guide.md").exists(),
                str(ROOT / "packages" / agent_id / "docs" / "trainer-guide.md"),
            )
        )

    ok, detail = run_cmd([sys.executable, str(ROOT / "scripts" / "quality_check.py")])
    checks.append(("quality_check 通过", ok, detail))

    ok, detail = run_cmd([str(ROOT / "agent-platform"), "doctor"])
    checks.append(("agent-platform doctor 通过", ok, detail))

    failed = [item for item in checks if not item[1]]
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}")
        if detail and (not ok):
            print(f"  {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
