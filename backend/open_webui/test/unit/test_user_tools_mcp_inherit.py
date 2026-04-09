import pathlib
import sys
from types import SimpleNamespace


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
        role="admin",
        settings=_Settings({"tools": {"mcp_server_connections": admin_connections}}),
    )

    monkeypatch.setattr(user_tools_mod.Users, "get_users", lambda: [admin_user])

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(role="user", settings=_Settings({}))

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert len(result) == 1
    assert result[0]["url"] == "https://mcp.example.com"
    assert result[0]["key"] == "admin-secret-key"
    assert result[0]["headers"]["X-Api-Key"] == "shared-header-key"
    assert all((item.get("transport_type") or "http").lower() != "stdio" for item in result)


def test_regular_user_does_not_inherit_when_disabled(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
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
    regular_user = SimpleNamespace(role="user", settings=_Settings({}))

    result = user_tools_mod.get_user_mcp_server_connections(request, regular_user)

    assert result == []


def test_regular_user_own_connections_override_admin_inheritance(monkeypatch):
    from open_webui.utils import user_tools as user_tools_mod

    admin_user = SimpleNamespace(
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

    request = _build_request(inherit_enabled=True)
    regular_user = SimpleNamespace(
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
