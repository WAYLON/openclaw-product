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
        df = jqdatasdk.get_price(
            "000001.XSHE",
            start_date="2024-01-02",
            end_date="2024-01-10",
            frequency="daily",
        )
    except Exception as exc:
        print("FAIL: 最小 get_price 调用失败")
        print(f"DETAIL: {exc}")
        return 1

    try:
        rows = len(df)
        cols = list(df.columns)
    except Exception:
        rows = "unknown"
        cols = "unknown"

    print("OK: 最小 get_price 调用成功")
    print(f"ROWS: {rows}")
    print(f"COLUMNS: {cols}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
