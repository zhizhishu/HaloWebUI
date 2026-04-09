import asyncio
import pathlib
import sys
from types import SimpleNamespace


_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.routers.openai import (  # noqa: E402
    _connection_supports_native_file_inputs,
    _get_default_responses_reasoning_summary,
    _looks_like_reasoning_summary_incompatible,
    _should_use_responses_api,
)
import open_webui.utils.middleware as middleware  # noqa: E402


def test_should_use_responses_api_respects_exclude_patterns():
    assert (
        _should_use_responses_api(
            "https://api.openai.com/v1",
            {"use_responses_api": True, "responses_api_exclude_patterns": ["mini"]},
            "gpt-4.1-mini",
        )
        is False
    )
    assert (
        _should_use_responses_api(
            "https://api.openai.com/v1",
            {"use_responses_api": True, "responses_api_exclude_patterns": ["mini"]},
            "gpt-4.1",
        )
        is True
    )


def test_should_use_responses_api_is_disabled_for_azure_connections():
    assert (
        _should_use_responses_api(
            "https://example-resource.openai.azure.com/openai/v1",
            {"use_responses_api": True, "azure": True},
            "gpt-4.1",
        )
        is False
    )


def test_connection_supports_native_file_inputs_defaults_to_official_openai_only():
    assert (
        _connection_supports_native_file_inputs(
            "https://api.openai.com/v1",
            {"use_responses_api": True},
        )
        is True
    )
    assert (
        _connection_supports_native_file_inputs(
            "https://openrouter.ai/api/v1",
            {"use_responses_api": True},
        )
        is False
    )


def test_connection_supports_native_file_inputs_honors_explicit_flag_and_guards():
    assert (
        _connection_supports_native_file_inputs(
            "https://proxy.example.com/v1",
            {"use_responses_api": True, "native_file_inputs_enabled": True},
        )
        is True
    )
    assert (
        _connection_supports_native_file_inputs(
            "https://api.openai.com/v1/chat/completions",
            {"use_responses_api": True, "native_file_inputs_enabled": True, "force_mode": True},
        )
        is False
    )
    assert (
        _connection_supports_native_file_inputs(
            "https://my-azure.openai.azure.com/openai/deployments/foo",
            {"use_responses_api": True, "native_file_inputs_enabled": True, "azure": True},
        )
        is False
    )
    assert (
        _connection_supports_native_file_inputs(
            "https://api.openai.com/v1",
            {"use_responses_api": False, "native_file_inputs_enabled": True},
        )
        is False
    )


def test_default_responses_reasoning_summary_defaults_to_auto_and_honors_overrides():
    assert _get_default_responses_reasoning_summary({"use_responses_api": True}) == "auto"
    assert (
        _get_default_responses_reasoning_summary(
            {"use_responses_api": True, "responses_reasoning_summary": False}
        )
        is None
    )
    assert (
        _get_default_responses_reasoning_summary(
            {"use_responses_api": True, "responses_reasoning_summary": "detailed"}
        )
        == "detailed"
    )


def test_looks_like_reasoning_summary_incompatible_matches_schema_errors():
    assert _looks_like_reasoning_summary_incompatible(
        400,
        {
            "error": {
                "message": "Unknown parameter: reasoning.summary",
            }
        },
    )
    assert _looks_like_reasoning_summary_incompatible(
        422,
        "Additional properties are not allowed ('summary' was unexpected in reasoning).",
    )
    assert not _looks_like_reasoning_summary_incompatible(
        400,
        {
            "error": {
                "message": "Unknown parameter: temperature",
            }
        },
    )


def test_prepare_openai_native_file_inputs_uploads_pdf_via_storage_provider(monkeypatch):
    file_id = "file_local_1"
    file_item = {"type": "file", "id": file_id, "processing_mode": "native_file"}
    file_obj = SimpleNamespace(
        id=file_id,
        path=f"/data/uploads/{file_id}_demo.pdf",
        filename="demo.pdf",
        meta={"content_type": "application/pdf"},
    )
    upload_call = {}

    monkeypatch.setattr(
        middleware.Files,
        "get_file_by_id",
        lambda current_file_id: file_obj if current_file_id == file_id else None,
    )
    monkeypatch.setattr(
        middleware,
        "_get_openai_user_config",
        lambda _user: (["https://api.openai.com/v1"], ["sk-test"], [{}]),
    )
    monkeypatch.setattr(
        middleware,
        "_resolve_openai_connection_by_model_id",
        lambda *_args, **_kwargs: (
            0,
            "https://api.openai.com/v1",
            "sk-test",
            {"use_responses_api": True},
        ),
    )
    monkeypatch.setattr(middleware, "_should_use_responses_api", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        middleware,
        "_connection_supports_native_file_inputs",
        lambda *_args, **_kwargs: True,
    )
    monkeypatch.setattr(middleware, "_get_openai_file_cache_key", lambda *_args, **_kwargs: "conn-1")
    monkeypatch.setattr(middleware, "_get_cached_openai_file_id", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(middleware, "_set_cached_openai_file_id", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        middleware.Storage,
        "get_file",
        lambda path: f"/tmp/{path.rsplit('/', 1)[-1]}",
    )

    async def fake_upload_file_to_openai(**kwargs):
        upload_call.update(kwargs)
        return "remote-file-1"

    monkeypatch.setattr(middleware, "_upload_file_to_openai", fake_upload_file_to_openai)

    request = SimpleNamespace(state=SimpleNamespace(connection_user=None))
    user = SimpleNamespace(id="user-1")
    form_data = {
        "model": "gpt-5.4",
        "messages": [
            {
                "role": "user",
                "content": "能看到这个文件吗？",
                "files": [dict(file_item)],
            }
        ],
    }
    metadata = {"files": [dict(file_item)]}

    asyncio.run(
        middleware._prepare_openai_native_file_inputs(
            request,
            form_data,
            metadata,
            user,
            {"id": "gpt-5.4", "owned_by": "openai"},
        )
    )

    assert upload_call["local_path"] == f"/tmp/{file_id}_demo.pdf"
    assert upload_call["filename"] == "demo.pdf"
    assert upload_call["content_type"] == "application/pdf"
    assert upload_call["user"] is user
    assert metadata["native_file_input_file_ids"] == [file_id]
    assert metadata["native_file_input_parts_by_message"] == {
        "0": [{"type": "input_file", "file_id": "remote-file-1"}]
    }
