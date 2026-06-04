# fe-gen2template

[![Plugin](https://img.shields.io/badge/plugin-1.1.0-blue.svg)](https://github.com/shouhutianshi/fe-gen2template)
[![tf-tech-spec](https://img.shields.io/badge/tf--tech--spec-1.3.0-green.svg)](skills/fast-to-template/references/skills/tf-tech-spec/SKILL.md)
[![scaffold-sync](https://img.shields.io/badge/scaffold--sync-1.1.0-green.svg)](skills/scaffold-sync/SKILL.md)

对话式前端项目脚手架，[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 插件。一键生成完整的 Vue 3 + Vite + TypeScript 项目，包含 AI 辅助开发配置、内部 Skill 和规范文档。

## 快速开始

```bash
# 安装（两行命令，无需 clone）
claude plugin marketplace add https://github.com/shouhutianshi/fe-gen2template
claude plugin install fe-gen2template

# 使用 — 任意目录下打开 Claude Code
claude
> /scaffold
```

**前提条件**：Claude Code、Bun 已安装。

### 一键安装脚本

```bash
curl -sL https://raw.githubusercontent.com/shouhutianshi/fe-gen2template/master/scripts/install.sh | bash
```

### 对话选项

运行 `/scaffold` 后会收集以下信息：

| # | 问题 | 选项 |
|---|------|------|
| 1 | 项目名称 | 自由输入，默认为当前目录名 |
| 2 | 输出目录 | 上一级目录（默认）/ 自定义路径 |
| 3 | 项目类型 | PC（Element Plus）/ H5（Vant 4）/ 两者 |
| 4 | 测试范围 | 仅单元测试 / 单元+E2E / 完整测试 |
| 5 | 状态管理 | 包含 Pinia / 不包含 |
| 6 | 内部 Skill | 包含 / 不包含 |

### 更新 / 卸载

```bash
# 更新到最新版（从 GitHub 重新安装）
claude plugin marketplace add https://github.com/shouhutianshi/fe-gen2template
claude plugin uninstall fe-gen2template && claude plugin install fe-gen2template

# 或在已生成的项目中直接同步最新 Skill/规范
> /scaffold-sync

# 卸载插件
claude plugin uninstall fe-gen2template
```

---

## 生成的项目包含什么

### 工程基础

- **Vue 3 + Vite + TypeScript** — 现代前端工程三件套
- **Element Plus / Vant 4 / 两者** — 按项目类型选择 UI 库
- **Tailwind CSS v4** — 原子化样式
- **Axios 封装** — 拦截器、重试、取消、类型定义
- **Pinia** — 状态管理（可选）
- **ESLint + Prettier** — 代码规范
- **Vitest / Playwright** — 单元测试 / E2E 测试（可选）
- **CI/CD** — `.gitlab-ci.yml` + `Dockerfile`

### AI 辅助开发配置（CLAUDE.md）

- **规范渐进加载** — 修改代码前按场景自动读取对应规范
- **路径分流** — 小任务 4 步快速路径，复杂任务走完整流程
- **验证门禁** — lint / typecheck / test / build 表格化标准
- **高风险变更清单** — 公共 API、权限、构建配置等需人工确认

### 开发规范文档（docs/conventions/）

9 份开发规范，覆盖完整开发生命周期：

| 规范 | 说明 |
|------|------|
| 组件规范 | 组件设计、命名、Props/Emits 定义 |
| 样式规范 | Tailwind 使用、CSS 变量、作用域 |
| 测试规范 | 单元测试、E2E 测试策略和写法 |
| API 联调 | 接口对接、Mock、错误处理 |
| 代码审查 | CR 流程和检查清单 |
| Git 规范 | 分支命名、提交信息格式 |
| 验证规范 | 上线前验证清单 |
| 并行开发 | 多人协作冲突避免 |
| 验收用例 | 验收测试用例生成 |

---

## Slash Commands

### 所有项目都包含

| 命令 | 说明 |
|------|------|
| `/update-readme` | 同步 README.md 和 CLAUDE.md 与项目真实状态 |

### 插件级命令（无需安装到项目）

| 命令 | 说明 |
|------|------|
| `/scaffold` | 对话式创建新前端项目 |
| `/scaffold-sync` | 同步最新 Skill/规范到已生成的项目（自动检测并刷新缓存） |

### 选择「包含内部 Skill」时额外包含

| 命令 | 说明 |
|------|------|
| `/commit` | Git 提交并自动推送 |
| `/cr` | 代码审查（交互式修复 / 多 agent 对抗审查） |
| `/conventions` | 一次性预加载全部开发规范 |
| `/investigate` | 并行调查 — 多个 Agent 同时排查不同方向 |
| `/gen-goal` | 生成可评审的目标，收敛任务方向 |
| `/debug` | 调试模式 |
| `/expert-mode` | 专家模式 |
| `/first-principles` | 第一性原理解释 |
| `/think-more` | 系统思维模板 |
| `/thinking-partner` | 批判性思考搭档 |
| `/research-brief-generator` | 研究简报生成器 |
| `/meta-suggestion-keyword-optimization` | 提示词优化器 |

---

## 插件内部 Skills

选择「包含内部 Skill」时，以下 Skills 会被复制到项目：

| Skill | 版本 | 说明 |
|-------|------|------|
| `tf-tech-spec` | 1.3.0 | 技术方案生成 — 从需求到技术方案的完整工作流 |
| `tf-fe-cr` | — | 代码审查 — 多维度检查清单和审查流程 |
| `kit-fe-arc` | — | 架构设计 — 根据规范和需求生成或更新全局架构协议 |
| `kit-fe-prd-split` | — | PRD 拆分 — 将产品需求拆解为高内聚低耦合的业务模块 |
| `kit-zyb-docs` | — | 文档获取 — 帮帮文档系统内容抓取（自动登录/Cookie 管理） |
| `kit-zyb-pms` | — | 项目管理 — 查询 PMS 需求关联的 Bug/缺陷列表 |

---

## 目录结构

```
fe-gen2template/
├── .claude-plugin/
│   ├── plugin.json              # 插件元信息
│   └── marketplace.json         # marketplace 注册
├── skills/
│   ├── fast-to-template/        # /scaffold 生成 Skill
│   │   ├── SKILL.md             # 对话流程和生成逻辑
│   │   ├── scripts/
│   │   │   ├── generate.sh      # 项目生成脚本
│   │   │   └── test-generate.sh # 生成测试
│   │   └── references/
│   │       ├── commands/         # 12 个 Slash 命令
│   │       ├── skills/           # 7 个子 Skill
│   │       ├── docs/             # mcp-setup.md
│   │       ├── types/            # 项目模板（pc/h5/both）
│   │       └── extras/           # E2E 模块
│   └── scaffold-sync/            # /scaffold-sync 同步 Skill
│       └── SKILL.md
├── scripts/
│   └── install.sh               # 一键安装脚本
├── CLAUDE.md
└── README.md
```

---

## 开发指南

### 修改插件

```bash
# 修改后验证 → 注册 → 安装
claude plugin validate .
claude plugin marketplace add .
claude plugin uninstall fe-gen2template && claude plugin install fe-gen2template
```

### 版本管理

修改任何文件后，同步递增以下位置的版本号：

| 文件 | 字段 |
|------|------|
| `.claude-plugin/plugin.json` | `version` |
| `package.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |
| `skills/scaffold-sync/SKILL.md` | frontmatter `version` |
| `skills/fast-to-template/references/skills/tf-tech-spec/SKILL.md` | frontmatter `version` |
| `README.md` | 顶部版本徽章 + Skills 表格中的版本列 |

> 其他 Skill（`tf-fe-cr`、`kit-fe-arc` 等）暂无 `version` 字段，后续补齐后加入本表。

递增规则：

- **minor**（1.1.0 → 1.2.0）：新增功能/章节/脚本
- **patch**（1.1.0 → 1.1.1）：修正措辞、小幅优化
- **major**（1.1.0 → 2.0.0）：删除章节、破坏性变更

### 新增 Command

Command 是 Slash 命令，位于 `references/commands/<命令名>.md`：

```markdown
---
description: 命令的一句话描述
version: 1.0.0
allowed-tools: Bash(git add:*), Bash(git status:*)
---

命令的完整指令内容。
```

### 新增 Skill

Skill 可被 Claude 自动触发或手动调用，位于 `references/skills/<技能名>/SKILL.md`：

```markdown
---
name: my-skill
version: 1.0.0
description: >-
  触发条件和使用场景。Claude 据此判断何时使用该技能。
---

技能的完整逻辑。如需额外资源文件，放在同目录下。
```

---

## 许可证

MIT
