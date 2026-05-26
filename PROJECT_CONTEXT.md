# PROJECT_CONTEXT.md

## 项目用途
- HaloWebUI 是 `zhizhishu/HaloWebUI` fork, 基于 `ztx888/HaloWebUI` / Open WebUI 继续维护。
- `main` 保持纯上游镜像; `custom` / `future` 承载本仓库二创和 GHCR 镜像发布。
- 当前重点能力已经收口: 接口配置, 模型继承, MCP 继承, 工具技能状态, 新旧聊天发送状态, 原生联网提示。

## 技术栈
- 前端: SvelteKit, Vite, TypeScript, Tailwind, Vitest.
- 后端: FastAPI, Python, SQLAlchemy/Peewee, pytest.
- 容器: Dockerfile, docker-compose, GHCR images.
- 发布分支: `custom` 与 `future` 都推送到 `origin`; `main` 对齐 `upstream/main`。

## 重要目录
- `src/`: 前端页面, 组件, stores, utils, i18n.
- `backend/open_webui/`: 后端 API, 配置, 路由, 工具链, 测试。
- `.github/workflows/`: 自定义回归与镜像构建流程。
- `scripts/`: 构建, 同步, 报告辅助脚本。
- `docs/`, `README.md`, `TROUBLESHOOTING.md`: 用户文档和项目说明。

## 启动与验证
- 前端开发: `npm run dev`.
- 前端测试: `npx vitest run <targets>`.
- 前端构建: `NODE_OPTIONS=--max-old-space-size=4096 npm run build`.
- 后端测试: `uv run pytest <targets> -q`.
- 常规发布门禁: 本地目标测试通过, GitHub custom/future Regression Guard 成功, Docker workflow 成功, GHCR `custom` / `slim` manifest 可读。

## 长期约定
- 不在 `main` 上放 fork-only 改动。
- 修复真实 bug 才提交并推送; 没有真实修复不做空提交。
- 不主动乱扫 GitHub issue; 已完成的六条线默认不再继续找事。
- 上游同步时先对齐 `main`, 再合入 `custom`, 最后同步 `future`。
- `AGENTS.md` 和 `TASK_LOG.md` 当前作为本地规则/接力文件保留, 默认不提交。

## 已知坑点
- PowerShell 默认编码可能把中文文件显示成乱码; 文件本身通常仍是 UTF-8。
- 全量 `npm run check` 可能被历史 Svelte/TS/A11y 诊断阻断; 需要区分本次改动新增问题和既有问题。
- Node 构建容易吃内存; 生产构建使用 `NODE_OPTIONS=--max-old-space-size=4096 npm run build`。
- 当前项目已补 `TASK.md` / `LOG.md`; `TASK_LOG.md` 保留为 legacy 长历史。

## 待确认
- 服务器是否已经拉取当前 `32c4d11` 镜像并重建容器, 由用户实际部署环境决定。
- 如果未来要把项目接力文件提交进仓库, 需要先由用户确认提交策略。
