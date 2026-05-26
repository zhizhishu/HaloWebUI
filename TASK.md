# TASK.md

## Handoff Summary

当前目标：提交项目接力文件, 同步本地 `future`, 将作者最新 `upstream/main` 合入 `main/custom/future`, 并保留本仓库二创。
已完成：
- 六条线代码工作已收口：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 当前代码基线：`custom` / `origin/custom` / `origin/future` = `32c4d11 Fix active chat model recovery`。
- 已补项目文件：`PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`。
- `TASK_LOG.md` 保留为旧历史长记录，不再作为默认当前接力入口。
下一步：
- 提交项目接力文件。
- 快进本地 `future` 到 `origin/future`。
- 同步 `main` 到作者最新 `upstream/main=785a055`。
- 合并作者更新到 `custom`, 再同步到 `future`。
- 跑目标测试/构建, 推送 `origin/main`, `origin/custom`, `origin/future`。
- 不再主动泛扫 issue；只在用户点名、真实复现、上游同步冲突、Actions/GHCR 失败时处理。
关键文件：
- `PROJECT_ID.md`
- `PROJECT_CONTEXT.md`
- `PROJECT_MAP.md`
- `TASK.md`
- `LOG.md`
- `TASK_LOG.md`
验证状态：
- 本轮正在执行上游同步; 项目文件整理已完成。
- 上一轮代码基线 `32c4d11` 已推送到 `origin/custom` 和 `origin/future`。
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
