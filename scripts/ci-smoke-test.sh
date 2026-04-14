#!/usr/bin/env bash

set -euo pipefail

IMAGE_REF="${IMAGE_REF:-}"
CONTAINER_NAME="${CONTAINER_NAME:-openwebui-smoke}"
HOST_PORT="${HOST_PORT:-18080}"
BASE_URL="${BASE_URL:-http://127.0.0.1:${HOST_PORT}}"
HEALTH_TIMEOUT_SEC="${HEALTH_TIMEOUT_SEC:-180}"

if [[ -z "$IMAGE_REF" ]]; then
  echo "IMAGE_REF is required" >&2
  exit 2
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

expect_status() {
  local path="$1"
  local allowed="$2"

  local code
  code="$(curl -sS -o "$TMP_DIR/body.tmp" -w '%{http_code}' "${BASE_URL}${path}" || true)"
  if [[ " ${allowed} " != *" ${code} "* ]]; then
    echo "[FAIL] ${path}: expected [${allowed}], got ${code}" >&2
    sed -n '1,80p' "$TMP_DIR/body.tmp" >&2 || true
    return 1
  fi
  echo "[ OK ] ${path}: ${code}"
  return 0
}

echo "[INFO] Pull image: ${IMAGE_REF}"
docker pull "$IMAGE_REF"

echo "[INFO] Start container: ${CONTAINER_NAME}"
docker run -d --rm \
  --name "$CONTAINER_NAME" \
  -p "${HOST_PORT}:8080" \
  -e WEBUI_AUTH=False \
  -e ENABLE_SIGNUP=False \
  -e WEBUI_SECRET_KEY=ci-smoke-key \
  "$IMAGE_REF" >/dev/null

echo "[INFO] Wait /health ready (timeout ${HEALTH_TIMEOUT_SEC}s)"
ready=0
for ((i=0; i<HEALTH_TIMEOUT_SEC; i+=3)); do
  code="$(curl -sS -o "$TMP_DIR/health.json" -w '%{http_code}' "${BASE_URL}/health" || true)"
  if [[ "$code" == "200" ]] && grep -q '"status"' "$TMP_DIR/health.json"; then
    ready=1
    break
  fi
  sleep 3
done

if [[ "$ready" != "1" ]]; then
  echo "[FAIL] /health not ready within timeout" >&2
  docker logs --tail=300 "$CONTAINER_NAME" >&2 || true
  exit 1
fi

echo "[ OK ] /health ready"

expect_status "/" "200 301 302 307 308"
expect_status "/health" "200"
expect_status "/health/db" "200"
expect_status "/api/version" "200"

# MCP-related minimal API verification (route exists and is reachable).
# In unauthenticated smoke mode, 401/403 are acceptable.
expect_status "/api/v1/configs/mcp_servers" "200 401 403"
expect_status "/api/v1/tools" "200 401 403"

echo "[INFO] Smoke test passed for ${IMAGE_REF}"
