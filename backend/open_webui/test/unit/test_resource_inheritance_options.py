import asyncio
import pathlib
import sys
from types import SimpleNamespace


_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.routers import users as users_router
from open_webui.models.models import Models
from open_webui.models.users import UserModel, UserSettings


class _WorkspaceModel:
    id = "workspace-preset"
    user_id = "admin-1"
    name = "Workspace Preset"
    is_active = True
    base_model_id = "admin.gpt"


def _make_admin():
    return UserModel(
        id="admin-1",
        name="Admin",
        email="admin@example.com",
        role="admin",
        profile_image_url="",
        last_active_at=0,
        updated_at=0,
        created_at=0,
        settings=UserSettings(ui={"connections": {}}),
    )


def _make_request():
    return SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(config=SimpleNamespace())),
        state=SimpleNamespace(),
    )


def test_resource_inheritance_options_include_admin_models_and_mcp(monkeypatch):
    admin = _make_admin()

    async def fake_get_all_base_models(_request, user=None):
        if getattr(user, "id", None) == admin.id:
            return [{"id": "admin.gpt", "name": "Admin GPT"}]
        return []

    monkeypatch.setattr(users_router.Users, "get_users", lambda: [admin])
    monkeypatch.setattr(
        "open_webui.utils.models.get_all_base_models", fake_get_all_base_models
    )
    monkeypatch.setattr(Models, "get_all_models", lambda: [_WorkspaceModel()])
    monkeypatch.setattr(
        users_router,
        "get_admin_mcp_inheritance_connections",
        lambda _request: [
            {
                "_inherit_id": "admin-1:0",
                "_inherited_from_user_id": "admin-1",
                "url": "https://mcp.example.com",
                "name": "Admin MCP",
                "transport_type": "streamable_http",
                "tool_count": 3,
            }
        ],
    )

    result = asyncio.run(
        users_router.get_resource_inheritance_options(_make_request(), session_user=admin)
    )

    assert result["admin_models"][0]["id"] == "admin.gpt"
    assert result["admin_models"][0]["owner_name"] == "Admin"
    assert result["admin_mcp_servers"][0]["id"] == "admin-1:0"
    assert result["admin_mcp_servers"][0]["name"] == "Admin MCP"
