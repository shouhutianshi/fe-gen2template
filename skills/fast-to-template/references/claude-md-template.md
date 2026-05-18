# CLAUDE.md

本文件是 Claude Code 在本仓库工作的项目级指令。直接用户指令优先于本文件；本文件优先于通用默认行为。涉及长任务、PRD、审查、部署或 Bug 闭环时，同时遵循 `docs/workflow.md`。

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
| PRD 读取 | `kit-zyb-docs` |
| 架构概览 | `kit-fe-arc` |
| PRD 拆模块 | `kit-fe-prd-split` |
| 技术方案 | `tf-tech-spec` |
| 代码审查 | `cr`（命令 `/cr`） |
| Bug 查询 | `kit-zyb-pms` |
| 提交推送 | `/commit` |
| 前后端联调 | `yapi` MCP |
| CI/CD | `/internal-gitlab` skill、`inf-autodeploy` MCP |
| 本地验证 | `Browser`（Codex）或 `Chrome`（Claude Code），按环境自动选择 |

## 工作方式

- 开始前先确认任务目标、约束和验收标准；信息不足且会影响方案时，先问清楚。
- 修改前先阅读相关代码、文档和最近上下文，优先沿用现有结构、命名、技术栈和工具链。
- 不扩大任务范围；不要把临近代码的风格问题、历史债务或无关重构带入当前变更。
- 需求规模判断：单模块 / ≤10 文件 → 快速路径（计划→实现→验证→提交）；多模块 / 多 agent → 完整路径（见 `docs/workflow.md`）。

## 验证要求

- 完成声明前必须有新鲜验证证据；没有运行验证就明确说明原因和风险。
- 优先运行与变更范围匹配的最小验证，再按风险扩展到 lint、typecheck、test、build、浏览器冒烟。
- TypeScript 检查不要裸跑 `tsc`；优先使用项目脚本，如 `bun run typecheck`。

## Git 与协作

- 工作区可能已有用户改动；不得回退、覆盖或格式化与当前任务无关的内容。
- 分支命名：`<type>/{{USERNAME}}/<name>`，type 为 feat / bugfix / hotfix / refactor / docs / chore。
- 提交用 `/commit`，审查用 `cr`（命令 `/cr`）。
- 禁止直接 push 到 protected 分支；禁止 `--force`，必须强推时用 `--force-with-lease` 且人工确认。
- 长任务、并行 agent、PRD 拆解、代码审查、CI 修复和发布流程按 `docs/workflow.md` 执行。

## 插件版本

本项目由 fe-influencers v{{SCAFFOLD_VERSION}} 生成。如需同步最新 Skill，执行 /scaffold-sync 或手动从插件目录复制。
