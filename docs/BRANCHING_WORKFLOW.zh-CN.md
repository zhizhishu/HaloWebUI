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

