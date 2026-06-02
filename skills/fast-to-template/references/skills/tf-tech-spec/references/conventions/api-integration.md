# 前后端联调规范

## API 层结构

```
src/api/
├── request.ts          # Axios 实例（拦截器、重试、401）
├── types.ts            # 通用类型（ApiResponse<T>, ApiError, RequestConfig）
└── modules/            # 按业务模块拆分
    ├── user.ts
    └── order.ts
```

## 请求封装规范

- 使用 `src/api/request.ts` 导出的 `request` 实例，不自行创建 axios 实例
- API 函数统一放在 `src/api/modules/` 下按模块拆分
- 每个模块的函数签名使用 TypeScript 严格类型

```typescript
// src/api/modules/user.ts
import { request } from '../request'
import type { ApiResponse } from '../types'

interface UserInfo {
  id: number
  name: string
  avatar: string
}

export function getUserInfo(id: number) {
  return request.get<ApiResponse<UserInfo>>(`/api/user/${id}`)
}

export function updateUserProfile(data: Partial<UserInfo>) {
  return request.put<ApiResponse<UserInfo>>('/api/user/profile', data)
}
```

## YApi 联调流程

使用 `yapi` MCP 查接口文档，确认：

1. **请求对齐** — 方法、路径、参数名与 YApi 文档一致
2. **响应对齐** — 字段名、类型、嵌套结构与文档匹配
3. **必填/选填** — 参数的 required 标记处理正确
4. **错误码** — 业务错误码（code !== 0/200）有对应 UI 提示
5. **鉴权** — 需要 token 的接口走 request 拦截器自动注入

## 环境变量

```
# .env.development
VITE_API_BASE_URL=http://localhost:3000

# .env.production
VITE_API_BASE_URL=https://api.example.com
```

- `request.ts` 通过 `import.meta.env.VITE_API_BASE_URL` 读取
- 不在代码中硬编码任何 API 地址

## Mock 策略

开发阶段可用 Vite 的 `server.proxy` 代理到后端：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
    },
  },
}
```

## 错误处理

- 网络错误、超时、401 由 `request.ts` 拦截器统一处理
- 业务错误（code !== 0/200）在调用处 try-catch 处理
- 不在每个 API 函数中重复写错误处理逻辑
