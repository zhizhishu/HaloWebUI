# PROJECT_MAP.md

## 快速找路
- 接口配置页面: `src/lib/components/admin/Settings/Connections.svelte`.
- provider 子卡片: `src/lib/components/admin/Settings/Connections/`.
- 用户资源继承 UI: `src/lib/components/admin/Settings/Users/EditUserModal.svelte`.
- 聊天主逻辑: `src/lib/components/chat/Chat.svelte`.
- 聊天输入与工具/技能选择: `src/lib/components/chat/MessageInput/`.
- 前端工具函数: `src/lib/utils/`.
- 后端配置和路由: `backend/open_webui/config.py`, `backend/open_webui/routers/`.
- 后端模型/MCP/工具权限: `backend/open_webui/utils/models.py`, `backend/open_webui/utils/user_tools.py`, `backend/open_webui/utils/user_resource_inheritance.py`, `backend/open_webui/utils/mcp.py`.

## 入口线索
- 前端入口: SvelteKit routes under `src/routes/`.
- 后端入口: `backend/open_webui/main.py`.
- provider 配置接口: `backend/open_webui/routers/openai.py`, `ollama.py`, `gemini.py`, `grok.py`, `anthropic.py`.
- OpenAI payload 处理: `backend/open_webui/utils/payload.py`.
- Responses/native web search: `backend/open_webui/utils/openai_responses.py`, `backend/open_webui/routers/retrieval.py`.
- Skill import/runtime: `backend/open_webui/routers/skills.py`, `backend/open_webui/utils/skill_importer.py`.

## 常改区域
- 模型继承: `backend/open_webui/utils/models.py`, `backend/open_webui/utils/chat.py`, `backend/open_webui/utils/user_resource_inheritance.py`.
- MCP 继承: `backend/open_webui/utils/user_tools.py`, `backend/open_webui/utils/mcp.py`, users/options route.
- 工具状态过滤: `src/lib/utils/tool-selection.ts`, `src/lib/utils/skill-selection.ts`, `Chat.svelte`.
- 聊天恢复/发送状态: `src/lib/utils/chat-response-state.ts`, `chat-model-recovery.ts`, `chat-history.test.ts`, `Chat.svelte`.
- 接口配置一致性: `src/lib/utils/provider-connections.ts`, provider card components, backend provider config routes.

## 验证线索
- 前端资源继承: `src/lib/utils/resource-inheritance.test.ts`.
- 前端工具/技能状态: `src/lib/utils/tool-selection.test.ts`, `src/lib/utils/skill-selection.test.ts`.
- 前端聊天状态: `chat-response-state`, `chat-event-state`, `chat-model-recovery`, `chat-history` tests.
- 后端资源/MCP: `backend/open_webui/test/unit/test_user_tools_mcp_inherit.py`, `test_resource_inheritance_options.py`, `test_mcp.py`.
- 后端 provider/payload: `test_model_reasoning_priority.py`, `test_payload_tool_call_sanitization.py`, provider config tests.

## 已知坑
- `mcp:<index>` / `server:<index>` 这类下标 ID 容易在删除/重排后串到新资源; 新逻辑优先使用稳定 ID。
- 旧聊天会保存 composer/tool/skill/model 状态; 恢复时要区分用户显式选择和旧空状态。
- provider 配置 UI 要等后端保存成功再保留新状态; 删除和编辑都需要失败回滚。
- web search 有结果但正文抓取为空时, 需要 fallback 到搜索摘要, 否则 sources 会空。

## 待确认
- 是否把 `PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md` 作为本地文件长期保留, 还是之后纳入 Git 提交。
- `TASK_LOG.md` 已作为 legacy 长历史保留; 默认不删除。
