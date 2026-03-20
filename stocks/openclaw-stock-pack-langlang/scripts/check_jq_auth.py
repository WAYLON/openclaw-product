#!/usr/bin/env python3
import os
import sys


def main():
    user = os.environ.get("JQ_USER")
    password = os.environ.get("JQ_PASS")

    if not user or not password:
        print("FAIL: 缺少环境变量 JQ_USER 或 JQ_PASS")
        return 1

    try:
        import jqdatasdk
    except Exception as exc:
        print("FAIL: 无法导入 jqdatasdk")
        print(f"DETAIL: {exc}")
        return 1

    try:
        jqdatasdk.auth(user, password)
    except Exception as exc:
        print("FAIL: 聚宽认证失败")
        print(f"DETAIL: {exc}")
        return 1

    print("OK: 聚宽认证成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
