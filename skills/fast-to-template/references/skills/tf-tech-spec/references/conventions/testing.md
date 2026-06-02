# 测试规范

## 测试分层与选型

| 层级 | 工具 | 覆盖范围 | 运行命令 |
| --- | --- | --- | --- |
| 单元 + 组件测试 | Vitest + @vue/test-utils | utils / composables / store / 组件渲染交互 | `bun run test` |
| 覆盖率 | @vitest/coverage-v8 | 统计行/分支/函数覆盖率 | `bun run test:coverage` |
| E2E 测试 | Playwright（可选） | 跨页面用户流程、关键业务路径 | `bun run test:e2e` |

统一入口：`bun run test`

注意：`package.json` 中只提供 `test`（Vitest）、`test:coverage`、`test:e2e`（Playwright）三个命令。不需要额外拆分 `test:unit` / `test:component` / `test:integration`，所有 Vitest 测试统一通过 `test` 命令运行。

## 选型依据

**Vitest**（单元 + 组件）
- 原生 Vite 集成，共享 vite.config.ts 的别名、插件配置，零额外配置
- 与 Jest API 兼容，迁移成本低
- 原生 ESM / TypeScript 支持
- 内置覆盖率（coverage-v8）、快照测试

**@vue/test-utils**（组件挂载）
- Vue 官方组件测试库，`mount` / `shallowMount` 控制挂载深度
- `find` / `trigger` / `setValue` 模拟用户操作

**Playwright**（E2E，可选）
- 跨浏览器支持，自动等待机制
- 内置 Codegen 录制、Trace Viewer 调试

## 测试策略：测什么、不测什么

| 测 | 不测 |
| --- | --- |
| composable 内部逻辑（状态变更、计算结果） | Element Plus / Vant 组件内部行为 |
| Pinia store 的 action / getter | Vue 响应式系统本身 |
| 工具函数（格式化、校验、映射） | 第三方库的正确性 |
| API 请求构造和响应解析（mock 后端） | CSS 类名是否存在 |
| 组件 emit 的事件和参数 | Tailwind class 组合效果 |
| 路由守卫逻辑（权限校验、重定向） | 浏览器原生 API 行为 |
| 关键用户流程（E2E）：登录→报名→上传→审核→结算 | 已被上游覆盖的重复逻辑 |
| 表单校验规则（必填、格式、范围） | 纯 UI 展示（颜色、间距） |

## 文件组织

```
src/
├── components/
│   ├── StatCard/
│   │   ├── StatCard.vue
│   │   └── StatCard.test.ts          # 组件测试，与组件同目录
│   └── FilterBar/
│       ├── FilterBar.vue
│       └── FilterBar.test.ts
├── composables/
│   ├── useTaskList.ts
│   └── useTaskList.test.ts           # composable 测试
├── stores/
│   ├── cooperation.ts
│   └── cooperation.test.ts           # store 测试
├── utils/
│   ├── format.ts
│   └── format.test.ts                # 工具函数测试
└── views/
    └── settlement/
        └── settlement.integration.test.ts  # 页面级集成测试

e2e/
├── fixtures/                          # 测试数据和种子
│   ├── seed.ts                        # 数据库种子脚本
│   └── test-data.ts                   # 测试用例常量
├── pages/                             # Page Object Model
│   ├── dashboard.page.ts
│   ├── cooperation.page.ts
│   ├── review.page.ts
│   └── settlement.page.ts
├── flows/                             # 按业务流程组织
│   ├── login.flow.ts
│   ├── enroll-and-upload.flow.ts
│   ├── review-and-settle.flow.ts
│   └── full-pipeline.flow.ts
└── e2e.config.ts                      # Playwright 配置
```

## 命名规范

| 场景 | 文件名 | 示例 |
| --- | --- | --- |
| 单元测试 | `*.test.ts` | `format.test.ts` |
| 组件测试 | `*.test.ts`（同目录） | `StatCard.test.ts` |
| 集成测试 | `*.integration.test.ts` | `settlement.integration.test.ts` |
| E2E 测试 | `*.flow.ts` | `review-and-settle.flow.ts` |
| 测试工具 | `test-utils.ts` | `src/test-utils.ts`（公共 mount helper） |

## 公共测试工具 (`src/test-utils.ts`)

```ts
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { vi } from 'vitest'
import type { ComponentMountingOptions } from '@vue/test-utils'
import type { Component } from 'vue'

// 统一 mount 工具：自动注入 Pinia / Router stub
export function mountWithPlugins(
  component: Component,
  options?: ComponentMountingOptions<any>,
) {
  setActivePinia(createPinia())
  return mount(component, {
    global: { plugins: [], stubs: { RouterLink: true, RouterView: true } },
    ...options,
  })
}

// 等待异步更新
export function flush() {
  return new Promise(resolve => setTimeout(resolve, 0))
}
```

## Vitest 配置要点 (`vitest.config.ts`)

```ts
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': resolve(__dirname, 'src') },
  },
  test: {
    globals: true,                    // 全局 describe/it/expect
    environment: 'jsdom',             // 组件测试需要 DOM
    include: [
      'src/**/*.test.ts',
      'src/**/*.integration.test.ts',
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{ts,vue}'],
      exclude: ['src/**/*.test.ts', 'src/**/*.d.ts', 'src/test-utils.ts'],
      thresholds: {
        statements: 70,
        branches: 60,
        functions: 70,
        lines: 70,
      },
    },
  },
})
```

## Playwright 配置要点 (`e2e/e2e.config.ts`)

```ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './flows',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? [['gitlab'], ['html']] : [['list']],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'bun run dev',
    port: 5173,
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    // CI 环境可追加 firefox / webkit
  ],
})
```

## CI 集成

```yaml
# .gitlab-ci.yml 测试阶段
test:unit:
  stage: test
  script:
    - bun run test:coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:e2e:
  stage: test
  script:
    - bun run build
    - bun run test:e2e
  artifacts:
    when: on_failure
    paths:
      - e2e/test-results/
      - e2e/playwright-report/
```

## 关键业务流程 E2E 覆盖清单

| 流程 | 覆盖范围 |
| --- | --- |
| 达人报名 | 登录 → 查看任务列表 → 进入任务详情 → 报名 → 验证合作单创建 |
| 投稿上传 | 进入合作单 → 上传视频 → 提交作品 → 验证审核单创建 |
| 审核通过 | 进入审核队列 → 选择审核单 → 播放视频 → 通过 → 验证结算单创建 |
| 审核驳回 | 进入审核队列 → 选择审核单 → 驳回 → 填写原因 → 验证状态变为待修改 |
| 结算流程 | 进入结算页面 → 勾选待结算 → 批量标注已结算 → 验证统计卡更新 |
| 撤销结算 | 已结算记录 → 撤销 → 验证回退为待结算 |
| 完整流程 | 报名 → 入选 → 上传 → 审核 → 结算，端到端验证全链路 |
