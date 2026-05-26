# TASK.md

## Handoff Summary

当前目标：作者最新 `upstream/main=785a055` 已合入 `custom`; 正在提交并推送 `custom/future`。
已完成：
- 六条线代码工作已收口：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 当前代码基线：`custom` / `origin/custom` / `origin/future` = `32c4d11 Fix active chat model recovery`。
- 已补项目文件：`PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`。
- `TASK_LOG.md` 保留为旧历史长记录，不再作为默认当前接力入口。
下一步：
- 提交合并结果。
- 推送 `origin/custom` 与 `origin/future`。
- 检查 GitHub Actions 与 GHCR 镜像。
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
风险/待确认：
- 服务器是否已拉取 `32c4d11` 镜像并重建容器，需要用户部署环境确认。
- 是否提交这些项目接力文件到 Git，需要用户单独拍板。
- 是否执行新一轮上游同步：`origin/main` 未追上 `upstream/main`, `custom/future` 未合入最新作者提交。
资源清理：
- 本轮未启动服务、未打开浏览器、未占用端口。
最后更新：2026-05-26 04:16:00 -07:00

## Active Tasks

- [x] **Goal:** 补齐 `TASK.md` / `LOG.md`, 并把项目文件入口从旧 `TASK_LOG.md` 切到新接力结构。
- [ ] **Goal:** 同步作者最新 `upstream/main` 到 `main/custom/future`, 保留二创并完成验证发布。

## Notes For Next Agent

- 回复用户时按全局规则称呼“宝宝”。
- `C:\Users\echo\Downloads\claude` 是父级存放目录，不是项目根。
- 当前真实项目根目录是 `C:\Users\echo\Downloads\claude\github\HaloWebUI`。
- 不要把六条线当成继续开放的待办；当前已完成。
- 不要主动广泛浏览上游 issue；需要时先用本地复现和测试证明问题。
- `AGENTS.md`, `PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`, `TASK_LOG.md` 当前都是本地项目接力文件，未提交 Git。
