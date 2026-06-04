---
name: scaffold-sync
version: 1.1.0
description: >-
  同步脚手架最新内容到当前项目。将 fe-gen2template 插件中最新的 Skill、Commands 和 Docs
  同步到当前已生成的前端项目。触发条件：用户说同步脚手架、更新规范、同步 skill、更新模板、
  scaffold-sync、sync scaffold、脚手架同步、脚手架更新、规范更新、skill 更新、模板更新、
  更新一下项目规范、项目里的 skill 过时了、把最新的脚手架内容拉下来、同步一下、更新脚手架。
  当用户提到项目中的规范或 skill 版本落后、需要与最新脚手架对齐时也使用本 skill。
  不用于：首次创建项目（用 /scaffold）、同步后端代码或非脚手架管理的文件。
---

同步 fe-gen2template 插件的最新 Skill、Commands 和 Docs 到当前项目。与 generate.sh 的复制范围保持一致。

## 前置检查

1. 确认当前项目由脚手架生成：检查 `CLAUDE.md` 是否包含 `scaffold-sync version` 标记或 `fe-gen2template` 关键字。未找到则提醒用户先 `/scaffold` 生成项目，询问是否继续
2. 检查 `.claude/skills/` 是否存在：
   - 不存在 → 询问用户是否补充同步 skills（初始生成时可能未选 `--skills`），同意后走「初始同步」
   - 存在 → 走「增量同步」

## 缓存刷新检查

在定位缓存路径之前，检查是否有插件更新，确保同步最新版本。支持两种刷新方式。

### 1. 检测是否需要刷新

```bash
REPO_DIR=~/code/fe-gen2template
```

- `$REPO_DIR` 存在且是 git 仓库 → 走**本地仓库刷新**
- 不存在 → 走**GitHub 直接刷新**

两种方式都需要先检测当前缓存版本与远程最新版本的差异。如果无法检测差异（如网络不通），询问用户是否强制刷新。

### 2. 本地仓库刷新

```bash
cd "$REPO_DIR"
git fetch origin master 2>/dev/null
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)
```

- `LOCAL` = `REMOTE` → 缓存已是最新，跳过刷新
- `LOCAL` ≠ `REMOTE` → 有新提交，询问用户是否刷新缓存

用户确认后执行：

```bash
cd "$REPO_DIR" && git pull --ff-only origin master
claude plugin marketplace add "$REPO_DIR"
claude plugin uninstall fe-gen2template && claude plugin install fe-gen2template
```

### 3. GitHub 直接刷新

无需本地 clone，直接从 GitHub 拉取最新版：

```bash
claude plugin marketplace add https://github.com/shouhutianshi/fe-gen2template
claude plugin uninstall fe-gen2template && claude plugin install fe-gen2template
```

### 4. 刷新后报告

刷新成功后报告版本变化：

```bash
OLD_VERSION=$(ls -d ~/.claude/plugins/cache/fe-gen2template/fe-gen2template/*/ 2>/dev/null | sort -V | head -1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
# ... install 后 ...
NEW_VERSION=$(ls -d ~/.claude/plugins/cache/fe-gen2template/fe-gen2template/*/ 2>/dev/null | sort -V | tail -1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
```

向用户报告：`插件已从 v${OLD_VERSION} 刷新到 v${NEW_VERSION}`。

### 5. 失败处理

| 场景 | 处理 |
|---|---|
| 本地仓库不存在 | 走 GitHub 直接刷新 |
| `git fetch` 失败（网络） | 走 GitHub 直接刷新 |
| `git pull --ff-only` 失败（分支分歧） | 中止，提示手动解决冲突后重试 |
| `marketplace add` 或 `plugin install` 失败 | 中止，提示手动运行安装脚本 |

> 注意：刷新后缓存目录版本号可能变化（如 1.0.0 → 1.1.0），后续「定位插件源」步骤会在刷新后重新定位，无需特殊处理。

## 定位插件源

```bash
SYNC_SRC=$(ls -d ~/.claude/plugins/cache/fe-gen2template/fe-gen2template/*/skills/fast-to-template/references 2>/dev/null | sort -V | tail -1)
```

为空则提示安装：`claude plugin install fe-gen2template`。定位后验证 `$SYNC_SRC/skills/tf-tech-spec/SKILL.md` 存在，不存在说明插件安装不完整。

插件版本号从缓存根目录的 `package.json` 读取（`SYNC_SRC` 向上 3 级）。

> 如果上一步执行了缓存刷新，缓存路径中的版本号目录可能已变化，本步骤会在刷新后重新定位。

## 同步内容

以下是与 generate.sh 一致的同步映射（**同步表是唯一真相源**，所有 cp 命令从此推导）：

| # | 源（`$SYNC_SRC/`） | 目标（项目） | 方式 |
|---|---|---|---|
| 1 | `skills/*` | `.claude/skills/` | 递归覆盖 |
| 2 | `commands/*.md` | `.claude/commands/` | 逐文件覆盖 |
| 3 | `docs/mcp-setup.md` | `docs/mcp-setup.md` | 直接覆盖 |
| 4 | `skills/tf-tech-spec/references/workflow.md` | `docs/workflow.md` | 直接覆盖 |
| 5 | `skills/tf-tech-spec/references/conventions/*` | `docs/conventions/` | 逐文件覆盖 |

> skills 采用递归复制，新增的子目录（如 `scripts/`）和文件（如 `conventions-guide.md`）自动包含，无需逐条维护。

**不动的文件**：`CLAUDE.md`、`AGENTS.md`、`.claude/settings.json`、`.claude/settings.local.json`。

## 同步策略

### 初始同步（项目无 skills）

根据同步表创建目录并复制全部内容。无需 diff。

### 增量同步（项目已有 skills）

1. 用 `diff -rq` 对比同步表中每对源和目标，整理三类变更：
   - **新增**：插件有、项目没有
   - **更新**：双方都有、内容不同
   - **删除**：项目有、插件没有
2. 输出变更摘要，询问用户确认
3. 确认后按同步表执行覆盖

**删除处理**：项目有但插件没有的文件，列出清单并逐一询问用户是删除还是保留。用户自建的 skill 目录（插件中无同名目录）不受影响。

## 同步后

1. **验证**：抽查关键文件存在且非空（如 `tf-tech-spec/SKILL.md`、`conventions-guide.md`、`self-check.md`、`scripts/*.sh`）；统计源和目标文件数是否一致
2. **版本标记**：读取插件 `package.json` 的 version，更新 `CLAUDE.md` 末尾 `<!-- scaffold-sync version: X.X.X -->`

## 版本管理

本 skill 使用 semver 版本号（frontmatter `version` 字段）。任何修改都应同步更新版本号：
- minor：新增同步步骤、验证规则、同步表条目
- patch：措辞修正、流程优化、小幅调整
- major：删除同步内容、破坏性变更同步策略
