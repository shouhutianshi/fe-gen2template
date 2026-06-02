---
name: scaffold-sync
description: "同步脚手架最新内容到当前项目。触发条件：用户说/scaffold-sync、同步脚手架、更新规范、同步skill、更新模板。将 fe-gen2template 插件中最新的 Skill、Commands 和 Docs 同步到当前已生成的前端项目。"
---

同步 fe-gen2template 脚手架的最新 Skill、Commands 和 Docs 到当前项目。

## 定位插件源目录

```bash
SYNC_SRC=$(ls -d ~/.claude/plugins/cache/fe-gen2template/fe-gen2template/*/skills/fast-to-template/references 2>/dev/null | sort -V | tail -1)
```

如果 `$SYNC_SRC` 为空，提示用户先安装插件：`claude plugin install fe-gen2template`。

## 同步内容

从 `$SYNC_SRC` 同步以下三项到当前项目：

| 源（插件） | 目标（项目） |
| --- | --- |
| `$SYNC_SRC/skills/*` | `.claude/skills/` |
| `$SYNC_SRC/commands/*.md` | `.claude/commands/` |
| `$SYNC_SRC/docs/mcp-setup.md` | `docs/mcp-setup.md` |
| `$SYNC_SRC/skills/tf-tech-spec/references/workflow.md` | `docs/workflow.md` |
| `$SYNC_SRC/skills/tf-tech-spec/references/conventions/*` | `docs/conventions/` |

## 同步策略

**直接覆盖**：skills、commands、docs 均由脚手架管理，用户不应直接修改这些文件。覆盖前输出变更摘要：

1. 列出新增文件（插件有、项目没有）
2. 列出更新文件（双方都有，内容不同）
3. 列出删除文件（项目有、插件没有）

输出摘要后询问用户确认，确认后执行同步。

**不动的文件**：`CLAUDE.md`、`AGENTS.md`、`.claude/settings.json`、`.claude/settings.local.json` 不在同步范围内。

## 同步后验证

```bash
ls .claude/skills/ .claude/commands/ docs/conventions/ docs/workflow.md docs/mcp-setup.md
```

## 版本记录

同步完成后，读取插件 `package.json` 的 version，更新 `CLAUDE.md` 末尾的版本号为最新插件版本。
