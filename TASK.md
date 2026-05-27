# TASK.md

## Current Goal

已完成: 修复 `custom` 分支用户资源继承指定模型/MCP 的回归风险, 收紧旧聊天 stale MCP 工具校验, 并补充项目收口规则。

## Completed

- 已确认项目根目录: `C:\Users\echo\Downloads\claude\github\HaloWebUI`.
- 已读取全局和项目规则: 父级 `C:\Users\echo\Downloads\claude` 只作为存放根目录, 本项目长期二创在 `custom`, `main` 保持贴近 upstream.
- 已拉取作者最新代码:
  - `upstream/main` 更新到 `f48d77a`.
  - 新增作者提交: API key 批量添加, 多模型讨论功能.
- 已同步 `origin/main` 到作者最新 `upstream/main`.
- 已把 `upstream/main` 合入 `custom`, merge commit: `eb8f4c5 Merge upstream main into custom`.
- 已人工解决 `src/lib/components/chat/Chat.svelte` 冲突:
  - 保留作者多模型讨论功能.
  - 保留 fork 的工具/技能选择过滤.
  - 保留 MCP stable id / 旧聊天发送状态修复.
  - 保留 chat completion 事件去重提交逻辑.
- 已完成 subagent 只读审计并关闭 subagent.
- 已补写干净 UTF-8 的 `TASK.md` / `LOG.md`, 替换原乱码接力内容.
- 已推送 `origin/custom` 和 `origin/future` 到 `d502e13`.
- 已确认 GitHub `Custom Regression Guard` 和 Docker 镜像 workflow 在 `custom` / `future` 全部成功.
- 已按用户要求确认: `main` 只作为作者同步线, 二创修复不写入 `main`.
- 已在 `AGENTS.md` 增加规则: 项目无需刻意重复打磨, 没有永远完美的项目; 完成目标、通过必要验证、风险可解释后应收口.
- 已用 2 个 subagent 复测继承链路:
  - 后端指出 normalize 会把畸形指定值放大成全部允许, MCP tool id 校验过松.
  - 前端指出指定模式在 options 未加载时可误保存空数组.
- 已修复后端继承 normalize:
  - `admin_models` / `admin_mcp_servers` 支持字符串布尔解析, `"false"` / `"0"` 不再被当作 true.
  - `admin_model_ids` / `admin_mcp_server_ids` 的畸形非 list 输入不再回退到 `None` 全量允许, 而是按空指定列表处理.
- 已修复本地 OpenAPI/MCP tool id 权限校验:
  - `validate_tool_ids_access` 现在会按当前用户过滤后的连接表解析 `server:` / `server_id:` / `mcp:` / `mcp_id:`.
  - 旧聊天里已删除、被继承指定列表排除、或被重新映射后不存在的 MCP 工具会被拒绝或在 sanitize 阶段清掉.
- 已修复用户编辑前端:
  - 指定模型/MCP 时复用同一次 options 加载 promise.
  - 指定模式保存前会确保资源继承选项已加载; 加载失败会阻止保存并提示.
  - options 正在加载时保存按钮禁用, 避免把“未加载”误保存成空指定.
  - 补齐英文/中文资源继承提示文案.

## Validation

- `rg -n "^(<<<<<<<|=======|>>>>>>>)" .`: 无冲突标记.
- `git diff --check`: 通过, 仅有 Git line-ending 提示.
- `uv run pytest backend/open_webui/test/unit/test_multi_model_discussion.py backend/open_webui/test/unit/test_model_reasoning_priority.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py -q`: 37 passed.
- `uv run pytest backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_model_reasoning_priority.py backend/open_webui/test/unit/test_multi_model_discussion.py -q`: 40 passed.
- `npx vitest run src/lib/apis/streaming/index.test.ts src/lib/utils/chat-response-state.test.ts src/lib/utils/chat-model-recovery.test.ts src/lib/utils/tool-selection.test.ts src/lib/utils/skill-selection.test.ts`: 33 passed.
- `npx vitest run src/lib/utils/chat-event-state.test.ts`: 2 passed.
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: 通过.
- `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py -q`: 35 passed.
- `npx vitest run src/lib/utils/resource-inheritance.test.ts`: 9 passed.
- `node -e "...JSON.parse..."`: en-US / zh-CN i18n JSON 均通过解析.
- `git diff --check`: 通过, 仅有 Git line-ending 提示.
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: 通过, 仅有既有 Svelte a11y/unused warnings.
- `npm run check`: 未通过; 失败来自全仓既有 5639 个类型诊断, 主要是旧 implicit any / i18n store 类型问题, 非本轮改动文件的单点回归.
- GitHub Actions:
  - `custom` Custom Regression Guard: success, run `26470361170`.
  - `future` Custom Regression Guard: success, run `26470363875`.
  - `custom` Docker workflow: success, run `26470361171`.
  - `future` Docker workflow: success, run `26470363938`.
- GHCR:
  - `ghcr.io/zhizhishu/halowebui:custom`: `sha256:557eb5029bcd47e9fdcd2a404343d0baceee124237805b8d8f6fd7d2f997300b`, includes `linux/amd64` and `linux/arm64`.
  - `ghcr.io/zhizhishu/halowebui:future`: `sha256:19742967a9259e24a10057d521b95e0d9d4e2e4eff23d3ae4465ec3326c25ab8`, includes `linux/amd64` and `linux/arm64`.

## Next Steps

- 当前用户继承指定模型/MCP 修复已在本地通过 targeted tests 和生产构建.
- 下一步如需发布, 在 `custom` 提交并推送, 再同步到 `future`; 不把二创修复写入 `main`.

## Risks

- 本轮主要冲突点是 `Chat.svelte`; 已经用 targeted tests 和生产构建覆盖.
- 作者新增多模型讨论会多次调用 `generate_chat_completion`; 已确认路径继续带 `user` 和当前 request, 继承模型/MCP 相关测试通过.
- 当前未启动 dev server, 未占用端口, 未打开浏览器.
- `main` 保持作者基线; `main` 的 CI 红点来自格式检查和少量全量测试预期, 本轮未在 `main` 写入二创修复.
- 本轮改动涉及共享工具校验路径, 已用 stale MCP 和继承指定测试覆盖; 仍建议部署后用一个普通用户实测“指定一个 MCP / 指定一个模型 / 旧聊天带旧 mcp id”三条路径.

## Last Updated

2026-05-27 04:10 -07:00
