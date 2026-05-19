# 组件开发规范

## 文件组织与命名

### 目录结构

```
src/
├── components/          # 通用组件（跨页面复用）
│   ├── BaseButton.vue
│   ├── BaseModal.vue
│   └── DataEmpty.vue
├── composables/         # 可复用逻辑（useXxx）
│   ├── useLoading.ts
│   └── usePagination.ts
└── views/
    └── Home/
        └── components/  # 页面私有组件（仅当前页面使用）
            └── HomeHeader.vue
```

- 通用组件放 `src/components/`，页面私有组件放 `views/<Page>/components/`
- PC+H5 项目：PC 私有组件放 `src/pc/views/<Page>/components/`，H5 同理

### 命名规范

- 组件文件：`PascalCase`，如 `UserAvatar.vue`、`BaseButton.vue`
- 通用组件以功能前缀区分：`Base`（基础）、`App`（全局布局）、`Data`（数据展示）
- composable 文件：`camelCase`，以 `use` 开头，如 `useLoading.ts`
- 组件 name：`<script setup>` 中不需要手动声明，依赖文件名自动推断

### 单文件组件组织顺序

```vue
<script setup lang="ts">
// 1. 类型导入
// 2. composable 导入
// 3. 组件导入
// 4. props/emits 定义
// 5. composable 调用
// 6. 响应式状态
// 7. 计算属性
// 8. 生命周期钩子
// 9. 方法
</script>

<template>
  <!-- 模板 -->
</template>

<style scoped>
/* 样式 */
</style>
```

- 始终使用 `<script setup lang="ts">`
- 始终使用 `<style scoped>`，避免全局样式污染

## Props / Events / Slots 规范

### Props

```typescript
// 使用 withDefaults + 类型声明，不使用 runtime defineProps
interface Props {
  title: string
  count?: number
  items: string[]
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
})

// 需要响应式时使用 toRefs/toRef
const { title } = toRefs(props)
```

- 必须定义 TypeScript 接口，不用运行时声明
- 可选 prop 必须提供默认值
- 避免用 `Object` / `Array` 默认值工厂之外的任何 `any`

### Events

```typescript
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', payload: { name: string; age: number }): void
  (e: 'delete', id: number): void
}>()
```

- 使用类型声明语法，不用运行时数组语法
- 事件名用 `camelCase`（模板中用 `@kebab-case`）
- 自定义 v-model：`update:modelValue`，支持命名 `update:xxx`

### Slots

```vue
<!-- 定义 -->
<slot name="header" :data="headerData" />
<slot /> <!-- 默认插槽 -->

<!-- 使用 -->
<template #header="{ data }">
  <span>{{ data.title }}</span>
</template>
<template #default>
  <p>默认内容</p>
</template>
```

- 具名插槽用 `#name` 缩写
- 作用域插槽暴露最小必要数据

### defineExpose

```typescript
// 只暴露必要的公共方法，不暴露内部状态
defineExpose({
  refresh,
  reset,
})
```

- 仅在父组件需要命令式调用时使用
- 优先通过 props/events 通信，expose 是最后手段

## Composable 规范

### 基本结构

```typescript
// useXxx.ts
import { ref, computed, onUnmounted } from 'vue'

export function useXxx(initialValue: number = 0) {
  // 1. 响应式状态
  const count = ref(initialValue)

  // 2. 计算属性
  const doubled = computed(() => count.value * 2)

  // 3. 方法
  function increment() {
    count.value++
  }

  // 4. 副作用（自动清理）
  const timer = setInterval(() => {}, 1000)
  onUnmounted(() => clearInterval(timer))

  // 5. 返回值：用对象，不用数组
  return {
    count,
    doubled,
    increment,
  }
}
```

### 约定

- 文件命名：`useXxx.ts`，放在 `src/composables/`
- 参数：接收 `Ref<T>` 或 `T`，文档中注明
- 返回值：始终返回对象（具名解构），不用数组
- 副作用：在 composable 内用 `onUnmounted` / `watchEffect` 自动清理
- 如果依赖组件实例（如 `onMounted`），在 JSDoc 中注明"必须在 setup 中调用"
- 纯逻辑无 DOM 依赖的 composable 优先考虑可测试性

### 常用 composable 示例

```typescript
// useLoading.ts
export function useLoading(initial = false) {
  const loading = ref(initial)
  const start = () => (loading.value = true)
  const stop = () => (loading.value = false)
  const withLoading = async <T>(fn: () => Promise<T>): Promise<T> => {
    start()
    try { return await fn() } finally { stop() }
  }
  return { loading, start, stop, withLoading }
}
```

## 组件拆分原则

### 何时拆分

| 信号 | 动作 |
|------|------|
| 单文件超过 200 行（不含 style） | 拆分 |
| 模板中同一区块超过 30 行 | 提取为子组件 |
| 同一逻辑在 2+ 页面复用 | 提取为通用组件或 composable |
| 组件职责 > 1 个 | 按职责拆分 |

### 分层策略

```
通用组件（src/components/）     ← 无业务逻辑，纯 UI 展示
    ↑
业务组件（views/X/components/） ← 包含业务逻辑，但仅限当前页面
    ↑
页面组件（views/X/index.vue）   ← 组合层，负责数据获取和布局
```

- 通用组件：零业务逻辑，所有数据通过 props/slots 传入，纯展示
- 业务组件：可包含特定业务逻辑（如调用某个 API），但仅限当前页面上下文
- 页面组件：组合层，负责数据获取、状态编排和子组件组装
- composable：当逻辑需要在多个组件间共享时提取，独立于组件层级

### 拆分检查清单

- [ ] 子组件通过 props 接收所有外部数据
- [ ] 子组件通过 emit 向上通信，不直接修改父组件状态
- [ ] 每个组件可独立理解，不需要阅读父组件代码
- [ ] 通用组件不依赖任何业务 API 或 store
