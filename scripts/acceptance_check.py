from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUSINESS_AGENTS = [
    "education-agent",
    "stock-agent",
    "loan-agent",
    "social-media-agent",
    "news-agent",
    "sales-agent",
]
SCENARIO_PROMPTS = {
    "main": "给全部 agent 安装一个共享 skill 时，应该怎么做？",
    "education-agent": "帮我把这份讲义整理成课堂重点",
    "stock-agent": "分析这只股票的风险和观察点",
    "loan-agent": "帮我整理这段材料说明",
    "social-media-agent": "帮我整理今天的社媒热点",
    "news-agent": "把今天几条新闻整理成摘要",
    "sales-agent": "总结这段客户对话，给我下一步建议",
}


def run_cmd(cmd: list[str], timeout: int = 45) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return False, f"命令不存在: {' '.join(cmd)}"
    except subprocess.TimeoutExpired:
        return False, f"命令超时: {' '.join(cmd)}"
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit={result.returncode}"
        return False, detail
    return True, result.stdout.strip()


def write_report(checks: list[tuple[str, bool, str]], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 验收记录",
        "",
        f"- 生成时间：{datetime.now().isoformat(timespec='seconds')}",
        f"- 项目目录：`{ROOT}`",
        "",
        "## 结果",
        "",
    ]
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        lines.append(f"- [{status}] {label}")
        if detail and not ok:
            lines.append(f"  - {detail}")
    lines.append("")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw 交付最小验收")
    parser.add_argument("--smoke", action="store_true", help="对 6 个业务 Agent 逐个执行最小回复测试")
    parser.add_argument("--probe-channels", action="store_true", help="附加执行 channels --probe（较慢）")
    parser.add_argument("--timeout", type=int, default=20, help="单个 OpenClaw 命令超时时间（秒）")
    parser.add_argument("--scenario", action="store_true", help="按角色验收模板执行标准场景问题")
    parser.add_argument("--report", default="", help="把验收结果写入 Markdown 文件")
    args = parser.parse_args()

    checks: list[tuple[str, bool, str]] = []

    openclaw_path = shutil.which("openclaw")
    checks.append(("openclaw 命令可用", bool(openclaw_path), openclaw_path or "未找到 openclaw"))

    if openclaw_path:
        ok, detail = run_cmd(["openclaw", "status", "--deep"], timeout=args.timeout)
        checks.append(("openclaw status --deep", ok, detail))

        ok, detail = run_cmd(["openclaw", "models", "status"], timeout=args.timeout)
        checks.append(("openclaw models status", ok, detail))

        if args.probe_channels:
            ok, detail = run_cmd(["openclaw", "channels", "status", "--probe"], timeout=args.timeout)
            checks.append(("openclaw channels status --probe", ok, detail))
        else:
            checks.append(("跳过 channels --probe（需显式开启）", True, ""))

        if args.smoke:
            for agent_id in BUSINESS_AGENTS:
                ok, detail = run_cmd(
                    [
                        "openclaw",
                        "agent",
                        "--agent",
                        agent_id,
                        "--message",
                        "请只回复ok",
                    ],
                    timeout=max(args.timeout, 30),
                )
                checks.append((f"{agent_id} 最小回复测试", ok, detail))

        if args.scenario:
            for agent_id in ["main", *BUSINESS_AGENTS]:
                prompt = SCENARIO_PROMPTS[agent_id]
                ok, detail = run_cmd(
                    [
                        "openclaw",
                        "agent",
                        "--agent",
                        agent_id,
                        "--message",
                        prompt,
                    ],
                    timeout=max(args.timeout, 45),
                )
                checks.append((f"{agent_id} 场景验收", ok, detail))

    failed = [item for item in checks if not item[1]]
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}")
        if detail and not ok:
            print(f"  {detail}")

    if args.report:
        write_report(checks, Path(args.report).expanduser())

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
