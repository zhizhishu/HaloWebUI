#!/usr/bin/env bash

set -euo pipefail

MODE="${1:-status}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$REPO_ROOT" ]]; then
  echo "Not inside a git repository" >&2
  exit 2
fi

cd "$REPO_ROOT"
EXCLUDE_FILE=".git/info/exclude"

ensure_exclude_entry() {
  local entry="$1"
  if ! grep -Fxq "$entry" "$EXCLUDE_FILE" 2>/dev/null; then
    printf '%s\n' "$entry" >> "$EXCLUDE_FILE"
  fi
}

show_status() {
  echo "[INFO] repo: $REPO_ROOT"
  echo "[INFO] local excludes:"
  grep -E '^\.serena/|^\.reports/' "$EXCLUDE_FILE" 2>/dev/null || echo "  (none)"

  if git ls-files -v uv.lock | grep -q '^S'; then
    echo "[INFO] uv.lock: skip-worktree=ON"
  else
    echo "[INFO] uv.lock: skip-worktree=OFF"
  fi

  echo "[INFO] git status --short"
  git status --short
}

case "$MODE" in
  enable)
    ensure_exclude_entry ".serena/"
    ensure_exclude_entry ".reports/"
    git update-index --skip-worktree uv.lock || true
    echo "[OK] Enabled local hygiene: .serena/.reports excluded, uv.lock skip-worktree on"
    show_status
    ;;
  disable)
    git update-index --no-skip-worktree uv.lock || true
    echo "[OK] Disabled uv.lock skip-worktree"
    show_status
    ;;
  status)
    show_status
    ;;
  *)
    echo "Usage: $0 [status|enable|disable]" >&2
    exit 2
    ;;
esac
