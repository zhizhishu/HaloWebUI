#!/usr/bin/env bash

set -euo pipefail

PREV_SHA="${1:-}"
NEW_SHA="${2:-}"
UPSTREAM_REF="${3:-upstream/main}"
OUTPUT_PATH="${4:-upstream-change-report.md}"

if [[ -z "$PREV_SHA" || -z "$NEW_SHA" ]]; then
  echo "Usage: $0 <prev_sha> <new_sha> [upstream_ref] [output_path]" >&2
  exit 1
fi

if ! git cat-file -e "${PREV_SHA}^{commit}" 2>/dev/null; then
  echo "Invalid prev_sha: ${PREV_SHA}" >&2
  exit 1
fi

if ! git cat-file -e "${NEW_SHA}^{commit}" 2>/dev/null; then
  echo "Invalid new_sha: ${NEW_SHA}" >&2
  exit 1
fi

if ! git rev-parse --verify "$UPSTREAM_REF" >/dev/null 2>&1; then
  echo "Invalid upstream_ref: ${UPSTREAM_REF}" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"

NOW_UTC="$(date -u +"%Y-%m-%d %H:%M:%S UTC")"
UPSTREAM_SHA="$(git rev-parse "$UPSTREAM_REF")"
UPSTREAM_COMMIT_TIME="$(git show -s --format='%ci' "$UPSTREAM_SHA")"
PREV_COMMIT_TIME="$(git show -s --format='%ci' "$PREV_SHA")"
NEW_COMMIT_TIME="$(git show -s --format='%ci' "$NEW_SHA")"
COMMIT_COUNT="$(git rev-list --count "${PREV_SHA}..${NEW_SHA}")"

commit_lines=""
if [[ "$COMMIT_COUNT" -gt 0 ]]; then
  commit_lines="$(git log --oneline --reverse "${PREV_SHA}..${NEW_SHA}")"
fi

changed_files=""
changed_dirs=""
if [[ "$COMMIT_COUNT" -gt 0 ]]; then
  changed_files="$(git diff --name-only "${PREV_SHA}..${NEW_SHA}")"
  changed_dirs="$(echo "$changed_files" | awk -F/ 'NF{print $1}' | sort -u)"
fi

risks=()
if [[ -n "$changed_files" ]]; then
  if echo "$changed_files" | grep -Eq '(^|/)backend/open_webui/.*/mcp|(^|/)test_user_tools_mcp_inherit.py|(^|/)test_mcp.py'; then
    risks+=("MCP 核心链路有改动，需优先回归“用户继承 + MCP 状态持久化”能力")
  fi
  if echo "$changed_files" | grep -Eq '(^|/)src/lib/components/|(^|/)src/lib/stores/'; then
    risks+=("前端交互层有改动，需重点复测高级选项工具值与 MCP 选择状态")
  fi
  if echo "$changed_files" | grep -Eq '(^|/)backend/open_webui/migrations|(^|/)alembic'; then
    risks+=("检测到数据库迁移改动，上线前需先做数据库备份")
  fi
  if echo "$changed_files" | grep -Eq '(^|/)\.github/workflows/|(^|/)Dockerfile|(^|/)docker-compose'; then
    risks+=("CI 或镜像构建链路有改动，需验证 custom 镜像发布流程")
  fi
fi

{
  echo "# 上游同步变更报告"
  echo
  echo "- 生成时间: ${NOW_UTC}"
  echo "- 上游锚点: ${UPSTREAM_SHA}"
  echo "- 上游时间: ${UPSTREAM_COMMIT_TIME}"
  echo "- 起始基线: ${PREV_SHA} (${PREV_COMMIT_TIME})"
  echo "- 本轮结果: ${NEW_SHA} (${NEW_COMMIT_TIME})"
  echo "- 新增提交数: ${COMMIT_COUNT}"
  echo

  echo "## 作者更新清单"
  if [[ "$COMMIT_COUNT" -eq 0 ]]; then
    echo "- （无新增提交）"
  else
    while IFS= read -r line; do
      [[ -n "$line" ]] && echo "- ${line}"
    done <<< "$commit_lines"
  fi
  echo

  echo "## 影响目录"
  if [[ -z "$changed_dirs" ]]; then
    echo "- （无目录变更）"
  else
    while IFS= read -r dir; do
      [[ -n "$dir" ]] && echo "- ${dir}"
    done <<< "$changed_dirs"
  fi
  echo

  echo "## 风险提示"
  if [[ ${#risks[@]} -eq 0 ]]; then
    echo "- 未检测到高风险路径（仍建议执行关键回归）。"
  else
    for item in "${risks[@]}"; do
      echo "- ${item}"
    done
  fi
} > "$OUTPUT_PATH"

echo "Generated report: ${OUTPUT_PATH}"
