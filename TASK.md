# TASK.md

## Current Goal

本轮用户管理“模型继承 / MCP 继承”可选范围 UI 修复，以及 `gpt-image-2` / OpenAI Images 兼容站 stream 参数回退修复已完成；当前追加修复继承模式控件无法点击/点击不生效问题，改为显式按钮事件链，待推送并等 CI/GHCR 后线上复测。

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

2026-06-08 04:05 -07:00


## Active Follow-up

用户在线上 `https://chat.agent-ai.vip/settings/account` 反馈资源继承仍像锁定/不可选。已用真实浏览器复测当前线上页面：编辑普通用户 `Duduen` 时，按钮 DOM 可点，但点击 `Specified` 后页面无 DOM 变化；当前加载的前端资产 `11.aKEI9WGW.js` 仍只有旧 `Specified / Disabled` 文案，未包含新 `Choose resources / Disable inheritance`，判断服务器仍跑旧前端包或未重建容器。

已完成：
- 修复提交 `3d3dd82 fix resource inheritance mode selector interaction` 已在 `future` / `custom`。
- GitHub Actions 已确认：
  - `future` Custom Regression Guard `27128391071`: success。
  - `future` Docker / GHCR workflow `27128391025`: success。
  - `custom` Custom Regression Guard `27128393562`: success。
  - `custom` Docker / GHCR workflow `27128393259`: success。
- GHCR 最新 manifest：
  - `ghcr.io/zhizhishu/halowebui:custom`: `sha256:48cf391d8a50273b750b9fc78ca3740bc8ee29c99c319975d47623e2c3873996`。
  - `ghcr.io/zhizhishu/halowebui:future`: `sha256:dfe6d2fb5ce359131727c1c357870ee8e96acf7f27adc034e0461ab7a84a072d`。
  - `ghcr.io/zhizhishu/halowebui:git-3d3dd82-slim`: `sha256:ee9720fd247d34323b6cd0935df91df73d8e0637a39652ea42523d64bf475edd`。

下一步：
- 当前追加修复：`EditUserModal.svelte` 将继承模式 radio/label 改为真正 `<button type="button" role="radio">`，同时绑定 `pointerdown` 和 `click` 显式调用 `setResourceMode`，避免隐藏 radio/label 默认行为在真实弹窗里不触发。
- 本地验证：
  - `npx --yes vitest run src/lib/utils/resource-inheritance.test.ts src/lib/utils/api-key-pool.test.ts --reporter=dot`: 12 passed。
  - `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py -q`: 35 passed, 3 warnings。
  - `svelte/compiler` + `svelte-preprocess` 单文件编译 `EditUserModal.svelte`: ok, no warnings。
  - `git diff --check`: passed，仅 Windows line-ending 提示。
- `npm run build` / `npm run check` 在本机 Windows 环境超时无输出，未得到功能错误；以单文件 Svelte 编译和 targeted tests 先兜底。
- 下一步：提交推送 `future/custom`，等待 CI/GHCR 后服务器重建 `halowebui` 容器并复测：点击 `指定资源` 应展示可选资源列表。
