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


def test_zip_import_route_passes_fallback_identifier(monkeypatch):
    captured = {}

    class _Upload:
        filename = "catalog-skill.zip"

        async def read(self):
            return b"zip-bytes"

    async def fake_import_skill_from_zip(filename, buffer, fallback_identifier=None):
        captured["filename"] = filename
        captured["buffer"] = buffer
        captured["fallback_identifier"] = fallback_identifier
        return SimpleNamespace(identifier=fallback_identifier, name="Catalog Skill")

    async def fake_upsert_imported_skill(user, payload):
        captured["user_id"] = user.id
        return {"skill": payload, "status": "created"}

    monkeypatch.setattr(skill_routes, "import_skill_from_zip", fake_import_skill_from_zip)
    monkeypatch.setattr(skill_routes, "_upsert_imported_skill", fake_upsert_imported_skill)

    result = asyncio.run(
        skill_routes.import_skill_from_zip_route(
            SimpleNamespace(),
            file=_Upload(),
            fallback_identifier="anthropics-skills-pdf",
            user=SimpleNamespace(id="admin-1", role="admin"),
        )
    )

    assert result["status"] == "created"
    assert captured == {
        "filename": "catalog-skill.zip",
        "buffer": b"zip-bytes",
        "fallback_identifier": "anthropics-skills-pdf",
        "user_id": "admin-1",
    }
