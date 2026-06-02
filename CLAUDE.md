# CLAUDE.md

本仓库是 fe-gen2template Claude Code 插件。通过 `/scaffold` 命令对话式生成完整的前端项目框架。

远程仓库：`https://git.zuoyebang.cc/toufang/fe-gen2template`

## 结构

- `.claude-plugin/` — 插件注册（plugin.json + marketplace.json）
- `skills/fast-to-template/` — 脚手架 Skill
  - `SKILL.md` — 对话流程和生成逻辑
  - `references/` — 模板和内容定义
- `scripts/` — 安装脚本

## 开发

修改 `skills/fast-to-template/` 下的文件，然后本地验证：

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install fe-gen2template
```

## 版本管理

修改 `skills/fast-to-template/references/skills/tf-tech-spec/` 下任何文件时，必须同时递增该目录 SKILL.md frontmatter 中的 `version` 字段：
- 新增功能/章节/脚本/参考文档 → minor 递增（1.1.0 → 1.2.0）
- 修正措辞/补全缺失/小幅优化 → patch 递增（1.0.0 → 1.0.1）
- 删除章节/破坏性变更 workflow → major 递增（1.0.0 → 2.0.0）

<!-- scaffold-sync version: 1.0.0 -->
