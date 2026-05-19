# fe-gen2template

前端项目脚手架 Claude Code 插件。通过对话式交互一键生成完整的 Vue 3 + Vite + TypeScript 项目框架。

## 前提条件

- 内网 / VPN 连接（需访问 `git.zuoyebang.cc`）
- Git 已安装，SSH key 已配置
- Claude Code 已安装
- Bun 已安装

## 安装

```bash
# 1. 克隆仓库（HTTPS 备选：https://git.zuoyebang.cc/toufang/fe-gen2template.git）
git clone git@git.zuoyebang.cc:toufang/fe-gen2template.git ~/code/fe-gen2template

# 2. 注册并安装插件
claude plugin marketplace add ~/code/fe-gen2template
claude plugin install fe-gen2template
```

## 使用

在任何目录打开 Claude Code，执行：

```
/scaffold
```

回答 6 个问题后自动生成完整项目：

| # | 问题 | 选项 |
|---|------|------|
| 1 | 项目名称 | 自由输入，默认为当前目录名 |
| 2 | 输出目录 | 上一级目录（默认）/ 自定义路径 |
| 3 | 项目类型 | PC（Element Plus）/ H5（Vant 4）/ 两者 |
| 4 | 测试范围 | 仅单元测试 / 单元+E2E / 完整测试 |
| 5 | 状态管理 | 包含 Pinia / 不包含 |
| 6 | 内部 Skill | 包含 / 不包含 |

## 更新

```bash
cd ~/code/fe-gen2template && git pull
claude plugin marketplace add ~/code/fe-gen2template
claude plugin install fe-gen2template
```

## 生成项目包含

- Vue 3 + Vite + TypeScript 完整工程
- Element Plus（PC）/ Vant 4（H5）/ 两者
- Tailwind CSS v4
- Axios 封装（拦截器、重试、取消、类型定义）
- Pinia 状态管理（可选）
- ESLint + Prettier
- Vitest 单元测试 / Playwright E2E（可选）
- .gitlab-ci.yml + Dockerfile
- CLAUDE.md — AI 辅助开发配置，包含：
  - **规范渐进加载** — 修改代码前按场景自动读取对应规范（组件、样式、测试、API 等）
  - **路径分流** — 小任务走快速路径（4 步），复杂任务走完整路径
  - **验证门禁** — lint / typecheck / test / build 通过标准表格化
  - **高风险变更清单** — 公共 API、权限、构建配置等需人工确认
- Slash Commands：
  - `scaffold-sync` — 从插件同步最新 Skill/规范到已生成的项目
  - `update-readme` — 同步 README.md 和 CLAUDE.md 与项目真实状态
  - `conventions` — 一次性预加载全部开发规范
  - `verify` — 执行本地验证清单并输出结果表格
  - `commit`、`debug` 等 13 个常用命令（仅 `--skills` 模式）
- 规范文档（docs/conventions/）— 组件、样式、测试、API 联调、代码审查、Git、验证、并行开发、验收用例生成

## 目录结构

```
fe-gen2template/
├── .claude-plugin/
│   ├── plugin.json           # 插件元信息（名称、版本、作者）
│   └── marketplace.json      # marketplace 注册信息
├── skills/
│   └── fast-to-template/
│       ├── SKILL.md          # /scaffold 主技能逻辑
│       ├── scripts/
│       │   └── generate.sh   # 项目生成脚本
│       └── references/
│           ├── commands/      # Slash 命令（.md 文件）
│           ├── skills/        # 子技能（目录 + SKILL.md）
│           ├── docs/          # 规范文档模板
│           ├── types/         # 项目类型模板（pc/h5/both）
│           └── extras/        # 额外模块（E2E 等）
├── scripts/
│   └── install.sh
├── CLAUDE.md
└── README.md
```

## 新增 Command

Command 是 Slash 命令，用户通过 `/命令名` 触发。

### 文件位置

`skills/fast-to-template/references/commands/<命令名>.md`

文件名即命令名（如 `commit.md` → `/commit`）。

### 文件格式

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*)
description: 命令的一句话描述，用于 / 触发时的提示
---

命令的完整指令内容，告诉 Claude 做什么。
支持 `!` 前缀动态插值，如 !`git status` 会在执行时替换为实际输出。
```

YAML frontmatter 字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `description` | 否 | 命令描述，用于 `/` 列表中的提示 |
| `allowed-tools` | 否 | 限制命令可使用的工具，格式 `Tool(pattern:)` |

### 示例

参考现有命令：`commit.md`（Git 提交推送）、`verify.md`（本地验证清单）、`conventions.md`（加载规范）。

## 新增 Skill

Skill 是可被 Claude 自动触发或手动调用的子技能，用于特定工作流（如技术方案生成、PRD 读取）。

### 文件位置

`skills/fast-to-template/references/skills/<技能名>/SKILL.md`

每个技能一个独立目录，目录名即技能标识。

### 文件格式

```markdown
---
name: my-skill
description: >-
  触发条件和使用场景描述。Claude 根据此描述判断何时使用该技能。
---

# 技能名称

技能的完整逻辑：使用时机、工作流程、接口说明、错误处理等。
如有额外资源文件，放在同目录下，用相对路径引用。
```

YAML frontmatter 字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 技能标识，全局唯一 |
| `description` | 是 | 触发条件和使用场景，Claude 据此自动匹配 |

### 附带资源

技能目录可包含额外文件，整个目录会被递归复制到目标项目：

```
skills/fast-to-template/references/skills/tf-tech-spec/
├── SKILL.md                          # 技能定义
└── references/
    ├── tech-spec-template.md         # 技术方案模板
    └── workflow.md                   # 工作流定义
```

### 示例

参考现有技能：`tf-tech-spec/`（技术方案生成）、`kit-zyb-docs/`（帮帮文档读取）、`kit-fe-arc/`（架构概览）。

## 安装流程（新增或修改 Command/Skill 后必做）

```bash
cd ~/code/fe-gen2template

# 1. 校验插件结构
claude plugin validate .

# 2. 注册到 marketplace
claude plugin marketplace add .

# 3. 安装插件
claude plugin install fe-gen2template
```

无需修改 `plugin.json` 或 `marketplace.json`，插件按目录结构自动发现 Command 和 Skill。

## 注意事项

- Command 和 Skill **仅在用户选择"包含内部 Skill"（Q6）时**才会被复制到目标项目，对应 `generate.sh` 中 `INCLUDE_SKILLS=true` 的分支。`scaffold-sync` 和 `update-readme` 例外，无条件复制到所有项目。
- 修改已有 Command/Skill 后，已生成的项目可通过 `/scaffold-sync` 同步最新内容。
- 分支命名格式为 `<type>/<name>`（如 `feat/login-module`），不包含开发者名称。
- `plugin.json` 中的 `version` 会在 `generate.sh` 中被读取并写入目标项目的 `CLAUDE.md` 和 `README.md`，发版时记得更新。
