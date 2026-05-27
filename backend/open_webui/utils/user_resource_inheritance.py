from __future__ import annotations

import re
from typing import Any, Optional

from open_webui.models.users import UserModel


RESOURCE_INHERITANCE_KEY = "resource_inheritance"
INHERIT_ADMIN_MODELS_KEY = "admin_models"
INHERIT_ADMIN_MCP_SERVERS_KEY = "admin_mcp_servers"
ADMIN_MODEL_IDS_KEY = "admin_model_ids"
ADMIN_MCP_SERVER_IDS_KEY = "admin_mcp_server_ids"

DEFAULT_RESOURCE_INHERITANCE = {
    INHERIT_ADMIN_MODELS_KEY: True,
    INHERIT_ADMIN_MCP_SERVERS_KEY: True,
    ADMIN_MODEL_IDS_KEY: None,
    ADMIN_MCP_SERVER_IDS_KEY: None,
}


def _as_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _get_settings_dict(user: Optional[UserModel]) -> dict:
    if not user or not getattr(user, "settings", None):
        return {}
    try:
        return _as_dict(user.settings.model_dump())
    except Exception:
        return _as_dict(getattr(user, "settings", None))


def _normalize_optional_ids(value: Any) -> Optional[list[str]]:
    if value is None:
        return None
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        item = str(item or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        normalized.append(item)
    return normalized


def _normalize_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "on"}:
            return True
        if normalized in {"false", "0", "no", "off"}:
            return False
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def normalize_resource_inheritance(value: Any) -> dict:
    raw = _as_dict(value)
    return {
        INHERIT_ADMIN_MODELS_KEY: _normalize_bool(
            raw.get(
                INHERIT_ADMIN_MODELS_KEY,
                DEFAULT_RESOURCE_INHERITANCE[INHERIT_ADMIN_MODELS_KEY],
            ),
            DEFAULT_RESOURCE_INHERITANCE[INHERIT_ADMIN_MODELS_KEY],
        ),
        INHERIT_ADMIN_MCP_SERVERS_KEY: _normalize_bool(
            raw.get(
                INHERIT_ADMIN_MCP_SERVERS_KEY,
                DEFAULT_RESOURCE_INHERITANCE[INHERIT_ADMIN_MCP_SERVERS_KEY],
            ),
            DEFAULT_RESOURCE_INHERITANCE[INHERIT_ADMIN_MCP_SERVERS_KEY],
        ),
        ADMIN_MODEL_IDS_KEY: _normalize_optional_ids(raw.get(ADMIN_MODEL_IDS_KEY)),
        ADMIN_MCP_SERVER_IDS_KEY: _normalize_optional_ids(
            raw.get(ADMIN_MCP_SERVER_IDS_KEY)
        ),
    }


def get_user_resource_inheritance(user: Optional[UserModel]) -> dict:
    settings = _get_settings_dict(user)
    return normalize_resource_inheritance(settings.get(RESOURCE_INHERITANCE_KEY))


def can_user_inherit_admin_models(user: Optional[UserModel]) -> bool:
    if not user or getattr(user, "role", None) == "admin":
        return False
    return bool(get_user_resource_inheritance(user)[INHERIT_ADMIN_MODELS_KEY])


def can_user_inherit_admin_mcp_servers(user: Optional[UserModel]) -> bool:
    if not user or getattr(user, "role", None) == "admin":
        return False
    return bool(get_user_resource_inheritance(user)[INHERIT_ADMIN_MCP_SERVERS_KEY])


def get_allowed_admin_model_ids(user: Optional[UserModel]) -> Optional[set[str]]:
    value = get_user_resource_inheritance(user).get(ADMIN_MODEL_IDS_KEY)
    return set(value) if isinstance(value, list) else None


def get_allowed_admin_mcp_server_ids(user: Optional[UserModel]) -> Optional[set[str]]:
    value = get_user_resource_inheritance(user).get(ADMIN_MCP_SERVER_IDS_KEY)
    return set(value) if isinstance(value, list) else None


def _is_allowed(allowed_ids: Optional[set[str]], candidates: list[Any]) -> bool:
    if allowed_ids is None:
        return True
    return any(str(candidate or "").strip() in allowed_ids for candidate in candidates)


def is_admin_model_allowed_for_user(
    user: Optional[UserModel], *candidate_ids: Any
) -> bool:
    return _is_allowed(get_allowed_admin_model_ids(user), list(candidate_ids))


def build_admin_model_resource_id(owner_id: Any, model: Any) -> str:
    owner = str(owner_id or "admin").strip()
    if isinstance(model, dict):
        model_id = str(
            model.get("selection_id")
            or model.get("id")
            or model.get("model")
            or model.get("name")
            or ""
        ).strip()
    else:
        model_id = str(model or "").strip()
    if not model_id:
        return ""
    return f"{owner}:model:{model_id}" if owner else model_id


def is_admin_mcp_server_allowed_for_user(
    user: Optional[UserModel], server_id: Any
) -> bool:
    return _is_allowed(get_allowed_admin_mcp_server_ids(user), [server_id])


MCP_CONNECTION_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")


def _normalize_mcp_connection_id(value: Any) -> str:
    connection_id = str(value or "").strip()
    return connection_id if MCP_CONNECTION_ID_RE.match(connection_id) else ""


def build_admin_mcp_server_resource_id(
    owner_id: Any, index: int, connection: Optional[dict] = None
) -> str:
    owner = str(owner_id or "admin").strip()
    stable_id = _normalize_mcp_connection_id(
        (connection or {}).get("id") if isinstance(connection, dict) else None
    )
    if stable_id:
        return f"{owner}:id:{stable_id}"
    return f"{owner}:{int(index)}"
