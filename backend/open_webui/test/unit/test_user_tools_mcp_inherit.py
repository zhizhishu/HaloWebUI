import pathlib
import sys
from types import SimpleNamespace

import pytest
from fastapi import HTTPException


# Ensure `open_webui` is importable when running tests from repo root.
_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))


class _Settings:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self):
        return self._payload


def _build_request(*, inherit_enabled: bool, legacy_connections=None):
    return SimpleNamespace(
        app=SimpleNamespace(
            state=SimpleNamespace(
                config=SimpleNamespace(
                    ENABLE_MCP_SERVER_INHERIT_FROM_ADMIN=inherit_enabled,
                    MCP_SERVER_CONNECTIONS=legacy_connections or [],
                    USER_PERMISSIONS={"features": {"direct_tool_servers": False}},
                )
            )
        )
    )


def test_regular_user_inherits_admin_mcp_connections_and_filters_stdio(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_connections = [
        {
            "transport_type": "http",
            "url": "https://mcp.example.com",
            "auth_type": "bearer",
            "key": "admin-secret-key",
            "headers": {"X-Api-Key": "shared-header-key"},
        },
        {
            "transport_type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-time"],
        },
    ]

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings({"tools": {"mcp_server_connections": admin_connections}}),
    )

    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(id="user-1", role="user", settings=_Settings({}))

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert len(result) == 1
    assert result[0]["url"] == "https://mcp.example.com"
    assert result[0]["key"] == "admin-secret-key"
    assert result[0]["headers"]["X-Api-Key"] == "shared-header-key"
    assert all((item.get("transport_type") or "http").lower() != "stdio" for item in result)


def test_regular_user_does_not_inherit_when_disabled(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://mcp.example.com"}
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=False)
    regular_user = SimpleNamespace(id="user-1", role="user", settings=_Settings({}))

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert result == []


def test_regular_user_resource_setting_disables_admin_mcp_inheritance(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://mcp.example.com"}
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "resource_inheritance": {
                    "admin_models": True,
                    "admin_mcp_servers": False,
                }
            }
        ),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert result == []


def test_regular_user_empty_own_mcp_connections_can_still_inherit(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://mcp.example.com"}
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings({"tools": {"mcp_server_connections": []}}),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert len(result) == 1
    assert result[0]["url"] == "https://mcp.example.com"


def test_regular_user_own_connections_override_admin_inheritance(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://admin-mcp.example.com"}
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])
    monkeypatch.setattr(user_tools_mod, "has_permission", lambda *_args, **_kwargs: True)

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://user-mcp.example.com"}
                    ]
                }
            }
        ),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert len(result) == 1
    assert result[0]["url"] == "https://user-mcp.example.com"


def test_regular_user_without_direct_tool_permission_uses_inherited_admin_mcp(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://admin-mcp.example.com"}
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])
    monkeypatch.setattr(user_tools_mod, "has_permission", lambda *_args, **_kwargs: False)

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://user-mcp.example.com"}
                    ]
                },
                "resource_inheritance": {
                    "admin_mcp_servers": True,
                    "admin_mcp_server_ids": ["admin-1:0"],
                },
            }
        ),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert len(result) == 1
    assert result[0]["url"] == "https://admin-mcp.example.com"


def test_regular_user_selected_admin_mcp_ids_filter_inherited_servers(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://first.example.com"},
                        {"transport_type": "http", "url": "https://second.example.com"},
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "resource_inheritance": {
                    "admin_mcp_servers": True,
                    "admin_mcp_server_ids": ["admin-1:1"],
                }
            }
        ),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert [item["url"] for item in result] == ["https://second.example.com"]


def test_regular_user_empty_selected_admin_mcp_ids_block_all_inherited_servers(
    monkeypatch,
):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
        id="admin-1",
        role="admin",
        settings=_Settings(
            {
                "tools": {
                    "mcp_server_connections": [
                        {"transport_type": "http", "url": "https://first.example.com"},
                        {"transport_type": "http", "url": "https://second.example.com"},
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "resource_inheritance": {
                    "admin_mcp_servers": True,
                    "admin_mcp_server_ids": [],
                }
            }
        ),
    )

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert result == []


def test_admin_mcp_inheritance_connections_mark_legacy_ids(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [])

    request = _build_request(
        inherit_enabled=True,
        legacy_connections=[
            {"transport_type": "http", "url": "https://legacy.example.com"}
        ],
    )

    result = user_tools_mod.get_admin_mcp_inheritance_connections(request)

    assert result[0]["_inherit_id"] == "legacy:0"
    assert result[0]["_inherited_from_user_id"] == "legacy"


def test_mcp_tool_ids_are_allowed_for_inherited_mcp_without_direct_permission(monkeypatch):
    from open_webui.utils import tools as tools_mod

    monkeypatch.setattr(
        tools_mod,
        "validate_requested_shared_tool_ids_access",
        lambda *_args, **_kwargs: None,
    )

    request = _build_request(inherit_enabled=True)
    user = SimpleNamespace(
        id="user-1",
        role="user",
        settings=_Settings(
            {
                "resource_inheritance": {
                    "admin_mcp_servers": True,
                }
            }
        ),
    )

    tools_mod.validate_tool_ids_access(["mcp:0"], user, request)

    with pytest.raises(HTTPException):
        tools_mod.validate_tool_ids_access(["server:0"], user, request)
