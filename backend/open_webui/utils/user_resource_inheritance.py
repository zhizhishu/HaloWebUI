from __future__ import annotations

from typing import Any, Optional

from open_webui.models.users import UserModel


RESOURCE_INHERITANCE_KEY = "resource_inheritance"
INHERIT_ADMIN_MODELS_KEY = "admin_models"
INHERIT_ADMIN_MCP_SERVERS_KEY = "admin_mcp_servers"

DEFAULT_RESOURCE_INHERITANCE = {
    INHERIT_ADMIN_MODELS_KEY: True,
    INHERIT_ADMIN_MCP_SERVERS_KEY: True,
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


def normalize_resource_inheritance(value: Any) -> dict:
    raw = _as_dict(value)
    return {
        key: bool(raw.get(key, default))
        for key, default in DEFAULT_RESOURCE_INHERITANCE.items()
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
