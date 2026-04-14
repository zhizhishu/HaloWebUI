#!/usr/bin/env bash

set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
SERVICE_NAME="${SERVICE_NAME:-open-webui}"
DATA_DESTINATION="${DATA_DESTINATION:-/app/backend/data}"
BACKUP_ROOT="${BACKUP_ROOT:-./backups}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:3000/health}"
SMOKE_URL="${SMOKE_URL:-http://127.0.0.1:3000/}"
HEALTH_TIMEOUT_SEC="${HEALTH_TIMEOUT_SEC:-180}"
RESTORE_DATA_ON_ROLLBACK="${RESTORE_DATA_ON_ROLLBACK:-1}"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 2
  fi
}

wait_http_ok() {
  local url="$1"
  local timeout="$2"
  local ok_codes="$3"

  local elapsed=0
  while (( elapsed < timeout )); do
    local code
    code="$(curl -sS -o /tmp/upgrade-check-body.$$ -w '%{http_code}' "$url" || true)"
    if [[ " ${ok_codes} " == *" ${code} "* ]]; then
      return 0
    fi
    sleep 3
    elapsed=$((elapsed + 3))
  done
  return 1
}

backup_volume() {
  local volume_name="$1"
  local archive_path="$2"
  docker run --rm \
    -v "${volume_name}:/source:ro" \
    -v "${BACKUP_ROOT}:/backup" \
    alpine:3.20 sh -c "cd /source && tar czf /backup/$(basename "$archive_path") ."
}

restore_volume() {
  local volume_name="$1"
  local archive_path="$2"
  docker run --rm \
    -v "${volume_name}:/data" \
    -v "${BACKUP_ROOT}:/backup" \
    alpine:3.20 sh -c "set -e; find /data -mindepth 1 -delete; tar xzf /backup/$(basename "$archive_path") -C /data"
}

backup_bind() {
  local bind_source="$1"
  local archive_path="$2"
  tar czf "$archive_path" -C "$bind_source" .
}

restore_bind() {
  local bind_source="$1"
  local archive_path="$2"
  find "$bind_source" -mindepth 1 -delete
  tar xzf "$archive_path" -C "$bind_source"
}

require_cmd docker
require_cmd curl

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Compose file not found: $COMPOSE_FILE" >&2
  exit 2
fi

mkdir -p "$BACKUP_ROOT"
TS="$(date +%Y%m%d-%H%M%S)"
META_FILE="${BACKUP_ROOT}/${SERVICE_NAME}-upgrade-${TS}.meta"
BACKUP_ARCHIVE="${BACKUP_ROOT}/${SERVICE_NAME}-data-${TS}.tar.gz"
ROLLBACK_OVERRIDE="${BACKUP_ROOT}/${SERVICE_NAME}-rollback-${TS}.override.yml"

CONTAINER_ID="$(docker compose -f "$COMPOSE_FILE" ps -q "$SERVICE_NAME" || true)"
if [[ -z "$CONTAINER_ID" ]]; then
  echo "Service ${SERVICE_NAME} is not running. Start it first, then rerun upgrade." >&2
  exit 2
fi

PREVIOUS_IMAGE="$(docker inspect "$CONTAINER_ID" --format '{{.Config.Image}}')"
MOUNT_TYPE="$(docker inspect "$CONTAINER_ID" --format '{{range .Mounts}}{{if eq .Destination "'"${DATA_DESTINATION}"'"}}{{.Type}}{{end}}{{end}}')"
MOUNT_SOURCE="$(docker inspect "$CONTAINER_ID" --format '{{range .Mounts}}{{if eq .Destination "'"${DATA_DESTINATION}"'"}}{{if eq .Type "volume"}}{{.Name}}{{else}}{{.Source}}{{end}}{{end}}{{end}}')"

echo "[INFO] Previous image: ${PREVIOUS_IMAGE}"
echo "[INFO] Data mount type: ${MOUNT_TYPE:-<none>}"
echo "[INFO] Data mount source: ${MOUNT_SOURCE:-<none>}"

if [[ -z "$MOUNT_TYPE" || -z "$MOUNT_SOURCE" ]]; then
  echo "Cannot determine data mount for destination ${DATA_DESTINATION}" >&2
  exit 2
fi

{
  echo "timestamp=${TS}"
  echo "service=${SERVICE_NAME}"
  echo "compose_file=${COMPOSE_FILE}"
  echo "previous_image=${PREVIOUS_IMAGE}"
  echo "mount_type=${MOUNT_TYPE}"
  echo "mount_source=${MOUNT_SOURCE}"
  echo "backup_archive=${BACKUP_ARCHIVE}"
} > "$META_FILE"

echo "[INFO] Backing up data..."
if [[ "$MOUNT_TYPE" == "volume" ]]; then
  backup_volume "$MOUNT_SOURCE" "$BACKUP_ARCHIVE"
elif [[ "$MOUNT_TYPE" == "bind" ]]; then
  backup_bind "$MOUNT_SOURCE" "$BACKUP_ARCHIVE"
else
  echo "Unsupported mount type: $MOUNT_TYPE" >&2
  exit 2
fi

echo "[INFO] Pull latest image for ${SERVICE_NAME}"
docker compose -f "$COMPOSE_FILE" pull "$SERVICE_NAME"

echo "[INFO] Recreate service"
docker compose -f "$COMPOSE_FILE" up -d --force-recreate "$SERVICE_NAME"

echo "[INFO] Run post-upgrade health checks"
if wait_http_ok "$HEALTH_URL" "$HEALTH_TIMEOUT_SEC" "200" \
  && wait_http_ok "$SMOKE_URL" "$HEALTH_TIMEOUT_SEC" "200 301 302 307 308"; then
  echo "[OK] Upgrade succeeded"
  echo "[INFO] Backup kept at ${BACKUP_ARCHIVE}"
  exit 0
fi

echo "[WARN] Upgrade health checks failed, starting rollback"
docker compose -f "$COMPOSE_FILE" logs --tail=200 "$SERVICE_NAME" || true

if [[ "$RESTORE_DATA_ON_ROLLBACK" == "1" ]]; then
  echo "[INFO] Restoring data backup"
  if [[ "$MOUNT_TYPE" == "volume" ]]; then
    restore_volume "$MOUNT_SOURCE" "$BACKUP_ARCHIVE"
  else
    restore_bind "$MOUNT_SOURCE" "$BACKUP_ARCHIVE"
  fi
else
  echo "[WARN] RESTORE_DATA_ON_ROLLBACK=0, skip data restore"
fi

cat > "$ROLLBACK_OVERRIDE" <<EOF2
services:
  ${SERVICE_NAME}:
    image: ${PREVIOUS_IMAGE}
EOF2

echo "[INFO] Recreate service with previous image"
docker compose -f "$COMPOSE_FILE" -f "$ROLLBACK_OVERRIDE" up -d --force-recreate "$SERVICE_NAME"

echo "[INFO] Run rollback health checks"
if wait_http_ok "$HEALTH_URL" "$HEALTH_TIMEOUT_SEC" "200" \
  && wait_http_ok "$SMOKE_URL" "$HEALTH_TIMEOUT_SEC" "200 301 302 307 308"; then
  echo "[OK] Rollback succeeded"
  echo "[INFO] Backup/meta: ${BACKUP_ARCHIVE}, ${META_FILE}"
  exit 1
fi

echo "[FAIL] Rollback failed, manual intervention required" >&2
exit 1
