# TASK.md

## Current Goal

本轮已完成用户管理“模型继承 / MCP 继承”可选范围 UI 修复，以及 `gpt-image-2` / OpenAI Images 兼容站 stream 参数回退修复；本地验证通过，代码准备提交并推送 `future`。

## Completed

- 已确认项目根目录: `C:\Users\echo\Downloads\claude\github\HaloWebUI`。
- 已确认作者 `upstream/main` 当前仍为 `37269bb`，未包含本轮修复点。
- 用户管理编辑弹窗：
  - 将继承范围从容易误点/不可见的下拉框改为 `All / Specified / Disabled` 三态按钮。
  - `Specified` 模式下展示可选管理员模型/MCP 列表，并提供 `Select all` / `Clear selection`。
  - 修复弹窗复用切换用户时编辑状态可能不重置的问题。
- 图片生成：
  - `gpt-image-*` 默认 stream / partial images 请求遇到兼容站 `400/422` 不支持时，自动移除 `stream` 与 `partial_images` 非流式重试。
  - `/images/edits` 同步支持同类非流式重试。
  - 修复 Images generations 返回 200 但无可识别图片时引用 chat 专属变量导致 `NameError` 的问题，改为可读 `HTTPException(400)`。
- i18n：补齐 `Select all` / `Clear selection` 中英文文案。

## Validation

- `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py backend/open_webui/test/unit/test_openai_image_node_helper.py backend/open_webui/test/unit/test_image_settings_url_normalization.py -q`: `139 passed, 6 warnings`。
- `npx vitest run src/lib/utils/resource-inheritance.test.ts src/lib/utils/api-key-pool.test.ts`: `2 files passed, 12 tests passed`。
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: 通过，仅既有 Svelte a11y/unused 与 chunk/pyodide warnings。
- `git diff --check`: 通过，仅 Windows line-ending 提示。

## Next Steps

- 提交本轮修复并推送 `future` 到 `origin/future`。
- 推送后等待 GitHub Actions / GHCR 构建结果。
- 部署后建议用管理员页面实测：普通用户指定 1 个模型、指定 1 个 MCP、清空指定列表、切回全部/禁用。
- 部署后建议用兼容 OpenAI Images 的 `gpt-image-2` 供应商实测：generation 与 edit 各一次，确认 stream 不支持时可回退。

## Risks

- `EditUserModal.svelte` 是用户管理共享 UI，后续同步上游时可能有小冲突；本轮为局部 UI 和状态初始化修复。
- 图片生成兼容逻辑只在 `400/422` 且错误文本同时命中 stream/partial_images 与 unsupported/unknown 参数时回退，避免吞掉其他真实错误。
- 当前未启动 dev server，未打开浏览器，未占用项目端口。

## Last Updated

2026-06-08 00:38 -07:00
