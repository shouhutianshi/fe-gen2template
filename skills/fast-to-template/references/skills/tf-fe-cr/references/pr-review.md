# 拉取请求评审

PR 评审使用**工作树模式**——在本地获取 PR 分支，以便评审可以读取 PR 分支精确版本的相关代码。这对于评审准确性至关重要。

## 参考资料

| 文件                 | 用途                     |
| -------------------- | ------------------------ |
| `code-checklist.md`  | 代码评审检查清单         |
| `doc-checklist.md`   | 文档评审检查清单         |
| `judgment-matrix.md` | 值得修复的标准和特殊规则 |

---

## 第一步：创建工作树

如果 `$ARGUMENTS` 是 URL，从中提取 PR 编号。

清理之前会话遗留的工作树：

```bash
for dir in /tmp/pr-review-*; do
    [ -d "$dir" ] || continue
    n=$(basename "$dir" | sed 's/pr-review-//')
    git worktree remove "$dir" 2>/dev/null
    git branch -D "pr-${n}" 2>/dev/null
done
```

验证 PR 目标：

```bash
gh repo view --json nameWithOwner --jq .nameWithOwner
gh pr view {number} --json headRefName,baseRefName,headRefOid,state,body
```

记录 `OWNER_REPO`。提取：`PR_BRANCH`、`BASE_BRANCH`、`HEAD_SHA`、`STATE`、`PR_BODY`。
如果任一命令失败，通知用户并中止。
如果 `$ARGUMENTS` 是包含 `{owner}/{repo}` 的 URL，验证其与 `OWNER_REPO` 匹配。若不匹配，通知用户不支持跨仓库 PR 评审并中止。
如果 `STATE` 不是 `OPEN`，通知用户并退出。

**如果当前分支等于 `PR_BRANCH` 且 HEAD 等于 `HEAD_SHA`**，跳过工作树创建——代码已在本地。

**否则**，创建工作树：

```bash
git fetch origin pull/{number}/head:pr-{number}
git worktree add --no-track /tmp/pr-review-{number} pr-{number}
cd /tmp/pr-review-{number}
```

如果工作树创建失败，通知用户并中止。

---

## 第二步：收集差异和上下文

```bash
git fetch origin {BASE_BRANCH}
git merge-base origin/{BASE_BRANCH} HEAD
git diff <merge-base-sha>
```

如果差异超过 200 行，先运行 `git diff --stat` 获取概览，然后使用 `git diff -- {file}` 逐文件读取差异，避免输出截断。

如果差异为空 → 清理工作树并退出。

获取现有的 PR 评审评论以去重：

```bash
gh api repos/{OWNER_REPO}/pulls/{number}/comments
```

---

## 第三步：评审

**内部分析**：

1. 基于差异，根据需要读取相关代码上下文以理解更改的正确性（例如：周边逻辑、基类、调用者）。
2. 阅读 `PR_BODY` 以理解声明的动机。验证实现是否真正实现了作者描述的内容。
3. 对代码文件应用 `code-checklist.md`，对文档文件应用 `doc-checklist.md`。使用 `judgment-matrix.md` 判断每个问题是否值得报告。
4. 检查之前 PR 评论中提出的问题是否已修复。
5. 对于每个潜在问题，执行二次验证：重新阅读周边代码并检查——是否有其他地方的保护或提前返回处理了此问题？调用链是否保证前置条件？我是否误解了生命周期或所有权？
6. **排除所有已排除的问题。仅保留确认存在的问题。**
7. 将确认的问题与现有的 PR 评论进行去重。

**输出规则**：仅向用户展示最终确认的问题。不输出分析过程、排除推理或已被考虑但已排除的问题。

---

## 第四步：清理并报告

如果创建了工作树，请清理它：

```bash
cd -
git worktree remove /tmp/pr-review-{number}
git branch -D pr-{number}
```

向用户展示结果：

- 摘要：一段描述更改目的和范围的段落。
- 整体评估：代码质量评估和关键改进方向。
- 问题列表（如果干净则为"未发现问题"）。

如果没有问题 → 询问是否提交批准评审并合并 PR：

1. 提交批准：

   ```bash
   gh api repos/{OWNER_REPO}/pulls/{number}/reviews --input - <<'EOF'
   {
     "commit_id": "{HEAD_SHA}",
     "event": "APPROVE"
   }
   EOF
   ```

2. 合并（压缩）：
   ```bash
   gh pr merge {number} --squash --delete-branch
   ```

如果用户拒绝，则不执行任何操作。跳过下面的评论提交。

如果发现问题 → 以以下格式向用户展示确认的问题：

```
{N}. [{优先级}] {文件}:{行号} — {问题描述和建议修复}
```

其中 `{优先级}` 是检查清单项目 ID（例如：A2、B1、C7）。然后要求用户使用**单一多选问题**选择要提交的问题，其中每个选项的标签是问题摘要（例如：`[A2] file:line — description`）。用户在一个提示中勾选多个选项。未勾选的问题将被跳过。

**必须**使用 `gh api` + heredoc。不要使用 `gh pr comment`、`gh pr review` 或任何创建非行级评论的命令：

```bash
gh api repos/{OWNER_REPO}/pulls/{number}/reviews --input - <<'EOF'
{
  "commit_id": "{HEAD_SHA}",
  "event": "COMMENT",
  "comments": [
    {
      "path": "relative/file/path",
      "line": 42,
      "side": "RIGHT",
      "body": "问题描述和建议修复"
    }
  ]
}
EOF
```

- `commit_id`：PR 分支的 HEAD SHA
- `path`：相对于仓库根目录的路径
- `line`：**新**文件中的行号（差异右侧）。必须在第三步期间通过读取工作树中的实际文件来确定——不要从差异块偏移量推导。
- `side`：始终为 `"RIGHT"`
- `body`：简洁，使用用户的对话语言，尽可能包含具体的修复建议

发现/提交/跳过的问题摘要。
