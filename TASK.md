# TASK.md

## Current Goal

本轮用户管理“模型继承 / MCP 继承”可选范围 UI 修复，以及 `gpt-image-2` / OpenAI Images 兼容站 stream 参数回退修复已完成；`custom` 与 `future` 已同步到同一提交并推送，CI / GHCR 已通过。

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
- Git：
  - 修复提交: `8e958f0 fix user inheritance controls and image stream fallback`。
  - `origin/future` 已推送到 `8e958f0`。
  - `origin/custom` 已快进同步到 `8e958f0`。
  - `main` / `origin/main` / `upstream/main` 保持作者线 `37269bb`，未混入二创修复。

## Validation

- 本地：
  - `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py backend/open_webui/test/unit/test_openai_image_node_helper.py backend/open_webui/test/unit/test_image_settings_url_normalization.py -q`: `139 passed, 6 warnings`。
  - `npx vitest run src/lib/utils/resource-inheritance.test.ts src/lib/utils/api-key-pool.test.ts`: `2 files passed, 12 tests passed`。
  - `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: 通过，仅既有 Svelte a11y/unused 与 chunk/pyodide warnings。
  - `git diff --check`: 通过，仅 Windows line-ending 提示。
- GitHub Actions：
  - `future` Custom Regression Guard `27123061077`: success。
  - `future` Docker / GHCR workflow `27123061117`: success。
  - `custom` Custom Regression Guard `27123644304`: success。
  - `custom` Docker / GHCR workflow `27123644271`: success。
- GHCR：
  - `ghcr.io/zhizhishu/halowebui:future`: `sha256:00dafb3099b60e7ae0471e5533a21e2baf3387d80e2368978620cea98072afee`。
  - `ghcr.io/zhizhishu/halowebui:custom`: `sha256:37c7c472e954826c0f96d2d1065444cdd1ea61b7bb062b47fcc242e9261fe176`。
  - `ghcr.io/zhizhishu/halowebui:git-8e958f0-slim`: `sha256:a86cbd9d65535bfea4f269b45ccdc8bd46ab4723c5983575d094e415d11b2b29`。

## Next Steps

- 部署后建议用管理员页面实测：普通用户指定 1 个模型、指定 1 个 MCP、清空指定列表、切回全部/禁用。
- 部署后建议用兼容 OpenAI Images 的 `gpt-image-2` 供应商实测：generation 与 edit 各一次，确认 stream 不支持时可回退。

## Risks

- `EditUserModal.svelte` 是用户管理共享 UI，后续同步上游时可能有小冲突；本轮为局部 UI 和状态初始化修复。
- 图片生成兼容逻辑只在 `400/422` 且错误文本同时命中 stream/partial_images 与 unsupported/unknown 参数时回退，避免吞掉其他真实错误。
- GitHub Actions 当前有 Node.js 20 deprecation annotation，非本轮功能失败；后续可单独升级 actions/runtime。
- 当前未启动 dev server，未打开浏览器，未占用项目端口。

## Last Updated

2026-06-08 02:22 -07:00


## Active Follow-up

用户在线上 `https://chat.agent-ai.vip/settings/account` 反馈资源继承仍像锁定/不可选。已用 Browser Relay 验证线上真实行为：编辑普通用户 `Duduen` 时，`All / Specified / Disabled` 按钮 DOM 为可点且 `pointer-events: auto`，但点击 `Specified` 后继承区域文本和状态不变，确认前端交互仍有回归。

本地修复：
- `EditUserModal.svelte` 将继承范围控件从纯按钮改为原生 radio group + label，避免按钮事件链不触发时状态无法切换。
- 文案从 `All / Specified / Disabled` 改为更明确的 `Inherit all / Choose resources / Disable inheritance`，中文为 `全部继承 / 指定资源 / 不继承`，避免“已禁用”被误解成控件锁定。

验证：
- `npx vitest run src/lib/utils/resource-inheritance.test.ts src/lib/utils/api-key-pool.test.ts`: 12 passed。
- `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py -q`: 35 passed, 3 warnings。
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: passed，仅既有 warnings。

下一步：提交并推送 `future/custom`，等待 CI/GHCR 后让服务器重新 `docker pull ghcr.io/zhizhishu/halowebui:custom` 并重建容器。
