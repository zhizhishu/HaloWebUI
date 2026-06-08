# TASK.md

## Current Goal

已完成本地合并与验证: 将作者最新 `upstream/main` (`37269bb`) 同步到 `main`, 合入二创分支 `custom`, 并准备同步到 `future` / 推送后等待 CI 与 GHCR。

## Completed

- 已确认项目根目录: `C:\Users\echo\Downloads\claude\github\HaloWebUI`.
- 已拉取作者最新 `upstream/main` 到 `37269bb`.
- 已将本地 `main` 快进到作者最新 `37269bb`; `origin/main` 已与作者线一致, 未写入二创改动.
- 已将 `main` 合入 `custom`, 本轮冲突文件:
  - `backend/open_webui/main.py`: 同时保留上游模型缓存失效 `invalidate_base_model_cache` 和 fork 的 `get_inherited_model_owner_id`.
  - `src/lib/components/chat/Chat.svelte`: 使用上游 `restoreChatInputDraft`, 同时保留 fork 的异常回退清理、工具/技能状态保护、旧聊天状态恢复链路.
- 已处理上游图片生成逻辑与 fork key-pool 兼容层的回归:
  - `backend/open_webui/routers/images.py`: settings 读取不再把单个显式图片 key 扩展成合成 `api_key_pool`; runtime 仍通过 key-pool 尝试逻辑使用单 key / 多 key.
  - `backend/open_webui/test/unit/test_image_settings_url_normalization.py`: 修正自动合并出的重复/错误 monkeypatch, 并让 mock response 显式提供 `elapsed_ms` 以覆盖 usage.
- 已确认关键二创能力仍在:
  - 用户继承管理员模型/MCP: 全部/指定/禁用.
  - stale MCP tool id 拒绝/清理.
  - 旧聊天发送状态、事件去重、模型恢复、工具/技能过滤.
  - API key pool 与图片生成连接选择.

## Validation

- 失败子集复测: `5 passed, 6 warnings`.
- `uv run pytest ... -q` 目标后端套件: `234 passed, 6 warnings`.
- `npx vitest run ...`: `10 files passed, 65 tests passed`.
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: 通过, `✓ built in 12m 28s`, 仅既有 Svelte a11y/unused warnings.
- `git diff --cached --check`: 通过, 仅 Windows line-ending 提示.
- 冲突标记: 已在冲突文件确认清空.

## Next Steps

- 推送 `custom` 到 `origin/custom`.
- 将 `custom` 快进同步到 `future`, 推送 `origin/future`.
- 等待 GitHub Actions / GHCR 完成最新 `custom` / `future` 镜像构建.
- 不把二创修复写入 `main`; `main` 继续保持作者纯净同步线.

## Risks

- 本轮作者更新较大, 包含图片生成、模型缓存、数据管理、PDF 字体、聊天输入/展示等路径; 已用后端图片/缓存/数据管理测试和生产构建覆盖.
- `Chat.svelte` 仍是长期高冲突文件; 本轮采用最小合并, 保留上游 draft restore 与 fork 状态保护.
- `npm run build` 在 Windows 本地耗时约 12 分钟; 首次 10 分钟超时后确认本轮构建进程归属并等待结束, 第二次落日志成功.
- 当前未启动 dev server, 未打开浏览器, 未占用项目端口.

## Last Updated

2026-06-07 20:03 -07:00
