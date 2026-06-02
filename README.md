# fe-gen2template

对话式前端项目脚手架，Claude Code 插件。一键生成完整的 Vue 3 + Vite + TypeScript 项目。

## 快速开始

```bash
# 安装
git clone git@git.zuoyebang.cc:toufang/fe-gen2template.git ~/code/fe-gen2template
claude plugin marketplace add ~/code/fe-gen2template
claude plugin install fe-gen2template

# 使用（任意目录下）
claude
> /scaffold
```

### 前提条件

- Claude Code、Bun、Git 已安装
- 内网 / VPN 连接（需访问 `git.zuoyebang.cc`）

### 对话选项

| # | 问题 | 选项 |
|---|------|------|
| 1 | 项目名称 | 自由输入，默认为当前目录名 |
| 2 | 输出目录 | 上一级目录（默认）/ 自定义路径 |
| 3 | 项目类型 | PC（Element Plus）/ H5（Vant 4）/ 两者 |
| 4 | 测试范围 | 仅单元测试 / 单元+E2E / 完整测试 |
| 5 | 状态管理 | 包含 Pinia / 不包含 |
| 6 | 内部 Skill | 包含 / 不包含 |

### 更新插件

```bash
cd ~/code/fe-gen2template && git pull
claude plugin marketplace add .
claude plugin install fe-gen2template
```

## 生成项目内容

### 工程基础

- Vue 3 + Vite + TypeScript
- Element Plus（PC）/ Vant 4（H5）/ 两者
- Tailwind CSS v4
- Axios 封装（拦截器、重试、取消、类型定义）
- Pinia 状态管理（可选）
- ESLint + Prettier
- Vitest 单元测试 / Playwright E2E（可选）
- .gitlab-ci.yml + Dockerfile

### AI 辅助开发（CLAUDE.md）

- **规范渐进加载** — 修改代码前按场景自动读取对应规范
- **路径分流** — 小任务 4 步快速路径，复杂任务走完整流程
- **验证门禁** — lint / typecheck / test / build 通过标准表格化
- **高风险变更清单** — 公共 API、权限、构建配置等需人工确认

### 规范文档（docs/）

9 份开发规范，覆盖组件、样式、测试、API 联调、代码审查、Git、验证、并行开发、验收用例生成。

## Slash Commands

所有生成的项目都包含：

| 命令 | 说明 |
|------|------|
| `/update-readme` | 同步 README.md 和 CLAUDE.md 与项目真实状态 |

此外，`/scaffold-sync` 是**插件级命令**，无需安装到项目，任意已生成项目都可直接调用，用于同步最新 Skill/规范。**注意**：`scaffold-sync` 从插件缓存读取内容，修改插件源码后需先重新安装插件（`claude plugin install fe-gen2template`）才能同步到最新。

选择"包含内部 Skill"（Q6）时额外包含：

| 命令 | 说明 |
|------|------|
| `/commit` | Git 提交并自动推送 |
| `/cr` | 代码审查（交互式修复 / 多 agent 对抗审查） |
| `/conventions` | 一次性预加载全部开发规范 |
| `/verify` | 执行本地验证清单并输出结果表格 |
| `/debug` 等 | 调试、架构设计、学习模式等 9 个命令 |

## 目录结构

```
fe-gen2template/
├── .claude-plugin/
│   ├── plugin.json           # 插件元信息
│   └── marketplace.json      # marketplace 注册
├── skills/fast-to-template/
│   ├── SKILL.md              # /scaffold 对话逻辑
│   ├── scripts/generate.sh   # 项目生成脚本
│   └── references/
│       ├── commands/          # Slash 命令
│       ├── skills/            # 子技能
│       ├── docs/              # 规范文档模板
│       ├── types/             # 项目类型模板（pc/h5/both）
│       └── extras/            # 额外模块（E2E 等）
├── scripts/install.sh
├── CLAUDE.md
└── README.md
```

## 开发指南

### 新增 Command

Command 是 Slash 命令，文件位于 `references/commands/<命令名>.md`，文件名即命令名。

```markdown
---
description: 命令的一句话描述
allowed-tools: Bash(git add:*), Bash(git status:*)
---

命令的完整指令内容。
```

### 新增 Skill

Skill 可被 Claude 自动触发或手动调用。每个技能一个目录，位于 `references/skills/<技能名>/SKILL.md`。

```markdown
---
name: my-skill
description: >-
  触发条件和使用场景。Claude 据此判断何时使用该技能。
---

技能的完整逻辑。如需额外资源文件，放在同目录下。
```

### 发布流程

修改 Command 或 Skill 后：

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install fe-gen2template
```

已生成的项目通过 `/scaffold-sync` 同步最新内容。

## 注意事项

- `scaffold-sync` 和 `update-readme` 无条件复制到所有项目，其余 Command/Skill 仅在 Q6 选"包含"时复制
- 分支命名格式为 `<type>/<name>`，不包含开发者名称
- `plugin.json` 中的 `version` 会写入目标项目的 CLAUDE.md，发版时记得更新
