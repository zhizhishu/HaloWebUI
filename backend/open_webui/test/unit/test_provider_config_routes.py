import asyncio
import pathlib
import sys
from types import SimpleNamespace

import pytest


_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.models.users import UserModel, UserSettings


def _make_user(connections: dict) -> UserModel:
    return UserModel(
        id="admin-1",
        name="Admin",
        email="admin@example.com",
        role="admin",
        profile_image_url="",
        last_active_at=0,
        updated_at=0,
        created_at=0,
        settings=UserSettings(ui={"connections": connections}),
    )


def _make_request():
    config = SimpleNamespace(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[],
        OPENAI_API_KEYS=[],
        OPENAI_API_CONFIGS={},
        ENABLE_GEMINI_API=True,
        GEMINI_API_BASE_URLS=[],
        GEMINI_API_KEYS=[],
        GEMINI_API_CONFIGS={},
        ENABLE_GROK_API=True,
        GROK_API_BASE_URLS=[],
        GROK_API_KEYS=[],
        GROK_API_CONFIGS={},
        ENABLE_ANTHROPIC_API=True,
        ANTHROPIC_API_BASE_URLS=[],
        ANTHROPIC_API_KEYS=[],
        ANTHROPIC_API_CONFIGS={},
        ENABLE_OLLAMA_API=True,
        OLLAMA_BASE_URLS=[],
        OLLAMA_API_CONFIGS={},
    )
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(config=config)))


@pytest.mark.parametrize(
    "module_name,provider,expected",
    [
        (
            "openai",
            "openai",
            {
                "OPENAI_API_BASE_URLS": ["https://openai.example.com/v1"],
                "OPENAI_API_KEYS": ["sk-openai"],
                "OPENAI_API_CONFIGS": {"0": {"name": "OpenAI Proxy"}},
            },
        ),
        (
            "gemini",
            "gemini",
            {
                "GEMINI_API_BASE_URLS": ["https://gemini.example.com/v1beta"],
                "GEMINI_API_KEYS": ["sk-gemini"],
                "GEMINI_API_CONFIGS": {"0": {"name": "Gemini Proxy"}},
            },
        ),
        (
            "grok",
            "grok",
            {
                "GROK_API_BASE_URLS": ["https://grok.example.com/v1"],
                "GROK_API_KEYS": ["sk-grok"],
                "GROK_API_CONFIGS": {"0": {"name": "Grok Proxy"}},
            },
        ),
        (
            "anthropic",
            "anthropic",
            {
                "ANTHROPIC_API_BASE_URLS": ["https://anthropic.example.com"],
                "ANTHROPIC_API_KEYS": ["sk-anthropic"],
                "ANTHROPIC_API_CONFIGS": {"0": {"name": "Anthropic Proxy"}},
            },
        ),
        (
            "ollama",
            "ollama",
            {
                "OLLAMA_BASE_URLS": ["https://ollama.example.com"],
                "OLLAMA_API_CONFIGS": {"0": {"name": "Ollama Proxy"}},
            },
        ),
    ],
)
def test_provider_config_routes_read_user_level_connections(
    module_name, provider, expected
):
    router = __import__(
        f"open_webui.routers.{module_name}", fromlist=["get_config"]
    )
    request = _make_request()
    user = _make_user({provider: expected})

    result = asyncio.run(router.get_config(request, user=user))

    for key, value in expected.items():
        if key.endswith("_CONFIGS"):
            assert result[key]["0"]["name"] == value["0"]["name"]
            assert result[key]["0"].get("prefix_id")
        else:
            assert result[key] == value


def test_openai_config_update_persists_user_level_connections(monkeypatch):
    from open_webui.routers import openai as openai_router
    from open_webui.utils import user_connections as user_connections_mod

    stored_user = _make_user({"openai": {}})

    def get_user_by_id(user_id):
        return stored_user if user_id == stored_user.id else None

    def update_user_settings_by_id(user_id, patch):
        nonlocal stored_user
        assert user_id == stored_user.id
        stored_user = stored_user.model_copy(
            update={
                "settings": UserSettings.model_validate(
                    {**stored_user.settings.model_dump(), **patch}
                )
            }
        )
        return stored_user

    monkeypatch.setattr(
        user_connections_mod.Users, "get_user_by_id", get_user_by_id
    )
    monkeypatch.setattr(
        user_connections_mod.Users,
        "update_user_settings_by_id",
        update_user_settings_by_id,
    )

    request = _make_request()
    form = openai_router.OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=["https://relay.example.com/v1"],
        OPENAI_API_KEYS=["sk-new"],
        OPENAI_API_CONFIGS={"0": {"name": "Relay"}},
    )

    result = asyncio.run(openai_router.update_config(request, form, user=stored_user))

    assert result["OPENAI_API_BASE_URLS"] == ["https://relay.example.com/v1"]
    assert result["OPENAI_API_KEYS"] == ["sk-new"]
    assert (
        stored_user.settings.ui["connections"]["openai"]["OPENAI_API_KEYS"]
        == ["sk-new"]
    )
