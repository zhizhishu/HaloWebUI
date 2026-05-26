# TASK.md

## Handoff Summary

当前目标：作者最新 `upstream/main=785a055` 已合入 `custom`; `custom/future` 已推到 `origin`; 代码同步完成, 正在修复 GitHub Docker 镜像发布 workflow 的 runner 下载失败红点。
已完成：
- 六条线代码工作已收口：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 当前代码基线：`custom` / `origin/custom` / `origin/future` = `f506f2b docs: record image publish blocker`。
- 已补项目文件：`PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`。
- `TASK_LOG.md` 保留为旧历史长记录，不再作为默认当前接力入口。
- 手动 `workflow_dispatch` 对 GitHub API 连续返回 HTTP 500; workflow 注释提交和 backend 单测注释提交也未触发 Actions。
- 本地 buildx 双架构构建失败在 `npm ci` 的 `ETIMEDOUT`; 已给 `.npmrc` 添加 fetch 重试/超时配置并推送。
- Docker workflow 已恢复触发, 但失败在 GitHub Runner 下载官方 Docker actions 的 Set up job 阶段, 不是代码构建阶段。
- 已将 `.github/workflows/docker-build.yaml` 改为纯 `git` / `docker` CLI 流程, 移除 `docker/setup-buildx-action`, `docker/login-action`, `docker/metadata-action`, `docker/build-push-action`, artifact actions 与 `actions/checkout` 的下载面。
- 首次去 action 化 run 已越过 Set up job, 但手写 checkout 的 `bearer` git 认证失败; 已改为 `basic x-access-token` extraheader。
下一步：
- 提交并推送 workflow 修复到 `custom` 与 `future`, 观察新 Docker workflow。
- 成功后复查 GHCR `custom` / `future` manifest 是否含 `linux/amd64` 与 `linux/arm64`。
- 不再主动泛扫 issue；只在用户点名、真实复现、上游同步冲突、Actions/GHCR 失败时处理。
关键文件：
- `PROJECT_ID.md`
- `PROJECT_CONTEXT.md`
- `PROJECT_MAP.md`
- `TASK.md`
- `LOG.md`
- `TASK_LOG.md`
- `.github/workflows/docker-build.yaml`
验证状态：
- 项目接力文件已提交为 `45f1584 docs: add project handoff files`。
- `origin/main` 已同步到 `upstream/main=785a055`。
- `custom` 已合并作者更新, 解决 `openai.py` 与 `test_model_reasoning_priority.py` 两处 import 冲突。
- 后端目标测试 `80 passed`; 上游新增/二创补充测试 `67 passed`; 前端关键 vitest `45 passed`; 生产构建成功。
- `gh run list` 显示最近一次自动 Actions 仍停在旧 SHA `32c4d11`; `619e11e` / `f7c0d64` / `4516d69` 没有 Actions check-runs。
- 本地 buildx 已登录 GHCR, 已创建 `halowebui-multi` builder 并注册 `arm64` binfmt; 首次双架构推送尝试因 npm 网络超时失败, 未推送新镜像。
- Docker workflow run `26448300909` / `26448300968` 已触发但失败在下载 `docker/setup-buildx-action` / `docker/login-action` / `docker/metadata-action` 的 action archive。
- 本地 `rg "uses:" .github/workflows/docker-build.yaml` 无匹配; `git diff --check` 通过; YAML 可解析。
- 去 action 化 run `26449592497` / `26449592535` 进入自定义 shell 步骤后失败在 `git fetch`, 原因为 GitHub git 不接受当前 `bearer` header; 已改为 `basic x-access-token`。
风险/待确认：
- GHCR `custom` 当前仍是旧成功镜像 digest; 服务器现在拉取不会得到本轮 workflow 修复后的新镜像。
- 新 workflow 会留下 `build-<branch>-<sha>-main/slim-<platform>` 临时平台标签, 用来替代 artifact/digest 传递并规避 action 下载失败。
资源清理：
- 本轮未启动 dev server、未打开浏览器、未占用端口; 临时 buildx builder 待清理。
最后更新：2026-05-26 06:05:04 -07:00

## Active Tasks

- [x] **Goal:** 补齐 `TASK.md` / `LOG.md`, 并把项目文件入口从旧 `TASK_LOG.md` 切到新接力结构。
- [ ] **Goal:** 修复 Docker 镜像发布 workflow 红点, 推送后确认 GHCR `custom` / `future` 新 manifest。

## Notes For Next Agent

- 回复用户时按全局规则称呼“宝宝”。
- `C:\Users\echo\Downloads\claude` 是父级存放目录，不是项目根。
- 当前真实项目根目录是 `C:\Users\echo\Downloads\claude\github\HaloWebUI`。
- 不要把六条线当成继续开放的待办；当前已完成。
- 不要主动广泛浏览上游 issue；需要时先用本地复现和测试证明问题。
- 项目接力文件已纳入 Git; 当前只等待最终 Actions/GHCR 门禁。
