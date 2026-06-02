# 样式规范（Tailwind CSS v4）

## 核心原则

1. **零 inline style** — 所有样式通过 Tailwind utility class 或 `@apply` 实现，禁止 `style="..."` 和 `:style="{}"`
2. **设计令牌归一** — 颜色、间距、字号、圆角等通过 `@theme` 指令在 CSS 中统一定义，禁止硬编码魔法值
3. **语义 class > 原子 class** — 复用 ≥3 次的组合提取为 `@apply` 语义 class，存入 `src/styles/` 对应文件
4. **组件样式内聚** — 组件样式写在 `<style scoped>` 中用 `@apply`，不跨组件穿透

## Tailwind CSS v4 配置

项目使用 Tailwind CSS v4 的 CSS-first 模式，**不需要** `tailwind.config.ts` 配置文件。

入口文件 `src/styles/index.css`：

```css
@import "tailwindcss";

/* 设计令牌通过 @theme 定义 */
@theme {
  --color-status-success: oklch(0.72 0.19 142);
  --color-status-warning: oklch(0.76 0.15 70);
  --color-status-danger: oklch(0.63 0.2 25);
  --color-status-info: oklch(0.7 0.05 250);

  --spacing-gap-xs: 4px;
  --spacing-gap-sm: 8px;
  --spacing-gap-md: 12px;
  --spacing-gap-lg: 16px;
  --spacing-gap-xl: 24px;
  --spacing-gap-2xl: 32px;

  --font-size-stat: 28px;
  --font-size-caption: 12px;

  --radius-card: 8px;
  --radius-tag: 4px;

  --shadow-card: 0 2px 12px rgba(0, 0, 0, 0.08);
  --shadow-card-hover: 0 4px 16px rgba(0, 0, 0, 0.12);
}
```

Vite 插件使用 `@tailwindcss/vite`（已配置在 `vite.config.ts`）。

## 设计令牌

所有令牌通过 `@theme` 指令在 `src/styles/index.css` 中定义。

### 间距

| CSS 变量 | Tailwind 用法 | 值 | 用途 |
| --- | --- | --- | --- |
| `--spacing-gap-xs` | `gap-gap-xs` / `p-gap-xs` | 4px | 图标与文字间距 |
| `--spacing-gap-sm` | `gap-gap-sm` / `p-gap-sm` | 8px | 表单项间距 |
| `--spacing-gap-md` | `gap-gap-md` / `p-gap-md` | 12px | 筛选栏控件间距 |
| `--spacing-gap-lg` | `gap-gap-lg` / `p-gap-lg` | 16px | 区块间距、卡片 padding |
| `--spacing-gap-xl` | `gap-gap-xl` / `p-gap-xl` | 24px | 大区块分隔 |
| `--spacing-gap-2xl` | `gap-gap-2xl` / `p-gap-2xl` | 32px | 页面区块分隔 |

### 颜色

| CSS 变量 | Tailwind 用法 | 用途 |
| --- | --- | --- |
| `--color-status-success` | `bg-status-success` / `text-status-success` | 活跃、已发布 |
| `--color-status-warning` | `bg-status-warning` / `text-status-warning` | 延期、待审核 |
| `--color-status-danger` | `bg-status-danger` / `text-status-danger` | 异常、已驳回 |
| `--color-status-info` | `bg-status-info` / `text-status-info` | 已结束 |

### 圆角 & 阴影

| CSS 变量 | Tailwind 用法 | 值 |
| --- | --- | --- |
| `--radius-card` | `rounded-card` | 8px |
| `--radius-tag` | `rounded-tag` | 4px |
| `--shadow-card` | `shadow-card` | `0 2px 12px rgba(0,0,0,0.08)` |
| `--shadow-card-hover` | `shadow-card-hover` | `0 4px 16px rgba(0,0,0,0.12)` |

## 语义 Class 提取规则

当 utility 组合出现 ≥3 次时，在 `src/styles/index.css` 中用 `@layer components` 提取：

```css
/* src/styles/index.css */
@import "tailwindcss";

@theme {
  /* 令牌定义... */
}

@layer components {
  .stat-card {
    @apply flex flex-col items-center gap-gap-xs p-gap-lg rounded-card cursor-pointer
           transition-all duration-200;
  }
  .stat-card--active {
    @apply border-b-2 border-b-blue-500;
  }
  .filter-bar {
    @apply flex flex-wrap gap-gap-md mb-gap-lg;
  }
  .kol-table__link {
    @apply text-blue-500 hover:underline cursor-pointer;
  }
}
```

## 文件组织

```
src/styles/
└── index.css                 # 唯一入口：@import "tailwindcss" + @theme + @layer components
```

Tailwind v4 推荐单文件管理，不需要拆分多个 SCSS 文件。语义 class 通过 `@layer components` 组织在同一文件中。

## 使用规范

**推荐**：
```html
<el-input v-model="q" class="w-[260px]" placeholder="搜索" clearable />
<el-select v-model="status" class="w-[160px]" placeholder="全部状态" clearable />
<el-card class="stat-card" @click="filterByStatus('ongoing')">
  <span class="text-[28px] font-semibold text-gray-800">{{ count }}</span>
</el-card>
```

**禁止**：
```html
<!-- 禁止 inline style -->
<el-input style="width: 260px" />
<!-- 禁止硬编码颜色 -->
<span style="color: #f56c6c">异常</span>
<!-- 禁止魔法数字间距 -->
<div style="margin-top: 16px" />
```
