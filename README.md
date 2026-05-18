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
  - `conventions` — 一次性预加载全部开发规范
  - `verify` — 执行本地验证清单并输出结果表格
  - `commit`、`debug` 等 13 个常用命令
- 规范文档（docs/conventions/）— 组件、样式、测试、API 联调、代码审查、Git、验证、并行开发、验收用例生成
