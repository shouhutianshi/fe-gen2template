#!/bin/bash
set -e

REPO_URL="git@git.zuoyebang.cc:toufang/fe-gen2template.git"
HTTPS_URL="https://git.zuoyebang.cc/toufang/fe-gen2template.git"
INSTALL_DIR="${HOME}/code/fe-gen2template"
DEFAULT_BRANCH="master"

echo "=> fe-gen2template 插件安装脚本"
echo ""

# 检查依赖
command -v git >/dev/null 2>&1 || { echo "Error: git 未安装"; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "Error: claude CLI 未安装"; exit 1; }

# Clone 或更新
if [ -d "$INSTALL_DIR" ]; then
  echo "=> 检测到已有安装，正在更新..."
  cd "$INSTALL_DIR"
  git fetch origin "$DEFAULT_BRANCH"
  git checkout "$DEFAULT_BRANCH"
  git pull --ff-only origin "$DEFAULT_BRANCH"
else
  echo "=> 正在克隆仓库..."
  mkdir -p "$(dirname "$INSTALL_DIR")"
  git clone --branch "$DEFAULT_BRANCH" "$REPO_URL" "$INSTALL_DIR" 2>/dev/null || \
    git clone --branch "$DEFAULT_BRANCH" "$HTTPS_URL" "$INSTALL_DIR"
fi

# 注册 marketplace
echo "=> 正在注册 marketplace..."
claude plugin marketplace add "$INSTALL_DIR"

# 安装插件
echo "=> 正在安装插件..."
claude plugin install fe-gen2template

echo ""
echo "=> 安装完成！"
echo "=> 在任何目录打开 Claude Code，执行 /scaffold 即可创建新项目"
