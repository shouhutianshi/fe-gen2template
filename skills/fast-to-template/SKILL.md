---
name: scaffold
description: "对话式前端项目脚手架。触发条件：用户执行 /scaffold、创建新项目、初始化前端工程、搭建前端框架、新建 Vue 项目、生成 H5 页面、搭个后台管理、帮我初始化前端、新建一个页面工程。当用户提到任何创建前端项目的意图时都应使用此 skill，即使用户没有明确提到'脚手架'或'scaffold'。通过对话收集信息后一键生成完整 Vue 3 + Vite + TypeScript 项目，包含 AI 辅助开发配置、内部 Skill、规范文档。"
---

# fe-gen2template — 前端项目脚手架

通过对话式交互一键生成完整的前端项目框架。

## 环境检测（必须在对话前执行）

开始前必须检测：

1. **目录状态**
   - 空目录 → 创建新项目
   - 已有 `package.json` → 进入"已有项目追加 AI 配置"模式

2. **依赖检测**
   ```bash
   which bun
   claude plugin list 2>/dev/null | grep superpowers
   ```
   - bun 不可用 → 提示安装 bun
   - superpowers 未安装 → 提示：`claude plugin install superpowers`

## 对话流程

### Q1: 项目名称

使用 AskUserQuestion，文本输入，默认值为当前目录名。

### Q2: 输出目录

使用 AskUserQuestion，选项：
- 上一级目录（推荐）
- 自定义路径

默认：上一级目录（`..`）。项目将创建为 `<输出目录>/<项目名称>`。

### Q3: 项目类型

使用 AskUserQuestion，选项：
- PC（Element Plus）
- H5（Vant 4）
- PC + H5

默认：PC

### Q4: 测试范围

使用 AskUserQuestion，选项：
- 仅单元测试（Vitest）
- 单元 + E2E（Vitest + Playwright）
- 完整测试金字塔（单元 + 组件 + 集成 + E2E）

默认：仅单元测试

### Q5: 状态管理

使用 AskUserQuestion，选项：
- 包含 Pinia（推荐）
- 不需要

默认：包含 Pinia

### Q6: 内部 Skill

使用 AskUserQuestion，选项：
- 包含（推荐）
- 不包含

默认：包含

## 参数映射

| 参数 | 来源 | 值 |
|---|---|---|
| --name | Q1 | 项目名称 |
| --output | Q2 | 输出目录，默认 `..`（上一级） |
| --type | Q3 | pc / h5 / both |
| --test-scope | Q4 | unit / unit+e2e / full |
| --pinia | Q5 | true / false |
| --skills | Q6 | true / false |
| --username | git config user.name | 默认 "dev" |
| --version | 读取 plugin.json version | 当前版本 |

## 生成

收集完答案后，执行技能目录下 `scripts/generate.sh`，传入所有参数。脚本会自动从 `plugin.json` 读取版本号（如果 --version 未指定）。

脚本内部流程：
1. `cp -r types/$TYPE/` — 复制完整类型模板
2. 处理 Pinia（替换 main.ts）、E2E（添加 playwright）、Skills/Commands
3. 复制 docs、skills、commands
4. `sed` 替换模板变量（`{{PROJECT_NAME}}`、`__PROJECT_NAME__` 用于 Vue 文件）
5. `python3` 清理 package.json 中未使用的依赖
6. 从模板生成 CLAUDE.md、AGENTS.md、README.md

## 已有项目追加模式

当检测到已有 `package.json` 时，由 Claude（而非脚本）手动处理：

1. **冲突检测**：列出将要创建的文件，逐一检查是否已存在
2. **备份**：`CLAUDE.md` → `CLAUDE.md.bak.<timestamp>`
3. **合并**：`.claude/settings.json` 保留用户已有配置，追加新配置项
4. **只追加**：仅复制 CLAUDE.md、AGENTS.md、`.claude/`、`docs/`，不修改已有代码

## 初始化验证

generate.sh 完成后，由 Claude 执行验证：

```bash
cd <项目名>
bun install
bun run typecheck
bun run lint
bun run build
git init && git add -A && git commit -m "chore: init project by fe-gen2template v<版本>"
```

如果任何步骤失败，报告错误并给出修复建议。

## 生成后指引

验证全部通过后，告知用户后续步骤：

```markdown
✅ 项目 <名称> 已生成并通过验证！

后续步骤：
- 启动开发：cd <名称> && bun run dev
- 运行测试：bun run test
- 运行构建：bun run build
- 配置 MCP：参考 docs/mcp-setup.md
- Python 依赖（如包含内部 Skill）：pip install -r .claude/skills/kit-zyb-docs/scripts/requirements.txt
```
