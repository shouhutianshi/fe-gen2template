#!/usr/bin/env bash
# 用法: bash baseline-scan.sh [项目根目录]
# 对仓库执行工程基线扫描，输出 Markdown 表格，可直接粘贴到技术方案「现状基线」章节。
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

echo "| 扫描项 | 发现位置 | 命中数 |"
echo "| --- | --- | --- | --- |"

scan() {
  local label="$1"
  shift
  local count=0
  local locations=""
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      locations="$locations $line"
      count=$((count + 1))
    fi
  done < <(grep -rn "$@" src/ --include='*.ts' --include='*.vue' --include='*.js' --include='*.css' 2>/dev/null | head -5)
  if [ "$count" -eq 0 ]; then
    echo "| $label | 未发现 | 0 |"
  else
    echo "| $label | ${locations# } | $count |"
  fi
}

scan "弹窗历史 API" -E 'ElMessageBox|MessageBox\.confirm|window\.alert|window\.confirm'
scan "剪贴板废弃 API" 'document\.execCommand'
scan "any 类型" ': any\b'
scan "类型断言 as" ' as '
scan "@ts-ignore" '@ts-ignore'
scan "硬编码颜色" -E '#[0-9a-fA-F]{3,8}[^0-9a-fA-F]|rgb\('
scan "!important" '!important'
scan "组件库全量导入" -E 'import ElementPlus from|import Vant from'
scan "大依赖静态导入" -E 'import.*cos-js-sdk|import.*echarts|import.*monaco-editor|import.*xlsx'

echo ""
echo "### 以下项目需手动审查（难以通过 grep 精确检测）"
echo ""
echo "| 扫描项 | 检查方式 | 状态 |"
echo "| --- | --- | --- |"
echo "| 类型分散定义 | 搜索同语义响应类型在多处定义（如 BackendResponse） | 需手动检查 |"
echo "| 重复工具函数 | 搜索同名/同义函数（如 formatTime/formatDate） | 需手动检查 |"
echo "| 列表 ref 误用 | 列表数据应用 shallowRef 而非 ref([]) | 需手动检查 |"
echo "| URL query 未校验 | 路由读 query 后是否做枚举校验 | 需手动检查 |"
echo "| 请求重试闭包 | request.ts 中 retryCount 是否在请求函数内部定义 | 需手动检查 |"
echo "| 列表竞态保护 | composable fetch list 是否有 latestFetchId / AbortController | 需手动检查 |"

# lint baseline
echo ""
echo "### Lint & Test Baseline"
echo ""
if command -v bun &>/dev/null && [ -f package.json ]; then
  echo -n "| lint error | "
  lint_result=$(bun run lint 2>&1) && echo "0 |" || echo "$(echo "$lint_result" | grep -c 'error') |"
  echo -n "| test failed | "
  test_result=$(bun run test 2>&1) && echo "0 |" || echo "$(echo "$test_result" | grep -c 'FAIL\|failed') |"
else
  echo "| lint error | 需手动运行 \`bun run lint\` | — |"
  echo "| test failed | 需手动运行 \`bun run test\` | — |"
fi
