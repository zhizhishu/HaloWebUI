<div align="center">
  <img src="./static/favicon.png" alt="HaloWebUI" width="120" height="120" />
  <h1>HaloWebUI</h1>
  <p><strong>自托管 AI 平台 / 多模型路由 / 管理员资源继承 / MCP 集成</strong></p>
  <p>
    基于 Open WebUI 深度定制，聚焦多供应商接口管理、普通用户资源继承、MCP 工具接入和私有化部署体验。
  </p>

  <a href="https://github.com/zhizhishu/HaloWebUI/stargazers">
    <img src="https://img.shields.io/github/stars/zhizhishu/HaloWebUI?style=for-the-badge&logo=github&color=f4c542" alt="Stars" />
  </a>
  <a href="https://github.com/zhizhishu/HaloWebUI/network/members">
    <img src="https://img.shields.io/github/forks/zhizhishu/HaloWebUI?style=for-the-badge&logo=github&color=8ac926" alt="Forks" />
  </a>
  <a href="https://github.com/zhizhishu/HaloWebUI/commits/custom">
    <img src="https://img.shields.io/github/last-commit/zhizhishu/HaloWebUI/custom?style=for-the-badge&logo=git&color=ff595e" alt="Last Commit" />
  </a>
  <a href="https://github.com/zhizhishu/HaloWebUI/blob/custom/LICENSE">
    <img src="https://img.shields.io/github/license/zhizhishu/HaloWebUI?style=for-the-badge&color=6a4c93" alt="License" />
  </a>

  <br/><br/>

  <img src="https://img.shields.io/badge/Svelte_4-FF3E00?style=flat-square&logo=svelte&logoColor=white" alt="Svelte 4" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
</div>

## 项目定位

HaloWebUI 是基于 [Open WebUI](https://github.com/open-webui/open-webui) 的二次定制分支。本仓库的 `main` 用于跟随上游，`custom` 用于承载本仓库自己的产品化改动和镜像发布。

当前 `custom` 分支重点解决这些场景：

- 管理员统一维护模型、供应商接口和 MCP 服务器。
- 普通用户按管理员授权继承可用模型和 MCP。
- 管理员可在用户管理中精细控制某个用户继承全部资源，或只继承指定资源。
- 前端显示本仓库 custom 版本号，公开仓库链接指向 `zhizhishu/HaloWebUI`。
- Docker 镜像发布到 `ghcr.io/zhizhishu/halowebui:custom`。

## Custom 分支更新

### Fork 品牌与版本

- 设置页显示 `V<upstream version> · custom-<commit>`，方便确认服务器当前运行的镜像是否已经包含最新提交。
- 前端仓库、反馈、更新提示、文档链接和镜像地址已指向 `zhizhishu/HaloWebUI` 与 `ghcr.io/zhizhishu/halowebui`。
- `custom` 分支保留 fork-only 能力，避免污染用于同步上游的 `main`。

### 管理员资源继承

管理员可以在用户管理编辑弹窗中为普通用户配置资源继承权限：

- `继承管理员模型`: 允许该用户使用管理员配置的模型。
- `继承管理员 MCP`: 允许该用户使用管理员配置的 MCP 服务器。
- `全部`: 自动包含当前和未来的管理员资源。
- `指定`: 只允许继承管理员选中的模型或 MCP 服务器。
- `指定` 且列表为空时，表示明确不继承任何管理员资源，不会回退成全部继承。

这套逻辑同时覆盖前端交互、保存 payload、后端模型权限判断和 MCP 工具权限判断。

### 接口配置修复

- 修复接口设置页看不到已保存 API 配置的问题。
- OpenAI、Gemini、Grok、Anthropic、Ollama 的配置读取路径统一读取管理员用户级 `ui.connections`。
- 保存配置时同步写回用户级连接配置，并兼容旧全局配置字段。
- 运行时能调用的 API 与设置页显示的 API 保持一致，减少“页面看不见但还能调用”的错觉。

### MCP 继承策略

- 用户自己的 MCP 配置优先。
- 当用户 MCP 配置为空时，可以继续继承管理员 MCP。
- 继承管理员 MCP 不再要求普通用户拥有自建直连 MCP 权限。
- 管理员可以按用户选择继承全部 MCP，或只继承指定 MCP 服务器。
- 继承候选项与运行时统一使用稳定资源 ID，兼容旧全局 MCP 配置。

### 旧聊天工具状态自修复

- 旧聊天页可能保存已经删除的 MCP/OpenAPI/工作区工具 ID，导致工具列表不同步、旧页面无法删除工具、继续对话时报错。
- `custom` 分支会在旧会话恢复、输入缓存恢复、URL 工具参数、模型默认工具、composer 持久化和实际发送请求时，按当前可用工具列表过滤失效 `tool_ids`。
- 后端在 chat middleware 和 function pipe 中加入请求级 sanitizer，会丢弃已删除、越界、禁用或当前用户不可读的工具 ID，避免旧页面状态把整次对话卡死。
- 配置/管理路径仍保留严格工具权限校验，避免为了兼容旧聊天而放松管理员配置安全边界。

### 已验证范围

最近一次 custom 分支回归覆盖了这些链路：

```bash
uv run pytest backend/open_webui/test/unit/test_resource_access_control.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_mcp.py -q
# MCP/工具权限与继承回归通过

npx vitest run src/lib/utils/tool-selection.test.ts src/lib/utils/resource-inheritance.test.ts src/lib/utils/model-capabilities.test.ts
# 旧聊天工具过滤、资源继承和模型能力回归通过

NODE_OPTIONS=--max-old-space-size=4096 npm run build
# production build passed
```

远端 `custom` 分支的 `Custom Regression Guard` 与 Docker 镜像构建也已通过。以上验证说明“可点击、可保存、模型可用、MCP 可用、指定为空不越权继承、旧聊天删除工具后仍可继续对话”这条核心链路未发现回归；服务器仍建议拉取最新镜像后在真实账号界面做一次人工确认。

## 核心功能

HaloWebUI 不是单纯的聊天前端，而是一套面向个人、团队和私有化场景的 AI 工作台。它把模型接入、资源授权、知识增强、MCP 工具和部署运维放在同一个控制面里，让管理员可以集中治理，让用户可以直接使用。

### 统一 AI 工作台

- 多会话、多模型、多模态入口集中在同一个 Web UI 中，适合日常问答、代码辅助、文件分析、知识库检索和团队协作。
- 支持 Web/PWA 访问，前端基于 Svelte、TypeScript 和 Tailwind CSS，界面响应快，适合桌面和移动端使用。
- 保留 Open WebUI 的成熟体验，同时在 `custom` 分支加入更适合自部署用户的资源管理和权限能力。

### 多模型与供应商网关

- 支持 OpenAI 兼容接口、Anthropic Claude、Google Gemini、xAI Grok、Ollama 等多类模型来源。
- 管理员可以统一维护 API Key、Base URL、模型列表和连接配置，减少每个用户重复填写接口的成本。
- 修复并统一接口配置读写路径，让设置页显示、运行时调用和已保存配置保持一致。
- 适合把多个商业模型、本地模型和代理接口聚合到一个入口中统一使用。

### 管理员资源继承

- 普通用户可以按管理员授权继承管理员模型，不需要自己配置同一套 API。
- 普通用户可以按管理员授权继承管理员 MCP 服务器，把工具能力按需下发给指定用户。
- 模型和 MCP 分别支持 `全部` 与 `指定` 两种继承范围，管理员能控制当前和未来资源是否自动开放。
- `指定` 且列表为空会被视为明确禁止继承，避免权限边界被误放大。

### MCP 工具生态

- 支持服务端 stdio MCP，适合接入私有工具、自动化脚本、内部系统和外部能力服务。
- 用户自己的 MCP 配置优先，空配置时可按权限继承管理员 MCP。
- 继承管理员 MCP 不要求普通用户拥有自建直连 MCP 权限，更符合团队集中治理场景。
- 旧聊天里残留的已删除 MCP/工具 ID 会被前后端过滤，避免删除工具后旧页面继续带失效工具发请求。
- 主镜像包含常用 stdio MCP 运行时组合，便于直接体验 `uvx`、`npx`、Git 源 MCP 等常见接入方式。

### 知识库与文件增强

- 继承 Open WebUI 的知识库、文件上传、RAG 检索和聊天上下文能力。
- 可把文档、资料和知识集合接入对话，让模型回答更贴近自己的数据。
- 适合构建个人资料库、团队知识库、客服问答、项目文档助手和代码资料助手。

### 用户、权限与团队治理

- 管理员可以在用户管理中配置每个用户的资源继承能力，不再把权限开关散落在连接设置里。
- 模型继承和 MCP 继承相互独立，适合给不同用户开放不同级别的 AI 和工具权限。
- 前端保存、后端鉴权和运行时调用都有回归测试覆盖，降低权限配置漂移的风险。

### 私有化部署与运维

- 支持 Docker、Docker Compose、PostgreSQL、Redis、反向代理和静态资源缓存优化。
- 提供 `custom` 与 `slim` 镜像，既能开箱体验完整能力，也能选择更轻量的部署形态。
- 设置页展示 `custom-<commit>` 版本，便于确认当前运行镜像是否包含最新修复。
- README 内保留服务器拉取镜像、重建容器、检查端口和查看日志的常用命令。

### 分支与发布策略

- `main` 保持跟随上游 Open WebUI，便于持续吸收社区更新。
- `custom` 承载本仓库的二改能力、产品化调整和 GHCR 镜像发布。
- 关键能力配套后端单测、前端纯逻辑测试、生产构建和 GitHub Actions 回归，避免改完只停留在“看起来能用”。

| 能力方向 | 解决的问题 | 当前状态 |
|----------|------------|----------|
| 多模型接入 | 多供应商、多代理、本地模型分散难管理 | 已接入并持续同步上游能力 |
| 用户资源继承 | 普通用户重复配置 API 和 MCP 成本高 | custom 分支已实现 |
| 精细授权 | 全部开放太粗，逐个配置太乱 | 支持全部/指定两种范围 |
| MCP 集成 | 工具调用需要服务端可控运行环境 | 支持 stdio MCP 与继承策略 |
| 旧聊天工具同步 | 删除 MCP/工具后旧页面仍带失效 ID 导致对话失败 | 前后端过滤失效 `tool_ids` |
| 配置一致性 | 页面看不到但运行时还能调用 | 已修复 provider 配置读写路径 |
| 私有化部署 | 自建服务需要稳定更新和排障入口 | 提供镜像、Compose 和检查命令 |

## 快速开始

> 必须挂载 `/app/backend/data`，否则数据库、上传文件和运行时数据不会持久化。

### Docker 运行

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name halowebui \
  --restart always \
  ghcr.io/zhizhishu/halowebui:custom
```

启动完成后访问 `http://localhost:3000`，首次注册的用户自动成为管理员。

### Docker Compose

```bash
git clone -b custom https://github.com/zhizhishu/HaloWebUI.git
cd HaloWebUI
docker compose up -d
```

默认使用：

- 镜像: `ghcr.io/zhizhishu/halowebui:custom`
- 端口: `${OPEN_WEBUI_PORT-3000}:8080`
- 数据卷: `open-webui:/app/backend/data`
- 容器名: `open-webui`

### 服务器更新镜像

如果服务器已经部署过本仓库镜像，可以在项目目录执行：

```bash
cd /root/HaloWebUI
docker pull ghcr.io/zhizhishu/halowebui:custom
docker compose up -d --force-recreate
```

如果你的服务器使用了单独的镜像 compose 文件，请按服务器实际文件名执行，例如：

```bash
docker compose -f docker-compose.image.yaml up -d --force-recreate
```

更新后建议检查：

```bash
docker ps
docker logs halowebui --tail 80
curl -I http://127.0.0.1:5060
```

端口号以你的部署配置为准。

## MCP stdio 说明

- stdio MCP 命令运行在 HaloWebUI 服务端容器内，不是在浏览器或你的本机 shell 中执行。
- `custom` 默认主镜像包含 stdio MCP 常用运行时组合，例如 `uv/uvx`、`node/npx` 与 `git`。
- `slim` 镜像更小，不适合作为 stdio MCP 开箱体验镜像，需要自行补充运行时。
- 某些自定义 MCP 会通过 Git 源安装，例如 `uvx --from git+https://...`，这类配置除了 `uv/uvx` 之外还依赖 `git`。
- MCP 配置保存后建议手动验证连接，确认服务端容器内的命令、环境变量和网络都可用。
- 不建议把 `fnm_multishells/...` 这类临时 shell 路径写成长期 MCP command，请使用容器主进程可见的稳定命令路径。
- stdio MCP 的资源占用取决于实际启动的 MCP 子进程，不是只保存配置就一定长期占用大量内存。

### 轻量版 slim

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name halowebui-slim \
  --restart always \
  ghcr.io/zhizhishu/halowebui:slim
```

```bash
docker compose -f docker-compose.yaml -f docker-compose.slim.yaml up -d
```

`slim` 适合更在意镜像体积、不需要 stdio MCP 开箱体验、愿意自行补充运行时的部署场景。

## 常用环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPEN_WEBUI_PORT` | Docker Compose 暴露端口 | `3000` |
| `WEBUI_DOCKER_TAG` | 镜像标签 | `custom` |
| `WEBUI_SECRET_KEY` | JWT 签名密钥，生产环境必须设置 | 随机生成 |
| `OPENAI_API_KEY` | OpenAI 兼容 API 密钥 | 空 |
| `OPENAI_API_BASE_URL` | OpenAI 兼容 API 地址 | `https://api.openai.com/v1` |
| `ANTHROPIC_API_KEY` | Anthropic Claude API 密钥 | 空 |
| `GEMINI_API_KEY` | Google Gemini API 密钥 | 空 |
| `OLLAMA_BASE_URL` | Ollama 服务地址 | `http://host.docker.internal:11434` |
| `DATABASE_URL` | PostgreSQL 数据库连接串 | SQLite 本地文件 |
| `REDIS_URL` | Redis 缓存地址 | 空 |
| `REQUESTS_VERIFY` | 后端 `requests` 是否校验证书 | `true` |
| `AIOHTTP_CLIENT_SESSION_SSL` | 后端 `aiohttp` 是否校验证书 | `true` |

使用自签证书时，优先把 CA 证书导入容器信任链；只有临时排障时才建议把证书校验开关设为 `false`。

## 反向代理与缓存

如果服务器带宽较低，首屏加载可能变慢。可以把浏览器访问入口放到 Nginx 或 CDN 后面，让前端静态资源就近缓存，接口和实时聊天仍转发到后端服务。

- `/api`、`/ws`、`/openai`、`/ollama`、`/gemini`、`/anthropic`、`/grok` 等路径继续反向代理到后端。
- `/_app/immutable/` 是带版本指纹的前端构建文件，可以设置较长缓存。
- `/assets/`、`/wasm/`、`/static/` 可以设置较短缓存。
- `/cache/`、上传文件和接口响应不建议套用长缓存。
- 如果前后端放到不同域名，需要单独处理跨域、登录态、WebSocket、上传下载等链路。

Nginx 示例：

```nginx
location /_app/immutable/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    expires 1y;
    add_header Cache-Control "public, max-age=31536000, immutable" always;
}

location /ws {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}

location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 技术架构

```text
Browser / PWA
  Svelte 4 / TypeScript / Tailwind CSS
        |
FastAPI backend
  Auth / Models / Providers / MCP / RAG / Files / Realtime
        |
Provider layer
  OpenAI-compatible / Anthropic / Gemini / Grok / Ollama
        |
Storage
  SQLite or PostgreSQL / Redis / Vector database / Local files
```

## 后续创新方向

这些方向适合继续和当前 custom 能力结合：

- 资源继承审计: 给管理员展示用户继承了哪些模型和 MCP，以及继承来源。
- 策略模板: 为不同用户组提供“全继承”“只继承模型”“只继承指定 MCP”等模板。
- MCP 健康检查: 展示 MCP 服务器连接状态、可用工具、最近错误和验证时间。
- 工具权限可视化: 在用户编辑弹窗中直观看到 MCP 工具级权限和继承结果。
- Provider 诊断: 对 API Key、Base URL、模型列表、网络错误做一键诊断。
- 发布回滚: 为 custom 镜像记录版本、提交、构建状态和回滚命令。
- 首屏体验优化: 对静态资源缓存、懒加载和移动端管理界面继续打磨。

## 贡献与同步

- 上游同步优先进入 `main`。
- 本仓库二改和产品创新进入 `custom`。
- 重要功能需要补充后端单测、前端纯逻辑测试或可执行回归。
- 提交前建议运行目标测试和 `git diff --check`。

## 致谢

HaloWebUI 基于 [Open WebUI](https://github.com/open-webui/open-webui) 深度定制开发。感谢 Open WebUI 社区的长期贡献。

## 许可证

本项目遵循 [BSD-3-Clause](LICENSE) 许可协议。
