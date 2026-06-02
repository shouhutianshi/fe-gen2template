# 验证规范

完成声明前必须有新鲜验证证据，按变更风险逐级扩展：

| 验证项 | 命令 | 通过标准 |
| --- | --- | --- |
| Lint | `bun run lint` | 0 error |
| TypeCheck | `bun run typecheck` | 0 error |
| Test | `bun run test` | 0 failed |
| Coverage | `bun run test:coverage` | ≥70% statements |
| Build | `bun run build` | 构建成功 |
| E2E（可选） | `bun run test:e2e` | 关键流程全部通过 |
| 冒烟 | Browser / Chrome | 核心路径可完成，控制台无阻断 error |

规则：
- 不裸跑 `tsc`，统一用项目脚本
- 命令以 `package.json` 和 CI 配置为准，不硬编码
- 只跑了部分验证时，结论只能说"已通过 X，Y 未验证"
- E2E 仅在 CI 或完整验证阶段运行，日常开发不强制本地跑
