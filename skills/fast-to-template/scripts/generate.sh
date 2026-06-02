#!/usr/bin/env bash
# fe-gen2template generator
set -euo pipefail

# --- Parse & validate args ---
NAME="" TYPE="" TEST_SCOPE="" USE_PINIA="" INCLUDE_SKILLS="" USERNAME="" VERSION="" OUTPUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; NAME="$2"; shift 2 ;;
    --type) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; TYPE="$2"; shift 2 ;;
    --test-scope) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; TEST_SCOPE="$2"; shift 2 ;;
    --pinia) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; USE_PINIA="$2"; shift 2 ;;
    --skills) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; INCLUDE_SKILLS="$2"; shift 2 ;;
    --username) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; USERNAME="$2"; shift 2 ;;
    --version) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; VERSION="$2"; shift 2 ;;
    --output) [[ -z "${2:-}" ]] && { echo "Error: $1 requires a value"; exit 1; }; OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done
[[ -z "$NAME" ]] && { echo "--name required"; exit 1; }
[[ "$NAME" =~ ^[a-z0-9][a-z0-9._-]*$ ]] || {
  echo "--name must be a safe npm package name: lowercase letters, numbers, '.', '_' or '-'";
  exit 1;
}
[[ "$NAME" != *..* ]] || { echo "--name must not contain '..'"; exit 1; }
[[ -z "$TYPE" || ! "$TYPE" =~ ^(pc|h5|both)$ ]] && { echo "--type must be pc|h5|both"; exit 1; }
: "${USERNAME:=dev}"
: "${TEST_SCOPE:=unit}"
: "${USE_PINIA:=false}"
: "${INCLUDE_SKILLS:=false}"
[[ "$TEST_SCOPE" =~ ^(unit|unit\+e2e|full)$ ]] || { echo "--test-scope must be unit|unit+e2e|full"; exit 1; }
[[ "$USE_PINIA" =~ ^(true|false)$ ]] || { echo "--pinia must be true|false"; exit 1; }
[[ "$INCLUDE_SKILLS" =~ ^(true|false)$ ]] || { echo "--skills must be true|false"; exit 1; }

# Read version from plugin.json if not specified
if [[ -z "$VERSION" ]]; then
  PLUGIN_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
  VERSION="$(python3 - "$PLUGIN_DIR/.claude-plugin/plugin.json" <<'PYEOF' 2>/dev/null || echo "1.0.0"
import json
import sys

with open(sys.argv[1]) as f:
    print(json.load(f)["version"])
PYEOF
)"
fi

TARGET="${OUTPUT:-.}/${NAME}"
REFS="$(cd "$(dirname "$0")/.." && pwd)/references"
HAS_E2E=false
[[ "$TEST_SCOPE" == *"e2e"* || "$TEST_SCOPE" == "full" ]] && HAS_E2E=true

# Fail if target already exists
if [[ -e "$TARGET" ]]; then
  echo "Error: ${TARGET} already exists"; exit 1
fi

# Rollback on failure: remove incomplete target directory
trap 'echo "==> Failed, cleaning up ${TARGET}"; rm -rf "${TARGET}"' ERR

echo "==> Generating ${NAME} (${TYPE}, pinia=${USE_PINIA}, e2e=${HAS_E2E}, skills=${INCLUDE_SKILLS})"

# 1. Copy complete type template
cp -r "${REFS}/types/${TYPE}" "${TARGET}"
mkdir -p "${TARGET}/.claude"
cat > "${TARGET}/.claude/settings.json" <<'JSONEOF'
{
  "enabledPlugins": {
    "superpowers@superpowers-marketplace": true
  }
}
JSONEOF
cat > "${TARGET}/.claude/settings.local.json" <<'JSONEOF'
{
  "permissions": {
    "allow": [
      "Bash(bun *)",
      "Bash(git *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(find *)",
      "Bash(echo *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(wc *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Read",
      "Write",
      "Edit"
    ]
  }
}
JSONEOF

# 2. Pinia: swap main.ts, clean stores
if [[ "$USE_PINIA" == "true" ]]; then
  mv "${TARGET}/src/main.pinia.ts" "${TARGET}/src/main.ts"
else
  rm -f "${TARGET}/src/main.pinia.ts"
  rm -rf "${TARGET}/src/stores"
fi

# 3. E2E
if [[ "$HAS_E2E" == "true" ]]; then
  cp "${REFS}/extras/e2e/playwright.config.ts" "${TARGET}/"
  mkdir -p "${TARGET}/e2e/"{fixtures,pages,flows}
  # Copy flow specs only if they exist (avoid glob fail under set -e)
  if compgen -G "${REFS}/extras/e2e/flows/*.ts" > /dev/null; then
    cp "${REFS}/extras/e2e/flows/"*.ts "${TARGET}/e2e/flows/"
  fi
fi

# 4. Skills & commands
mkdir -p "${TARGET}/.claude/commands"
cp "${REFS}/commands/update-readme.md" "${TARGET}/.claude/commands/"
if [[ "$INCLUDE_SKILLS" == "true" ]]; then
  mkdir -p "${TARGET}/.claude/skills"
  cp -r "${REFS}/skills/"* "${TARGET}/.claude/skills/"
  for cmd in "${REFS}/commands/"*.md; do
    basename=$(basename "$cmd")
    [[ "$basename" == "update-readme.md" ]] && continue
    cp "$cmd" "${TARGET}/.claude/commands/"
  done
fi

# 5. Docs (mcp-setup + workflow + conventions from skill)
mkdir -p "${TARGET}/docs/conventions"
cp "${REFS}/docs/mcp-setup.md" "${TARGET}/docs/"
cp "${REFS}/skills/tf-tech-spec/references/workflow.md" "${TARGET}/docs/"
cp -r "${REFS}/skills/tf-tech-spec/references/conventions/"* "${TARGET}/docs/conventions/"

# 6. Substitute variables
python3 - "$TARGET" "$NAME" "$USERNAME" "$VERSION" <<'PYEOF'
from pathlib import Path
import sys

target = Path(sys.argv[1])
replacements = {
    "{{PROJECT_NAME}}": sys.argv[2],
    "__PROJECT_NAME__": sys.argv[2],
    "{{USERNAME}}": sys.argv[3],
    "{{SCAFFOLD_VERSION}}": sys.argv[4],
}
suffixes = {".json", ".ts", ".vue", ".html", ".yml", ".md", ".css"}

for path in target.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix not in suffixes and not path.name.startswith(".env"):
        continue
    text = path.read_text()
    updated = text
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    if updated != text:
        path.write_text(updated)
PYEOF

# 7. Clean package.json
python3 - "$TARGET/package.json" "$USE_PINIA" "$HAS_E2E" << 'PYEOF'
import json, sys
path, use_pinia, has_e2e = sys.argv[1], sys.argv[2] == 'true', sys.argv[3] == 'true'
with open(path) as f:
    pkg = json.load(f)
if not use_pinia:
    pkg['dependencies'].pop('pinia', None)
    pkg['dependencies'].pop('pinia-plugin-persistedstate', None)
if not has_e2e:
    pkg['devDependencies'].pop('@playwright/test', None)
    pkg['scripts'].pop('test:e2e', None)
with open(path, 'w') as f:
    json.dump(pkg, f, indent=2, ensure_ascii=False)
    f.write('\n')
PYEOF

# 8. CLAUDE.md, AGENTS.md, README
case "$TYPE" in pc) UI="element-plus";; h5) UI="vant";; both) UI="element-plus + vant";; esac
python3 - "$REFS" "$TARGET" "$UI" "$USERNAME" "$VERSION" <<'PYEOF'
from pathlib import Path
import sys

refs, target = Path(sys.argv[1]), Path(sys.argv[2])
ui, username, version = sys.argv[3], sys.argv[4], sys.argv[5]

claude = (refs / "claude-md-template.md").read_text()
claude = (
    claude
    .replace("{{UI_LIBRARY}}", ui)
    .replace("{{USERNAME}}", username)
    .replace("{{SCAFFOLD_VERSION}}", version)
)
(target / "CLAUDE.md").write_text(claude)

agents = (refs / "agents-md-template.md").read_text()
agents = agents.replace("{{USERNAME}}", username)
(target / "AGENTS.md").write_text(agents)
PYEOF

# README
{
  echo "# ${NAME}"
  echo ""
  echo "Vue 3 + Vite + TypeScript 前端项目$([[ "$TYPE" == "both" ]] && echo "，支持 PC（Element Plus）和 H5（Vant 4）")。"
  echo ""
  echo "## 快速开始"
  echo ""
  printf '\`\`\`bash\nbun install && bun run dev\n\`\`\`\n'
  echo ""
  echo "| 命令 | 说明 |"
  echo "| --- | --- |"
  echo '| `bun run dev` | 开发服务器 |'
  echo '| `bun run build` | 类型检查 + 构建 |'
  echo '| `bun run typecheck` | TypeScript 检查 |'
  echo '| `bun run lint` | ESLint |'
  echo '| `bun run test` | 单元测试 |'
  [[ "$HAS_E2E" == "true" ]] && echo '| `bun run test:e2e` | E2E 测试 |'
  [[ "$HAS_E2E" == "true" ]] && { echo ""; echo "## E2E 浏览器依赖"; echo ""; printf '\`\`\`bash\nbunx playwright install chromium\n\`\`\`\n'; }
  [[ "$INCLUDE_SKILLS" == "true" ]] && { echo ""; echo "## Python 依赖"; echo ""; printf '\`\`\`bash\npip install -r .claude/skills/kit-zyb-docs/scripts/requirements.txt\n\`\`\`\n'; }
  echo ""
  echo "## 文档"
  echo ""
  echo "- [开发规范](docs/conventions/)"
  echo "- [工作流](docs/workflow.md)"
  echo "- [MCP 配置](docs/mcp-setup.md)"
  echo ""
  echo "---"
  echo ""
  echo "本项目由 fe-gen2template v${VERSION} 生成。"
} > "${TARGET}/README.md"

echo "==> Done! ${TARGET}"
