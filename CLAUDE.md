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
