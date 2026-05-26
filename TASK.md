# TASK.md

## Handoff Summary

当前目标：作者最新 `upstream/main=785a055` 已合入 `custom`; `custom/future` 已推到 `origin`; 正在通过 push 触发最终 GitHub Actions 与 GHCR 镜像门禁。
已完成：
- 六条线代码工作已收口：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 当前代码基线：`custom` / `origin/custom` / `origin/future` = `619e11e docs: record upstream sync`。
- 已补项目文件：`PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`。
- `TASK_LOG.md` 保留为旧历史长记录，不再作为默认当前接力入口。
- 手动 `workflow_dispatch` 对 GitHub API 连续返回 HTTP 500; 改用 workflow 注释修复提交触发 `push` workflows。
下一步：
- 提交并推送 workflow 注释修复提交到 `origin/custom` 与 `origin/future`。
- 等待 `Custom Regression Guard` 与 `Create and publish Docker images with specific build args` 成功。
- 复查 GHCR `custom` / `slim` manifest 是否仍含 `linux/amd64` 与 `linux/arm64`。
- 不再主动泛扫 issue；只在用户点名、真实复现、上游同步冲突、Actions/GHCR 失败时处理。
关键文件：
- `PROJECT_ID.md`
- `PROJECT_CONTEXT.md`
- `PROJECT_MAP.md`
- `TASK.md`
- `LOG.md`
- `TASK_LOG.md`
验证状态：
- 项目接力文件已提交为 `45f1584 docs: add project handoff files`。
- `origin/main` 已同步到 `upstream/main=785a055`。
- `custom` 已合并作者更新, 解决 `openai.py` 与 `test_model_reasoning_priority.py` 两处 import 冲突。
- 后端目标测试 `80 passed`; 上游新增/二创补充测试 `67 passed`; 前端关键 vitest `45 passed`; 生产构建成功。
- `gh run list` 显示最近一次自动 Actions 仍停在旧 SHA `32c4d11`; `619e11e` 没有 check-runs, 所以本轮补一个非文档 workflow 注释提交来触发门禁。
风险/待确认：
- 等 GitHub Actions 与 GHCR 镜像门禁完成后，服务器再拉取新镜像并重建容器。
资源清理：
- 本轮未启动服务、未打开浏览器、未占用端口。
最后更新：2026-05-26 04:58:00 -07:00

## Active Tasks

- [x] **Goal:** 补齐 `TASK.md` / `LOG.md`, 并把项目文件入口从旧 `TASK_LOG.md` 切到新接力结构。
- [ ] **Goal:** 同步作者最新 `upstream/main` 到 `main/custom/future`, 保留二创并完成验证发布。

## Notes For Next Agent

- 回复用户时按全局规则称呼“宝宝”。
- `C:\Users\echo\Downloads\claude` 是父级存放目录，不是项目根。
- 当前真实项目根目录是 `C:\Users\echo\Downloads\claude\github\HaloWebUI`。
- 不要把六条线当成继续开放的待办；当前已完成。
- 不要主动广泛浏览上游 issue；需要时先用本地复现和测试证明问题。
- 项目接力文件已纳入 Git; 当前只等待最终 Actions/GHCR 门禁。
