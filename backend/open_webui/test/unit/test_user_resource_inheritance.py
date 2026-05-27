import pathlib
import sys


_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))


def test_resource_inheritance_normalize_defaults_to_all():
    from open_webui.utils.user_resource_inheritance import (
        DEFAULT_RESOURCE_INHERITANCE,
        normalize_resource_inheritance,
    )

    assert normalize_resource_inheritance(None) == DEFAULT_RESOURCE_INHERITANCE


def test_resource_inheritance_normalize_preserves_empty_specified_lists():
    from open_webui.utils.user_resource_inheritance import (
        normalize_resource_inheritance,
    )

    result = normalize_resource_inheritance(
        {
            "admin_models": True,
            "admin_model_ids": [],
            "admin_mcp_servers": True,
            "admin_mcp_server_ids": [],
        }
    )

    assert result["admin_model_ids"] == []
    assert result["admin_mcp_server_ids"] == []


def test_resource_inheritance_normalize_does_not_expand_malformed_ids_to_all():
    from open_webui.utils.user_resource_inheritance import (
        normalize_resource_inheritance,
    )

    result = normalize_resource_inheritance(
        {
            "admin_model_ids": "admin:model:gpt",
            "admin_mcp_server_ids": {"id": "admin-1:0"},
        }
    )

    assert result["admin_model_ids"] == []
    assert result["admin_mcp_server_ids"] == []


def test_resource_inheritance_normalize_parses_string_booleans():
    from open_webui.utils.user_resource_inheritance import (
        normalize_resource_inheritance,
    )

    result = normalize_resource_inheritance(
        {
            "admin_models": "false",
            "admin_mcp_servers": "0",
        }
    )

    assert result["admin_models"] is False
    assert result["admin_mcp_servers"] is False
