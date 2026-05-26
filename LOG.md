# LOG.md

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
- 清理: 未启动 dev server, 未打开浏览器, 未占用端口; subagent 已关闭.
- 后续: 推送 `custom/future`, 等 GitHub Actions 与 GHCR 镜像门禁.

### Docker Workflow Recovery

- 完成: 此前已把 Docker workflow 从官方 Docker actions 降级为纯 `git` / `docker` CLI 流程, 避开 GitHub Runner 下载 actions 失败.
- 完成: `custom` 和 `future` Docker workflow 曾成功通过 build / merge / smoke-test.
- 现状: 本轮推送后仍需重新检查最新 GitHub Actions 和 GHCR manifest.

### Project Handoff

- 完成: 项目接力文件已改为 `PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`.
- 完成: `TASK.md` / `LOG.md` 已重写为干净 UTF-8 中文, 替换原乱码内容.
- 约定: `TASK_LOG.md` 只保留为 legacy 长历史, 默认不再作为当前接力入口.
