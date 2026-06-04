#!/usr/bin/env bash
# 用法: bash generate-template.sh <目标文件路径> <项目名称>
# 生成完整的技术方案模板到指定路径。模型只需读取需要填写的章节。
set -euo pipefail

TARGET="${1:?用法: generate-template.sh <目标路径> <项目名>}"
PROJECT="${2:-project}"

mkdir -p "$(dirname "$TARGET")"

cat > "$TARGET" << 'TEMPLATE'
# 前端技术方案模板

生成技术方案时按本模板组织。章节标题使用 `##` 作为顶级标题；不适用章节保留标题并写"本章不涉及"。

## 〇、背景、目标、边界与验收口径

### 需求来源

| 来源 | 标识 | 读取时间 | 关键结论 |
| --- | --- | --- | --- |

### 背景与现状

- 当前业务/系统现状：
- 本次要解决的问题：
- 现有代码或架构约束：

### 现状基线

> 生成方式：按 SKILL.md「工程基线扫描清单」对仓库执行 grep，结果填入下表。每个方案都必填，让本方案 awareness 现有工程基本面。

| 扫描项 | 发现位置 | 严重度 | 本方案是否触及 | 本方案处理 | 遗留 | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 弹窗历史 API（ElMessageBox / Teleport / alert / confirm） |  |  |  |  |  |  |
| 剪贴板废弃 API（document.execCommand） |  |  |  |  |  |  |
| 类型分散定义（同语义响应类型在多处） |  |  |  |  |  |  |
| any / as / @ts-ignore 滥用 |  |  |  |  |  |  |
| 重复工具函数 |  |  |  |  |  |  |
| 列表 ref 误用（应用 shallowRef） |  |  |  |  |  |  |
| URL query 未校验 |  |  |  |  |  |  |
| 硬编码颜色 |  |  |  |  |  |  |
| !important 滥用 |  |  |  |  |  |  |
| 组件库全量导入 |  |  |  |  |  |  |
| 大依赖静态导入 |  |  |  |  |  |  |
| 请求重试闭包共享 |  |  |  |  |  |  |
| 列表竞态保护缺失 |  |  |  |  |  |  |
| lint baseline | error 数：__ |  |  |  |  |  |
| test baseline | failed 数：__ |  |  |  |  |  |

### 目标与非目标

| 类型 | 内容 | 验收/说明 |
| --- | --- | --- |
| 目标 |  |  |
| 非目标 |  |  |

范围不扩大：列出本期不修复的债务、不重构的模块、不附带的功能改动。

### 成功标准

列出 3-6 条可验证的前端交付标准。

### 术语约定

| 术语 | 定义 | 来源 |
| --- | --- | --- |

### 假设与待确认项

| ID | 问题 | 来源/冲突 | 影响 | 推荐处理 | Owner | 状态 |
| --- | --- | --- | --- | --- | --- | --- |

## 一、页面总览

### 页面清单

| 页面 | 端 | 路由/入口 | 实现方式 | 验收要点 |
| --- | --- | --- | --- | --- |

### 全局前端约定

- 全局鉴权：
- 页面切换和筛选状态策略：
- 全局 loading / 骨架屏策略：
- 全局异常处理：
- 兼容范围和降级策略：

### 页面还原约定

> 参照 `docs/conventions/acceptance-case-generation.md` 页面还原验收要求。每个页面必须覆盖以下还原点。

#### 布局结构

| 页面 | 区块划分（筛选栏/统计卡/操作栏/列表/分页） | 响应式断点 | 设计稿参照 |
| --- | --- | --- | --- |

#### 交互状态覆盖

| 元素 | 默认 | hover | disabled | loading | 错误态 | 空态 |
| --- | --- | --- | --- | --- | --- | --- |
| 按钮 |  |  |  |  | — | — |
| 表格 |  | — | — |  |  |  |
| 表单 |  | — |  | — |  | — |
| 弹窗 | — | — | — |  | — | — |
| 分页 |  | — |  | — | — | — |

#### 数据状态

| 页面 | loading 态 | 空状态 | 错误态 | 组件库 |
| --- | --- | --- | --- | --- |
|  | 骨架屏/Spin | 插图+引导文案 | el-message 通知 | PC=Element Plus / H5=Vant 4 |

### UI 规格详表

> 参照 `docs/conventions/styles.md` 的 @theme 设计令牌体系。**禁止**写死像素值（`font-size: 14px`）和色值（`color: #333`），只允许设计令牌引用或语义化描述。无设计稿时，非标准布局必须标记为待确认项。

#### UI 令牌映射表

列出本方案涉及的 @theme 设计令牌与 UI 元素的对应关系。

| 令牌类别 | @theme 令牌名 | Tailwind 用法 | 应用元素 | 数值（仅作参考） |
| --- | --- | --- | --- | --- |
| 字号 | `--font-size-base` | `text-base` | 全局正文 | 16px |
| 字号 | `--font-size-sm` | `text-sm` | 表格单元格、辅助文字 | 14px |
| 字色 | `--color-text-primary` | `text-gray-900` | 标题、主文案 | — |
| 字色 | `--color-text-secondary` | `text-gray-500` | 描述、占位符 | — |
| 间距 | `--spacing-4` | `p-4` / `gap-4` | 卡片内边距 | 16px |
| 圆角 | `--radius-md` | `rounded-md` | 卡片、弹窗 | 6px |

#### 组件规格表

逐页列出组件的规格详情。简单需求（≤10 文件 / 单页）只填必填列，复杂需求全量填写。

| 组件名 | 父组件 | 子组件 | UI 组件库 | 字号令牌 | 字色令牌 | CSS Class | 空间定位 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _必填_ | _必填_ | _选填_ | _必填_ | _选填_ | _选填_ | _选填_ | _必填_ |

列说明：
- **组件名**：Vue 组件文件名（kebab-case），如 `user-table`
- **父组件**：直接父组件名，根组件填页面路由名
- **子组件**：直接子组件列表，如 `UserAvatar, UserStatus`
- **UI 组件库**：具体 Element Plus / Vant 组件名，如 `el-table`、`van-list`、`el-button`
- **字号令牌**：设计令牌引用，如 `text-sm`；无设计稿时填「待确认」
- **字色令牌**：设计令牌引用，如 `text-gray-700`；无设计稿时填「待确认」
- **CSS Class**：使用的语义 class 或 `@apply` 组合；如 `@apply flex items-center gap-2`
- **空间定位**：描述与兄弟组件的相对位置，如「筛选栏下方」「操作栏右侧」「统计卡与列表之间」

#### 组件关系图（复杂需求必填）

复杂需求（多模块 / 多页面 / 组件 >10 个）必须补充组件关系图，描述组件树结构和空间布局。

Mermaid 组件树模板：

```mermaid
graph TD
  Page["页面组件"] --> FilterBar["筛选栏"]
  Page --> StatCards["统计卡区域"]
  Page --> ActionBar["操作栏"]
  Page --> DataTable["数据表格"]

  FilterBar --> DateRange["el-date-picker"]
  FilterBar --> StatusSelect["el-select"]

  StatCards --> CardA["统计卡 A"]
  StatCards --> CardB["统计卡 B"]

  ActionBar --> AddBtn["el-button: 新增"]
  ActionBar --> ExportBtn["el-button: 导出"]

  DataTable --> NameCell["名称 + UserAvatar"]
  DataTable --> StatusCell["UserStatus"]
  DataTable --> ActionCell["操作按钮组"]
```

ASCII 空间布局模板（描述页面从上到下的布局关系）：

```
┌──────────────────────────────────────────┐
│ 筛选栏 (FilterBar)                        │
│  [日期范围] [状态下拉]  [搜索] [重置]      │
├──────────────────────────────────────────┤
│ 统计卡区域 (StatCards)  ← flex row        │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐             │
│  │ A  │ │ B  │ │ C  │ │ D  │             │
│  └────┘ └────┘ └────┘ └────┘             │
├──────────────────────────────────────────┤
│ 操作栏 (ActionBar)  ← flex justify-between│
│  [新增] [导出]           [批量操作 ▼]      │
├──────────────────────────────────────────┤
│ 数据表格 (DataTable)                       │
│  名称 | 状态 | 创建时间 | 操作             │
│  ─────────────────────────────            │
│  ···                                     │
├──────────────────────────────────────────┤
│ 分页器 (el-pagination)  ← 右对齐          │
└──────────────────────────────────────────┘
```

## 二、全局工程方案

### 1. 应用边界与目录建议

写目录树和说明：
- 多端应用隔离方式。
- 共享能力位置。
- 组件封装规则：复用 2 个以上页面才进 shared，否则留页面私有。
- 构建入口区分。
- 与 README、`docs/conventions/*`、现有代码的差异。

### 2. 模块边界与文件所有权

| 模块 | 高内聚职责 | 私有状态 | 对外契约 | 禁止耦合 | 测试所有权 |
| --- | --- | --- | --- | --- | --- |

| 模块 | Owner | 允许修改 | 禁止修改 | 共享契约 | 集成顺序 | 验证命令 |
| --- | --- | --- | --- | --- | --- | --- |

### 3. 路由、跳转与状态保留

#### 路由表

| 页面 | path | name | 权限/菜单 key | 说明 |
| --- | --- | --- | --- | --- |

#### 跳转参数表

| 来源 | 动作 | 目标 | 参数 | 目标页行为 |
| --- | --- | --- | --- | --- |

#### 状态保留策略

| 场景 | 策略 | 说明 |
| --- | --- | --- |

### 4. 前后端联调约束

只写前端视角的接口契约，不写后端实现。

#### 数据格式约定

- ID 类型：
- 时间格式：
- 金额格式：
- 状态/枚举来源：

#### 请求约定

- 接口前缀：
- 写操作请求头：
- 版本/并发参数：
- 幂等参数：

#### 响应约定

```typescript
interface ApiResponse<T> {
  code: string
  message: string
  data: T
  requestId: string
}

interface ApiError {
  code: string
  message: string
  requestId: string
  detail?: unknown
  current?: unknown
}
```

#### 错误处理约定

| 状态码/错误码 | 前端行为 | 用户反馈 | 是否上报 |
| --- | --- | --- | --- |

#### 主接口索引

| 模块 | 接口 | 方法 | 用途 | 请求来源 | 响应来源 | 需版本 |
| --- | --- | --- | --- | --- | --- | --- |

#### 跨端事务边界

| 操作 | 前端调用 | 后端保证结论 | 前端处理 |
| --- | --- | --- | --- |

### 5. 权限矩阵

| 角色 | 路由权限 | 按钮/操作权限 key | 无权限表现 | 接口错误态 |
| --- | --- | --- | --- | --- |

### 6. 前端安全

- URL query 白名单与非法枚举清理。
- 外链 `rel="noopener noreferrer"` 与协议限制。
- H5 token 存储、过期、清理策略。
- 文件上传前端提示和限制。
- 导入文件公式注入防护。
- 敏感信息脱敏和日志限制。

### 7. 请求策略、性能与兼容

- 列表查询封装模式。
- 搜索 debounce、分页和筛选重置。
- 请求取消、轮询和页面可见性。
- 大数据量列表、导入、导出策略。
- 浏览器/容器/移动端兼容范围。
- i18n 或多语言不涉及时说明原因。

### 8. 可观测性与埋点

| 事件/错误 | 触发时机 | 属性 | 用途 | 本期/后续 |
| --- | --- | --- | --- | --- |

### 9. 部署、灰度与回滚

| 项 | 方案 |
| --- | --- |
| 构建目标 |  |
| 部署入口 |  |
| 环境变量 |  |
| Feature flag / 灰度 |  |
| 回滚方式 |  |
| 发布后监控 |  |

### 10. 验收用例与测试策略

验收用例生成遵循 `docs/conventions/acceptance-case-generation.md`，每个页面必须包含一条页面还原用例（layer=component），覆盖布局区块、组件映射、交互状态、数据状态和设计令牌使用。

```typescript
interface AcceptanceCase {
  id: string
  module: string
  layer: 'unit' | 'component' | 'integration' | 'e2e' | 'manual'
  source: string
  preconditions: string[]
  fixture: string
  steps: string[]
  expected: string[]
  negative?: string[]
  owner: string
}
```

#### 验证矩阵

| 验证项 | 命令来源 | 推荐命令 | 通过标准 | 未执行风险 |
| --- | --- | --- | --- | --- |

### 11. 风险清单

| 风险 | 等级 | 缓解措施 | Owner | 验收 |
| --- | --- | --- | --- | --- |

## 二·甲、前端工程基线

> 本章把项目硬规则与日常工程规范收口为方案自检项。生成方案时先读 `CLAUDE.md`、`~/.claude/projects/<project>/memory/MEMORY.md` 及索引 feedback、`docs/conventions/*`，把硬规则填入下表。

### 1. 项目硬规则索引

| 来源 | 关键规则 | 在本方案的应用点 |
| --- | --- | --- |
| `CLAUDE.md` |  |  |
| `memory/MEMORY.md` + feedback |  |  |
| `docs/conventions/components.md` |  |  |
| `docs/conventions/styles.md` |  |  |
| `docs/conventions/testing.md` |  |  |
| `docs/conventions/verification.md` |  |  |
| `docs/conventions/api-integration.md` |  |  |
| `docs/conventions/code-review.md` |  |  |
| `docs/conventions/git.md` |  |  |
| `docs/conventions/parallel-development.md` |  |  |

### 2. 类型契约收口

- 响应类型集中位置：例如 `src/api/types.ts`，其他文件只 re-export。
- 业务实体类型集中位置：例如 `src/<scope>/types/*.ts`。
- 禁止：在 composable / view 中重新声明 BackendResponse 等响应类型。
- 本方案新增/修改的类型清单：

| 类型 | 位置 | 用途 | 来源 |
| --- | --- | --- | --- |

### 3. 组件与泛型

- 通用组件（`src/components/**`）使用泛型 `generic="T extends object"` 消除 `any`，例如表格、卡片、选择器。
- 业务组件 props 必须有显式类型，禁止 `props: any` 或 `defineProps<any>()`。
- 文件命名：组件文件名 `kebab-case`（如 `user-avatar.vue`），import 时 `PascalCase`（如 `import UserAvatar from './user-avatar.vue'`）。
- 组件层级：通用组件（`src/components/`，零业务逻辑）→ 业务组件（`views/<Page>/components/`，仅当前页面）→ 页面组件（组合层）。
- 子组件数据通过 props 传入、emit 通信，禁止通过 ref 直接操作子组件内部。
- 本方案涉及的组件改造：

| 组件 | 现状 | 目标 | 验证 |
| --- | --- | --- | --- |

### 4. 弹窗规范

- 默认：`el-dialog` + 项目统一的 `useConfirmDialog` / `dialog-baseline` 类。
- 禁止：`ElMessageBox.confirm`、`window.alert`、`window.confirm`、`Teleport` 弹窗，除非硬规则允许。
- 本方案涉及的弹窗：

| 触发点 | 原始实现 | 目标实现 | 拦截方式 |
| --- | --- | --- | --- |

### 5. 废弃 API 清理

| API | 替换 | 范围 | 优先级 |
| --- | --- | --- | --- |
| `document.execCommand('copy')` | `navigator.clipboard.writeText` |  |  |
| `Event` 兼容写法 | 现代标准 API |  |  |
| 其他（列） |  |  |  |

### 6. 响应式选型

| 数据形态 | 选型 | 理由 |
| --- | --- | --- |
| 列表数据（数组 of 对象） | `shallowRef` | 避免深层代理开销 |
| 表单状态（扁平字段） | `ref` / `reactive` | 模板深追踪 |
| 大对象一次性替换 | `shallowRef` | 仅触发引用变化 |
| DOM/组件实例 ref | `useTemplateRef` / `ref(null)` | 标准 |

### 7. URL query 校验

- 路由/页面读 query 时必须有白名单与枚举校验，非法值回退默认。
- 列出本方案涉及的 query key 与校验规则：

| Query key | 类型/枚举 | 默认值 | 校验失败处理 |
| --- | --- | --- | --- |

### 8. 样式 token

- 颜色、间距、圆角、阴影统一来自 `src/styles/index.css` 的 `@theme` 定义。
- 禁止：硬编码 `#xxxxxx`、`rgb()`、`rgba()`、`!important`、inline `style="..."`、`:style="{...}"`。
- 本方案涉及样式改动：

### 9. 动态 import 与按需加载

| 依赖 | 触发场景 | 导入方式 | 收益 |
| --- | --- | --- | --- |
| 例如 `cos-js-sdk-v5` | 用户点击上传 | `await import(...)` | 首屏体积 -X KB |

### 10. lint / test baseline

- 方案开始前 baseline：

| 项 | 数值 | 来源 |
| --- | --- | --- |
| lint error | __ | `bun run lint` |
| lint warning | __ | `bun run lint` |
| test failed | __ | `bun run test` |
| coverage statements | __% | `bun run test:coverage` |

- 本期处理范围：修哪些、留哪些、owner 是谁。

## 二·乙、性能与稳定性

### 1. 组件库按需加载

| 端 | 组件库 | 当前 | 目标 | 迁移策略 |
| --- | --- | --- | --- | --- |
| PC | Element Plus | 全量 / 按需 | 按需 + `ElConfigProvider` |  |
| H5 | Vant | 全量 / 按需 | 按需 |  |

### 2. 构建拆包

| Chunk | 包含 | 触发条件 | 预期体积 |
| --- | --- | --- | --- |
| `vendor` | Vue / Vue Router / Pinia / Axios | 首屏 |  |
| `element-plus` | Element Plus 组件 | PC 路由 |  |
| `vant` | Vant 组件 | H5 路由 |  |
| 其他 |  |  |  |

`vite.config.ts` 中 `manualChunks` 配置片段（如需要）：

```ts
// 在 build.rollupOptions.output.manualChunks 中
```

### 3. 请求层隐性陷阱

| 陷阱 | 检查方式 | 本方案处理 |
| --- | --- | --- |
| 重试计数闭包共享 | `request.ts` 中 `retryCount` 是否定义在请求函数内部 |  |
| 并发请求互相取消 | 是否每个请求独立 AbortController |  |
| 401 重定向时机 | 拦截器是否在重试前判断 |  |
| 错误重试上限 | 是否有最大重试次数 |  |

### 4. 列表竞态保护

每个列表 composable 必须声明竞态保护策略：

| 列表 | 保护方式 | 实现位置 |
| --- | --- | --- |
|  | `latestFetchId` 自增 + 回包校验 |  |
|  | `AbortController` 主动取消 |  |

模式示例：

```ts
let fetchId = 0
async function fetchList() {
  const id = ++fetchId
  const res = await api.list(...)
  if (id !== fetchId) return // 丢弃过期响应
  state.value = res.data
}
```

### 5. 大依赖动态 import

| 依赖 | 大小（gzip） | 触发条件 | 收益 |
| --- | --- | --- | --- |
|  |  |  |  |

### 6. 首屏体积预算

| 项 | 预算 | 实测 | 评估 |
| --- | --- | --- | --- |
| 首屏 JS（gzip） | ≤ __ KB |  |  |
| 首屏 CSS | ≤ __ KB |  |  |
| LCP | ≤ __ s |  |  |

## 三、功能拆解 / 改动清单

按模块逐个展开。每个模块至少包含：

### <模块名>

#### 职责与入口

- 职责：
- 路由/入口：
- 依赖模块：
- 禁止耦合：

#### 统计卡/概览区

每个统计卡项：实现、API、响应、逻辑、交互、验收、边界。

#### 筛选条件

每个筛选项：组件、props、选项来源、URL 同步、校验、验收。

#### 列表字段

每列：组件、宽度/对齐、展示逻辑、状态映射、空值、验收、边界。

#### 操作

每个操作：按钮、权限、API、参数、响应、确认弹窗、重复提交保护、成功/失败反馈、边界。

#### CRUD / 表单

字段、校验规则、默认值、提交接口、错误回填、关闭/重置策略。

#### 改动项

逐项列出本方案对现有代码的改动（新增功能方案也会涉及对既有文件、组件、接口、类型的改动）。

每个改动项必须覆盖十个维度：

| 维度 | 要求 |
| --- | --- |
| 实现 | 组件名、关键 props、布局、样式 class 或既有组件封装 |
| API | 方法、路径、参数、请求头、幂等/版本参数 |
| 响应 | 前端期望的数据结构、错误结构、空数据结构 |
| 逻辑 | 排序、筛选、状态映射、权限判断、副作用 |
| 交互 | 点击、跳转、确认、hover、快捷键、移动端手势 |
| 验收 | 用户可见结果和可执行检查方式 |
| 边界 | 空数据、加载失败、超时、权限不足、并发冲突、兼容降级 |
| 影响面 | 受影响的页面/模块/接口/测试，附 grep 结果或位置列表 |
| 回滚 | 出问题时如何快速还原（feature flag、commit revert、双写、灰度） |
| 测试 | unit/component/integration/e2e/manual 层级与 owner |

改动清单表：

| 改动 | 文件 | 现状 | 目标 | 影响面 | 验证 | 回滚 | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |

#### 测试所有权

| 用例 | 层级 | 来源 | Owner |
| --- | --- | --- | --- |

## 四、核心数据模型

### 基础约定

ID、时间、金额、文件、用户展示等基础格式。

### 统一枚举表

| 枚举 | value | 含义 | 展示映射 | 来源 |
| --- | --- | --- | --- | --- |

### 字段命名规范

| 字段类型 | 命名 | 示例 |
| --- | --- | --- |

### TypeScript 接口定义

每个核心实体给出完整 interface，并标注来源。

### 数据模型关系

用文本或 ASCII 图描述实体关系和页面数据流向。

## 五、前端状态流转

### 实现方案

- 状态管理选型及理由。
- 并发处理：携带 `version` 或等价参数；收到 `409` 后提示刷新并重新拉取。
- 状态转移约束：TypeScript 映射表 + `canTransition` 校验函数。

### 状态机

每个状态机包含：
- ASCII 流转图。
- 转移触发点与 API 表。
- 权限和前置条件。
- 成功/失败反馈。
- 前端不负责保证后端原子性，只调用正确 API 并处理响应。

| 转移 | 触发端 | 前置条件 | API | 参数 | 成功表现 | 失败表现 |
| --- | --- | --- | --- | --- | --- | --- |

## 六、功能一致性索引

### 需求追踪矩阵

| PRD 条目 | 模块 | 路由/入口 | 接口 | 数据模型 | 用例 | 验收标准 |
| --- | --- | --- | --- | --- | --- | --- |

### 联调检查清单

| 检查项 | 来源 | 方案位置 | 状态 |
| --- | --- | --- | --- |
| 枚举值 |  |  |  |
| 路由路径 |  |  |  |
| 金额字段 |  |  |  |
| 版本参数 |  |  |  |
| 权限 key |  |  |  |
| 错误码 |  |  |  |
| 字段迁移（如有重命名） |  |  |  |
| 列表竞态保护 |  |  |  |
| 请求层重试/取消 |  |  |  |
| 弹窗规范遵守 |  |  |  |
| 样式 token 遵守 |  |  |  |
| 组件文件名 kebab-case + import PascalCase | `components.md` | 二·甲·3 |  |
| 页面区块与设计稿一一对应 | `acceptance-case-generation.md` | 一·页面还原约定 |  |
| 交互状态覆盖（disabled/loading/空态/错误态） | `acceptance-case-generation.md` | 一·页面还原约定 |  |
| 组件库映射（PC=Element Plus，H5=Vant 4） | `acceptance-case-generation.md` | 一·页面还原约定 |  |
| lint/test baseline |  |  |  |

## 附录

### 后续迭代

| 内容 | 原因 | 触发条件 |
| --- | --- | --- |

### 参考链接

只记录必要来源摘要，不泄露凭据、Cookie、Token、账号、未脱敏内部链接或敏感截图内容。
TEMPLATE

echo "✅ 模板已生成到: $TARGET ($(wc -l < "$TARGET") 行)"
