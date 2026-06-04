#!/bin/bash
set -e

GITHUB_URL="https://github.com/shouhutianshi/fe-gen2template"
LOCAL_DIR="${HOME}/code/fe-gen2template"
DEFAULT_BRANCH="master"

echo "=> fe-gen2template 插件安装脚本"
echo ""

# 检查依赖
command -v claude >/dev/null 2>&1 || { echo "Error: claude CLI 未安装"; exit 1; }

# 注册 marketplace（优先从 GitHub URL，无需 clone）
echo "=> 正在注册 marketplace..."
if claude plugin marketplace add "$GITHUB_URL" 2>/dev/null; then
  echo "   已从 GitHub 注册 marketplace"
else
  echo "   GitHub 注册失败，尝试本地路径..."
  if [ -d "$LOCAL_DIR" ]; then
    claude plugin marketplace add "$LOCAL_DIR"
    echo "   已从本地目录注册 marketplace"
    # 同步本地仓库
    cd "$LOCAL_DIR" && git fetch origin "$DEFAULT_BRANCH" 2>/dev/null && \
      git checkout "$DEFAULT_BRANCH" 2>/dev/null && \
      git pull --ff-only origin "$DEFAULT_BRANCH" 2>/dev/null || true
  else
    echo "Error: 本地目录 $LOCAL_DIR 不存在，且 GitHub 注册失败"
    echo "请检查网络连接后重试，或手动 clone 仓库："
    echo "  git clone $GITHUB_URL $LOCAL_DIR"
    echo "  claude plugin marketplace add $LOCAL_DIR"
    exit 1
  fi
fi

# 安装插件
echo "=> 正在安装插件..."
claude plugin install fe-gen2template

echo ""
echo "=> 安装完成！"
echo "=> 在任何目录打开 Claude Code，执行 /scaffold 即可创建新项目"
