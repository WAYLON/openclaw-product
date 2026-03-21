#!/usr/bin/env bash
set -euo pipefail

DEFAULT_PORT="${1:-9222}"
USER_DATA_DIR="${HOME}/.openclaw/browser-devtools-profile"

find_browser() {
  case "$(uname -s)" in
    Darwin)
      if [ -d "/Applications/Google Chrome.app" ]; then
        printf '%s\n' "/Applications/Google Chrome.app"
        return 0
      fi
      ;;
    Linux)
      for candidate in google-chrome-stable google-chrome chromium chromium-browser; do
        if command -v "$candidate" >/dev/null 2>&1; then
          command -v "$candidate"
          return 0
        fi
      done
      ;;
  esac
  return 1
}

find_free_port() {
  local port="$1"
  while lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; do
    port=$((port + 1))
  done
  printf '%s\n' "$port"
}

BROWSER_BIN="$(find_browser || true)"
if [ -z "$BROWSER_BIN" ]; then
  echo "错误: 未找到可用的 Chrome/Chromium 浏览器"
  exit 1
fi

PORT="$(find_free_port "$DEFAULT_PORT")"
mkdir -p "$USER_DATA_DIR"

if [ "$(uname -s)" = "Darwin" ]; then
  nohup open -na "$BROWSER_BIN" --args \
    --remote-debugging-port="$PORT" \
    --remote-debugging-address=127.0.0.1 \
    --user-data-dir="$USER_DATA_DIR" \
    --no-first-run \
    --no-default-browser-check \
    --new-window \
    about:blank \
    >"$USER_DATA_DIR/chrome-devtools.log" 2>&1 &
else
  nohup "$BROWSER_BIN" \
    --remote-debugging-port="$PORT" \
    --remote-debugging-address=127.0.0.1 \
    --user-data-dir="$USER_DATA_DIR" \
    --no-first-run \
    --no-default-browser-check \
    --new-window \
    about:blank \
    >"$USER_DATA_DIR/chrome-devtools.log" 2>&1 &
fi

sleep 2

if curl -fsS "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "OK: 标准 DevTools Chrome 已启动"
  echo "PORT=${PORT}"
  echo "LIST=http://127.0.0.1:${PORT}/json/list"
  exit 0
fi

echo "FAIL: 已尝试启动标准 DevTools Chrome，但 /json/version 仍不可读"
echo "日志: $USER_DATA_DIR/chrome-devtools.log"
exit 1
