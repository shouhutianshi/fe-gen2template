# CLAUDE.md

本文件是 Claude Code 在本仓库工作的项目级指令。直接用户指令优先于本文件；本文件优先于通用默认行为。

## 行为准则

- 偏向谨慎而非速度，简单任务自行判断。
- 先思考再编码 — 不假设，不掩饰困惑。多种解释列出来，更简单的方法说出来，不清楚就问。
- 简洁优先 — 不添加未要求的功能/抽象/灵活性，不为不可能的场景做错误处理。
- 精准修改 — 只动必须动的代码。不"改进"相邻代码，不重构没坏的东西，匹配现有风格。
- 目标驱动 — 任务转化为可验证目标，定义成功标准后循环验证。

## 技术栈

Vite、TypeScript、Vue 3、ES6、{{UI_LIBRARY}}。实际命令以目标工程的 `package.json` 和 CI 配置为准，不硬编码命令。

## 核心工具

| 用途 | 工具 |
| --- | --- |
| 架构概览 | `kit-fe-arc` |
| 技术方案与需求拆解 | `kit-fe-prd-split` + `tf-tech-spec`（条件路由） |
| 代码审查 | `cr`（命令 `/cr`） |
| Bug 查询 | `kit-zyb-pms` |
| 提交推送 | `/commit` |
| 前后端联调 | `yapi` MCP |
| CI/CD | `/internal-gitlab` skill、`inf-autodeploy` MCP |
| 本地验证 | `Browser`（Codex）或 `Chrome`（Claude Code），按环境自动选择 |

## 规范渐进加载

**执行任何代码修改前，第一步是判断需要读取哪些规范文件。** 读取后严格遵守其中的规则，不要凭印象编写代码。读取时向用户输出提示（如"正在读取组件规范..."）。

| 即将执行 | 先读取 |
| --- | --- |
| 创建/修改 .vue 组件 | `docs/conventions/components.md` |
| 创建/修改 Pinia Store | `docs/conventions/components.md`（composable 章节） |
| 编写样式 | `docs/conventions/styles.md` |
| 编写测试 | `docs/conventions/testing.md` |
| 对接/新增 API | `docs/conventions/api-integration.md` |
| 配置路由/路由守卫 | `docs/conventions/components.md`（composable 章节） |
| 修改环境变量/构建配置 | `docs/conventions/verification.md` |
| 代码审查 | `docs/conventions/code-review.md` |
| 创建分支/提交 | `docs/conventions/git.md` |
| 复杂需求（>10 文件 / 多模块 / 多 agent） | `docs/workflow.md` |
| 提交前验证 | `docs/conventions/verification.md` |
| 并行开发 | `docs/conventions/parallel-development.md` |
| 生成验收用例 | `docs/conventions/acceptance-case-generation.md` |

每个文件只需在本次会话中首次涉及时读取一次。长会话中若不确定规则，重新读取对应规范。

## 路径分流

开始任务前判断规模，选择执行路径：

| 维度 | 快速路径 | 完整路径 |
| --- | --- | --- |
| 变更文件数 | ≤ 10 | > 10 或涉及多模块 |
| 涉及模块 | 单模块 | 2+ 模块 |
| 需求类型 | bugfix / hotfix / chore / 小功能 | feat / 重构 / 多人协作 |
| agent 数 | 1 | 2+ |

- **快速路径**（4 步）：计划 → 实现 → 验证 → 提交。
- **完整路径**：读取 `docs/workflow.md` 后按流程执行。

## 验证门禁

任何"完成""通过""可以发布"的声明前，必须有**本轮新鲜验证证据**：

| 验证项 | 命令 | 通过标准 |
| --- | --- | --- |
| Lint | `bun run lint` | 0 error |
| Typecheck | `bun run typecheck` | 0 error（不裸跑 `tsc`） |
| Test | `bun run test` | 0 failed |
| Coverage | `bun run test:coverage` | ≥70% statements |
| Build | `bun run build` | 构建成功 |
| E2E（可选） | `bun run test:e2e` | 关键流程全部通过 |

只跑了部分验证时，只能说"已通过 X，Y 未验证"，不能扩大结论。

## 分支与提交

- 分支命名：`<type>/<name>`，详细规则见 `docs/conventions/git.md`。
- 提交用 `/commit`，审查用 `cr`（命令 `/cr`）。

## 高风险变更（提交前必须人工确认）

- 公共 API 或数据格式变更
- 路由、权限、登录态、支付、埋点、实验分流变更
- 构建配置、部署配置、依赖版本变更
- 测试基线更新或快照大规模变化
- 多模块共享状态、store、缓存、全局样式变更

## 工作方式

- 开始前先确认任务目标、约束和验收标准；信息不足且会影响方案时，先问清楚。
- 修改前先阅读相关代码、文档和最近上下文，优先沿用现有结构、命名、技术栈和工具链。
- 不扩大任务范围；不要把临近代码的风格问题、历史债务或无关重构带入当前变更。

## 插件版本

本项目由 fe-gen2template v{{SCAFFOLD_VERSION}} 生成。如需同步最新 Skill/规范，执行 `/scaffold-sync`（插件级命令，任意项目可用）。
