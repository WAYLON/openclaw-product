#!/usr/bin/env python3
import sys


def main():
    try:
        import jqdatasdk  # noqa: F401
    except Exception as exc:
        print("FAIL: 无法导入 jqdatasdk")
        print(f"DETAIL: {exc}")
        return 1

    print("OK: 已成功导入 jqdatasdk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
