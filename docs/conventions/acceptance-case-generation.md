# 功能描述到测试用例生成规范

本文基于项目的 PRD 技术规格文档和 `docs/conventions/testing.md`，定义如何从 PRD 的功能描述、模块拆解和验收口径生成可执行、可追溯的测试用例。

## 适用范围

- 适用于项目 PRD 中定义的各业务模块。
- 当前仓库缺少正式的 `docs/architecture/overview.md` 和 `docs/architecture/boundaries.md` 时，先以 PRD 内「模块边界与测试所有权」和「功能一致性索引」作为拆解依据。
- 生成的是验收用例和测试设计，不替代具体测试代码；落地代码时仍按 `docs/conventions/testing.md` 的文件组织和命令执行。

## 输入：功能描述格式

每条功能描述尽量整理为以下字段；PRD 中已有的 `实现 / API / 参数 / 响应 / 逻辑 / 交互 / 校验 / 验收 / 边界` 可以直接映射。

```markdown
### <功能点名称>

**模块：** <项目定义的业务模块名>
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

每条用例使用以下 `AcceptanceCase` 结构：

```typescript
interface AcceptanceCase {
  id: string
  module: string // 业务模块名，与 PRD 定义一致
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

`id` 建议使用 `AC-<MODULE>-<FEATURE>-<LAYER>-<NNN>`，例如 `AC-ORDER-CREATE-INTEGRATION-001`。

## 生成流程

### 1. 先确定模块归属

按模块拥有用户入口和断言结果的原则归属测试。根据项目 PRD 中定义的模块列表，每个模块应明确其测试所有权范围，例如：

| 模块示例 | 测试所有权 |
| --- | --- |
| 数据看板 | 统计卡、局部 loading、空状态、轮询暂停、跳转 query |
| 列表管理 | 筛选 query、跨页选择、状态流转、状态冲突 |
| 表单/发布 | 发布校验、视图切换、状态机、详情路由 |
| 审核/审批 | 队列切换、错误态、通过/驳回事务结果 |
| 批量操作 | 单条/批量操作、部分失败、撤销原因、格式校验 |
| 移动端 H5 | 登录、提交、上传断点续传、驳回修改、数据隔离 |
| 共享契约 | 状态流转、格式化、权限 key、字典和类型守卫 |

跨模块链路不要塞进单个模块的集成测试；只放到 E2E 或人工验收。

### 2. 再选择测试层级

| 层级 | 选择条件 | 典型断言 |
| --- | --- | --- |
| `unit` | 纯函数、状态机、格式化、权限判断、query 清洗 | 输入输出、非法枚举、边界值、错误码映射 |
| `component` | 单组件、表单、弹窗、上传控件、统计卡、批量操作栏 | 渲染、交互、emit、禁用状态、表单校验 |
| `integration` | 单页面 + 状态管理 + Router + msw handler | 请求参数、响应解析、列表刷新、错误提示、路由 query |
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

- `source` 写到 PRD 的具体章节或条目，例如 `docs/prd/tech-spec.md#三功能拆解-2-列表管理-状态变更`。
- `preconditions` 只写业务和环境前置，不写测试实现细节。
- `fixture` 必须引用稳定数据，例如 `e2e/fixtures/orders.ts#sampleOrder` 或 `src/mocks/handlers/orders.ts`。
- `steps` 使用用户行为描述，避免写内部变量赋值。
- `expected` 至少包含一个用户可见结果或后端副作用。
- `negative` 只放失败断言；复杂失败场景单独拆成新用例。
- `owner` 填模块所有者，例如对应的模块名。

## 优先级规则

| 优先级 | 生成对象 | 示例 |
| --- | --- | --- |
| P0 | 状态流转、副作用、跨模块核心链路 | 创建 -> 审批 -> 执行 -> 完成 |
| P0 | 写操作携带 `version` 且处理 `409/422` | 状态变更、审核通过/驳回、关键写操作 |
| P1 | 列表筛选、分页、URL query、空状态、loading | 列表筛选、跨页选择 |
| P1 | 文件、导入导出、上传、下载 | Excel 导入导出、分片上传 |
| P2 | 纯展示、标签颜色、hover、tooltip | 状态标签、金额列、提示文案 |

P2 中如果只是第三方组件内部行为或 Tailwind class 组合效果，不生成自动化用例；只在视觉检查或人工验收中记录。

## 示例用例

### 看板跳转详情

```json
{
  "id": "AC-DASHBOARD-GOTO-DETAIL-E2E-001",
  "module": "dashboard",
  "layer": "e2e",
  "source": "docs/prd/tech-spec.md#三功能拆解-1-数据看板-跳转详情",
  "preconditions": [
    "用户已登录",
    "存在一条待处理记录，recordId=record-001"
  ],
  "fixture": "e2e/fixtures/records.ts#pendingRecord",
  "steps": [
    "打开首页看板",
    "在待处理区块点击 record-001 所在行的「查看详情」",
    "等待路由跳转到详情页"
  ],
  "expected": [
    "浏览器地址为 /detail?recordId=record-001",
    "详情页自动定位到 record-001",
    "目标记录出现高亮效果"
  ],
  "owner": "dashboard"
}
```

### 列表状态变更成功

```json
{
  "id": "AC-LIST-STATUS-CHANGE-INTEGRATION-001",
  "module": "list",
  "layer": "integration",
  "source": "docs/prd/tech-spec.md#三功能拆解-2-列表管理-状态变更",
  "preconditions": [
    "列表存在状态为 pending 的记录",
    "该记录 version=3"
  ],
  "fixture": "src/mocks/handlers/list.ts#pendingRecord",
  "steps": [
    "打开列表页",
    "点击 pending 记录的「审批」按钮",
    "在二次确认中点击确认"
  ],
  "expected": [
    "发送 PATCH /api/records/:id/status",
    "请求体包含 status=approved 和 version=3",
    "成功后列表重新拉取",
    "该行状态展示为「已审批」",
    "操作按钮切换为对应的后续操作"
  ],
  "owner": "list"
}
```

### 版本冲突

```json
{
  "id": "AC-LIST-STATUS-CHANGE-INTEGRATION-002",
  "module": "list",
  "layer": "integration",
  "source": "docs/prd/tech-spec.md#二全局工程方案-3-统一接口契约-错误码",
  "preconditions": [
    "列表存在状态为 pending 的记录",
    "服务端返回 409 版本冲突"
  ],
  "fixture": "src/mocks/handlers/list.ts#versionConflict",
  "steps": [
    "打开列表页",
    "点击「审批」并确认"
  ],
  "expected": [
    "页面展示后端返回的错误 message",
    "当前行状态不变",
    "不展示成功提示"
  ],
  "negative": [
    "不得在 409 时乐观更新状态"
  ],
  "owner": "list"
}
```

### 表单发布校验

```json
{
  "id": "AC-FORM-PUBLISH-COMPONENT-001",
  "module": "form",
  "layer": "component",
  "source": "docs/prd/tech-spec.md#三功能拆解-3-表单-发布",
  "preconditions": [
    "发布弹窗已打开"
  ],
  "fixture": "src/mocks/fixtures/forms.ts#emptyForm",
  "steps": [
    "不填写任何必填字段",
    "点击「确认」"
  ],
  "expected": [
    "表单展示必填错误提示",
    "确认提交被阻止",
    "不发送 POST 请求"
  ],
  "owner": "form"
}
```

### 批量操作部分失败

```json
{
  "id": "AC-BATCH-OPERATION-INTEGRATION-001",
  "module": "batch",
  "layer": "integration",
  "source": "docs/prd/tech-spec.md#三功能拆解-6-批量操作-批量处理",
  "preconditions": [
    "列表存在 3 条待处理记录",
    "批量接口返回 BatchResult[]，其中 1 条失败"
  ],
  "fixture": "src/mocks/handlers/batch.ts#batchPartialFailure",
  "steps": [
    "打开列表页",
    "勾选 3 条待处理记录",
    "点击「批量处理」并确认"
  ],
  "expected": [
    "页面展示部分成功和失败明细",
    "成功项在刷新后状态更新",
    "失败项状态不变并提供重试入口",
    "统计卡在列表刷新后更新"
  ],
  "owner": "batch"
}
```

## 质量检查清单

生成完用例后逐条检查：

- 是否能追溯到 PRD 的模块、接口、状态机或验收条目。
- 是否选择了最小合适层级，未把纯函数放到 E2E，未把跨模块副作用放到单元测试。
- 是否有稳定 fixture，且 fixture 覆盖正常、空、权限不足、状态冲突、非法状态、边界值、超长文本、缺失可选字段。
- 是否包含正向、反向、边界三类用例，且拆分清晰。
- 是否断言用户可见行为、请求参数、状态变化、路由变化、错误提示或权限结果。
- 是否避免断言第三方 UI 库、框架 API 和 CSS class 组合效果。
- 是否为写操作覆盖 `version`、重复点击、`403/409/422/500+` 至少一种关键失败路径。
- 是否为核心跨模块链路覆盖 E2E。

## 生成提示词模板

```text
你是前端测试用例生成器。请根据以下功能描述生成 AcceptanceCase[]。

约束：
1. 先判断模块归属，再选择最小合适测试层级：unit/component/integration/e2e/manual。
2. 每条用例必须填写 id、module、layer、source、preconditions、fixture、steps、expected、owner。
3. 正向、反向、边界用例分开输出。
4. expected 至少包含一个用户可见结果或接口副作用。
5. fixture 必须引用稳定测试数据，不允许临时编造魔法数据。
6. 不测试第三方组件内部行为、CSS class 组合效果或框架响应式系统本身。
7. 写操作必须覆盖 version、错误提示、失败不改前端状态。

功能描述：
<粘贴 PRD 中某个功能点的模块、入口、API、逻辑、交互、校验、验收、边界>

输出格式：
Markdown 表格 + JSON AcceptanceCase 示例。
```
