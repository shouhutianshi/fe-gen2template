# 技术方案自检清单

交付方案前逐项检查。每项对应本目录 `conventions/` 下的具体文档，检查时先读对应文档再逐条核对。

## 需求追踪

- PRD/Story/Bug 每个本期需求都能追踪到模块、路由/入口、接口、用例和验收标准。
- 主接口索引、功能拆解、数据模型、状态流转中的字段、枚举、路径无冲突。
- 待确认项都有 owner、影响和推荐处理；阻断项未关闭时不声明方案可进入开发。

## 组件与文件约定

> 参照 `conventions/components.md`

- 组件文件名使用 `kebab-case`（如 `user-avatar.vue`），import 使用 `PascalCase`（如 `import UserAvatar from './user-avatar.vue'`）。
- 通用组件放 `src/components/`，页面私有组件放 `views/<Page>/components/`，不得在 views 外创建仅单页使用的组件。
- 组件层级清晰：通用组件（零业务逻辑）→ 业务组件（仅当前页面）→ 页面组件（组合层）。
- 子组件通过 props 接收数据、emit 通信，不通过 ref 直接操作子组件（除 `defineExpose` 暴露的方法外）。
- 单文件超 200 行需拆分；同一区块超 30 行提取子组件。
- 始终使用 `<script setup lang="ts">` 和 `<style scoped>`。
- Props 必须定义 TypeScript 接口，不用运行时声明；可选 prop 必须提供默认值。

## 样式约定

> 参照 `conventions/styles.md`

- 颜色、间距使用设计令牌（`@theme` 定义的 `--spacing-*`、`--color-*` 变量），无硬编码 hex/rgb。
- 零 inline style（`style="..."` 和 `:style="{}"`）。
- 重复 ≥3 次的 utility 组合提取为 `@apply` 语义 class。
- 无 `!important`（除非硬规则允许）。

## API 与联调约定

> 参照 `conventions/api-integration.md`

- API 函数放在 `src/api/modules/` 下按模块拆分，使用 `src/api/request.ts` 导出的实例。
- 响应类型集中在 `src/api/types.ts` + re-export，本方案不新增 `any`/`as`/`@ts-ignore`。
- 每个写操作都有前端校验、版本/并发处理、成功反馈、失败反馈和重复提交保护。
- 网络错误、超时、401 由拦截器统一处理；业务错误在调用处 try-catch。

## 页面还原约定

> 参照 `conventions/acceptance-case-generation.md` 页面还原验收要求

- 每个页面的布局区块（筛选栏、统计卡、操作栏、列表、分页）与设计稿一一对应。
- 交互状态完整：按钮有 disabled/loading 态，表格有 loading/空状态/错误态，表单有校验错误提示，弹窗有关闭确认。
- 数据状态完整：空状态有插图+引导文案，加载态有骨架屏/Spin，错误态有 el-message 通知，不得静默失败。
- 组件库映射正确：PC 用 Element Plus，H5 用 Vant 4，不混用。
- 验收用例包含页面还原用例（layer=component）。

## 状态与性能

- 每个列表都有 loading、empty、error、分页、筛选重置、**竞态保护（latestFetchId 或 AbortController）**和 URL 同步策略。
- 列表数据响应式选型已声明（`ref` vs `shallowRef`），深层代理开销已评估。
- 弹窗、剪贴板、文件下载遵守项目硬规则，未使用废弃 API。
- URL query 参数读取处有枚举校验和白名单，防穿透。
- 大依赖声明按需加载或动态 import 策略。
- 请求层显式说明重试闭包、并发取消、错误重试上限等隐性陷阱的处理方式。
- 构建拆包策略已声明（manualChunks / 组件库独立 chunk / vendor 拆分）。

## 测试约定

> 参照 `conventions/testing.md`

- 测试分层正确：单元（Vitest）/ 组件（@vue/test-utils）/ 集成 / E2E（Playwright）/ 手工验收。
- 测试文件 `*.test.ts` 与被测文件同目录；集成测试 `*.integration.test.ts`。
- 覆盖率阈值：statements ≥70%、branches ≥60%、functions ≥70%、lines ≥70%。
- 不测第三方组件内部行为、CSS class 组合效果或框架响应式系统本身。

## 验证约定

> 参照 `conventions/verification.md`

- 六级验证阶梯已制定：lint → typecheck → test → coverage → build → smoke。
- 每级验证有明确的通过标准（0 error / 0 failed / ≥70% coverage / 构建成功）。
- 验证命令来自 `package.json` 或 CI 配置，不裸跑 `tsc`，不硬编码命令。
- 只跑了部分验证时，结论只能说"已通过 X，Y 未验证"，不扩大。

## 代码审查约定

> 参照 `conventions/code-review.md`

- 方案提交前需用 `/cr` 审查，A 级问题（正确性与安全性）必须关闭或有技术反驳。
- B 级问题（列表渲染 key、副作用依赖、大依赖按需导入、重复逻辑）建议通过。
- 不审查第三方库内部行为、基于假设的未来需求。

## 分支与提交约定

> 参照 `conventions/git.md`

- 分支命名 `<type>/<name>`，name 使用需求 ID 或英文 kebab-case 摘要。
- 提交使用 `/commit`，格式 `<type>: <中文描述>`。
- 禁止直接 push 到 `main`/`master`；禁止 `--force`。

## 并行开发约定（条件性）

> 参照 `conventions/parallel-development.md`，仅在方案涉及多 agent 协作时检查。

- 各模块文件所有权不重叠，共享契约已冻结。
- 同一文件集合、同一公共 API、共享契约未稳定时不得并行实现。

## UI 规格编造风险检查（条件性）

> 仅在方案包含「UI 规格详表」时检查。复杂需求（多模块 / 组件 >10 个）必须检查。

- 无硬编码字号值（`font-size: 14px`）；字号只使用 @theme 令牌引用（如 `text-sm`）或标注「待确认」。
- 无硬编码色值（`color: #333`、`rgb()`、`rgba()`）；字色只使用 @theme 令牌引用（如 `text-gray-700`）或标注「待确认」。
- CSS class 来自设计令牌、Tailwind utility 或组件库标准用法；不编造不存在的 class。
- 非标准布局（非典型上下/左右流式布局）有设计稿参照或已标记为「待确认」。
- 组件关系（父子/兄弟）与功能拆解章节一致，无矛盾。

## 工程与安全

- 权限矩阵覆盖路由、按钮、接口错误态和无权限降级表现。
- 每项改动都有影响面、验证、回滚；不附带未声明的功能改动或无关重构。
- 埋点、错误上报、性能、兼容、i18n、灰度、回滚未涉及时明确写"本章不涉及"。
- 验证矩阵命令来自实际项目脚本或约定文档；不存在脚本时已记录风险。
- **lint/test baseline 已评估**：方案开始前的 error 数已记录，本方案不引入新 error，顺手修复项明确。
- 未泄露凭据、Cookie、Token、未脱敏内部链接或敏感截图内容。
