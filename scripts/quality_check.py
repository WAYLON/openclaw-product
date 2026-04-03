from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_AGENT_COUNT = 6


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    required_files = [
        ROOT / "pyproject.toml",
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / ".gitignore",
        ROOT / "Makefile",
        ROOT / "agent-platform",
        ROOT / ".github" / "workflows" / "ci.yml",
        ROOT / ".github" / "CODEOWNERS",
        ROOT / "docs" / "installation" / "平台安装教程.md",
        ROOT / "docs" / "installation" / "7个Agent-渠道绑定与模型分配总表.md",
        ROOT / "docs" / "delivery" / "版本发布流程.md",
    ]

    for path in required_files:
        checks.append((f"文件存在: {path.relative_to(ROOT)}", path.exists(), str(path)))

    py_files = sorted(
        path for path in ROOT.rglob("*.py")
        if ".git" not in path.parts and ".platform" not in path.parts
    )
    compile_cmd = [sys.executable, "-m", "py_compile", *[str(path) for path in py_files]]
    compile_result = subprocess.run(compile_cmd, cwd=ROOT, capture_output=True, text=True)
    checks.append(("Python 语法检查", compile_result.returncode == 0, compile_result.stderr.strip()))

    installed_agents = sorted(path for path in (ROOT / "agents").iterdir() if path.is_dir())
    checks.append((f"业务 Agent 目录数量不少于 {EXPECTED_AGENT_COUNT}", len(installed_agents) >= EXPECTED_AGENT_COUNT, str(len(installed_agents))))

    package_docs = sorted((ROOT / "packages").glob("*/docs/trainer-guide.md"))
    checks.append((f"交付包 trainer-guide 覆盖 {EXPECTED_AGENT_COUNT} 个业务 Agent", len(package_docs) >= EXPECTED_AGENT_COUNT, str(len(package_docs))))

    failed = [item for item in checks if not item[1]]
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}")
        if detail and not ok:
            print(f"  {detail}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
