# LOG.md

## 2026-05-26

### 六条线修复收口

- 完成：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示六条线已完成本轮修复和验证。
- 修改：代码基线推进到 `32c4d11 Fix active chat model recovery`, 并推送到 `origin/custom` 与 `origin/future`。
- 验证：上一轮已多次运行目标前端 vitest、后端 pytest、生产构建, 并确认 GitHub Regression Guard / Docker workflow / GHCR manifest。
- 清理：未保留本地服务或端口。
- 后续：除非用户点名、真实复现、上游同步冲突或发布门禁失败, 不再主动围绕六条线继续找 issue。

### 项目接力文件整理

- 完成：新增 `PROJECT_ID.md`, `PROJECT_CONTEXT.md`, `PROJECT_MAP.md`, `TASK.md`, `LOG.md`。
- 修改：`PROJECT_ID.md` 改为指向 `TASK.md` / `LOG.md`; `TASK_LOG.md` 保留为 legacy 历史长记录。
- 验证：只做文档/接力文件整理, 未改业务代码, 未运行构建/测试。
- 清理：未启动服务、未打开浏览器、未占用端口。
- 后续：这些文件目前未提交 Git; 是否纳入仓库由用户单独决定。

### 同步状态复核

- 完成：重新读取全局 `AGENTS.md`, 执行 `git fetch --all --prune`, 修正 `PROJECT_ID.md` 中会和 allowed path 冲突的 `forbidden_paths` 写法。
- 发现：`custom` 与 `origin/custom` 同步; 当前工作分支无未推送代码提交。
- 发现：本地 `future` 分支落后 `origin/future` 12 个提交, 但 `origin/future` 与 `origin/custom` 已在 `32c4d11`。
- 发现：本地 `main=a0ba442` 落后 `origin/main` 3 个提交, 落后 `upstream/main` 4 个提交; `origin/main=8fb18db` 落后 `upstream/main=785a055` 1 个提交。
- 后续：是否同步作者最新 `upstream/main` 到 `main/custom/future`, 需要用户决定。

### 同步作者最新 main 到 custom

- 完成：提交项目接力文件 `45f1584 docs: add project handoff files`; 快进本地 `future` 到 `origin/future`; 将 `origin/main` 推到作者最新 `upstream/main=785a055`。
- 完成：把作者最新提交合入 `custom`, 冲突只在 `backend/open_webui/routers/openai.py` 和 `backend/open_webui/test/unit/test_model_reasoning_priority.py`; 已同时保留 custom 的 `sanitize_incomplete_tool_call_messages` / Ollama 显式参数测试和 upstream 的 `normalize_openai_compatible_reasoning_controls`。
- 验证：后端目标回归 `80 passed`; 上游新增数据管理/TTS + 二创补充回归 `67 passed`; 前端关键工具/继承/聊天状态 vitest `45 passed`; `NODE_OPTIONS=--max-old-space-size=4096 npm run build` 成功。
- 清理：未启动 dev server, 未打开浏览器, 未占用端口。
- 后续：提交并推送 `custom/future`, 等 GitHub Actions 与 GHCR 镜像门禁。

### 最终门禁触发

- 完成：`origin/custom` 与 `origin/future` 已在 `619e11e`; `origin/main` 已在作者最新 `785a055`。
- 发现：GitHub 自动 Actions 仍只显示旧 SHA `32c4d11`; 直接 `workflow_dispatch` 对回归和镜像 workflow 连续返回 HTTP 500。
- 修改：修复 `.github/workflows/custom-regression-guard.yaml` 中一行调度注释; 如果该提交仍未触发 Actions, 再用 backend 单测注释提交命中 `backend/**` 路径。
- 验证：提交后等待 `Custom Regression Guard` 与 `Create and publish Docker images with specific build args`; GHCR 需复查 `custom` / `slim` 双架构 manifest。

### 镜像发布降级处理

- 发现：`f7c0d64` 与 `4516d69` push 事件存在, 但 GitHub Actions 仍未创建 run; 仓库 Actions 权限为 enabled/write, workflow 状态为 active。
- 尝试：本地登录 GHCR, 创建 `halowebui-multi` buildx builder, 注册 `arm64` binfmt, 按 workflow 等价参数构建 `custom` / `future` / `git-4516d69` 双架构镜像。
- 结果：本地双架构构建在 `npm ci` 阶段因 `ETIMEDOUT` 失败, 未推送新镜像。
- 修改：给 `.npmrc` 添加 npm fetch 重试和超时配置, 供后续 GitHub Actions 或本地 buildx 重试使用。
- 结果：`.npmrc` 提交 `c3c7dc9` 成功触发 Docker workflow, 但 `custom` run `26448300909` 和 `future` run `26448300968` 均失败在 Set up job 下载官方 Docker actions 阶段; 本机 curl 对相同 codeload URL 返回 200, 判断为 GitHub Runner 下载侧问题。
- 后续：等 GitHub Runner/codeload 恢复后 rerun failed jobs, 或在网络更稳定环境重跑本地 buildx 双架构推送。

### Docker workflow 去 action 化

- 完成：确认 `26448300909` 与 `26448300968` 红点都死在 Set up job 下载 `docker/setup-buildx-action`, `docker/login-action`, `docker/metadata-action` 的 codeload archive, 不是代码、测试或 Dockerfile 构建失败。
- 修改：将 `.github/workflows/docker-build.yaml` 改为纯 `git` / `docker` CLI 流程, 去掉 Docker 官方 actions、artifact actions 与 `actions/checkout` 的下载依赖。
- 验证：`rg "uses:" .github/workflows/docker-build.yaml` 无匹配; `git diff --check` 通过; YAML 可解析。
- 清理：未启动 dev server, 未打开浏览器, 未占用端口。
- 后续：提交并推送到 `custom` / `future`, 观察新 Docker workflow, 成功后复查 GHCR `custom` / `future` 双架构 manifest。
