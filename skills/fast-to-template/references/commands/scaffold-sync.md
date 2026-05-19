同步 fe-gen2template 脚手架的最新 Skill、Commands 和 Docs 到当前项目。

## 定位插件源目录

```bash
# 找到最新版本的插件安装路径
SYNC_SRC=$(ls -d ~/.claude/plugins/cache/fe-gen2template/fe-gen2template/*/skills/fast-to-template/references 2>/dev/null | sort -V | tail -1)
```

如果 `$SYNC_SRC` 为空，提示用户先安装插件：`claude plugin install fe-gen2template`。

## 同步内容

从 `$SYNC_SRC` 同步以下三项到当前项目：

| 源（插件） | 目标（项目） |
| --- | --- |
| `$SYNC_SRC/skills/*` | `.claude/skills/` |
| `$SYNC_SRC/commands/*.md` | `.claude/commands/` |
| `$SYNC_SRC/docs/*` | `docs/` |

## 同步策略

**直接覆盖**：skills、commands、docs 均由脚手架管理，用户不应直接修改这些文件。覆盖前输出变更摘要：

1. 列出新增文件（插件有、项目没有）
2. 列出更新文件（双方都有，内容不同）
3. 列出删除文件（项目有、插件没有）

输出摘要后询问用户确认，确认后执行同步。

**不动的文件**：`CLAUDE.md`、`AGENTS.md`、`.claude/settings.json`、`.claude/settings.local.json` 不在同步范围内。

## 同步后验证

```bash
# 确认 skills 目录非空
ls .claude/skills/

# 确认 commands 目录非空
ls .claude/commands/

# 确认 docs 目录完整
ls docs/conventions/ docs/workflow.md docs/mcp-setup.md
```

## 版本记录

同步完成后，读取插件 `package.json` 的 version，更新 `CLAUDE.md` 最后一行的版本号：

```
本项目由 fe-gen2template vX.Y.Z 生成。
```

改为最新的插件版本。
