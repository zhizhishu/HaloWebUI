# TASK_LOG

project_name: HaloWebUI
project_root: C:\Users\echo\Downloads\claude\github\HaloWebUI

## 迭代（2026-05-09）
- 范围：继续检查作者 `upstream/main` 是否更新，将 `main` 作为纯上游镜像同步，再把作者更新合入 `future/custom` 并保留本仓库二改能力。
- 预期成果：
  - 记录作者本轮新增提交与当前远端指针。
  - 将本地/远端 `main` 对齐作者 `upstream/main`。
  - 将作者更新与本仓库二改内容整合到 `future`，验证后推进到 `custom`。
  - 保留并回归二改核心能力：普通用户继承管理员 MCP 配置、MCP 工具选择状态持久化。
- 原则：
  - KISS：`main` 只镜像上游，冲突只在 `future` 解决。
  - YAGNI：只处理本轮同步和必要冲突，不额外开发新功能。
  - DRY：复用已有分支规范、报告脚本和回归命令。
  - SOLID：保持 `main/future/custom` 职责分离。

### 目标清单
- [x] ~~**目标:** 拉取 upstream/origin 最新引用并确认本轮同步范围~~ (创建于: 2026-05-09 11:14:34 | **完成于: 2026-05-09 11:15:27**)
  - 拉取结果: `git fetch --all --prune` 成功。
  - 作者/镜像主线: `upstream/main=origin/main=b2eecdc`，自动同步 workflow 最近 3 次均成功，最新 run `25593548373` 于 `2026-05-09T05:59:59Z` 成功。
  - 本地状态: `main=bad335e` 仍是旧本地指针；`future=origin/future=77f6e93`；`custom=origin/custom=7582195`。
  - 作者更新清单: 从旧基线 `bad335e` 到新 `upstream/main` 已发生上游历史改写，`git rev-list main...origin/main = 156/163`；本轮需要在新上游基线上重建/整合二改，而不是直接普通 merge。
- [x] ~~**目标:** 在新 upstream/main 基线上重放并保留本仓库二改提交~~ (创建于: 2026-05-09 11:15:27 | **完成于: 2026-05-09 11:39:40**)
  - 重建结果: `future=origin/future=custom=origin/custom=ead4224`，均基于 `main/origin/main/upstream/main=b2eecdc`。
  - 保留二改: 普通用户继承管理员 MCP 配置、MCP 工具选择持久化、custom/future 镜像构建与回归脚本、分支工作流文档均已重放。
  - 本轮额外修正: 对齐上游 MCP 工具安全命名、管理员配置测试夹具、OpenAI 图像路由/usage 断言；补充 bare `responses` 端点识别兼容。
  - 验证结果: 后端目标回归 `121 passed`；前端关键回归 `19 passed`；预发布脚本 `failures=0`。
  - 远端同步: 已执行 `git push --force-with-lease origin future:future custom:custom`；`main` 保持纯上游镜像未写入二改。
  - 远端验证: 2026-05-09 11:52:05 确认 `custom/future` 的 `Custom Regression Guard` 与 Docker image build workflow 均为 `success`。
  - 已知非阻塞警告: 依赖弃用/缺少本地 ffmpeg、vite-plugin-svelte 的第三方包导出提示、预发布脚本未找到本地 Docker 镜像。

## 迭代（2026-05-10）
- 范围：拉取作者 `upstream/main` 与本仓库 `origin` 最新引用；保持 `main` 为纯上游镜像；如作者有新提交，将更新合入 `custom` 并保留二改内容。
- 预期成果：
  - 确认 `upstream/main`、`origin/main`、本地 `main` 是否一致。
  - 确认 `custom` 是否已包含最新 `main`。
  - 如存在上游更新，按最小冲突方式合并并验证二改能力。
- 原则：
  - KISS：先判断是否有真实上游更新，无更新不制造合并提交。
  - YAGNI：只做同步与保留二改，不新增功能。
  - DRY：复用现有回归脚本和分支策略。
  - SOLID：继续保持 `main` 与 `custom` 职责分离。

### 目标清单
- [x] ~~**目标:** 拉取最新 upstream/origin 并确认是否需要把更新合入 custom~~ (创建于: 2026-05-10 22:48:34 | **完成于: 2026-05-10 22:49:36**)
  - 拉取结果: `git fetch --all --prune` 成功。
  - 主线状态: `main=origin/main=upstream/main=b2eecdc`，作者本轮暂无新提交。
  - 二改状态: `custom=origin/custom=future=origin/future=ead4224`，`custom...main = 22/0`，说明二改分支包含最新 `main` 且未落后。
  - 处理结论: 无需新建 merge/rebase 提交；继续保留现有二改内容。
  - 验证方式: 分支指针与 ahead/behind 检查；本轮无代码变更，未重复运行测试。

## 迭代（2026-05-11）
- 范围：新增二改能力，让管理员可以用开关控制普通用户是否继承管理员可用模型。
- 预期成果：
  - 新增持久化配置开关，默认开启以符合当前二改预期。
  - 普通用户模型列表在开关开启时并入管理员可用模型，关闭时保持原有访问控制行为。
  - 保持 `main` 不变，仅在 `custom` 上实现 fork-only 功能。
- 原则：
  - KISS：复用现有模型访问控制和连接路由，不引入独立授权体系。
  - YAGNI：只实现管理员模型继承开关，不扩展其它资源继承。
  - DRY：复用现有模型列表、权限判断和配置 API 模式。
  - SOLID：模型继承逻辑独立封装，避免散落到多处路由。

### 目标清单
- [x] ~~**目标:** 新增管理员模型继承开关并覆盖后端回归测试~~ (创建于: 2026-05-11 07:48:01 | **完成于: 2026-05-11 08:20:27**)
  - 变更结果: 新增 `ENABLE_MODEL_INHERIT_FROM_ADMIN` 持久化配置，默认开启；管理员可在连接高级设置中切换“普通用户继承管理员模型”。
  - 后端行为: 开关开启时普通用户会并入管理员可用 base model 和管理员私有 workspace model，请求路由到拥有该模型的管理员连接；关闭或无配置时保持原访问控制。
  - 影响文件: `backend/open_webui/config.py`、`backend/open_webui/main.py`、`backend/open_webui/routers/configs.py`、`backend/open_webui/utils/models.py`、`backend/open_webui/utils/chat.py`、`src/lib/apis/configs/index.ts`、`src/lib/components/admin/Settings/Connections.svelte`、相关单测。
  - 验证结果: `test_models_sharing.py` 8 passed；模型访问/模型共享/MCP 继承组合回归 21 passed；前端 vitest 19 passed；`git diff --check` 通过；严格冲突标记检查无命中。
  - 已知情况: `npm run check` 仍被仓库既有全局 TypeScript/Svelte 诊断阻断，首批错误在 `AutoCompletion.js`、`katex-extension.ts`、`utils/index.ts`、`MessageInput.svelte` 等非本次改动文件。
  - 分支属性: fork-only 二改，继续只属于 `custom`；不要合入 `main` 纯上游镜像。
- [x] ~~**目标:** 让管理员连接设置页能实际显示模型继承开关~~ (创建于: 2026-05-12 01:36:59 | **完成于: 2026-05-12 01:40:46**)
  - 变更结果: `/settings/connections` 现在会按角色渲染；管理员显示全局连接管理页和 `Inherit Admin Models` 开关，普通用户仍显示个人连接偏好页。
  - 影响文件: `src/routes/(app)/settings/connections/+page.svelte`。
  - 验证结果: `npx vitest run src/lib/utils/model-capabilities.test.ts` 2 passed；`git diff --check` 通过。
  - 部署提醒: 当前远端 `origin/custom=ead4224` 仍不包含本次未提交二改；需要提交推送并等待 GHCR 镜像重建后，服务器拉新镜像才会看到该页面。

## 迭代（2026-05-12）
- 范围：把本地 `custom` 上的模型继承与连接页修复提交到远端，触发 GHCR `custom` 镜像重建，解决服务器拉取旧镜像导致页面仍看不到新开关的问题。
- 预期成果：
  - 只提交本次功能代码与测试，不提交本地规则文件。
  - 推送 `custom` 到 `origin/custom`。
  - 给出服务器拉取新镜像后的验证方式。
- 原则：
  - KISS：直接推进已有二改到镜像发布链路，不引入额外部署方式。
  - YAGNI：不改 1Panel、端口和反代配置，只解决镜像内容未更新。
  - DRY：复用现有 Docker image workflow 和 `custom` 分支发布流程。
  - SOLID：继续保持 `main` 纯上游、`custom` 承载 fork-only 二改。

### 目标清单
- [x] ~~**目标:** 提交并推送 custom 二改以触发 GHCR 镜像重建~~ (创建于: 2026-05-12 17:10:15 | **完成于: 2026-05-12 17:29:38**)
  - 变更结果: 已提交 `8386da0 feat: allow users to inherit admin models` 并推送到 `origin/custom`。
  - 验证结果: 后端继承/MCP 组合回归 `21 passed`；前端 `model-capabilities` vitest `2 passed`；`git diff --check` 无空白错误，仅 Windows 换行提示。
  - Actions 状态: `Custom Regression Guard` 已成功；`Create and publish Docker images with specific build args` 正在构建 GHCR 镜像。
  - 服务器下一步: 等 Docker workflow 成功后，在服务器执行 `docker pull ghcr.io/zhizhishu/halowebui:custom` 并 `docker compose -f docker-compose.image.yaml up -d --force-recreate`。

## 迭代（2026-05-12 晚）
- 范围：整理 fork 品牌与权限入口；让前端显示本仓库 custom 版本，把公开 GitHub 链接指向 `zhizhishu/HaloWebUI`，并把管理员模型/MCP 继承控制迁移到用户管理。
- 预期成果：
  - 用户可在前端看到 fork custom 版本号。
  - 前端可见仓库、反馈、更新等链接不再指向作者仓库。
  - 管理员能在用户管理中按用户控制是否继承管理员模型和 MCP。
  - 修复普通用户空 MCP 配置挡住管理员 MCP 继承的问题。
- 原则：
  - KISS：权限开关集中到用户编辑弹窗，不再散落在连接页。
  - YAGNI：不引入复杂角色系统，只在现有 user.settings 中保存 fork-only 权限。
  - DRY：模型和 MCP 共用同一套“继承管理员资源”用户设置读取逻辑。
  - SOLID：后端权限判断集中封装，前端只负责展示和保存。

### 目标清单
- [x] ~~**目标:** 实现 fork 版本/链接与用户级继承权限控制~~ (创建于: 2026-05-12 18:01:36 | **完成于: 2026-05-12 18:38:43**)
  - 变更结果: 前端设置页显示 `V<upstream version> · custom-<commit>` 与 `Custom` 标识；前端仓库、反馈、更新提示、README、Compose、排障/贡献/安全文档和 K8s 示例中的公开使用链接/镜像指向 `zhizhishu/HaloWebUI` / `ghcr.io/zhizhishu/halowebui`。
  - 权限入口: 移除连接页里的全局模型继承开关，把普通用户的 `Inherit Admin Models` 与 `Inherit Admin MCP` 放到用户管理编辑弹窗，并保存到 `user.settings.resource_inheritance`。
  - 后端行为: 模型继承和 MCP 继承都同时受全局配置与用户级设置控制；普通用户保存过空 MCP 配置时仍可继承管理员 MCP，非空用户 MCP 配置继续优先生效。
  - 验证结果: `uv run pytest backend/open_webui/test/unit/test_models_sharing.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py -q` 14 passed；`npx vitest run src/lib/utils/model-capabilities.test.ts` 2 passed；`git diff --check` 通过；针对本次新增/改动前端文件过滤 `npm run check` 未发现新增诊断。
  - 已知情况: 全量 `npm run check` 仍被仓库既有 TS/Svelte 诊断阻断，主要集中在旧的全局类型问题和未收紧的历史文件；本轮未扩大处理范围。
  - 部署下一步: 提交并推送 `custom` 后等待 GHCR 镜像构建完成，服务器再拉取 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器。
- [x] ~~**目标:** 修复 custom regression guard 的测试数据库目录初始化~~ (创建于: 2026-05-12 18:48:59 | **完成于: 2026-05-12 18:50:56**)
  - 变更结果: `Custom Regression Guard` 后端 MCP 回归在 workflow 中使用 `.reports/data` 作为临时 `DATA_DIR`，并在 pytest 前创建目录，避免 GitHub runner 因 SQLite 文件目录不存在而误报。
  - 验证结果: 本地用临时 `DATA_DIR` 跑 `uv run pytest backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_mcp.py -q`，34 passed；`git diff --check` 通过。
- [x] ~~**目标:** 修复继承 MCP 的工具权限链路并细化用户继承选择~~ (创建于: 2026-05-12 19:12:17 | **完成于: 2026-05-12 19:46:24**)
  - 变更结果: 继承 MCP 不再依赖普通用户的自建直连工具权限；`resource_inheritance` 支持模型和 MCP 分别选择“全部管理员资源”或“仅指定资源”；用户管理编辑弹窗会加载管理员模型/MCP 候选项并保存选择。
  - 兼容修复: MCP 继承候选项与运行时统一使用 `admin_id:index` / `legacy:index` 资源 ID，避免旧全局 MCP 配置在选中后无法继承。
  - 验证结果: 后端继承/MCP/模型回归 `50 passed`；前端 `model-capabilities` vitest `2 passed`；`npm run check` 过滤本次前端改动文件无新增诊断；`git diff --check` 通过，仅有 Windows 换行提示。
- [x] ~~**目标:** 修复接口配置页不显示已保存 API 的读写路径问题~~ (创建于: 2026-05-12 20:03:18 | **完成于: 2026-05-12 20:18:04**)
  - 变更结果: OpenAI/Gemini/Grok/Anthropic/Ollama 的 `/config` 接口改为读取管理员用户级 `ui.connections`，避免运行时可调用但设置页显示为空；`/config/update` 保存后也写回用户级连接，同时同步旧全局配置字段以保持兼容。
  - 工具函数: 新增 `get_user_connection_provider_config`，统一在读路径执行只读迁移和 provider 级配置获取，减少各 provider 自己拼迁移逻辑。
  - 验证结果: 后端 provider 配置/用户连接/模型继承/MCP 回归 `60 passed`；前端 `model-capabilities` vitest `2 passed`；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `f36113c fix: show saved provider connections` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器拉取新镜像并重建容器后即可在接口配置页看到已保存 API。
- [x] ~~**目标:** 修复用户管理资源继承没有显式细化选择的问题~~ (创建于: 2026-05-13 13:23:38 | **完成于: 2026-05-13 13:44:54**)
  - 变更结果: 用户编辑弹窗里的模型/MCP 继承从隐藏在“All”开关后的列表，改成了明确的“全部/指定”选择模式；指定模式直接展示可选管理员模型和 MCP 服务器、已选数量和空状态，管理员可以直接看到并保存精细选择。
  - 验证结果: `npx svelte-check --tsconfig ./tsconfig.json` 过滤本次文件未见新增诊断；后端模型/MCP 继承回归 `20 passed`；前端关键 vitest `2 passed`；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `9e0a21e fix: expose resource inheritance selection` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
- [x] ~~**目标:** 补齐资源继承新文案的中文本地化词条~~ (创建于: 2026-05-13 13:48:34 | **完成于: 2026-05-13 14:05:15**)
  - 变更结果: 将用户管理资源继承弹窗中新加的 scope、说明、空状态、All/Specified、selected 数量文案补进 `zh-CN` / `zh-TW` 词条，避免中文界面落回英文默认值。
  - 验证结果: `zh-CN` / `zh-TW` JSON 解析通过；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `46b20de fix: localize resource inheritance copy` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
- [x] ~~**目标:** 修复资源继承“指定”模式无法稳定切换和展示选择项的问题~~ (创建于: 2026-05-13 14:48:11 | **完成于: 2026-05-13 15:17:52**)
  - 变更结果: 将模型/MCP 继承范围从按钮点击改为原生 radio 分段控件，用不可变状态更新替代深层对象赋值；点击“指定”后会稳定进入指定模式并展开候选列表，候选项异步加载完成后也会自动填充当前可选资源。
  - 回归覆盖: 新增 `/users/resource-inheritance/options` 单测，确认管理员模型与管理员 MCP 候选项会返回给用户管理弹窗。
  - 验证结果: 后端资源继承/模型/MCP 回归 `21 passed`；`EditUserModal.svelte` 过滤 `svelte-check` 无新增诊断；前端 `model-capabilities` vitest `2 passed`；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `e4d2ab6 fix: make resource inheritance selection interactive` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器拉取 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器后即可看到“指定”模式可点击和可选择。
- [x] ~~**目标:** 复查并加固用户管理资源继承“指定”交互在生产镜像中的点击行为~~ (创建于: 2026-05-13 18:51:52 | **完成于: 2026-05-13 19:08:50**)
  - 变更结果: 移除“全部/指定”的隐藏 radio/label 交互，改回显式 `type="button"` 按钮；按钮点击直接写入继承范围，避免生产环境中隐藏输入框事件没有触发导致“指定”看起来点不动。
  - 验证结果: 后端资源继承/模型/MCP 回归 `21 passed`；`EditUserModal.svelte` 过滤 `svelte-check` 无新增诊断；前端 `model-capabilities` vitest `2 passed`；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `cf97316 fix: harden resource inheritance scope toggle` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器再次拉取 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器，确认用户管理编辑弹窗里的“指定”可直接点击并展开候选列表。
- [x] ~~**目标:** 用可执行前端回归复现并修复资源继承“全部/指定”来回切换问题~~ (创建于: 2026-05-13 20:35:30 | **完成于: 2026-05-13 21:08:16**)
  - 变更结果: 将用户管理资源继承 scope 改成原生 `select` 下拉框，并为模型/MCP 分别维护显式 scope 状态；切到“全部”明确写回 `null`，切到“指定”明确写入当前候选 ID 数组，避免按钮/隐藏输入事件和 `null`/数组隐式判断导致 UI 卡住。
  - 复用抽象: 新增 `resource-inheritance.ts`，统一 normalize、scope 判断、scope 切换、单项勾选和计数逻辑；弹窗只调用这些纯函数，减少模型与 MCP 两套状态逻辑漂移。
  - 回归覆盖: 新增 `resource-inheritance.test.ts`，覆盖模型全部→指定→全部、MCP 全部→指定→全部、模型/MCP 独立切换、指定模式下取消所有 MCP 单项仍保持指定模式。
  - 验证结果: 新增前端逻辑回归 `4 passed`；前端关键 vitest 合计 `6 passed`；后端资源继承/模型/MCP 回归 `21 passed`；`EditUserModal.svelte` 与新工具文件过滤 `svelte-check` 无新增诊断；`npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `1070f76 fix: make resource inheritance scope switching reliable` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器再次拉取 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器后，用户管理编辑弹窗应显示原生“全部/指定”下拉框，AI 模型和 MCP 都能来回切换。
- [x] ~~**目标:** 验证资源继承 UI 保存、模型使用与 MCP 权限完整链路~~ (创建于: 2026-05-14 10:27:27 | **完成于: 2026-05-14 10:51:40**)
  - 变更结果: 补充资源继承边界测试，覆盖 UI 状态保存 payload、模型继承使用、MCP 继承使用和“指定为空”权限隔离场景。
  - 前端覆盖: `resource-inheritance.test.ts` 新增“从全部取消单项会保存为指定剩余项”和“无候选时指定保存为空数组”测试，确认 UI payload 不会错误退回全部。
  - 后端覆盖: 模型继承新增 `admin_model_ids=[]` 阻断所有管理员模型测试；MCP 继承新增 `admin_mcp_server_ids=[]` 阻断所有管理员 MCP 服务器测试，确认指定为空不会越权继承。
  - 验证结果: 后端资源继承/模型/MCP 回归 `23 passed`；前端资源继承和模型能力回归 `8 passed`；资源继承相关 `svelte-check` 无新增诊断；`npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows 换行提示。
  - 远端结果: 已提交并推送 `ca8524f test: cover resource inheritance permission boundaries` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 结论: 当前自动化覆盖确认“可点击/可保存/可用模型/MCP/指定权限隔离”这条链路未发现回归；仍需服务器拉取新镜像后在真实账号界面做最终人工确认。
- [x] ~~**目标:** 将本仓库二改、验证结果和后续创新方向写入 README~~ (创建于: 2026-05-14 11:38:38 | **完成于: 2026-05-14 11:45:48**)
  - 变更结果: README 已改为 UTF-8 中文说明，写清 custom 分支定位、fork 版本/链接、用户级模型与 MCP 资源继承、接口配置修复、MCP 继承策略、验证结果、部署更新命令和后续创新方向。
  - 验证结果: `git diff --check` 通过，仅有 Windows LF/CRLF 提示。
  - 远端结果: 已提交并推送 `976a87a docs: document custom branch changes` 到 `origin/custom`；按提交号查询未发现新的 workflow run，README 文档提交可能未触发工作流。
- [x] ~~**目标:** 补强 README 核心功能说明，让项目介绍更完整和产品化~~ (创建于: 2026-05-14 12:31:53 | **完成于: 2026-05-14 12:34:52**)
  - 变更结果: 将短 bullet 版“核心能力”改成“核心功能”产品化区块，覆盖统一 AI 工作台、多模型与供应商网关、管理员资源继承、MCP 工具生态、知识库与文件增强、用户权限治理、私有化部署和分支发布策略，并新增能力矩阵表。
  - 验证结果: `git diff --check` 通过，仅有 Windows LF/CRLF 提示。
  - 远端结果: 已提交并推送 `5c001f6 docs: expand core features` 到 `origin/custom`；按提交号查询未发现新的 workflow run，README 文档提交可能未触发工作流。
- [x] ~~**目标:** 修复用户管理资源继承需要先开总开关、模型/MCP 范围无法稳定切换和字体错位问题~~ (创建于: 2026-05-14 17:17:04 | **完成于: 2026-05-14 17:52:55**)
  - 变更结果: 用户管理编辑弹窗中的模型/MCP 继承控制从“总开关 + 范围选择”改为单一三态下拉（已禁用/全部/指定）；指定模式直接展示候选资源列表，模型和 MCP 可独立从关闭切到指定或全部，不再需要先开总按钮；同时统一行高、select 高度和文本布局，缓解字体错位。
  - 测试覆盖: `resource-inheritance.test.ts` 新增模型“关闭→指定→全部”和 MCP“关闭→指定且不影响模型”的状态回归，覆盖保存 payload 中的布尔开关与资源 ID 组合。
  - 验证结果: 前端资源继承/模型能力 vitest `10 passed`；后端资源继承/模型/MCP 权限回归 `23 passed`；过滤 `svelte-check` 未发现 `EditUserModal.svelte` 或 `resource-inheritance` 相关诊断；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示。
  - 浏览器检查: Browser Relay 可连接真实 Chrome，但当前没有 HaloWebUI 已登录目标标签；未擅自导航用户现有标签，浏览器实点需服务器更新后在真实页面确认。
  - 远端结果: 已提交并推送 `c2fe54c fix: simplify resource inheritance controls` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器拉取最新 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器后，在用户管理编辑弹窗确认模型/MCP 下拉均可直接切换“已禁用/全部/指定”。
- [x] ~~**目标:** 修复资源继承“指定”下拉显示已切换但候选列表不展开的问题~~ (创建于: 2026-05-14 18:10:05 | **完成于: 2026-05-14 18:32:05**)
  - 变更结果: 移除资源继承 select 的本地绑定状态，把下拉显示、说明文案、计数胶囊和候选列表展开条件全部直接绑定到 `resource_inheritance` payload；选择“指定”会立即写入数组 payload，并用 keyed select 强制 DOM 与 payload 对齐，避免下拉看似选中但真实权限仍为“全部”。
  - 测试覆盖: 新增“选项尚未加载时切到指定也必须写入空数组 payload”的前端状态测试，确认指定模式不会是假状态。
  - 验证结果: 前端资源继承/模型能力 vitest `11 passed`；后端资源继承/模型/MCP 权限回归 `23 passed`；过滤 `svelte-check` 未发现 `EditUserModal.svelte` 或 `resource-inheritance` 相关诊断；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示。
  - 远端结果: 已提交并推送 `17b0f09 fix: derive resource inheritance selects from payload` 到 `origin/custom`；`Custom Regression Guard` 和 Docker 镜像构建均已成功。
  - 部署下一步: 服务器拉取最新 `ghcr.io/zhizhishu/halowebui:custom` 并重建容器后，选择“指定”时应立即从“当前及未来”变为 `x/y selected` 并展开可选管理员资源列表。
- [x] ~~**目标:** 复核资源继承“指定”问题根因并补强防回归验证~~ (创建于: 2026-05-14 18:48:49 | **完成于: 2026-05-14 18:51:08**)
  - 根因复核: 上一版存在 select 本地绑定状态与真实 `resource_inheritance` payload 两个状态源，可能导致下拉显示“指定”，但 payload 仍为 `null`，说明、计数和候选列表继续按“全部/当前及未来”渲染。
  - 当前确认: `EditUserModal.svelte` 已无 `modelResourceMode` / `mcpResourceMode` / `bind:value` 本地状态；select 的 value、说明文案、计数胶囊和候选列表展开条件均直接读取同一个 payload。
  - 验证结果: 复跑前端资源继承/模型能力 vitest `11 passed`；远端 `17b0f09` 的 `Custom Regression Guard` 与 Docker 镜像构建均为 success。

## 迭代（2026-05-18）
- 范围：修复 `Sync Fork Main With Upstream` 定时任务持续失败导致 GitHub 反复提醒的问题；拉取作者 `upstream/main` 最新内容，并融合到本仓库 `custom/future`，保留已创建的 fork 创新功能。
- 预期成果：
  - 明确任务书中已记录的本仓库创新功能范围。
  - 修复同步 workflow 在 checkout 纯上游 `main` 后找不到 custom 脚本的问题。
  - 将最新上游提交同步到 `main`，再融合到 `custom/future`。
  - 验证 custom 创新功能的核心回归，避免上游更新冲掉二改内容。
- 原则：
  - KISS：把同步失败点收敛到 workflow 自身，不把 custom 脚本塞进纯上游 `main`。
  - YAGNI：只修复当前反复报错和本轮上游同步，不扩大到无关部署/面板配置。
  - DRY：复用现有报告脚本能力或等价内联逻辑，避免同步链路依赖错误分支文件。
  - SOLID：继续保持 `main` 只镜像上游，`custom/future` 承载 fork 创新功能。

### 目标清单
- [x] ~~**目标:** 修复上游同步 workflow 报错并拉取最新上游内容~~ (创建于: 2026-05-18 18:18:57 | **完成于: 2026-05-18 18:49:04**)
  - 创新记录确认: 任务书已记录 fork custom 版本/链接、`ghcr.io/zhizhishu/halowebui` 镜像、用户级模型/MCP 资源继承、MCP 权限链路、接口配置显示修复、README 核心功能与后续创新方向。
  - 上游同步结果: 已拉取 `upstream/main` 最新提交 `f131cbf`，并将 `origin/main` 更新为同一提交，保持 `main` 作为纯上游镜像。
  - 融合结果: 已把 `upstream/main` 合并进 `custom`，生成合并提交 `f65702a`；随后提交 `8694284 fix: keep upstream sync report script available` 修复同步 workflow；`origin/custom` 与 `origin/future` 均已推送到 `8694284`，本地 `future` 分支也已快进到 `origin/future`。
  - 报错根因: `Sync Fork Main With Upstream` 在 checkout 纯上游 `main` 后尝试运行只存在于 custom/future 的 `scripts/generate-upstream-change-report.sh`，导致定时任务反复失败并触发 GitHub 提醒。
  - 修复方案: workflow 改为在临时目录从默认分支 `custom` 提取报告脚本，再对纯上游 `main` 生成同步报告；这样 `main` 仍保持纯净，不需要塞入 fork-only 脚本。
  - 验证结果: 后端目标回归 `72 passed`；前端目标 vitest `15 passed`；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功；冲突标记检查通过；报告脚本模拟生成成功。
  - GitHub Actions 结果: 手动 `Sync Fork Main With Upstream` run `26028348458` success；`Custom Regression Guard` 在 `custom` run `26028335637` 与 `future` run `26028335647` 均 success；Docker 镜像 workflow 在 `custom` run `26028335607` 与 `future` run `26028335622` 均 success。
  - 注意事项: `main` 上仍能看到一次历史失败的 Python/Frontend/Docker run，来自本轮手动推送纯上游 `main` 时触发的旧工作流，其中 Docker 失败包含 GHCR `502 Bad Gateway`；修复后的同步 workflow 已成功，后续定时同步使用 `GITHUB_TOKEN` 推送时通常不会继续触发这些 main push 工作流。

## 迭代（2026-05-19）
- 范围：修复旧对话页面残留已删除 MCP/工具 ID，导致工具列表不同步、无法从旧页面删除、继续对话时报错的问题。
- 预期成果：
  - 旧聊天恢复时自动丢弃当前用户已不可用或已删除的工具/MCP ID。
  - 发送消息前再次按最新工具列表净化 `tool_ids`，避免旧页面状态卡死对话。
  - 后端对失效 MCP/工具引用做容错过滤，防止前端旧缓存或旧历史 payload 直接导致接口失败。
  - 增加回归测试覆盖“删除工具后旧会话继续对话”的核心链路。
- 原则：
  - KISS：只处理已失效工具 ID 的过滤与同步，不重做工具系统。
  - YAGNI：不做数据库批量迁移，打开旧会话和发送时即时修正即可。
  - DRY：前端统一使用同一个工具 ID 过滤逻辑，避免恢复、模型默认工具和发送三处各写一套。
  - SOLID：前端负责 UI 状态同步，后端负责最终权限与存在性兜底。

### 目标清单
- [x] ~~**目标:** 修复旧对话残留已删除 MCP/工具导致无法继续对话的问题~~ (创建于: 2026-05-19 15:07:39 | **完成于: 2026-05-19 15:50:35**)
  - 根因确认: 旧聊天的 `composer_state` / 本地输入缓存会保存 `selected_tool_ids`，删除接口-工具里的 MCP/OpenAPI/工作区工具后，旧页面仍可能带着旧 `mcp:<idx>` 或工具 ID 发送；后端随后用这些旧 ID 严格加载 MCP runtime，越界/禁用/已删除时会把整次对话卡死。
  - 前端修复: 新增 `tool-selection` 工具函数，统一规范化和过滤工具 ID；旧会话恢复、输入缓存恢复、URL 工具参数、模型默认工具、composer 持久化和实际发送请求都会按当前 `$tools` 列表丢弃已删除工具。
  - 后端修复: 新增 `sanitize_tool_ids_for_request`，在 chat middleware 和 function pipe 调用正式校验/加载工具前过滤掉已删除、越界、禁用或当前用户不可读的工具 ID；通用 `validate_tool_ids_access` 仍保持严格行为，避免配置/管理路径失去校验。
  - 回归覆盖: 新增前端 `tool-selection.test.ts`，覆盖去重、工具列表未加载时保留、工具加载后删除旧 MCP/工具 ID、当前无可用工具时清空；后端新增 sanitizer 单测，覆盖删除工作区工具与失效 MCP 下标。
  - 验证结果: 前端 `npx vitest run src/lib/utils/tool-selection.test.ts src/lib/utils/resource-inheritance.test.ts src/lib/utils/model-capabilities.test.ts` 15 passed；后端 `uv run pytest backend/open_webui/test/unit/test_resource_access_control.py backend/open_webui/test/unit/test_user_tools_mcp_inherit.py backend/open_webui/test/unit/test_mcp.py -q` 50 passed；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示。
  - 已知情况: 全量 `svelte-check` 仍被仓库既有 TS/A11y 诊断阻断，未命中新加的 `tool-selection` 文件；本轮以 vitest、后端 pytest 和生产构建作为阻断级验证。

## 迭代（2026-05-20）
- 范围：拉取作者 `upstream/main` 最新项目内容，保持本仓库 `main` 纯上游镜像，再融合到 `custom/future` 并保留本仓库二创功能，重点保护最近修复的旧聊天 MCP/工具残留同步 bug。
- 预期成果：
  - 确认作者最新提交与本仓库分支差异。
  - 将 `origin/main` 对齐 `upstream/main`。
  - 将作者更新合入 `custom` 与 `future`，保留 fork 版本、资源继承、接口配置修复、README 二创说明、MCP 旧聊天工具过滤等功能。
  - 跑关键回归和构建，确认无冲突标记后推送到 `origin`。
- 原则：
  - KISS：按既有 `main -> custom/future` 流程同步，不额外改分支策略。
  - YAGNI：只融合作者更新与必要冲突修复，不顺手改无关功能。
  - DRY：复用现有测试脚本和 MCP/资源继承回归用例。
  - SOLID：继续保持 `main` 只承载上游，fork-only 二创留在 `custom/future`。

### 目标清单
- [x] ~~**目标:** 拉取作者最新上游并融合本仓库二创到 custom/future~~ (创建于: 2026-05-20 09:39:10 | **完成于: 2026-05-20 10:15:03**)
  - 上游同步结果: 已拉取作者 `upstream/main` 最新提交 `be6b483`（修复图片高级参数弹窗显示问题），并将本仓库 `origin/main` 对齐到同一提交，继续保持 `main` 纯上游镜像。
  - 融合结果: 已在 `custom` 合并 `upstream/main`，生成合并提交 `7771c16 Merge remote-tracking branch 'upstream/main' into custom`；本地与远端 `custom/future` 均已指向 `7771c16`。
  - 冲突处理: 唯一冲突在 `src/lib/components/chat/Chat.svelte` 的 import/发送路径附近；已同时保留作者新增的默认联网搜索模式解析和本仓库 `filterAvailableToolIds` 工具过滤链路，并补齐第二条发送路径的 `requestToolIds` 过滤变量。
  - 二创保留确认: fork 版本/链接、用户级模型与 MCP 资源继承、接口配置显示修复、README 二创说明、旧聊天 MCP/工具残留过滤与后端 sanitizer 均保留。
  - 本地验证: 前端 `tool-selection/resource-inheritance/model-capabilities/native-web-search` vitest `25 passed`；后端 MCP/资源继承/联网搜索目标回归 `69 passed`；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future`；`Custom Regression Guard` 在 custom run `26177424397`、future run `26177424549` 均 success；Docker 镜像 workflow 在 custom run `26177424395`、future run `26177424551` 均 success。
  - 注意事项: 构建仍输出仓库既有 Svelte/A11y 警告与部分第三方依赖提示，但未阻断生产构建；`AGENTS.md` 与 `TASK_LOG.md` 仍按本地项目记录保留为未跟踪文件，未提交到 Git。
- [x] ~~**目标:** 将旧聊天 MCP/工具残留修复补进 README 长期记录~~ (创建于: 2026-05-20 21:56:35 | **完成于: 2026-05-20 21:58:17**)
  - 变更结果: README 新增“旧聊天工具状态自修复”区块，写清旧聊天保存已删除 MCP/OpenAPI/工作区工具 ID 的根因、前端过滤链路、后端请求级 sanitizer 和配置路径严格校验边界。
  - 额外记录: README 的验证范围、MCP 工具生态和能力矩阵已补充“旧聊天删除工具后仍可继续对话/前后端过滤失效 `tool_ids`”。
  - 远端结果: 已提交并推送 `5e724f0 docs: record stale chat tool cleanup` 到 `origin/custom` 与 `origin/future`；README 文档提交未触发新的 Actions，上一轮 `7771c16` 的 custom/future 回归与 Docker 镜像构建仍为 success。

## 迭代（2026-05-24）
- 范围：拉取作者 `upstream/main` 最新项目内容，融合到本仓库 `custom/future` 并保留二创能力，同时修复新建对话发送按钮卡住/无效的问题。
- 预期成果：
  - 将 `origin/main` 对齐作者最新 `upstream/main`。
  - 将作者更新合入 `custom/future`，保留 fork 版本、资源继承、接口配置修复、旧聊天工具状态自修复等二创能力。
  - 定位并修复新建聊天发送链路中按钮无效或请求无法发出的问题。
  - 跑关键回归和生产构建后推送到你的 GitHub。
- 原则：
  - KISS：优先修发送链路的直接阻断点，不重写聊天系统。
  - YAGNI：只处理本次上游同步与发送卡住，不扩大到无关 UI 改造。
  - DRY：复用已有 tool-selection、资源继承、聊天发送测试覆盖。
  - SOLID：保持 `main` 纯上游，fork-only 修复留在 `custom/future`。

### 目标清单
- [x] ~~**目标:** 同步作者最新并修复新建对话发送按钮无效问题~~ (创建于: 2026-05-24 23:18:45 | **完成于: 2026-05-25 16:38:10**)
  - 上游同步结果: 已将 `origin/main` 对齐作者 `upstream/main` 最新提交 `a0ba442`，保持 `main` 纯上游镜像。
  - 融合结果: 已在 `custom` 合并 `upstream/main` 并推送合并提交 `6f41b9b`；`origin/custom` 与 `origin/future` 均已更新到该提交。
  - 冲突处理: 解决 workflow、images、users、MCP tests、tools 和 Chat.svelte 冲突；保留 fork 资源继承、旧聊天工具状态自修复、接口配置修复，同时合入上游 MCP 超时提示、用户默认设置、API key pool、图片/技能/停止状态更新。
  - 新建对话发送修复: 新增 `hasActiveChatResponse`，只把未完成 assistant 回复或真实 task 视为生成中；当前消息为 user 时不再误显示 Stop，也不再阻断后续发送。
  - 验证结果: 前端目标 vitest `21 passed`；后端目标 pytest `63 passed`；Node 22 下 `npm run build` 生产构建成功。
  - 浏览器验证情况: 本地 Vite dev server 监听 5173 后请求首字节超时，已关闭页面并释放端口；以单测覆盖 UI 状态、后端回归和生产构建作为本轮阻断级验证。
  - 远端结果: `Custom Regression Guard` 在 custom run `26391060216`、future run `26391060231` 均 success；Docker 镜像 workflow 在 custom run `26391060195`、future run `26391060219` 均 success。

## 迭代（2026-05-25 整理）
- 范围：按全局 AGENTS 项目边界协议重读并整理 HaloWebUI 项目状态，确认当前分支、远端 Actions、README 二创记录和本地接力文件是否可续接。
- 预期成果：
  - 确认父级 `C:\Users\echo\Downloads\claude` 只是存放根目录，不在父级创建日志或计划。
  - 确认真实项目根目录、当前分支、远端分支和最新发布状态。
  - 将新建对话发送按钮卡住修复补进 README，避免后续迭代遗忘该二创修复。
  - 记录本轮整理结论和下一步建议。
- 原则：
  - KISS：只整理项目状态和 README 记录，不做无关代码改造。
  - YAGNI：不创建新的 PROJECT_ID/TASK/LOG 体系，继续兼容项目已有 `TASK_LOG.md`。
  - DRY：README 只补充缺失的新建对话发送修复，不重复展开已有资源继承和旧聊天工具同步说明。
  - SOLID：继续保持 `main` 纯上游、`custom/future` 承载 fork-only 二创和镜像发布。

### 目标清单
- [x] ~~**目标:** 整理当前项目状态与 README 二创记录~~ (创建于: 2026-05-25 22:47:12 | **完成于: 2026-05-25 22:49:52**)
  - 项目边界: `C:\Users\echo\Downloads\claude` 未发现根级 `AGENTS.md`，按用户粘贴的全局 AGENTS 执行；真实项目为 `C:\Users\echo\Downloads\claude\github\HaloWebUI`。
  - 项目文件: `PROJECT_ID.md`、`PROJECT_CONTEXT.md`、`PROJECT_MAP.md`、`TASK.md`、`LOG.md` 均不存在；项目当前继续使用本地未跟踪 `AGENTS.md` 与 `TASK_LOG.md` 作为规则和接力记录。
  - 分支状态: 当前分支 `custom` 与 `origin/custom` 对齐在 `6f41b9b`；本地 `future` 与 `origin/future` 也在同一提交；`main` 对齐 `upstream/main=a0ba442`。
  - 远端验证: `custom` 最新 `Custom Regression Guard` run `26391060216` success，Docker run `26391060195` success；`future` 最新 `Custom Regression Guard` run `26391060231` success，Docker run `26391060219` success。
  - README 整理: 确认 README 文件本身是 UTF-8 正常中文，PowerShell 默认输出乱码只是终端编码显示问题；已补充“新建对话发送状态修复”、更新验证范围和能力矩阵。
  - 工作区说明: 本轮只修改 `README.md` 和本地 `TASK_LOG.md`；`AGENTS.md` 与 `TASK_LOG.md` 仍为本地未跟踪文件，未提交到 Git。

## 迭代（2026-05-26 上游 Issue 收集）
- 范围：使用 Browser Relay 查看原作者 `ztx888/HaloWebUI` 的公开 GitHub Issues，收集可能影响本仓库 `custom/future` 的 bug 线索。
- 预期成果：
  - 只读取公开 issue，不操作远端 issue/评论/标签。
  - 按影响面整理 bug 线索，标出是否可能影响本仓库二创能力。
  - 给出下一步需要验证或修复的候选清单。
- 原则：
  - KISS：先做公开 issue 信息收集和归类，不直接改代码。
  - YAGNI：不扩大到全站爬取或无关仓库。
  - DRY：优先复用 GitHub issue 列表和结构化字段，不手动复制大段正文。
  - SOLID：把上游 bug 情报与本仓库代码修改分开，避免未验证线索直接进入实现。

### 目标清单
- [ ] **目标:** 修复本地 MCP/OpenAPI 工具索引 ID 在删除或重排后误指向新工具
  - 创建于: 2026-05-25 15:51:48 -07:00
  - 复现依据: 本地工具服务器在工具列表和聊天请求中使用 `mcp:<index>` / `server:<index>`。当管理员或用户删除、重排 MCP/OpenAPI 服务器后，旧聊天或本地状态里的 `mcp:0` 仍可能匹配当前新的第 0 个服务器，导致已删除工具在旧页面上看似残留，甚至误调用新的工具。
  - 计划: 给保存后的本地 MCP/OpenAPI 连接补稳定连接 ID；`/api/v1/tools/` 对新连接优先暴露稳定工具 ID；后端聊天请求解析稳定 ID 到当前索引并保留旧索引兼容；前端工具过滤和阀门入口识别新稳定 ID；补前后端回归。

- [x] ~~**目标:** 收集原作者公开 issue 中的 bug 线索~~ (创建于: 2026-05-26 00:45:54 | **完成于: 2026-05-26 00:48:39**)
  - 收集范围: 原作者公开仓库 `ztx888/HaloWebUI` 的 GitHub Issues；Browser Relay 确认页面显示 open issues 为 4 个，`gh issue list --label bug --state all --limit 100` 拉取 bug 标签 issue 共 26 条。
  - 当前仍 open 的 bug: `#25 issue: 多问题汇总`、`#14 issue: 多问题汇总`、`#7 issue: 多问题汇总`。其中 `#25` 涉及标题/标签生成、MCP 标题描述同步、Azure/OpenAI/Responses 配置保存、reasoning 页面刷新抖动、图片生成设置 500 等；`#14` 涉及模型排序无法拖动、部分 API 不应带 Thinking 参数；`#7` 涉及 Qwen/思考参数与权限组/计费建议。
  - 最近已关闭但建议复核的 bug: `#53` 社区 skill 只能导入一个；`#50` `/api/config` 首次加载值不全；`#43` Gemini 图像生成参考图未传；`#38` 代码执行结果折叠/Excel 上传解析；`#37` 模型连接已失效；`#36` `/api/v1/skills/` 疯狂请求；`#34` 图片生成成功后仍报错；`#41` 原生联网走 `/v1/responses` 的用户误解/兼容提示。
  - 与本仓库 custom 高相关项: 资源/接口配置链路优先关注 `#50`、`#37`、`#25` 的 Azure/OpenAI/Responses 切换；聊天体验优先关注 `#25` 的刷新抖动和标题/标签生成；MCP 体验优先关注 `#25` 的 MCP 标题描述同步；技能/工具生态优先关注 `#53` 与 `#36`。
  - 处理结论: 本轮只收集和归类，不改代码；下一步建议先针对 `#50/#37/#25/#53/#36` 做本仓库可复现性验证，再决定是否在 `custom` 加防回归测试或单独修复。
  - 浏览器清理: 借用的 GitHub 标签已导航回原来的 `https://github.com/zhizhishu/sub-store/pkgs/container/sub-store`，未关闭用户原有标签。

## 长期计划（2026-05-26 起：上游 bug 情报 -> custom 回归 -> GitHub/GHCR 发布）
- 目标：把原作者 issue 中值得关注的问题转成长期固定工作流，避免每次只靠临时修 bug；每轮都必须确认 GitHub Actions 和 GHCR 镜像状态后再让服务器更新。
- 当前基线：
  - 本地/远端 `custom`：`6f41b9b Merge upstream/main into custom`
  - 本地/远端 `future`：`6f41b9b`
  - `main`/`upstream/main`：`a0ba442`
  - 最新 `custom` Docker workflow：run `26391060195` success
  - 最新 `future` Docker workflow：run `26391060219` success
  - `ghcr.io/zhizhishu/halowebui:custom` manifest 可读，包含 linux/amd64 与 linux/arm64
  - GitHub Packages 版本 API 当前 token 缺 `read:packages`，不能作为固定检查；以 Docker workflow success + `docker manifest inspect` 作为镜像门禁。

### 固定节奏
1. 每周或每次上游有新提交时：
   - `git fetch --all --prune`
   - 查看 `upstream/main` 与 `origin/main/custom/future` 差异。
   - 查看原作者 `ztx888/HaloWebUI` 最新 open bug 与最近 closed bug。
2. 每轮同步前：
   - `main` 只对齐 `upstream/main`，不放二创。
   - `custom` 合并 `main/upstream/main` 并保留 fork-only 能力。
   - `future` 快进或同步到 `custom`，作为同内容镜像发布分支。
3. 每轮修复前：
   - 先从 issue 清单选 1-3 个高价值问题，不同时展开太多。
   - 优先补可执行回归，再做最小实现。
   - 代码改动后更新 `TASK_LOG.md`，README 只记录长期能力或部署必读内容。
4. 每轮推送发布：
   - 本地目标测试通过后推 `origin/custom` 与 `origin/future`。
   - 读取 GitHub Actions：
     - `Custom Regression Guard` 必须 success。
     - `Create and publish Docker images with specific build args` 必须 success。
   - 读取镜像：
     - `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom`
     - 必须确认 manifest 可读且包含目标架构。
   - 服务器更新命令固定为：
     ```bash
     cd /root/HaloWebUI
     docker pull ghcr.io/zhizhishu/halowebui:custom
     docker compose -f docker-compose.image.yaml up -d --force-recreate
     docker ps
     docker logs halowebui --tail 80
     curl -I http://127.0.0.1:5060
     ```

### 问题池优先级
- P0 / 发布前必测：
  - `#50 /api/config 有时候值不全`：首次打开、cookie 失效但 localStorage token 存在时，接口配置、联网方式、资源继承配置必须完整。
  - `#37 模型连接已失效`：旧 provider 配置、迁移后模型连接、普通用户继承管理员模型后对话必须可用。
  - `#25` 中 Azure/OpenAI/Responses 配置切换：保存后刷新不应回退；Responses 开关可以取消；位置删除/新增后不残留旧配置。
- P1 / custom 二创高相关：
  - `#25` 中 MCP 标题/描述同步：管理员配置的 MCP 展示信息应同步到聊天主页面和用户继承视图。
  - `#25` 中标题/标签生成：Gemini/OpenAI 任务模型返回空内容时要有兼容或说明；左侧标题应及时更新。
  - `#53` 社区 skill 只能导入一个、`#36` skills 疯狂请求：验证 skill/tool/MCP 状态不会互相污染或造成请求风暴。
- P2 / 扩展回归：
  - `#38` 代码执行结果折叠与 Excel 上传解析。
  - `#43` Gemini 图像生成参考图传递。
  - `#41` 原生联网走 `/v1/responses`：保留说明和错误提示，避免用户误以为 Responses API 开关失效。

### 验收门禁
- 后端：资源继承、provider 配置、MCP/tool 权限、聊天请求、联网搜索相关 pytest。
- 前端：`tool-selection`、`resource-inheritance`、`model-capabilities`、聊天响应状态、skill/tool 状态相关 vitest。
- 构建：`NODE_OPTIONS=--max-old-space-size=4096 npm run build`。
- 远端：custom/future 两条分支的 Regression Guard 与 Docker workflow 全部 success。
- 镜像：GHCR `custom` manifest 可读；服务器拉取后页面版本显示 `custom-<commit>` 与目标提交一致。

## 迭代（2026-05-26 六线回归）
- 范围：围绕用户指定的六条线逐步验证：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 预期成果：
  - 先用现有目标测试确认是否已有防回归覆盖。
  - 若复现真实问题，补最小测试和修复，随后推送 GitHub 并等 GHCR 镜像门禁。
  - 若未复现，只记录验证结果，不做无意义改动。
- 原则：
  - KISS：一次只处理能被测试证明的问题。
  - YAGNI：没有复现或没有风险证据的 issue 不提前开发。
  - DRY：复用现有 provider/resource/MCP/tool/native search 测试套件。
  - SOLID：把配置、权限、工具状态和聊天状态各自验证清楚，避免一个修复污染另一条线。

### 目标清单
- [x] ~~**目标:** 跑通六条线现有目标回归并识别缺口~~ (创建于: 2026-05-26 01:05:44 | **完成于: 2026-05-25 10:53:41 -07:00**)
  - 2026-05-25 10:29:47 本轮继续：确认项目无 `PROJECT_ID.md`，按项目 `AGENTS.md` 使用 `custom` 与本地 `TASK_LOG.md`；已发现 `/api/config` 前端无参刷新会在 cookie 缺失但 localStorage token 存在时降级为未登录配置，准备做最小修复并补前端回归。
  - 相关 issue 二次筛选: 只保留会影响本仓库 custom/future 六条线的问题：接口配置/全局接口 `ztx888#50/#47/#37/#25`，MCP/工具/技能 `ztx888#53/#45/#36`、`open-webui#24906/#24618/#19313/#24038/#24195/#20896`，新旧聊天状态 `open-webui#25052/#22525/#14806`，原生联网/Responses 提示 `ztx888#41`，默认参数继承 `open-webui#24930`。OAuth、Logo、迁移说明、首屏性能、图片参考图等暂不进入本轮六线计划。
  - 修复结果: 提交 `248eaba Fix authenticated backend config refresh`，让 `getBackendConfig()` 无参刷新默认读取 `localStorage.token`，避免已登录页面在 cookie 缺失时请求到未登录版 `/api/config`；显式 `getBackendConfig('')` 仍保留公开配置行为。
  - 影响文件: `src/lib/apis/index.ts`、`src/lib/apis/index.test.ts`、`README.md`。
  - 验证结果: 前端目标回归 9 files / 43 tests passed；后端 provider/model/resource/MCP/native-search/chat 目标回归 138 passed；`git diff --check` 通过；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `248eaba`；GitHub Actions run `26413135943/26413135979/26413135981/26413136030` 截至记录时仍在 `in_progress`，需后续确认 Regression Guard 与 Docker workflow 最终结论。
  - GHCR 状态: 推送后旧 manifest 已确认可读并包含 `linux/amd64` 与 `linux/arm64`；需在 Docker workflow success 后再次确认 `ghcr.io/zhizhishu/halowebui:custom`。
  - 工作区说明: `AGENTS.md` 与 `TASK_LOG.md` 仍是本地未跟踪文件，未提交；本次提交只包含代码、测试和 README。
- [x] ~~**目标:** 只保留与本仓库六条线相关的 issue，并修复 native web search 与函数/MCP 工具冲突~~ (创建于: 2026-05-25 11:31:41 -07:00 | **完成于: 2026-05-25 11:36:00 -07:00**)
  - 筛选结论: 只把会影响本仓库 `custom/future` 的接口配置、模型继承、MCP 继承、工具/技能状态、新旧聊天发送状态、原生联网提示纳入后续问题池；OAuth、Logo、迁移文档、首屏性能、图片参考图、代码执行折叠等暂不纳入本轮六线计划。
  - 保留问题池: `ztx888#50/#47/#37/#25` 归入接口配置/Responses 切换；`ztx888#53/#45/#36` 归入技能/工具状态；`ztx888#25` 的 MCP 标题描述同步、标题/标签生成、刷新抖动归入 MCP/聊天状态；`ztx888#41` 与 open-webui native function/tool 相关 issue 归入原生联网提示；`open-webui#24930` 归入默认参数/继承行为观察。
  - 已修真实风险: `backend/open_webui/utils/openai_responses.py` 在 `native_web_search_required=True` 且同时存在 function tools 时不再强制 `tool_choice={"type":"web_search"}`，改为保留 `tool_choice="auto"`，避免原生联网场景把 MCP/OpenAPI/工作区函数工具挤掉。
  - 影响文件: `backend/open_webui/utils/openai_responses.py`、`backend/open_webui/test/unit/test_openai_responses.py`。
  - 验证结果: `test_openai_responses.py` 与 `test_auto_web_search_decision.py` 26 passed；前端 native/tool/model/chat 状态目标 vitest 22 passed；六线前端目标 43 passed；六线后端目标 139 passed；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已提交并推送 `5ae5da5 Keep function tools available with native web search` 到 `origin/custom` 与 `origin/future`；custom/future 的 `Custom Regression Guard` 与 Docker workflow 均为 success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述两个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复旧式 MCP 配置描述在继承/工具列表中不同步~~ (创建于: 2026-05-25 11:44:00 -07:00 | **完成于: 2026-05-25 11:52:32 -07:00**)
  - 复现依据: `get_mcp_server_display_metadata()` 已兼容旧式 `config.remark` 作为 MCP 显示名，但描述只读取根级 `description`；旧全局或旧用户 MCP 配置若把说明保存在 `config.description`，用户继承可选 MCP 列表和聊天工具列表会丢失管理员写的描述。
  - 修复结果: MCP 显示元数据现在按 `server.description -> config.description -> default_description` 解析描述，保持根级新格式优先，同时兼容旧配置。
  - 影响文件: `backend/open_webui/utils/mcp.py`、`backend/open_webui/test/unit/test_mcp.py`。
  - 验证结果: 定点 MCP/继承回归 `13 passed`；后端 MCP/继承/资源权限/skill 目标回归 `66 passed`；前端 tool/resource/model 目标 vitest `17 passed`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示。
  - 远端结果: 已提交 `51f8160 Preserve legacy MCP descriptions` 并推送到 `origin/custom` 与 `origin/future`；custom run `26415350900/26415350907` success，future run `26415350831/26415350836` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/arm64` 与 `linux/amd64`。
  - 工作区说明: Git 只提交了上述两个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 保留用户当次对话显式采样参数，避免被模型默认参数覆盖~~ (创建于: 2026-05-25 12:25:38 -07:00 | **完成于: 2026-05-25 12:25:38 -07:00**)
  - 复现依据: 新增失败用例证明 `apply_model_params_to_body_openai()` 会把用户 payload 中的 `temperature=0.3` 覆盖为模型默认 `temperature=0.8`；这会影响继承管理员模型后普通用户当次对话参数优先级。
  - 修复结果: OpenAI 与 Ollama 模型默认参数现在只补齐缺失字段，不覆盖用户 payload 已显式给出的 `temperature/top_p/max_tokens/reasoning_effort` 等映射参数；Ollama 显式 `max_tokens` 会先转换为 `num_predict` 并保留用户值。
  - 影响文件: `backend/open_webui/utils/payload.py`、`backend/open_webui/test/unit/test_model_reasoning_priority.py`。
  - 验证结果: 定点模型参数回归包含在后端六线目标套件中，`123 passed, 6 warnings`；前端 tool/resource/model/native-search/chat 状态 vitest `31 passed`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；本轮工作树此前已执行 `NODE_OPTIONS=--max-old-space-size=4096 npm run build` 并成功写入 `build`。
  - 远端结果: 已提交 `4fd84c6 Preserve explicit chat sampling params` 并推送到 `origin/custom` 与 `origin/future`；custom run `26416514038/26416514039` success，future run `26416514059/26416513998` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述两个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 清理旧聊天、URL 和本地状态里的陈旧 skill 选择~~ (创建于: 2026-05-25 13:03:45 -07:00 | **完成于: 2026-05-25 13:03:45 -07:00**)
  - 复现依据: tool/MCP 选择已有前端 `filterAvailableToolIds()` 与后端 `sanitize_tool_ids_for_request()` 双层保护，但 skill 选择此前只在 `Chat.svelte` 内临时过滤；当 skill 列表已加载为空或旧聊天/URL/local state 带有已删除 skill id 时，前端状态仍可能残留，和工具行为不一致。
  - 修复结果: 新增 `filterAvailableSkillIds()` 统一规范化、去重并按已加载 skill 列表过滤；聊天页恢复 composer state、chat input state、URL `skills/skill-ids`、模型默认 skill、旧消息 `<$skill>` 标签和请求 `skill_ids` 时都走同一过滤逻辑。列表未加载时暂存规范化 id，列表已解析为空时清空陈旧 id；若 skills store 已被其他页面预热为非空，也会视为可用列表并立即过滤。
  - 影响文件: `src/lib/components/chat/Chat.svelte`、`src/lib/utils/skill-selection.ts`、`src/lib/utils/skill-selection.test.ts`。
  - 验证结果: 前端目标回归 `6 files / 35 tests passed`；后端 MCP/资源权限/skill 目标回归 `61 passed, 1 warning`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 远端结果: 已提交 `3dd886f Drop stale chat skill selections` 并推送到 `origin/custom` 与 `origin/future`；custom run `26417790636/26417790615` success，future run `26417790602/26417790582` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: 计划只提交上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复接口配置删除连接保存失败时 UI 假删除的问题~~ (创建于: 2026-05-25 13:27:34 -07:00 | **完成于: 2026-05-25 13:47:40 -07:00**)
  - 复现依据: `Connections.svelte` 中 OpenAI/Gemini/Grok/Anthropic/Ollama 删除连接时先改本地数组与 config，再调用 `update*Handler(...)` 且不 `await`；子连接卡片的确认弹窗也不等待 `onDelete()`。如果后端保存失败或被并发保存覆盖，UI 会先消失，但后端旧接口仍可能保留并继续可调用。
  - 修复结果: 新增 provider 连接删除重排工具函数；OpenAI/Gemini/Grok/Anthropic/Ollama 删除连接时先快照、保存失败回滚，且确认弹窗会等待 `onDelete()` 完成。若同一 provider 在删除保存期间发生了新的保存请求，则不盲目回滚覆盖新状态。
  - 影响文件: `src/lib/components/admin/Settings/Connections.svelte`、5 个 provider 连接卡片、`src/lib/utils/provider-connections.ts`、`src/lib/utils/provider-connections.test.ts`。
  - 验证结果: 前端接口/六线目标回归 `9 files / 38 tests passed`；后端 provider/Responses 回归 `48 passed, 3 warnings`；定点 provider helper 回归 `4 files / 12 tests passed`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功，输出 `Wrote site to "build"`。
  - 远端结果: 已提交 `6ea46fa Fix provider connection delete persistence` 并推送到 `origin/custom` 与 `origin/future`；custom run `26419259373/26419259392` success，future run `26419278829/26419278819` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/arm64` 与 `linux/amd64`。
  - 工作区说明: Git 只提交了上述代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复 LobeHub 预置 Skill 安装后无法稳定识别已安装状态~~ (创建于: 2026-05-25 14:13:29 -07:00 | **完成于: 2026-05-25 14:39:18 -07:00**)
  - 复现依据: 真实下载 `anthropics-skills-pdf` 与 `anthropics-skills-pptx` 后，后端 ZIP 导入保存的 identifier 为 `zip.<hash>`，而前端 LobeHub 预置卡片用 `entry.identifier` 判断是否已安装；因此从预置卡片安装后可能仍显示可安装，造成社区 Skill 添加状态混乱。
  - 修复结果: 给远程 ZIP 导入增加可选 fallback identifier；后端仅在 SKILL.md 未声明 identifier 时使用该 fallback；普通 URL/GitHub/手动 ZIP 导入默认行为不变。LobeHub 预置安装时传入 `entry.identifier`，安装后卡片能稳定识别已安装状态。
  - 影响文件: `backend/open_webui/utils/skill_importer.py`、`backend/open_webui/routers/skills.py`、`src/lib/apis/skills/index.ts`、`src/lib/components/workspace/Skills.svelte`、相关前后端测试。
  - 验证结果: 后端 skill/runtime/route 目标回归 `11 passed`；前端 skill/tool/resource/native-search/chat 目标回归 `33 passed`；扩展后端六线目标回归 `95 passed, 6 warnings`；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已提交 `b8baa50 Fix catalog skill install recognition` 并推送到 `origin/custom` 与 `origin/future`；custom run `26420505172/26420505145` success，future run `26420506193/26420506195` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/arm64` 与 `linux/amd64`。
  - 工作区说明: Git 只提交了上述代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复旧聊天终态 assistant 消息导致输入框误判为仍在生成~~ (创建于: 2026-05-25 14:38:10 -07:00 | **完成于: 2026-05-25 15:03:39 -07:00**)
  - 创建于: 2026-05-25 14:38:10 -07:00
  - 复现依据: `MessageInput.svelte` 的发送/停止按钮由 `hasActiveChatResponse(history, taskIds)` 控制；旧聊天如果保存了 `stopped`、`stoppedByUser`、`error` 或 `completedAt`，但历史数据没有规范写回 `done=true`，会被 `done !== true` 误判为仍在生成，导致页面只显示“停止”按钮，新消息发送入口像是卡住。
  - 修复结果: 已提交 `7e7ef69 Fix stale chat response busy state`，在 `chat-response-state.ts` 中集中识别 assistant 终态消息；保留新发送空 assistant 占位的 active 状态，只排除已停止、已出错或已完成的旧消息。
  - 验证结果: `chat-response-state` 定点回归 6 passed；六线前端目标套件 8 files / 41 tests passed；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future`；custom run `26421124523/26421124522` success，future run `26421124529/26421124539` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了 `src/lib/utils/chat-response-state.ts` 与对应测试；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复单连接 modelref 选择值误报模型连接已失效~~ (创建于: 2026-05-25 15:11:49 -07:00 | **完成于: 2026-05-25 15:35:34 -07:00**)
  - 创建于: 2026-05-25 15:11:49 -07:00
  - 复现依据: `resolve_provider_connection_by_model_id()` 对裸 `gpt-4o` 在单连接配置下能解析成功，但对等价的新版选择值 `modelref::openai::personal::none::gpt-4o` 会进入 `model_connection_stale`，导致旧页面/缓存选择或单连接模型也可能报“模型连接已失效，请重新选择模型”。
  - 修复结果: 已提交 `41f626c Fix single-connection modelref routing`，将没有 `connection_id` / `prefix_id` / `connection_index` 的 modelref 视为普通模型选择，保留 provider 校验，并回落到单连接/唯一候选解析；显式连接 ID 或旧 index 仍保持严格校验。
  - 影响文件: `backend/open_webui/utils/model_identity.py`、`backend/open_webui/test/unit/test_model_identity.py`。
  - 验证结果: 定点 `test_model_identity.py` 9 passed；provider/model/resource 相关回归 42 passed；base cache/resource 继承回归 3 passed；六线后端目标回归 116 passed；六线前端目标 vitest 8 files / 41 tests passed；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `41f626c`；custom/future 的 `Custom Regression Guard` 分别为 run `26422235490` / `26422250059` success；Docker workflow run `26422235495` / `26422250054` 截至记录时仍在 `in_progress`。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述两个后端文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复旧聊天/本地状态中的 MCP/OpenAPI 下标工具 ID 删除重排后误指向新工具~~ (创建于: 2026-05-25 16:21:38 -07:00 | **完成于: 2026-05-25 16:55:19 -07:00**)
  - 创建于: 2026-05-25 16:21:38 -07:00
  - 复现依据: 本地 OpenAPI/MCP 工具此前使用 `server:<index>` / `mcp:<index>` 作为持久选择值；删除或重排服务器后，旧聊天和本地状态里的 `mcp:0` / `server:0` 可能指向当前新的第 0 个服务器，导致已删除工具仍残留并破坏新旧聊天发送。
  - 修复结果: 已提交 `cc7286b Fix stable tool server selections`，给本地 OpenAPI/MCP 连接分配稳定 `id`；工具列表展示 `server_id:<id>` / `mcp_id:<id>`；请求时映射回当前运行时下标；当前连接已有稳定 ID 时丢弃旧下标选择，避免误路由。
  - 影响文件: `backend/open_webui/routers/configs.py`、`backend/open_webui/routers/tools.py`、`backend/open_webui/utils/mcp.py`、`backend/open_webui/utils/tools.py`、`src/lib/components/admin/Settings/Tools.svelte`、`src/lib/components/chat/Chat.svelte`、`src/lib/components/chat/Controls/Valves.svelte`、相关前后端测试。
  - 验证结果: 后端六线目标回归 `131 passed, 6 warnings`；前端六线目标回归 `8 files / 43 tests passed`；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `cc7286b`；custom/future 的 `Custom Regression Guard` 和 Docker workflow 全部 `success`。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 复核原生联网提示、模型/MCP 继承和接口配置三条线当前状态~~ (创建于: 2026-05-25 16:55:19 -07:00 | **完成于: 2026-05-25 17:02:01 -07:00**)
  - 复核结果: 本轮未复现新的真实 bug，因此未修改业务代码、未推送新提交。
  - 原生联网/Responses: 前端 `native-web-search`、`web-search-mode`、`connection-errors` 定点回归 `13 passed`；后端 `auto_web_search_decision`、`native_web_search_support`、`openai_responses` 定点回归 `34 passed, 6 warnings`。
  - 模型/MCP 继承: 后端资源继承、MCP 继承、资源权限、模型共享和 provider base model 回归 `47 passed, 3 warnings`；前端资源继承、模型能力、工具选择回归 `19 passed`。
  - 接口配置: 后端 provider config/user connections/provider access/model identity/openai connection verification 回归 `42 passed, 3 warnings`；前端 API/config/provider helper/model capability 回归 `10 passed`。
  - 处理原则: 按用户要求，没有证据的点不改；没有修复就不推空提交。
- [x] ~~**目标:** 修复工具调用参数别名回归守护，确保工具/技能状态测试覆盖 `queries -> query`~~ (创建于: 2026-05-25 17:02:01 -07:00 | **完成于: 2026-05-25 17:34:11 -07:00**)
  - 复现依据: 六线后端组合回归中 `test_tool_call_normalization.py::test_param_alias_mapping_queries_to_query` 失败；生产代码已经支持 `queries -> query` 的 `ies -> y` 别名映射，但测试本地 `_map_aliases()` 模拟器仍只支持简单去尾 `s`，导致回归守护误报。
  - 修复结果: 已提交 `c24aae3 Fix tool call alias regression guard`，让测试模拟器同时覆盖 `queries -> query`、普通复数去尾 `s`、`query -> queries` 和普通单数加 `s`，与生产工具调用归一化逻辑保持一致。
  - 影响文件: `backend/open_webui/test/unit/test_tool_call_normalization.py`。本次是测试守护修复，不改生产业务逻辑。
  - 验证结果: 后端六线组合回归 `163 passed, 6 warnings`；前端六线组合回归 `10 files / 50 tests passed`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `c24aae3`；custom run `26425310628/26425310581` success，future run `26425317591/26425317596` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 复核 `#36` Skills 疯狂请求/页面抖动在当前 custom 的可复现性~~ (创建于: 2026-05-25 17:34:11 -07:00 | **完成于: 2026-05-25 17:40:01 -07:00**)
  - 复核范围: 原作者 `ztx888/HaloWebUI#36` 现为 closed，原始现象是点击会话生成后不断请求 `/api/v1/skills/`，并伴随 CodeMirror `EditorView.update` 崩溃；该问题归入本仓库六条线中的“工具技能状态 / 新旧聊天发送状态”。
  - 代码检查: 当前 `Chat.svelte` 已用 `hasResolvedSkills` + `isLoadingSkills` 避免聊天页重复拉取 skills；`InputMenu.svelte` 已用 `loadingSkills` 避免打开菜单时并发重复拉取；`Skills.svelte` 仅在 onMount、手动刷新或导入/删除/安装等用户动作后刷新。
  - 编码确认: 技能状态中文文案在源码 UTF-8 中正常；PowerShell 输出里偶发 mojibake 属终端显示问题，不是源码乱码。
  - 验证结果: 前端 skill/tool/chat/resource/model 目标回归 `6 files / 31 tests passed`；后端 skill/MCP/tool/chat 目标回归 `76 passed, 1 warning`；`git diff --check` 通过。
  - 处理结论: 本轮未复现新的真实 bug，未修改业务代码，未推送空提交；继续保留该项作为工具技能状态的观察点。
- [x] ~~**目标:** 修复 provider 连接编辑保存失败时 UI 假保存的问题~~ (创建于: 2026-05-25 17:48:42 -07:00 | **完成于: 2026-05-25 18:06:45 -07:00**)
  - 创建于: 2026-05-25 17:48:42 -07:00
  - 复现依据: OpenAI/Gemini/Grok/Anthropic/Ollama 连接卡片编辑时先把 `url/key/config` 写入父级绑定状态，再等待后端保存；如果保存失败，界面会显示新配置，但后端仍保留旧接口，属于“接口配置页面状态和运行时状态不一致”的同类风险。
  - 修复结果: 新增 `submitProviderConnectionEdit()`，五个 provider 编辑入口保存失败时会回滚到旧的 `url/key/config`，保存成功才保留新状态；同时补了保存成功和保存失败回滚的前端回归。
  - 影响文件: `src/lib/utils/provider-connections.ts`、`src/lib/utils/provider-connections.test.ts`、OpenAI/Gemini/Grok/Anthropic/Ollama 五个连接卡片。
  - 验证结果: provider helper 定点 `6 passed`；前端六线目标 `9 files / 50 tests passed`；后端 provider/model/resource/MCP/tool 相关目标 `121 passed, 6 warnings`；`npm run check` 全量仍有既有历史诊断，但过滤本次 touched files 无新增诊断；`git diff --check` 通过；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已提交 `982b6b6 Rollback provider edits on save failure` 并推送到 `origin/custom` 与 `origin/future`；custom run `26426521593/26426521623` success，future run `26426521608/26426521607` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/arm64` 与 `linux/amd64`。
  - 工作区说明: Git 只提交了上述代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复 MCP 继承指定范围使用下标导致删除/重排后误继承的问题~~ (创建于: 2026-05-25 18:55:08 -07:00 | **完成于: 2026-05-25 19:39:54 -07:00**)
  - 范围: 只针对六条线中的模型继承与 MCP 继承；继续兼顾工具可用性边界，避免指定范围只是 UI 假选择。
  - 已确认: 当前项目为 `C:\Users\echo\Downloads\claude\github\HaloWebUI`，分支 `custom`，无 `PROJECT_ID.md`；`AGENTS.md` 与 `TASK_LOG.md` 为本地未跟踪接力文件，不提交。
  - 复现依据: MCP 继承指定范围原先保存 `admin-1:0` / `admin-1:1` 这类管理员连接下标；管理员删除或重排 MCP 后，普通用户可能从旧下标误继承到另一个新 MCP，和此前工具选择下标误指向问题同类。
  - 修复结果: 带稳定 `id` 的管理员 MCP 继承资源现在使用 `admin-1:id:<connection-id>`；旧下标只在连接没有稳定 ID 时回退使用。用户管理的 MCP 可选列表会暴露稳定 ID，后端过滤也按稳定 ID 判断，旧下标不会再匹配带稳定 ID 的连接。
  - 影响文件: `backend/open_webui/utils/user_resource_inheritance.py`、`backend/open_webui/utils/user_tools.py`、`backend/open_webui/routers/users.py`、`backend/open_webui/test/unit/test_user_tools_mcp_inherit.py`、`backend/open_webui/test/unit/test_resource_inheritance_options.py`。
  - 验证结果: MCP 继承定点回归 `15 passed, 3 warnings`；前端六线目标 `9 files / 50 tests passed`；后端 MCP/继承/权限/模型身份目标 `104 passed, 3 warnings`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已提交 `d528bdb Stabilize inherited MCP selections` 并推送到 `origin/custom` 与 `origin/future`；custom run `26429213239/26429213238` success，future run `26429214296/26429214312` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了上述五个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 完成稳定模型继承选择的远端门禁验证~~ (创建于: 2026-05-25 19:40:00 -07:00 | **完成于: 2026-05-25 20:45:31 -07:00**)
  - 范围: 只针对六条线中的模型继承；验证上一轮 `d5aba02 Stabilize inherited model selections` 是否已经完整通过远端回归和镜像发布。
  - 修复结果: 管理员模型继承指定范围使用稳定资源 ID `admin-<owner>:model:<selection-or-model>`，同名/同 ID 模型不再互相串权；前端可选列表显示 `display_id`，后端运行时保留 legacy raw model ID / selection ID 兼容。
  - 本地验证: 后端定点模型/资源继承 `16 passed`；后端六线相关子集 `100 passed`；前端 resource/model/tool/native-search 目标 vitest `29 passed`；`git diff --check` 通过；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: `origin/custom`、`origin/future` 与本地 `HEAD` 均为 `d5aba025aed81ef96d817e1a25cd6078e5dd28b7`；custom Regression run `26430726320` success，custom Docker run `26430726334` success；future Regression run `26430735616` success，future Docker run `26430735610` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 与 `ghcr.io/zhizhishu/halowebui:slim` 均成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交了稳定模型继承相关代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 复核并修复旧聊天恢复时工作区模型默认工具丢失的问题~~ (创建于: 2026-05-25 21:09:29 -07:00 | **完成于: 2026-05-25 21:42:06 -07:00**)
  - 范围: 六条线中的工具/技能状态与新旧聊天发送状态；对照上游 `open-webui#24677`。
  - 现象: 工作区模型带默认 tools，新聊天选择模型时默认工具会出现；切回该模型的旧聊天后默认工具不再选中。
  - 复现依据: 旧聊天若保存了 `composer_state.selected_tool_ids=[]` 且 `tool_selection_touched=false`，此前 `Chat.svelte` 会因为存在整体 `composer_state` 而阻止模型默认 `meta.toolIds` 回填，导致旧聊天工具默认值丢失。
  - 修复结果: 已提交 `88096b7 Restore model default tools for old chats`。聊天恢复现在区分整体 composer state 与真正有效的工具/技能选择状态；空且未触碰的旧工具/技能选择不会挡住模型默认工具/技能回填，非空选择或用户显式清空仍会保留。
  - 影响文件: `src/lib/components/chat/Chat.svelte`、`src/lib/utils/composer-selection-state.ts`、`src/lib/utils/composer-selection-state.test.ts`。
  - 验证结果: 前端定点 `14 passed`；前端六线目标组合 `8 files / 41 tests passed`；后端工具/MCP/继承边界 `30 passed, 3 warnings`；`git diff --check` 通过；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功。
  - 远端结果: 已推送到 `origin/custom` 与 `origin/future`；custom run `26432378643/26432378642` success，future run `26432378654/26432378701` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`；`slim` 标签也可解析 amd64/arm64。
  - 工作区说明: Git 只提交了上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
- [x] ~~**目标:** 修复技能 `$` 单独发送后请求消息为空的问题~~ (创建于: 2026-05-25 21:54:07 -07:00 | **完成于: 2026-05-25 22:06:34 -07:00**)
  - 范围: 六条线中的工具技能状态与新旧聊天发送状态；对照上游 `open-webui#24929`。
  - 预期: 用户只选择技能但未输入额外文本时，请求发往模型的最后一条 user message 不再是空字符串；有真实文本、图片/文件消息和普通消息不受影响。
  - 验证计划: 补前端定点单测，运行技能/工具/聊天状态相关 vitest；必要时运行生产构建；确有修复后提交并推送 `origin/custom` 与 `origin/future`。
  - 复现依据: `Chat.svelte` 构造请求时会剥掉 `<$skillId|label>`，此前 skill-only user message 会变成 `content: ""`，触发 Bedrock 等 provider 的空文本校验错误。
  - 修复结果: 技能标签提取与清洗迁入 `skill-selection.ts`；user message 若原文包含技能标签且剥离后为空，会在模型请求中使用 `.` 作为最小非空文本；普通空消息不加占位，图片消息不再附带空 text block。
  - 影响文件: `src/lib/components/chat/Chat.svelte`、`src/lib/utils/skill-selection.ts`、`src/lib/utils/skill-selection.test.ts`。
  - 验证结果: 定点前端回归 `3 files / 19 tests passed`；前端六线目标组合 `10 files / 61 tests passed`；后端 skill/tool/MCP 相关回归 `25 passed, 1 warning`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 工作区说明: 计划只提交上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，不提交。
- [x] ~~**目标:** 修复停止工具调用后重发导致 tool call/result 不匹配的问题~~ (创建于: 2026-05-25 22:26:10 -07:00 | **完成于: 2026-05-25 22:59:01 -07:00**)
  - 范围: 六条线中的工具技能状态、新旧聊天发送状态，以及 MCP/OpenAPI 工具链稳定性；对照上游 `open-webui#24940`。
  - 现象: 用户在工具调用执行中点击停止后，重发同一消息会触发 provider 侧 `invalid params, tool call and result not match (2013)` 或 `tool call result does not follow tool call`。
  - 计划: 先定位聊天历史转换、停止生成状态落盘和请求 payload 组装链路；只在确认存在真实不一致时做最小修复；补定点回归后运行六线相关测试。确有修复才提交并推送 `origin/custom` 与 `origin/future`。
  - 复现依据: 停止生成时可能落下 assistant `tool_calls`，但没有紧随其后的 matching `role: tool` 结果；重发时 OpenAI-compatible provider 会拒绝这种半截工具调用历史。
  - 修复结果: 已提交 `ec65a9b Sanitize incomplete tool call history`。在 OpenAI 出口 payload 组装后净化不完整工具调用消息组；完整 `assistant tool_calls + tool result` 保留，缺失结果的工具调用会被丢弃或仅保留可见 assistant 文本，孤立/重复的 tool result 会被过滤。
  - 影响文件: `backend/open_webui/utils/payload.py`、`backend/open_webui/routers/openai.py`、`backend/open_webui/test/unit/test_payload_tool_call_sanitization.py`。
  - 验证结果: 后端定点 `34 passed, 1 warning`；此前六线后端组合 `118 passed, 6 warnings`、前端六线组合 `16 files / 79 tests passed`；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `ec65a9b`；custom/future 的 `Custom Regression Guard` 与 Docker workflow 全部 success；`ghcr.io/zhizhishu/halowebui:custom` 与 `:slim` 均可解析 `linux/amd64` 和 `linux/arm64` manifest。
  - 工作区说明: Git 只提交上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，不提交。
- [x] ~~**目标:** 修复联网搜索有结果但正文加载失败后没有 sources 注入的问题~~ (创建于: 2026-05-25 23:54:15 -07:00 | **完成于: 2026-05-25 23:54:15 -07:00**)
  - 范围: 六条线中的原生联网提示；对照上游 `open-webui#25038` 的 “SearXNG 有结果但 No sources / JSONResponse error” 现象。
  - 复现依据: 当前代码已用 `_get_generation_response_content()` 避开 `JSONResponse` 下标错误，但当搜索引擎返回 URL 后网页加载器返回空 docs 时，`process_web_search()` 会返回空 `collection_names/docs`，聊天侧无法注入任何 source。
  - 修复结果: 网页加载器无正文时回退为搜索结果摘要 direct docs；若无可用摘要则保留 URL 并报告失败数量。Grok 搜索乱码修复改为优先尝试 `cp1252 -> utf-8`，覆盖 `æœˆ/æ—¥` 这类真实乱码。
  - 影响文件: `backend/open_webui/routers/retrieval.py`、`backend/open_webui/retrieval/web/grok.py`、`backend/open_webui/test/unit/test_retrieval_web_results.py`、`backend/open_webui/test/unit/test_auto_web_search_decision.py`。
  - 验证结果: 联网相关后端回归 `42 passed, 6 warnings`；后端六线组合回归 `112 passed, 6 warnings`；`git diff --check` 通过，仅 Windows LF/CRLF 提示。
  - 远端结果: 已提交 `3514db5 Fallback to search snippets when web loading fails` 并推送到 `origin/custom` 与 `origin/future`；custom/future 的 `Custom Regression Guard` 和 Docker workflow 全部 success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 与 `:slim` 均成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交上述四个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，不提交。
- [x] ~~**目标:** 修复 outlet/replace 事件在首条流式助手消息 UI 中被旧引用覆盖的问题~~ (创建于: 2026-05-26 00:29:27 -07:00 | **完成于: 2026-05-26 00:54:39 -07:00**)
  - 范围: 六条线中的“新旧聊天发送状态 / 工具技能状态”；对照上游 `open-webui#24852`。
  - 复现依据: `chatEventHandler` 处理 `chat:completion` 时先把旧 `message` 引用传入异步完成处理；`chatCompletedHandler` / outlet / replace 可能已经更新 `history.messages[id]`，但外层返回后又把旧 `message` 写回，导致当前 UI 显示旧流式内容，刷新后才看到后端已持久化的替换内容。
  - 筛选结论: 本轮只处理与本仓库六条主线相关的问题；`open-webui#24852` 命中“新旧聊天发送状态 / 工具技能状态”，其它泛化 issue 不纳入本轮。
  - 修复结果: `chat:completion` 异步完成后重新从 `history.messages[event.message_id]` 取最新消息，避免 outlet/replace/filter 更新被旧引用覆盖；保存完成态时改用当前 `history` 重新生成消息列表，避免保存旧 `messages` 快照。
  - 影响文件: `src/lib/components/chat/Chat.svelte`、`src/lib/utils/chat-event-state.ts`、`src/lib/utils/chat-event-state.test.ts`。
  - 验证结果: 前端六线相关回归 `11 files / 62 tests passed`；后端六线相关子集 `64 passed, 3 warnings`；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 远端结果: 已提交 `70189ee Fix outlet replacements after chat completion` 并推送到 `origin/custom` 与 `origin/future`；custom run `26439807724/26439807676` success，future run `26439819522/26439819551` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 与 `:slim` 均成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。

## 收口决定（2026-05-26）
- 当前六条线工作已收口完成：接口配置、模型继承、MCP 继承、工具技能状态、新旧聊天发送状态、原生联网提示。
- 后续不再主动泛扫或扩大 GitHub issue 池；除非用户点名、服务器真实复现、上游同步冲突、Actions/GHCR 发布失败，否则不再围绕这六条线继续找事。
- “镜像门禁”只作为发布确认：代码已推到 `origin/custom` / `origin/future` 后，GitHub 回归和 Docker 镜像构建都成功，且 GHCR 镜像 manifest 可读并包含 `linux/amd64` / `linux/arm64`，才建议服务器拉新镜像。
- 当前完成基线：`custom` / `origin/custom` / `origin/future` = `32c4d11 Fix active chat model recovery`。
- 本地说明：`TASK_LOG.md` 与 `AGENTS.md` 继续只作为本机接力文件，不提交到 Git。

## 迭代（2026-05-26 项目习惯文件整理）
- 范围：重读全局 `AGENTS.md`，按当前项目长期维护习惯补齐缺失的项目边界和理解文件；不移动、不整理父级文件夹。
- 已完成：
  - 新增 `PROJECT_ID.md`：锁定真实项目根目录、读写边界、Serena/ACE 范围，并声明当前继续使用旧式 `TASK_LOG.md`。
  - 新增 `PROJECT_CONTEXT.md`：记录项目用途、技术栈、重要目录、验证方式、长期约定和已知坑点。
  - 新增 `PROJECT_MAP.md`：记录接口配置、模型/MCP 继承、工具/技能、聊天状态、联网搜索等常用找路入口。
- 未做：
  - 未创建 `TASK.md` / `LOG.md`，因为项目 `AGENTS.md` 已约定继续使用 `TASK_LOG.md`；除非用户明确要求迁移，否则不拆。
  - 未提交 Git；新增项目习惯文件目前和 `AGENTS.md` / `TASK_LOG.md` 一样作为本地接力文件。
- 上一轮遗留判定：
  - 六条线代码修复本身已完成并推送。
  - 是否在服务器拉取 `32c4d11` 镜像并重建容器，仍取决于用户部署环境。
  - 是否把这些项目习惯文件纳入 Git，需用户单独拍板。

### 追加（2026-05-26 03:57:50 -07:00）
- 用户已明确允许创建 `TASK.md` / `LOG.md`。
- 已新增 `TASK.md` 作为当前接力入口, 新增 `LOG.md` 作为简短历史记录。
- 已更新 `PROJECT_ID.md` 和本地 `AGENTS.md`, 后续默认使用 `TASK.md` / `LOG.md`; `TASK_LOG.md` 保留为 legacy 长历史。

### 追加（2026-05-26 04:08:00 -07:00）
- 重新读取全局 `AGENTS.md` 后, 修正 `PROJECT_ID.md` 的 `forbidden_paths` 写法: 不再把父级存放目录写成路径级禁止项, 避免和当前项目 allowed path 产生包含关系冲突; 改为 notes 中声明不得写父级或兄弟项目。
- 复核远端同步状态: 当前 `custom` 与 `origin/custom` 同步在 `32c4d11`; 本地 `future` 落后 `origin/future` 12 个提交; 本地 `main` 落后 `origin/main` 3 个提交, 落后 `upstream/main` 4 个提交; `origin/main` 落后 `upstream/main` 1 个提交。
- 当前结论: 业务代码无本地未推送提交; 但有未提交的项目接力文件, 且作者上游已有新提交尚未同步进 `main/custom/future`。

### 追加（2026-05-26 04:30:00 -07:00）
- 已提交项目接力文件 `45f1584 docs: add project handoff files`。
- 已将 `origin/main` 同步到作者最新 `upstream/main=785a055`。
- 已将作者更新合入 `custom`; 冲突只在 `openai.py` 和 `test_model_reasoning_priority.py`, 已保留双方 import 与二创逻辑。
- 本地验证: 后端目标回归 `80 passed`; 上游新增/二创补充回归 `67 passed`; 前端关键 vitest `45 passed`; 生产构建成功。
- [x] ~~**目标:** 修复工具/Filter 输出中的标准 details 折叠块解析过窄问题~~ (创建于: 2026-05-26 01:32:24 -07:00 | **完成于: 2026-05-26 01:46:00 -07:00**)
  - 范围: 六条线中的工具技能状态与新旧聊天发送状态；对照上游 `open-webui#24854` / `#24634` / `#24635`。
  - 复现依据: 当前 `src/lib/utils/marked/extension.ts` 只识别 `<details...>\n` 与 `<summary>...</summary>\n`；新增回归测试确认一行式 `<details><summary>...</summary>...</details>` 会被 marked 当成普通 `html`，带属性 summary 也无法抽出 summary，导致折叠 UI 不出现。
  - 修复结果: 已提交 `13329eb Fix details markdown tokenization`；details tokenizer 现在支持一行式 details、summary 带属性、单/双引号或布尔属性，并保留嵌套 details 的闭合匹配。
  - 影响文件: `src/lib/utils/marked/extension.ts`、`src/lib/utils/marked/extension.test.ts`。
  - 验证结果: 定点 `extension/headings` 回归 `9 passed`；前端六线相关回归 `12 files / 68 tests passed`；`git diff --check` 无空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 工作区说明: Git 只提交上述两个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，不提交。

- [x] ~~**目标:** 修复损坏/循环聊天历史导致旧聊天页面卡死的问题~~ (创建于: 2026-05-26 02:13:06 -07:00 | **完成于: 2026-05-26 02:21:10 -07:00**)
  - 范围: 六条线中的新旧聊天发送状态；对照上游 `open-webui#15189` / `#14806` 的旧聊天 loading 风险。
  - 复现依据: `createMessagesList()` 原先递归追溯 `parentId`，`Messages.svelte` 也手写 while 追溯父链；循环 parent 链会递归爆栈或无限循环，损坏 current/parent 链可能把旧聊天页面卡在 loading/空状态。
  - 修复结果: `createMessagesList()` 改为带 `visited` guard 的迭代路径构建；缺失 current/parent 会安全停止；消息渲染组件复用安全路径并按窗口大小截取，避免旧聊天损坏历史拖死 UI。
  - 影响文件: `src/lib/utils/index.ts`、`src/lib/components/chat/Messages.svelte`、`src/lib/utils/chat-history.test.ts`。
  - 验证结果: 定点聊天历史/响应/事件回归 `3 files / 11 tests passed`；前端六线相关回归 `12 files / 64 tests passed`；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 工作区说明: 本地 `AGENTS.md` 与 `TASK_LOG.md` 仍只作接力文件，不提交。

- [x] ~~**目标:** 修复多回复旧聊天切回后模型下拉恢复到第一条回复模型的问题~~ (创建于: 2026-05-26 02:53:04 -07:00 | **完成于: 2026-05-26 03:23:30 -07:00**)
  - 范围: 六条线中的新旧聊天发送状态与模型继承；对照上游 `open-webui#25052`。
  - 复现依据: 当前 `recoverLoadedChatModelState()` 会优先使用已持久化的 `chatContent.models`；多次 regenerate 后该字段可能仍是第一条回复模型，即使 `history.currentId` 指向当前活跃的最新 assistant 回复。
  - 筛选结论: 只处理与本仓库六条主线相关的问题；`open-webui#25052` 命中“新旧聊天发送状态 / 模型继承”，MCP OAuth、OpenAPI native tools、MCP resource/result 展示等问题当前 fork 未发现同路径风险，本轮排除。
  - 修复结果: 已提交 `32c4d11 Fix active chat model recovery`。旧聊天恢复模型选择时优先沿 `history.currentId` 的活跃父链读取 assistant `modelIdx` 对应模型，避免 stale `chatContent.models` 把下拉框恢复到第一条 regenerate 回复；非活跃模型槽位仍保留持久化选择。
  - 影响文件: `src/lib/components/chat/Chat.svelte`、`src/lib/utils/chat-model-recovery.ts`、`src/lib/utils/chat-model-recovery.test.ts`。
  - 验证结果: 前端六线相关回归 `10 files / 57 tests passed`；`git diff --check` 无实际空白错误，仅 Windows LF/CRLF 提示；`NODE_OPTIONS=--max-old-space-size=4096 npm run build` 生产构建成功并写入 `build`。
  - 远端结果: 已推送 `origin/custom` 与 `origin/future` 到 `32c4d11845a20dbadf793f34d8d68ba8c683cbc0`；custom run `26446194210/26446194204` success，future run `26446201982/26446202067` success。
  - GHCR 状态: `docker manifest inspect ghcr.io/zhizhishu/halowebui:custom` 与 `:slim` 均成功，manifest list 包含 `linux/amd64` 与 `linux/arm64`。
  - 工作区说明: Git 只提交上述三个代码/测试文件；`AGENTS.md` 与 `TASK_LOG.md` 继续作为本地未跟踪接力文件保留，未提交。
