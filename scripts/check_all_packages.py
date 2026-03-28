from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.validate_package import validate_package


def main() -> int:
    package_roots = sorted((ROOT / "packages").glob("*"))
    failed = False

    for package_dir in package_roots:
        if not package_dir.is_dir():
            continue
        agent_id = package_dir.name
        source_agent_dir = ROOT / "agents" / agent_id
        errors = validate_package(package_dir, source_agent_dir)
        if errors:
            failed = True
            print(f"[FAIL] {agent_id}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[PASS] {agent_id}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
