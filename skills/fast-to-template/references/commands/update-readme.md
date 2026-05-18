# 更新 README.md

同步 **README.md**（及按需 **CLAUDE.md**）与仓库真实结构、依赖与脚本。

## Claude 执行要点（精简）

1. **读配置**：根与各 workspace 包 `package.json`、`pnpm-workspace.yaml`；有 Nuxt 时读 `apps/web/nuxt.config.ts` 等，**勿假设根目录存在 `vite.config.ts`**。
2. **扫目录**：`apps/`、`packages/`、`config/`、与文档相关的 `.claude/` 路径，更新「目录结构」树。
3. **对清单**：按 [references 完整检查清单](./references/update-readme.md) 核对 README 各章节；只修改与现状不一致处。
4. **CLAUDE.md**：若需创建/更新，写仓库约定与 Claude 专用指引，避免重复 README 全文（可链到 README 章节）。

**约束**：保持现有文档风格；脚本与路径可执行、可验证；不编造未出现的 env 或字段。

## 输出

- 更新后的 `README.md`（必选）。
- `CLAUDE.md`（在已存在或用户明确要求时更新）。

**README 应覆盖哪些章节、Schema/脚本/环境变量如何核对** → 见 [references/update-readme.md](./references/update-readme.md)。
