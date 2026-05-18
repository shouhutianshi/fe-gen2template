# 前端需求长任务工作流（迁移版快照）

这是 `tf-tech-spec` 的自带工作流参考，随 skill 一起迁移。目标仓库若有更高优先级的用户指令、仓库指令或团队约定，先遵循那些约定；本文件提供本 skill 的默认门禁和产物格式。

## 硬规则

- 需求没有拆清楚，不进入开发。
- 没有新鲜验证证据，不声明完成、不提交、不合并、不发布。
- 多 agent 可以并行审阅和调查，但同一 worktree 或同一文件所有权不要并行实现。
- TypeScript 检查不要裸跑 `tsc`；进入实际前端工程目录后，优先用项目脚本，例如 `bun run typecheck`。
- 本地验证命令必须尽量与 CI job 一致；不一致时记录原因和风险。
- 审查 skill 名称为 `cr`，命令形态通常为 `/cr`。

## Skill 路由

| 场景 | 使用 skill / 工具 | 产物 / 退出条件 |
| --- | --- | --- |
| 读取帮帮文档 PRD | `kit-zyb-docs` | 导出 markdown，记录原始 URL、`fileId`、导出时间 |
| 架构概览初始化 | `kit-fe-arc` | 生成或更新 `docs/architecture/overview.md` |
| 复杂 PRD 拆模块 | `kit-fe-prd-split` | `docs/architecture/boundaries.md` 和子 PRD 文档 |
| 查询需求关联 Bug | `kit-zyb-pms` | 需求关联未关闭 Bug 列表，按 P0-P4 分类 |
| 本地分支 / MR / 文件审查 | `cr`（命令 `/cr`） | 审查结论、风险等级、自动修复或人工确认记录 |
| 提交与推送 | `/commit` | 自动生成 commit message、暂存、提交并 push |
| 前后端联调 | `yapi` MCP 或目标仓库接口文档 | 确认请求/响应/错误码匹配，记录联调结果 |

`kit-fe-prd-split` 的前置条件是存在架构概览。若 `docs/architecture/overview.md` 不存在，先用 `kit-fe-arc` 生成或在方案中把架构缺失列为阻断项。增量需求还应有 `docs/architecture/boundaries.md`；没有模块地图时，先按全新需求模式生成模块地图。

## 路径分流

| 判定维度 | 快速路径 | 完整路径 |
| --- | --- | --- |
| 变更文件数 | <= 10 个文件 | > 10 个文件或涉及多模块 |
| 涉及模块数 | 单模块 | 2+ 模块 |
| 需求类型 | bugfix / hotfix / chore / 小功能 | feat / 重构 / 多人协作 |
| 预估 agent 数 | 1 个 | 2+ 个 |

快速路径：计划 -> 实现 -> 验证 -> `cr` 审查 -> `/commit`。

完整路径：PRD 获取 -> 架构/模块拆解 -> 技术方案 -> 实施计划 -> worktree 准备 -> 分任务实现 -> 集成验证 -> 联调 -> `cr` 审查 -> `/commit` -> CI/部署 -> 冒烟 -> PMS Bug 闭环 -> 收尾。

## 阶段门禁

| 阶段 | 进入条件 | 必做动作 | 退出条件 | 失败处理 |
| --- | --- | --- | --- | --- |
| 需求准入 | 有 PRD / Story / Bug 来源 | 导出或记录需求来源、ID、验收标准 | 输入资料可追溯 | 缺权限则停下说明 |
| 需求拆解 | 有 PRD 和架构概览 | 拆模块、契约、公共能力 | 模块地图和子需求清楚 | 架构缺失则先补架构 |
| 技术方案 | 模块边界基本清楚 | 用 `tf-tech-spec` 生成前端方案 | 接口、状态、权限、验证、风险可追踪 | 未知项进待确认表，阻断项不进入开发 |
| 计划固化 | 技术方案可执行 | 写任务计划和验证命令 | 每个任务有文件、步骤、验证 | 计划有歧义则先修计划 |
| 工作区准备 | 计划已批准 | 检测或创建 worktree | 记录 branch、worktree、base sha、owner、allowed files、baseline verification | baseline 失败先判断历史问题还是阻断 |
| 任务执行 | worktree 可用 | 按文件所有权实现、自测、评审 | 每个任务 verified | BLOCKED 时补上下文、拆任务或人工决策 |
| 集成验证 | 子任务均 verified | 串行合并 / rebase，跑相关和全量验证 | 本地全量验证通过 | 失败用系统化排障定位 |
| 前后端联调 | 本地验证通过 | 查接口文档，确认请求/响应/错误码 | 接口契约一致 | 不匹配则改代码或推动接口文档更新 |
| 审查提交 | 联调通过 | 用 `cr` 审查，再 `/commit` | 审查问题关闭，提交范围明确 | 高风险变更需人工确认 |
| CI / 部署 | 已 push 或 MR 创建 | 查看 pipeline，部署目标环境 | CI 全绿，部署 commit 匹配 | CI/部署失败停下定位 |
| 冒烟 / PMS | 部署完成 | 浏览器冒烟，查需求关联 Bug | 核心路径通过，P0-P2 无阻断 | 修 Bug 后回到验证和提交 |
| 收尾 | 发布闭环完成 | 选择合并、MR、保留或清理 | 分支、MR、worktree 状态清楚 | 丢弃必须明确确认 |

## 状态文件

长任务建议创建 `docs/tasks/<需求ID或名称>/status.md`：

```markdown
# <需求名> 状态

**需求 ID:** <PMS Story ID>
**PRD:** <帮帮文档 URL / fileId>
**主分支:** <main / master / release/...>
**集成分支:** <type>/{{USERNAME}}/<feature>
**Base SHA:** <git rev-parse HEAD>
**当前阶段:** <阶段名>
**最后一次通过验证:** <命令 + 时间 + 摘要>
**阻断项:** <无 / 列表>

## 任务状态

| 任务 | Agent / Owner | Worktree | 文件所有权 | 状态 | 最新提交 | 验证证据 |
| --- | --- | --- | --- | --- | --- | --- |

## 决策记录

| 时间 | 决策 | 原因 | 影响 |
| --- | --- | --- | --- |
```

状态枚举：`TODO`、`IN_PROGRESS`、`DONE_WITH_CONCERNS`、`NEEDS_CONTEXT`、`BLOCKED`、`REVIEWING`、`VERIFIED`。

恢复任务时先执行：

```bash
git status --short
git branch --show-current
git log --oneline -10
```

## 多 Agent 原则

可以并行：
- 不同业务模块，文件所有权不重叠。
- 不同测试失败域，根因互不依赖。
- 文档审查、风险审查、测试命令发现等只读任务。

不能并行：
- 同一个文件集合的实现。
- 同一个公共 API 的不同方向修改。
- 数据结构、路由、store、构建配置等共享契约未稳定时的多方改动。
- 多个 worktree 同时 merge 到集成分支。

文件所有权矩阵：

| 模块 / 任务 | Worktree | Owner | 允许修改 | 禁止修改 | 集成顺序 |
| --- | --- | --- | --- | --- | --- |

所有审查统一用 `cr`（命令 `/cr`）：每个 Implementer 完成后由 Controller 用 `cr` 审查，多模块合并后再用 `cr` 做集成审查。

## 分支与 Worktree

默认分支命名：`<type>/{{USERNAME}}/<name>`。

常用 `type`：`feat`、`bugfix`、`hotfix`、`refactor`、`docs`、`chore`。

创建分支前必须确认最终分支名符合 `<type>/{{USERNAME}}/<name>`。`name` 建议使用需求 ID、Bug ID 或英文 kebab-case 摘要。

创建 worktree 前检测是否已经在 linked worktree：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null
git branch --show-current
git status --short
```

合并规则：
- 由集成 owner 串行合并，不允许多个 agent 同时合并。
- 合并前更新 base，检查冲突风险。
- 每合并一个模块跑相关最小验证；全部合并后跑全量验证。
- 冲突解决后必须重新跑受影响验证，不能复用冲突前结果。

## 本地验证与 CI 对齐

进入实际前端工程目录后先发现脚本：

```bash
pwd
ls
test -f package.json && bun pm pkg get scripts
test -f package.json && cat package.json
find . -maxdepth 4 -type f \( \
  -name '.gitlab-ci.yml' -o \
  -name 'vite.config.*' -o \
  -name 'tsconfig*.json' -o \
  -name 'eslint.config.*' \
\)
```

验证矩阵：

| 验证项 | 命令来源 | 推荐命令形态 | 通过标准 |
| --- | --- | --- | --- |
| 依赖安装 | 锁文件 / CI | `bun install --frozen-lockfile` 或项目等价命令 | 无错误退出 |
| Lint | `package.json scripts` | `bun run lint` | 0 error |
| Typecheck | `package.json scripts` | `bun run typecheck` | 0 error；不要裸跑 `tsc` |
| Unit / Component Test | `package.json scripts` | `bun run test` | 0 failed |
| Build | `package.json scripts` | `bun run build` | 构建成功，产物生成 |
| Preview / Smoke | Vite / 项目脚本 | `bun run preview` 或项目等价命令 | 核心页面可访问，无阻断错误 |

如果脚本名不同，以 `package.json` 为准。没有脚本时，不能臆造命令；记录"未发现脚本"，并补充项目约定或向负责人确认。

完成声明前必须有本轮新鲜验证证据。若只跑了部分验证，结论只能说"已通过 X，Y 未验证"，不能扩大结论。

## 审查、提交与 Push

提交前流程：

1. 用 `git status --short` 和 `git diff` 确认变更范围。
2. 用 `cr`（命令 `/cr`）审查本地分支、MR、提交或文件。
3. Critical 和 Important 问题必须修复或给出技术反驳；高风险变更需要人工确认。
4. 根据审查意见改代码后，重新跑 `cr` 或记录最终审查的 base/head SHA，确保最终 diff 已审。
5. 重新运行相关验证。
6. 用 `/commit` 提交并 push。禁止直接 push 到 protected `main` / `master` 分支；禁止 `--force`，必须强推时只能人工确认后使用 `--force-with-lease`。
7. 创建或更新 MR，确认 target branch、reviewer、关联 Story/Bug。
8. 记录远程分支、MR、pipeline 链接。

高风险变更包括公共 API 或数据格式、路由、权限、登录态、支付、埋点、实验分流、构建配置和部署策略变更。

## 完成检查清单

- [ ] PRD / Story / Bug 来源可追溯。
- [ ] 模块边界、共享契约和文件所有权清楚。
- [ ] 本地验证命令来自项目脚本或 CI。
- [ ] 关键验证有新鲜证据。
- [ ] `cr` 审查完成，Critical / Important 问题已关闭或有技术反驳。
- [ ] CI、部署、冒烟、PMS Bug 闭环状态已记录。
- [ ] 未泄露凭据、Cookie、Token、内部敏感链接或未脱敏截图。
