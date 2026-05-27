# LOG.md

## 2026-05-27

### User Resource Inheritance Fix

- 完成: 在 `custom` 修复用户资源继承指定模型/MCP 的回归风险; `main` 继续保持作者同步线, 不写入二创修复.
- 完成: 使用 2 个 subagent 做只读复测:
  - 后端审计定位继承 normalize 放大、MCP tool id 校验偏松、模型 alias 语义风险.
  - 前端审计定位指定模式 options 未加载时可能误保存空数组.
- 修改:
  - `backend/open_webui/utils/user_resource_inheritance.py`: 字符串布尔值正确解析; 畸形指定 ids 不再回退为全量继承.
  - `backend/open_webui/utils/tools.py`: `validate_tool_ids_access` 对本地 OpenAPI/MCP tool id 按过滤后的连接表做存在性和启用状态校验.
  - `src/lib/components/admin/Users/UserList/EditUserModal.svelte`: 指定模式保存前确保 options 已加载; 加载中禁用保存; 加载失败阻止保存.
  - `src/lib/i18n/locales/en-US/translation.json` / `zh-CN/translation.json`: 补齐资源继承文案.
  - `AGENTS.md`: 增加“项目无需刻意重复打磨, 没有永远完美的项目”收口规则.
  - `backend/open_webui/test/unit/test_user_resource_inheritance.py` / `test_user_tools_mcp_inherit.py`: 新增 normalize、stale MCP tool id、sanitize 覆盖.
- 验证:
  - `uv run pytest backend/open_webui/test/unit/test_user_resource_inheritance.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_resource_inheritance_options.py backend/open_webui/test/unit/test_models_sharing.py -q`: 35 passed.
  - `npx vitest run src/lib/utils/resource-inheritance.test.ts`: 9 passed.
  - i18n JSON 解析: passed.
  - `git diff --check`: passed, 仅 Git line-ending 提示.
  - `NODE_OPTIONS=--max-old-space-size=4096 npm run build`: passed, 仅既有 Svelte warnings.
  - `npm run check`: failed, 原因是全仓既有 5639 个类型诊断, 非本轮改动引入.
- 后续:
  - 可提交并推送 `custom`, 再同步 `future`.
  - 部署后建议用普通用户实测指定一个模型、指定一个 MCP、旧聊天 stale `mcp:*` 三条路径.

## 2026-05-26

### Upstream Sync: `f48d77a`

- 完成: 拉取作者最新 `upstream/main`, 发现新增 API key 批量添加和多模型讨论功能.
- 完成: 将 `origin/main` 同步到作者最新 `f48d77a`.
- 完成: 将作者更新合入 `custom`, merge commit 为 `eb8f4c5 Merge upstream main into custom`.
- 冲突: `src/lib/components/chat/Chat.svelte`.
- 处理: 保留作者多模型讨论功能, 同时保留 fork 的工具/技能过滤, MCP stable id, 旧聊天发送状态修复, chat completion 事件去重提交逻辑.
- 审计: subagent 指出 `Chat.svelte` 是唯一明确阻断风险; 合并后已按建议补齐验证.
- 验证:
  - 后端 targeted pytest: 37 passed.
  - 后端继承/多模型讨论补充 pytest: 40 passed.
  - 前端 targeted vitest: 33 passed.
  - 前端 chat-event vitest: 2 passed.
  - 生产构建: `NODE_OPTIONS=--max-old-space-size=4096 npm run build` passed.
- GitHub:
  - `custom` Custom Regression Guard: success, run `26470361170`.
  - `future` Custom Regression Guard: success, run `26470363875`.
  - `custom` Docker workflow: success, run `26470361171`.
  - `future` Docker workflow: success, run `26470363938`.
- GHCR:
  - `ghcr.io/zhizhishu/halowebui:custom`: `sha256:557eb5029bcd47e9fdcd2a404343d0baceee124237805b8d8f6fd7d2f997300b`, includes `linux/amd64` and `linux/arm64`.
  - `ghcr.io/zhizhishu/halowebui:future`: `sha256:19742967a9259e24a10057d521b95e0d9d4e2e4eff23d3ae4465ec3326c25ab8`, includes `linux/amd64` and `linux/arm64`.
- 清理: 未启动 dev server, 未打开浏览器, 未占用端口; subagent 已关闭.
- 后续: 当前 `custom/future` 同步任务已收口; `main` 的 Python CI / Frontend Build 红点可作为单独任务处理.

### Docker Workflow Recovery

- 完成: 此前已把 Docker workflow 从官方 Docker actions 降级为纯 `git` / `docker` CLI 流程, 避开 GitHub Runner 下载 actions 失败.
- 完成: `custom` 和 `future` Docker workflow 曾成功通过 build / merge / smoke-test.
- 现状: 本轮最新 `custom/future` Docker workflow 已成功, GHCR 双架构 manifest 已确认.

### Project Handoff

- 完成: 项目接力文件已改为 `PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`.
- 完成: `TASK.md` / `LOG.md` 已重写为干净 UTF-8 中文, 替换原乱码内容.
- 约定: `TASK_LOG.md` 只保留为 legacy 长历史, 默认不再作为当前接力入口.
