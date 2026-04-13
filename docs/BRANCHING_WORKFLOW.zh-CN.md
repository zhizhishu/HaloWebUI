# HaloWebUI 分支协作规范（Fork 维护版）

本文档用于约束本仓库的日常同步、开发与审核流程，目标是让 `main`、`custom`、`future` 职责稳定、可追溯。

## 分支职责

- `main`
  - 仅用于同步上游 `upstream/main`。
  - 不直接承载本仓库二改功能。
- `custom`
  - 稳定分支，线上部署默认使用。
  - 只合并已验证通过的改动。
- `future`
  - 预集成分支，用于功能试验、冲突消化与回归验证。
  - 验证通过后再合并到 `custom`。
- `feature/*`
  - 短生命周期功能分支。
  - 从 `future` 拉出，完成后合回 `future`。

## 同步策略

1. 上游同步：`main` 由工作流自动与 `upstream/main` 对齐。
2. 定期集成：将 `main` 合并到 `future`，处理冲突并完成回归。
3. 发布节奏：`future` 稳定后，再合并到 `custom`。
4. 热修复：若直接在 `custom` 修复，需 `cherry-pick` 回 `future`。

## 镜像策略

- `main` 推送：构建主线镜像（含 `latest` 逻辑）。
- `custom` 推送：构建 `:custom` 分支镜像。
- `future` 推送：构建 `:future` 分支镜像，便于预发验证。

## 镜像溯源守则（强制）

每次“拉取作者镜像并开始二改”前，必须先记录以下溯源信息到任务日志（`TASK_LOG.md`）：

1. 作者镜像 `RepoDigest`（唯一镜像身份）
2. 作者镜像 `Created` 时间（镜像构建时间）
3. 上游 `upstream/main` 提交哈希与提交时间（源码时间锚点）

推荐命令：

```bash
# 1) 拉取作者镜像（示例）
docker pull ghcr.io/ztx888/halowebui:main

# 2) 记录镜像身份与时间
IMAGE_REF="ghcr.io/ztx888/halowebui:main"
IMAGE_DIGEST=$(docker image inspect "$IMAGE_REF" --format '{{index .RepoDigests 0}}')
IMAGE_CREATED_AT=$(docker image inspect "$IMAGE_REF" --format '{{.Created}}')

# 3) 记录上游源码锚点
git fetch upstream main
UPSTREAM_SHA=$(git rev-parse upstream/main)
UPSTREAM_COMMIT_TIME=$(git show -s --format='%ci' "$UPSTREAM_SHA")

echo "IMAGE_DIGEST=$IMAGE_DIGEST"
echo "IMAGE_CREATED_AT=$IMAGE_CREATED_AT"
echo "UPSTREAM_SHA=$UPSTREAM_SHA"
echo "UPSTREAM_COMMIT_TIME=$UPSTREAM_COMMIT_TIME"
```

任务日志模板（可直接复制）：

```text
- [ ] **目标:** <本次二改目标> (创建于: YYYY-MM-DD HH:MM:SS)
  - 镜像基线: <IMAGE_DIGEST>
  - 镜像时间: <IMAGE_CREATED_AT>
  - 上游基线: <UPSTREAM_SHA>
  - 上游时间: <UPSTREAM_COMMIT_TIME>
```

说明：
- 若镜像时间晚于上次记录，必须先做差异评估再改 `future/custom`。
- 发布问题回溯时，以 `IMAGE_DIGEST + UPSTREAM_SHA` 作为唯一溯源键。

## 作者更新清单守则（每轮强制）

每一轮同步前，必须先生成“作者更新清单”并写入 `TASK_LOG.md`，避免在未知变更上直接二改。

强制命令：

```bash
# 1) 同步远端
git fetch upstream main

# 2) 以上一轮记录的上游基线为起点，生成新增提交清单
# 例：LAST_UPSTREAM_SHA=89911af
LAST_UPSTREAM_SHA=<上次记录的上游基线SHA>
git log --oneline --reverse ${LAST_UPSTREAM_SHA}..upstream/main

# 3) 记录最新上游锚点
UPSTREAM_SHA=$(git rev-parse upstream/main)
UPSTREAM_COMMIT_TIME=$(git show -s --format='%ci' "$UPSTREAM_SHA")
echo "UPSTREAM_SHA=$UPSTREAM_SHA"
echo "UPSTREAM_COMMIT_TIME=$UPSTREAM_COMMIT_TIME"
```

任务日志模板（可直接复制）：

```text
- [ ] **目标:** <本轮同步与二改目标> (创建于: YYYY-MM-DD HH:MM:SS)
  - 上轮上游基线: <LAST_UPSTREAM_SHA>
  - 本轮上游基线: <UPSTREAM_SHA>
  - 本轮上游时间: <UPSTREAM_COMMIT_TIME>
  - 作者更新清单:
    - <commit1> <summary>
    - <commit2> <summary>
```

规则：
- 未记录作者更新清单，不允许进入 `main -> future` 合并步骤。
- 合并后必须再做一次“二改保留清单（强制）”回归验证。

## 开发与审核建议

1. 所有功能改动优先进入 `future`，避免直接污染 `custom`。
2. PR 建议方向：
   - 功能 PR：`feature/* -> future`
   - 发布 PR：`future -> custom`
   - 同步 PR：`main -> future`
3. 合并前至少执行：
   - 相关单元测试
   - 关键路径手工验证（MCP 配置、工具调用、模型对话）
4. 审核重点：
   - 是否引入与上游冲突的改动
   - 是否破坏 `main` 的纯同步定位
   - 是否在 `custom` 引入未经验证的实验功能

## 二改保留清单（强制）

以下能力为本仓库二改核心能力，**每次同步 `main -> future` 后必须验证，不得回归**：

1. 普通用户继承管理员 MCP 配置能力（含开关控制）。
2. MCP 工具选择状态持久化能力（避免会话中被自动重置）。

强制回归命令：

```bash
uv run pytest \
  backend/open_webui/test/unit/test_user_tools_mcp_inherit.py \
  backend/open_webui/test/unit/test_mcp.py
```

若回归失败：
- 不允许直接合并 `future -> custom`。
- 需先修复并补充测试，再进入发布流程。

## 本地常用命令

```bash
# 更新 main（若未依赖自动同步）
git checkout main
git fetch upstream
git merge --ff-only upstream/main || git merge --no-edit upstream/main
git push origin main

# main 合到 future
git checkout future
git merge main

# future 合到 custom
git checkout custom
git merge future

# 从 future 开功能分支
git checkout future
git checkout -b feature/xxx
```
