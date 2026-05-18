# 功能描述到测试用例生成规范

本文基于 `docs/prd/kol-platform-tech-spec.md` 和 `docs/conventions/testing.md`，定义如何从 PRD 的功能描述、模块拆解和验收口径生成可执行、可追溯的测试用例。

## 适用范围

- 适用于达人平台 PRD 中的 `dashboard`、`cooperation`、`task`、`kol`、`review`、`settlement`、`kol-h5`、`shared-contracts` 模块。
- 当前仓库缺少正式的 `docs/architecture/overview.md` 和 `docs/architecture/boundaries.md`，因此先以 PRD 内「模块边界与测试所有权」和「功能一致性索引」作为拆解依据。
- 生成的是验收用例和测试设计，不替代具体测试代码；落地代码时仍按 `docs/conventions/testing.md` 的文件组织和命令执行。

## 输入：功能描述格式

每条功能描述尽量整理为以下字段；PRD 中已有的 `实现 / API / 参数 / 响应 / 逻辑 / 交互 / 校验 / 验收 / 边界` 可以直接映射。

```markdown
### <功能点名称>

**模块：** <dashboard | cooperation | task | kol | review | settlement | kol-h5 | shared-contracts>
**入口：** <路由、页面区块、组件或接口>
**用户动作：** <点击、输入、选择、提交、上传、跳转等>
**接口契约：** <method path、请求参数、响应字段、错误码>
**状态变化：** <前端状态、后端副作用、路由 query、实体状态机>
**校验规则：** <必填、长度、枚举、版本号、权限、文件限制等>
**验收结果：** <用户可见结果、接口副作用、数据刷新、跳转定位>
**边界异常：** <空数据、超时、403、409、422、部分失败、弱网、重复点击>
**测试数据：** <fixture 文件或稳定数据名称>
```

缺字段时不要补想象需求；优先回到 PRD 的模块条目、主接口索引、状态流转和功能一致性索引中查证。

## 输出：验收用例格式

每条用例使用 PRD 已定义的 `AcceptanceCase` 结构：

```typescript
interface AcceptanceCase {
  id: string
  module: 'dashboard' | 'cooperation' | 'task' | 'kol' | 'review' | 'settlement' | 'kol-h5' | 'shared-contracts'
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

`id` 建议使用 `AC-<MODULE>-<FEATURE>-<LAYER>-<NNN>`，例如 `AC-COOPERATION-STATUS-INTEGRATION-001`。

## 生成流程

### 1. 先确定模块归属

按模块拥有用户入口和断言结果的原则归属测试：

| 模块 | 测试所有权 |
| --- | --- |
| `dashboard` | 统计卡、局部 loading、空状态、轮询暂停、跳转 query |
| `cooperation` | 筛选 query、跨页选择、入选/不选、状态冲突 |
| `task` | 发布校验、视图切换、任务状态机、详情路由 |
| `kol` | 表单校验、导入失败行、导出权限、配额与标签 |
| `review` | 队列切换、视频错误态、通过/驳回事务结果 |
| `settlement` | 单条/批量结算、部分失败、撤销原因、金额格式 |
| `kol-h5` | 登录、报名、上传断点续传、驳回修改、数据隔离 |
| `shared-contracts` | 状态流转、格式化、权限 key、字典和类型守卫 |

跨模块链路不要塞进单个模块的集成测试；只放到 E2E 或人工验收。

### 2. 再选择测试层级

| 层级 | 选择条件 | 典型断言 |
| --- | --- | --- |
| `unit` | 纯函数、状态机、格式化、权限判断、query 清洗 | 输入输出、非法枚举、边界值、错误码映射 |
| `component` | 单组件、表单、弹窗、上传控件、统计卡、批量操作栏 | 渲染、交互、emit、禁用状态、表单校验 |
| `integration` | 单页面 + Pinia + Router + msw handler | 请求参数、响应解析、列表刷新、错误提示、路由 query |
| `e2e` | 跨页面、跨端、核心业务副作用 | 登录、跳转、状态流转、后续页面可见结果 |
| `manual` | SSO、真机浏览器、真实视频播放、弱网、外部系统 | 环境、账号、截图、时间、人工观察结论 |

一个功能点通常生成 3 类用例：正向主路径、反向失败路径、边界路径。不要把三类行为混在同一条用例中。

### 3. 从字段推导用例类型

| 功能描述字段 | 生成用例 |
| --- | --- |
| `实现` 提到组件、按钮、弹窗 | 组件测试：渲染、点击、禁用、loading、表单错误 |
| `API / 参数 / 响应` | 集成测试：请求方法、路径、参数、响应解析、错误码 |
| `逻辑` 提到状态机或计算 | 单元测试：合法流转、非法流转、边界计算 |
| `交互` 提到跳转、定位、高亮 | 集成或 E2E：路由 query、目标页选中、高亮消退 |
| `校验` 提到必填、长度、文件限制 | 组件测试：错误提示、禁止提交、边界值 |
| `验收` 提到跨模块可见 | E2E：前置模块动作完成后，后续模块能看到副作用 |
| `边界` 提到空、超时、失败、部分成功 | 集成测试：msw 返回异常，断言提示和状态不变 |
| `权限 / 安全` | 集成或手工验收：按钮显隐只是体验，接口 403 必须处理 |

### 4. 填充用例字段

- `source` 写到 PRD 的具体章节或条目，例如 `docs/prd/kol-platform-tech-spec.md#三功能拆解-2-合作动态-入选`。
- `preconditions` 只写业务和环境前置，不写测试实现细节。
- `fixture` 必须引用稳定数据，例如 `e2e/fixtures/cooperations.ts#appliedCooperation` 或 `src/mocks/handlers/cooperations.ts`。
- `steps` 使用用户行为描述，避免写内部变量赋值。
- `expected` 至少包含一个用户可见结果或后端副作用。
- `negative` 只放失败断言；复杂失败场景单独拆成新用例。
- `owner` 填模块所有者，例如 `cooperation`、`review`、`kol-h5`。

## 本 PRD 的优先级规则

| 优先级 | 生成对象 | 示例 |
| --- | --- | --- |
| P0 | 状态流转、副作用、跨模块核心链路 | 报名 -> 入选 -> 上传 -> 审核 -> 结算 |
| P0 | 写操作携带 `version` 且处理 `409/422` | 入选、不选、审核通过/驳回、结算、撤销 |
| P1 | 列表筛选、分页、URL query、空状态、loading | 合作动态筛选、结算跨页选择 |
| P1 | 文件、导入导出、上传、下载 | 达人 Excel 导入导出、H5 分片上传 |
| P2 | 纯展示、标签颜色、hover、tooltip | 状态标签、金额列、提示文案 |

P2 中如果只是第三方组件内部行为或 Tailwind class 组合效果，不生成自动化用例；只在视觉检查或人工验收中记录。

## 示例用例

### Dashboard 跳转审核

```json
{
  "id": "AC-DASHBOARD-GOTO-REVIEW-E2E-001",
  "module": "dashboard",
  "layer": "e2e",
  "source": "docs/prd/kol-platform-tech-spec.md#三功能拆解-1-今日-dashboard-去审核",
  "preconditions": [
    "运营端已登录",
    "存在一条待审核视频，reviewId=review-001"
  ],
  "fixture": "e2e/fixtures/reviews.ts#pendingReview",
  "steps": [
    "打开 /dashboard",
    "在待审核视频区块点击 review-001 所在行的「去审核」",
    "等待路由跳转到审核工作台"
  ],
  "expected": [
    "浏览器地址为 /review?reviewId=review-001",
    "审核队列自动选中 review-001",
    "目标审核单出现高亮效果"
  ],
  "owner": "dashboard"
}
```

### 合作动态入选成功

```json
{
  "id": "AC-COOPERATION-SELECT-INTEGRATION-001",
  "module": "cooperation",
  "layer": "integration",
  "source": "docs/prd/kol-platform-tech-spec.md#三功能拆解-2-合作动态-入选",
  "preconditions": [
    "合作动态列表存在状态为 applied 的合作单",
    "该合作单 version=3"
  ],
  "fixture": "src/mocks/handlers/cooperations.ts#appliedCooperation",
  "steps": [
    "打开 /cooperation",
    "点击 applied 合作单的「入选」按钮",
    "在二次确认中点击确认"
  ],
  "expected": [
    "发送 PATCH /api/cooperations/:id/status",
    "请求体包含 status=shooting 和 version=3",
    "成功后列表重新拉取",
    "该行状态展示为「拍摄中」",
    "操作按钮切换为「查看达人」「查看任务」"
  ],
  "owner": "cooperation"
}
```

### 合作动态版本冲突

```json
{
  "id": "AC-COOPERATION-SELECT-INTEGRATION-002",
  "module": "cooperation",
  "layer": "integration",
  "source": "docs/prd/kol-platform-tech-spec.md#二全局工程方案-3-统一接口契约-错误码",
  "preconditions": [
    "合作动态列表存在状态为 applied 的合作单",
    "服务端返回 409 版本冲突"
  ],
  "fixture": "src/mocks/handlers/cooperations.ts#versionConflict",
  "steps": [
    "打开 /cooperation",
    "点击「入选」并确认"
  ],
  "expected": [
    "页面展示后端返回的错误 message",
    "当前行状态仍为「已报名」",
    "不展示成功提示"
  ],
  "negative": [
    "不得在 409 时乐观更新为「拍摄中」"
  ],
  "owner": "cooperation"
}
```

### 任务发布表单校验

```json
{
  "id": "AC-TASK-PUBLISH-COMPONENT-001",
  "module": "task",
  "layer": "component",
  "source": "docs/prd/kol-platform-tech-spec.md#三功能拆解-3-任务-crud-c-发布任务",
  "preconditions": [
    "发布任务弹窗已打开"
  ],
  "fixture": "src/mocks/fixtures/tasks.ts#emptyPublishForm",
  "steps": [
    "不填写任务名称、预算、截止时间、负责人和等级",
    "点击「确认」"
  ],
  "expected": [
    "表单展示必填错误提示",
    "确认提交被阻止",
    "不发送 POST /api/tasks"
  ],
  "owner": "task"
}
```

### 结算批量部分失败

```json
{
  "id": "AC-SETTLEMENT-BATCH-INTEGRATION-001",
  "module": "settlement",
  "layer": "integration",
  "source": "docs/prd/kol-platform-tech-spec.md#三功能拆解-6-结算-批量标注已结算",
  "preconditions": [
    "结算列表存在 3 条 pending 结算单",
    "批量结算接口返回 BatchResult[]，其中 1 条失败"
  ],
  "fixture": "src/mocks/handlers/settlements.ts#batchPartialFailure",
  "steps": [
    "打开 /settlement",
    "勾选 3 条待结算记录",
    "点击「批量标注已结算」并确认"
  ],
  "expected": [
    "页面展示部分成功和失败明细",
    "成功项在刷新后变为「已结算」",
    "失败项仍为「待结算」并提供重试入口",
    "统计卡在列表刷新后更新"
  ],
  "owner": "settlement"
}
```

## 质量检查清单

生成完用例后逐条检查：

- 是否能追溯到 PRD 的模块、接口、状态机或验收条目。
- 是否选择了最小合适层级，未把纯函数放到 E2E，未把跨模块副作用放到单元测试。
- 是否有稳定 fixture，且 fixture 覆盖正常、空、权限不足、状态冲突、非法状态、边界金额、超长文本、缺失可选字段。
- 是否包含正向、反向、边界三类用例，且拆分清晰。
- 是否断言用户可见行为、请求参数、状态变化、路由变化、错误提示或权限结果。
- 是否避免断言 Element Plus、Vant、Vue、浏览器原生 API 和 Tailwind class 组合效果。
- 是否为写操作覆盖 `version`、重复点击、`403/409/422/500+` 至少一种关键失败路径。
- 是否为跨端核心链路覆盖 E2E：达人报名、入选、上传、审核通过、结算。

## 生成提示词模板

```text
你是前端测试用例生成器。请根据以下功能描述生成 AcceptanceCase[]。

约束：
1. 先判断模块归属，再选择最小合适测试层级：unit/component/integration/e2e/manual。
2. 每条用例必须填写 id、module、layer、source、preconditions、fixture、steps、expected、owner。
3. 正向、反向、边界用例分开输出。
4. expected 至少包含一个用户可见结果或接口副作用。
5. fixture 必须引用稳定测试数据，不允许临时编造魔法数据。
6. 不测试第三方组件内部行为、Tailwind class 组合效果或 Vue 响应式系统本身。
7. 写操作必须覆盖 version、错误提示、失败不改前端状态。

功能描述：
<粘贴 PRD 中某个功能点的模块、入口、API、逻辑、交互、校验、验收、边界>

输出格式：
Markdown 表格 + JSON AcceptanceCase 示例。
```
