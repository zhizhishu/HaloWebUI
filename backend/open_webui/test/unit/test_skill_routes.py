import asyncio
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from open_webui.models.skills import SkillModel
from open_webui.routers import skills as skill_routes


def _skill(name: str):
    return SkillModel(
        id="skill-1",
        user_id="admin-1",
        name=name,
        description="",
        content="",
        source="manual",
        meta={},
        is_active=True,
        updated_at=1,
        created_at=1,
    )


def test_next_skill_prompt_command_uses_skill_name_and_avoids_duplicates(monkeypatch):
    existing_commands = {"skill-release-writer", "skill-release-writer-2"}
    monkeypatch.setattr(
        skill_routes.Prompts,
        "get_prompt_by_command",
        lambda command: object() if command in existing_commands else None,
    )

    assert (
        skill_routes._next_skill_prompt_command(_skill("Release Writer"))
        == "skill-release-writer-3"
    )


def test_non_admin_cannot_install_skill_runtime():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            skill_routes.install_skill_runtime_route(
                "skill-1", user=SimpleNamespace(role="user")
            )
        )

    assert exc_info.value.status_code == 403


def test_non_admin_cannot_uninstall_skill_runtime():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            skill_routes.uninstall_skill_runtime_route(
                "skill-1", user=SimpleNamespace(role="user")
            )
        )

    assert exc_info.value.status_code == 403


def test_non_admin_cannot_update_skill_auto_activation():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            skill_routes.update_skill_auto_activation_route(
                "skill-1",
                skill_routes.SkillAutoActivationForm(auto_enabled=True),
                user=SimpleNamespace(role="user"),
            )
        )

    assert exc_info.value.status_code == 403
