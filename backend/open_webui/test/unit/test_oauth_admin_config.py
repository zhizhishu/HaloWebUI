from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from open_webui import config as webui_config
from open_webui.routers import auths as auths_router


def _request(webui_url="https://halo.example.com", existing_secret=""):
    config = SimpleNamespace(
        WEBUI_URL=webui_url,
        OAUTH_CLIENT_SECRET=existing_secret,
    )
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(config=config)))


def _form(**overrides):
    data = {
        "ENABLE_OAUTH_LOGIN": True,
        "WEBUI_URL": "https://halo.example.com",
        "OAUTH_PROVIDER_NAME": "Authentik",
        "OPENID_PROVIDER_URL": "https://auth.example.com/application/o/halo/.well-known/openid-configuration",
        "OAUTH_CLIENT_ID": "client-id",
        "OAUTH_CLIENT_SECRET": "client-secret",
        "OAUTH_SCOPES": "openid email profile",
        "ENABLE_OAUTH_SIGNUP": True,
        "OAUTH_MERGE_ACCOUNTS_BY_EMAIL": False,
        "OAUTH_ALLOWED_DOMAINS": "*",
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_oauth_admin_update_requires_secret_when_enabled():
    with pytest.raises(HTTPException) as exc_info:
        auths_router._prepare_oauth_admin_update(
            _request(existing_secret=""),
            _form(OAUTH_CLIENT_SECRET=""),
        )

    assert exc_info.value.status_code == 400
    assert "客户端密钥未填写" in exc_info.value.detail


def test_oauth_admin_update_keeps_existing_secret_when_blank():
    update = auths_router._prepare_oauth_admin_update(
        _request(existing_secret="stored-secret"),
        _form(OAUTH_CLIENT_SECRET=""),
    )

    assert update["client_secret"] == ""
    assert update["redirect_uri"] == "https://halo.example.com/oauth/oidc/callback"


def test_oauth_admin_update_accepts_disabled_without_required_fields():
    update = auths_router._prepare_oauth_admin_update(
        _request(),
        _form(
            ENABLE_OAUTH_LOGIN=False,
            OPENID_PROVIDER_URL="",
            OAUTH_CLIENT_ID="",
            OAUTH_CLIENT_SECRET="",
        ),
    )

    assert update["enabled"] is False


def test_oauth_admin_config_never_returns_secret(monkeypatch):
    monkeypatch.setattr(auths_router.ENABLE_OAUTH_LOGIN, "value", True)
    monkeypatch.setattr(auths_router.OAUTH_PROVIDER_NAME, "value", "Authentik")
    monkeypatch.setattr(
        auths_router.OPENID_PROVIDER_URL,
        "value",
        "https://auth.example.com/application/o/halo/.well-known/openid-configuration",
    )
    monkeypatch.setattr(auths_router.OPENID_REDIRECT_URI, "value", "")
    monkeypatch.setattr(auths_router.OAUTH_CLIENT_ID, "value", "client-id")
    monkeypatch.setattr(auths_router.OAUTH_CLIENT_SECRET, "value", "stored-secret")
    monkeypatch.setattr(auths_router.OAUTH_SCOPES, "value", "openid email profile")
    monkeypatch.setattr(auths_router.ENABLE_OAUTH_SIGNUP, "value", True)
    monkeypatch.setattr(auths_router.OAUTH_MERGE_ACCOUNTS_BY_EMAIL, "value", False)
    monkeypatch.setattr(auths_router.OAUTH_ALLOWED_DOMAINS, "value", ["*"])

    config = auths_router._get_oauth_admin_config(_request())

    assert config["OAUTH_CLIENT_SECRET"] == ""
    assert config["OAUTH_CLIENT_SECRET_CONFIGURED"] is True
    assert (
        config["OPENID_REDIRECT_URI"] == "https://halo.example.com/oauth/oidc/callback"
    )


def test_oauth_provider_list_follows_admin_enable_flag(monkeypatch):
    original_providers = dict(webui_config.OAUTH_PROVIDERS)

    try:
        monkeypatch.setattr(webui_config.OAUTH_CLIENT_ID, "value", "client-id")
        monkeypatch.setattr(webui_config.OAUTH_CLIENT_SECRET, "value", "client-secret")
        monkeypatch.setattr(
            webui_config.OPENID_PROVIDER_URL,
            "value",
            "https://auth.example.com/application/o/halo/.well-known/openid-configuration",
        )
        monkeypatch.setattr(
            webui_config.OPENID_REDIRECT_URI,
            "value",
            "https://halo.example.com/oauth/oidc/callback",
        )
        monkeypatch.setattr(webui_config.OAUTH_PROVIDER_NAME, "value", "Authentik")

        monkeypatch.setattr(webui_config.ENABLE_OAUTH_LOGIN, "value", True)
        webui_config.load_oauth_providers()
        assert webui_config.OAUTH_PROVIDERS["oidc"]["name"] == "Authentik"

        monkeypatch.setattr(webui_config.ENABLE_OAUTH_LOGIN, "value", False)
        webui_config.load_oauth_providers()
        assert "oidc" not in webui_config.OAUTH_PROVIDERS
    finally:
        webui_config.OAUTH_PROVIDERS.clear()
        webui_config.OAUTH_PROVIDERS.update(original_providers)
