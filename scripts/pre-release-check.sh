#!/usr/bin/env bash

set -uo pipefail

TARGET_BRANCH="${TARGET_BRANCH:-custom}"
RUN_TESTS="${RUN_TESTS:-1}"
FETCH_REMOTE="${FETCH_REMOTE:-1}"
ALLOW_DIRTY="${ALLOW_DIRTY:-0}"
AUTHOR_IMAGE="${AUTHOR_IMAGE:-ghcr.io/ztx888/halowebui:main}"
CUSTOM_IMAGE="${CUSTOM_IMAGE:-ghcr.io/zhizhishu/halowebui:custom}"

failures=0
warnings=0

note() {
  printf '[INFO] %s\n' "$1"
}

ok() {
  printf '[ OK ] %s\n' "$1"
}

warn() {
  warnings=$((warnings + 1))
  printf '[WARN] %s\n' "$1"
}

fail() {
  failures=$((failures + 1))
  printf '[FAIL] %s\n' "$1"
}

run_cmd() {
  local title="$1"
  local cmd="$2"
  note "$title"
  if bash -lc "$cmd"; then
    ok "$title"
  else
    fail "$title"
  fi
}

check_ref_exists() {
  local ref="$1"
  git rev-parse --verify "$ref" >/dev/null 2>&1
}

compute_divergence() {
  local left="$1"
  local right="$2"
  git rev-list --left-right --count "${left}...${right}" 2>/dev/null || echo "-1 -1"
}

report_image() {
  local image_ref="$1"
  local label="$2"

  if ! command -v docker >/dev/null 2>&1; then
    warn "docker 不可用，跳过 ${label} 镜像溯源检查"
    return
  fi

  if ! docker image inspect "$image_ref" >/dev/null 2>&1; then
    warn "本地未找到 ${label} 镜像: ${image_ref}"
    return
  fi

  local digest created
  digest="$(docker image inspect "$image_ref" --format '{{index .RepoDigests 0}}' 2>/dev/null || true)"
  created="$(docker image inspect "$image_ref" --format '{{.Created}}' 2>/dev/null || true)"
  note "${label} 镜像: ${image_ref}"
  note "${label} Digest: ${digest:-<none>}"
  note "${label} Created: ${created:-<none>}"
}

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [[ -z "$REPO_ROOT" ]]; then
  echo "Not inside a git repository" >&2
  exit 2
fi

cd "$REPO_ROOT"

note "Repo: $REPO_ROOT"
note "Target branch: ${TARGET_BRANCH}"

if [[ "$FETCH_REMOTE" == "1" ]]; then
  note "Fetching remotes..."
  if git fetch --all --prune; then
    ok "git fetch --all --prune"
  else
    warn "git fetch 失败，将基于本地 refs 继续检查"
  fi
fi

current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" == "$TARGET_BRANCH" ]]; then
  ok "当前分支为 ${TARGET_BRANCH}"
else
  warn "当前分支是 ${current_branch}，目标发布分支是 ${TARGET_BRANCH}"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  if [[ "$ALLOW_DIRTY" == "1" ]]; then
    warn "工作区非干净状态（ALLOW_DIRTY=1，按警告处理）"
  else
    fail "工作区非干净状态（请先提交或暂存）"
  fi
  git status --short
else
  ok "工作区干净"
fi

note "Branch pointers:"
for ref in main origin/main upstream/main future origin/future custom origin/custom; do
  if check_ref_exists "$ref"; then
    printf '  - %-14s %s\n' "$ref" "$(git rev-parse --short "$ref")"
  else
    printf '  - %-14s %s\n' "$ref" "<missing>"
  fi
done

if check_ref_exists main && check_ref_exists upstream/main; then
  read -r ahead behind <<<"$(compute_divergence main upstream/main)"
  note "main vs upstream/main: ahead=${ahead} behind=${behind}"
  if [[ "$behind" -gt 0 ]]; then
    fail "main 落后于 upstream/main"
  else
    ok "main 与 upstream/main 已对齐或超前"
  fi
else
  warn "main 或 upstream/main 不存在，跳过对齐检查"
fi

if check_ref_exists future && check_ref_exists main; then
  read -r ahead behind <<<"$(compute_divergence future main)"
  note "future vs main: ahead=${ahead} behind=${behind}"
  if [[ "$behind" -gt 0 ]]; then
    fail "future 落后于 main"
  else
    ok "future 已包含 main"
  fi
else
  warn "future 或 main 不存在，跳过 future 检查"
fi

if check_ref_exists custom && check_ref_exists future; then
  read -r ahead behind <<<"$(compute_divergence custom future)"
  note "custom vs future: ahead=${ahead} behind=${behind}"
  if [[ "$behind" -gt 0 ]]; then
    fail "custom 落后于 future"
  else
    ok "custom 已包含 future"
  fi
else
  warn "custom 或 future 不存在，跳过 custom 检查"
fi

if check_ref_exists upstream/main; then
  upstream_sha="$(git rev-parse upstream/main)"
  upstream_time="$(git show -s --format='%ci' "$upstream_sha")"
  note "Upstream baseline: ${upstream_sha} (${upstream_time})"
fi

if [[ "$RUN_TESTS" == "1" ]]; then
  if command -v uv >/dev/null 2>&1; then
    run_cmd \
      "后端 MCP 核心回归" \
      "uv run pytest backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_mcp.py"
  else
    fail "未找到 uv，无法执行后端回归"
  fi

  if command -v npx >/dev/null 2>&1; then
    run_cmd \
      "前端关键回归" \
      "npx vitest run src/lib/utils/headings.test.ts src/lib/utils/file-upload-errors.test.ts"
  else
    fail "未找到 npx，无法执行前端回归"
  fi
else
  warn "RUN_TESTS=0，已跳过测试"
fi

report_image "$AUTHOR_IMAGE" "作者"
report_image "$CUSTOM_IMAGE" "自定义"

echo
note "Summary: failures=${failures}, warnings=${warnings}"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

exit 0
