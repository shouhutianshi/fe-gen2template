# Conventions 摘要索引

生成方案时按需读取本目录（`references/conventions/`）下的文档。以下是各文档的关键规则摘要和触发场景，方便判断何时需要加载哪个文档。

## 索引

| 文档 | 关键规则 | 何时读取 |
| --- | --- | --- |
| **components.md** | 文件名 kebab-case，import PascalCase；通用/业务/页面三层组件架构；单文件 >200 行拆分；`<script setup lang="ts">` + `<style scoped>`；Props 必须有 TypeScript 接口 | 设计组件、拆分功能、定义 props |
| **styles.md** | 设计令牌通过 `@theme` 定义（颜色/间距/圆角/阴影）；零 inline style；语义 class ≥3 次提取为 `@apply`；禁止硬编码色值和 `!important` | 涉及样式、布局、设计稿还原 |
| **api-integration.md** | `request.ts` 统一 Axios 实例；API 按 `src/api/modules/` 拆分；类型集中 `api/types.ts`；错误拦截器统一处理 | 涉及接口调用、前后端联调 |
| **acceptance-case-generation.md** | 页面还原三表（布局区块/交互状态/数据状态）；验收用例 `AcceptanceCase` 结构；页面还原用例（layer=component）；还原检查清单 | 写验收用例、还原检查、测试策略 |
| **testing.md** | Vitest + @vue/test-utils；`*.test.ts` 同目录；不测第三方组件内部；覆盖率 ≥70%；E2E 用 Playwright | 涉及测试策略、验证矩阵 |
| **code-review.md** | A/B/C 三级审查优先级（正确性 > 质量 > 约定）；排除项 | 审查前 |
| **verification.md** | lint / typecheck / test / coverage / build / smoke 六级验证；不裸跑 `tsc`；只跑部分验证时结论不扩大 | 验证阶段、写验证矩阵 |
| **git.md** | 分支 `<type>/<name>`；提交用 `/commit`；禁止 push 到 main/master | 分支创建、提交阶段 |
| **parallel-development.md** | 可并行：不同模块/不同测试域/只读；不可并行：同一文件集/共享契约未稳定/同时 merge | 多 agent 协作、拆任务 |

## 使用方式

1. **方案生成开始前**：读 `components.md` 和 `styles.md`，确保组件设计和样式方案符合约定。
2. **涉及接口联调时**：读 `api-integration.md`，确认 API 层结构和类型收口策略。
3. **写验收用例时**：读 `acceptance-case-generation.md`，确保覆盖页面还原和交互状态。
4. **写测试策略时**：读 `testing.md`，确认测试分层和文件组织。
5. **验证阶段**：读 `verification.md`，确认验证矩阵和命令来源。
6. **多 agent 协作时**：读 `parallel-development.md`，确认文件所有权和并行规则。
