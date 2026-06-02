---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Bash(git pull:*)
description: 创建 git 提交并自动推送
---

## 上下文

- 当前 git 状态: !`git status`
- 当前变更（暂存和未暂存）: !`git diff HEAD`
- 当前分支: !`git branch --show-current`
- 最近提交: !`git log --oneline -10`

## 任务

根据以上变更，创建 git 提交并推送。按以下步骤执行：

### 1. 生成提交信息

分析 diff，生成约定式提交信息：

- 格式：`<type>: <中文描述>`
- 类型：`feat`、`fix`、`refactor`、`perf`、`style`、`docs`、`chore`
- 描述：简洁中文，不超过 50 字
- 风格与上面的最近提交保持一致
- **禁止**在提交信息中添加任何 Co-Authored-By 行（如 `Co-Authored-By: Claude`、`Co-Authored-By: Happy` 等）

### 2. 暂存并提交

暂存所有变更文件，使用 HEREDOC 格式提交：

```bash
git add -A
git commit -m "$(cat <<'EOF'
<type>: <描述>
EOF
)"
```

### 3. 自动推送

提交成功后，**自动推送到远程，无需确认**：

- 获取当前分支：`git branch --show-current`
- 如果分支已追踪远程，执行 `git push`
- 如果分支没有上游，执行 `git push -u origin <branch>`
- 如果推送失败（远程领先），先执行 `git pull --rebase` 再重试推送
- 在 `master`/`main` 分支上同样推送——用户主动调用 /commit 说明就是要推送

**不要在推送前询问确认。** 用户期望 commit + push 是一体的原子操作。
