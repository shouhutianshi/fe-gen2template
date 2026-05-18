# 分支与提交规范

## 分支规范

格式：`<type>/{{USERNAME}}/<name>`

| type | 用途 |
| --- | --- |
| `feat` | 新功能或需求开发 |
| `bugfix` | 普通缺陷修复 |
| `hotfix` | 线上紧急修复 |
| `refactor` | 不改变行为的重构 |
| `docs` | 文档变更 |
| `chore` | 工程化、配置、依赖、脚本等 |

示例：`feat/dev-user/homework-module`、`bugfix/dev-user/login-error`

规则：
- `name` 使用需求 ID、Bug ID 或英文 kebab-case 摘要，避免空格和特殊字符
- 禁止直接 push 到 `main` / `master`
- 禁止 `--force`，必须强推时用 `--force-with-lease` 且人工确认

## 提交规范

使用 `/commit` 自动生成并推送，格式：`<type>: <中文描述>`

| type | 用途 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 缺陷修复 |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `style` | 代码风格（不影响逻辑） |
| `docs` | 文档 |
| `chore` | 工程/配置/依赖 |

示例：`feat: 添加作业模块列表页`、`fix: 修复登录态过期未跳转`
