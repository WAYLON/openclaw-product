#!/bin/sh
set -eu

PROXY_URL="${PROXY_URL:-http://127.0.0.1:7897}"
NO_PROXY_VALUE="${NO_PROXY_VALUE:-localhost,127.0.0.1,::1}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
AUTH_SOURCE="${1:-}"
MODEL_PATCH="${2:-}"

HTTP_PROXY="$PROXY_URL"
HTTPS_PROXY="$PROXY_URL"
ALL_PROXY="$PROXY_URL"
NO_PROXY="$NO_PROXY_VALUE"
NODE_USE_ENV_PROXY=1
export HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY NODE_USE_ENV_PROXY

log() {
  printf '%s\n' "$*"
}

append_env_block() {
  target="$1"
  mkdir -p "$(dirname "$target")"
  touch "$target"
  tmp="$(mktemp)"
  awk '
    BEGIN {skip=0}
    /^# >>> openclaw proxy >>>$/ {skip=1; next}
    /^# <<< openclaw proxy <<<$/{skip=0; next}
    skip==0 {print}
  ' "$target" >"$tmp"
  {
    printf '# >>> openclaw proxy >>>\n'
    printf 'export HTTP_PROXY=%s\n' "$HTTP_PROXY"
    printf 'export HTTPS_PROXY=%s\n' "$HTTPS_PROXY"
    printf 'export ALL_PROXY=%s\n' "$ALL_PROXY"
    printf 'export NO_PROXY=%s\n' "$NO_PROXY"
    printf 'export NODE_USE_ENV_PROXY=%s\n' "$NODE_USE_ENV_PROXY"
    printf '# <<< openclaw proxy <<<\n'
  } >>"$tmp"
  mv "$tmp" "$target"
}

set_macos_plist_env() {
  plist="$1"
  if [ ! -f "$plist" ]; then
    return 0
  fi
  /usr/libexec/PlistBuddy -c "Print :EnvironmentVariables" "$plist" >/dev/null 2>&1 || /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables dict" "$plist"
  for key in HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY NODE_USE_ENV_PROXY; do
    value=$(eval "printf '%s' \"\${$key}\"")
    /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:$key $value" "$plist" >/dev/null 2>&1 || \
      /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:$key string $value" "$plist"
  done
}

persist_runtime_env() {
  append_env_block "$HOME/.profile"
  append_env_block "$HOME/.zprofile"
  append_env_block "$HOME/.bash_profile"

  uname_s="$(uname -s)"
if [ "$uname_s" = "Darwin" ]; then
    launchctl setenv HTTP_PROXY "$HTTP_PROXY"
    launchctl setenv HTTPS_PROXY "$HTTPS_PROXY"
    launchctl setenv ALL_PROXY "$ALL_PROXY"
    launchctl setenv NO_PROXY "$NO_PROXY"
    launchctl setenv NODE_USE_ENV_PROXY "$NODE_USE_ENV_PROXY"
    set_macos_plist_env "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
  elif [ "$uname_s" = "Linux" ]; then
    mkdir -p "$HOME/.config/environment.d"
    cat >"$HOME/.config/environment.d/openclaw-proxy.conf" <<EOF
HTTP_PROXY=$HTTP_PROXY
HTTPS_PROXY=$HTTPS_PROXY
ALL_PROXY=$ALL_PROXY
NO_PROXY=$NO_PROXY
NODE_USE_ENV_PROXY=$NODE_USE_ENV_PROXY
EOF
    if command -v systemctl >/dev/null 2>&1; then
      systemctl --user import-environment HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY NODE_USE_ENV_PROXY >/dev/null 2>&1 || true
      systemctl --user set-environment HTTP_PROXY="$HTTP_PROXY" HTTPS_PROXY="$HTTPS_PROXY" ALL_PROXY="$ALL_PROXY" NO_PROXY="$NO_PROXY" NODE_USE_ENV_PROXY="$NODE_USE_ENV_PROXY" >/dev/null 2>&1 || true
      mkdir -p "$HOME/.config/systemd/user/openclaw-gateway.service.d"
      cat >"$HOME/.config/systemd/user/openclaw-gateway.service.d/proxy.conf" <<EOF
[Service]
Environment=HTTP_PROXY=$HTTP_PROXY
Environment=HTTPS_PROXY=$HTTPS_PROXY
Environment=ALL_PROXY=$ALL_PROXY
Environment=NO_PROXY=$NO_PROXY
Environment=NODE_USE_ENV_PROXY=$NODE_USE_ENV_PROXY
EOF
      systemctl --user daemon-reload >/dev/null 2>&1 || true
    fi
fi
}

require_runtime_bins() {
  missing=0
  for bin in openclaw curl node; do
    if ! command -v "$bin" >/dev/null 2>&1; then
      log "错误: 缺少必需命令 $bin"
      missing=1
    fi
  done
  if [ "$missing" -ne 0 ]; then
    exit 1
  fi
}

verify_new_shell() {
  log "== verify shell env =="
  "${SHELL:-/bin/sh}" -lc 'printf "HTTP_PROXY=%s\nHTTPS_PROXY=%s\nALL_PROXY=%s\nNO_PROXY=%s\nNODE_USE_ENV_PROXY=%s\n" "$HTTP_PROXY" "$HTTPS_PROXY" "$ALL_PROXY" "$NO_PROXY" "$NODE_USE_ENV_PROXY"'
}

verify_runtime_env() {
  log "== verify runtime env =="
  uname_s="$(uname -s)"
  if [ "$uname_s" = "Darwin" ]; then
    launchctl getenv HTTP_PROXY || true
    launchctl getenv HTTPS_PROXY || true
    launchctl getenv ALL_PROXY || true
    launchctl getenv NO_PROXY || true
    launchctl getenv NODE_USE_ENV_PROXY || true
  elif [ "$uname_s" = "Linux" ] && command -v systemctl >/dev/null 2>&1; then
    systemctl --user show-environment | grep -E '^(HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|NO_PROXY|NODE_USE_ENV_PROXY)=' || true
  fi
}

verify_curl_proxy() {
  log "== curl proxy test =="
  curl -sSI --max-time 15 --proxy "$HTTP_PROXY" https://www.gstatic.com/generate_204 | head -n 3
}

verify_node_proxy() {
  log "== node fetch proxy test =="
  node - <<'NODE'
const target = 'https://www.gstatic.com/generate_204';
fetch(target, { method: 'HEAD' })
  .then((res) => {
    console.log(`status=${res.status}`);
    console.log(`proxy=${process.env.HTTP_PROXY || ''}`);
    console.log(`node_use_env_proxy=${process.env.NODE_USE_ENV_PROXY || ''}`);
  })
  .catch((err) => {
    console.error(`fetch_error=${err.message}`);
    process.exit(1);
  });
NODE
}

verify_no_proxy() {
  log "== no_proxy localhost test =="
  port=18880
  node - <<'NODE' >/tmp/openclaw-localhost-test.log 2>&1 &
const http = require('http');
const port = 18880;
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'content-type': 'text/plain' });
  res.end('ok');
});
server.listen(port, '127.0.0.1', () => {
  setTimeout(() => server.close(() => process.exit(0)), 4000);
});
NODE
  server_pid=$!
  sleep 1
  curl -sS --max-time 5 "http://127.0.0.1:${port}" >/tmp/openclaw-localhost-127.out
  curl -sS --max-time 5 "http://localhost:${port}" >/tmp/openclaw-localhost-localhost.out
  wait "$server_pid"
  printf '127.0.0.1=%s\n' "$(cat /tmp/openclaw-localhost-127.out)"
  printf 'localhost=%s\n' "$(cat /tmp/openclaw-localhost-localhost.out)"
  rm -f /tmp/openclaw-localhost-127.out /tmp/openclaw-localhost-localhost.out /tmp/openclaw-localhost-test.log
}

merge_model_patch() {
  if [ -z "$MODEL_PATCH" ] || [ ! -f "$MODEL_PATCH" ]; then
    return 0
  fi
  node - "$MODEL_PATCH" "$OPENCLAW_HOME/openclaw.json" <<'NODE'
const fs = require('fs');
const patchPath = process.argv[2];
const basePath = process.argv[3];
const patch = JSON.parse(fs.readFileSync(patchPath, 'utf8'));
const base = JSON.parse(fs.readFileSync(basePath, 'utf8'));
base.auth = patch.auth;
base.models = patch.models;
base.agents = base.agents || {};
base.agents.defaults = base.agents.defaults || {};
base.agents.defaults.model = patch.agents.defaults.model;
base.agents.defaults.models = patch.agents.defaults.models;
fs.writeFileSync(basePath, JSON.stringify(base, null, 2));
NODE
}

install_auth_profile() {
  if [ -z "$AUTH_SOURCE" ] || [ ! -f "$AUTH_SOURCE" ]; then
    return 0
  fi
  mkdir -p "$OPENCLAW_HOME/agents/main/agent"
  node - "$AUTH_SOURCE" "$OPENCLAW_HOME/agents/main/agent/auth-profiles.json" <<'NODE'
const fs = require('fs');

const [sourcePath, targetPath] = process.argv.slice(2);
const source = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
let target = {
  version: 1,
  profiles: {},
  order: {},
  lastGood: {},
};

if (fs.existsSync(targetPath)) {
  target = JSON.parse(fs.readFileSync(targetPath, 'utf8'));
  target.version = target.version || 1;
  target.profiles = target.profiles || {};
  target.order = target.order || {};
  target.lastGood = target.lastGood || {};
}

function decodeJwtExp(token) {
  if (!token || token.split('.').length < 2) return null;
  const payload = token.split('.')[1];
  const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized + '='.repeat((4 - normalized.length % 4) % 4);
  const decoded = JSON.parse(Buffer.from(padded, 'base64').toString('utf8'));
  return decoded.exp ? decoded.exp * 1000 : null;
}

function mergeAuthProfiles(data) {
  target.version = data.version || target.version || 1;
  target.profiles = { ...target.profiles, ...(data.profiles || {}) };
  target.order = { ...target.order, ...(data.order || {}) };
  target.lastGood = { ...target.lastGood, ...(data.lastGood || {}) };
  if (data.usageStats) {
    target.usageStats = { ...(target.usageStats || {}), ...data.usageStats };
  }
}

if (source.profiles && source.order) {
  mergeAuthProfiles(source);
} else if (source.tokens && source.tokens.access_token && source.tokens.refresh_token) {
  const access = source.tokens.access_token;
  const refresh = source.tokens.refresh_token;
  const accountId = source.tokens.account_id || source.tokens.user_id || source.user_id || 'unknown';
  const expires = decodeJwtExp(access) || Date.now() + 60 * 60 * 1000;
  target.profiles['openai-codex:default'] = {
    type: 'oauth',
    provider: 'openai-codex',
    access,
    refresh,
    expires,
    accountId,
  };
  target.order['openai-codex'] = ['openai-codex:default'];
  target.lastGood['openai-codex'] = 'openai-codex:default';
} else {
  throw new Error('无法识别认证文件格式，只支持 auth-profiles.json 或 ~/.codex/auth.json');
}

fs.writeFileSync(targetPath, JSON.stringify(target, null, 2));
NODE
  chmod 600 "$OPENCLAW_HOME/agents/main/agent/auth-profiles.json"
}

clean_runtime_state() {
  log "== cleanup runtime =="
  openclaw gateway stop >/dev/null 2>&1 || true
  find "$OPENCLAW_HOME/agents" -type f \( -name '*.lock' -o -name '.lock' -o -name 'session.lock' \) -delete 2>/dev/null || true
  find "$HOME/.codex" -type f \( -name '*.lock' -o -name '.lock' \) -delete 2>/dev/null || true
}

restart_services() {
  log "== restart services =="
  openclaw config set gateway.mode local >/dev/null 2>&1 || true
  openclaw gateway install >/dev/null 2>&1 || true
  openclaw gateway restart >/dev/null 2>&1 || openclaw gateway start >/dev/null 2>&1 || true
}

final_validate() {
  log "== final validate =="
  openclaw agent --agent main --message "Reply with OK only." --json
}

require_runtime_bins
persist_runtime_env
install_auth_profile
merge_model_patch
clean_runtime_state
restart_services
verify_new_shell
verify_runtime_env
verify_curl_proxy
verify_node_proxy
verify_no_proxy
final_validate
