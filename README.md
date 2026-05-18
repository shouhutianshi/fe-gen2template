# fe-influencers

前端项目脚手架 Claude Code 插件。通过对话式交互一键生成完整的 Vue 3 + Vite + TypeScript 项目框架。

## 前提条件

- 内网 / VPN 连接（需访问 `git.zuoyebang.cc`）
- Git 已安装，SSH key 已配置
- Claude Code 已安装
- Bun 已安装

## 安装

```bash
# 1. 克隆仓库（HTTPS 备选：https://git.zuoyebang.cc/toufang/fe-influencers.git）
git clone git@git.zuoyebang.cc:toufang/fe-influencers.git ~/code/fe-influencers

# 2. 注册并安装插件
claude plugin marketplace add ~/code/fe-influencers
claude plugin install fe-influencers
```

## 使用

在任何目录打开 Claude Code，执行：

```
/scaffold
```

回答 5 个问题后自动生成完整项目。

## 更新

```bash
cd ~/code/fe-influencers && git pull
claude plugin marketplace add ~/code/fe-influencers
claude plugin install fe-influencers
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
- CLAUDE.md + AGENTS.md（AI 辅助开发配置）
- 内部 Skill（kit-zyb-docs、kit-fe-arc 等 6 个）
- Slash Commands（commit、debug 等 13 个）
- 规范文档（docs/conventions/）
