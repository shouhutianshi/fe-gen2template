#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GENERATE="${SCRIPT_DIR}/generate.sh"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

assert_absent() {
  [[ ! -e "$1" ]] || fail "unexpected path exists: $1"
}

assert_no_placeholders() {
  local project="$1"
  if grep -R -n -E '(\{\{PROJECT_NAME\}\}|__PROJECT_NAME__|\{\{USERNAME\}\}|\{\{SCAFFOLD_VERSION\}\})' "$project"; then
    fail "unresolved template placeholders in $project"
  fi
}

assert_single_version_section() {
  local project="$1"
  local count
  count="$(grep -c '^## 插件版本$' "$project/CLAUDE.md")"
  [[ "$count" == "1" ]] || fail "expected one plugin version section, got $count"
}

assert_package_lacks() {
  local project="$1"
  local needle="$2"
  if grep -q "$needle" "$project/package.json"; then
    fail "package.json should not contain $needle"
  fi
}

assert_not_git_ignored() {
  local path="$1"
  if git -C "$SCRIPT_DIR/../../.." check-ignore -q "$path"; then
    git -C "$SCRIPT_DIR/../../.." check-ignore -v "$path" >&2
    fail "required template asset is ignored by git: $path"
  fi
}

assert_fails() {
  if "$@" >/tmp/fe-gen2template-test-fail.log 2>&1; then
    cat /tmp/fe-gen2template-test-fail.log >&2
    fail "command should have failed: $*"
  fi
}

assert_fails bash "$GENERATE" \
  --name '../escaped' \
  --type pc \
  --test-scope unit \
  --pinia false \
  --skills false \
  --username tester \
  --output "$TMP_DIR"

assert_fails bash "$GENERATE" \
  --name 'Bad Name' \
  --type pc \
  --test-scope unit \
  --pinia false \
  --skills false \
  --username tester \
  --output "$TMP_DIR"

assert_fails bash "$GENERATE" \
  --name bad-scope \
  --type pc \
  --test-scope bogus \
  --pinia false \
  --skills false \
  --username tester \
  --output "$TMP_DIR"

assert_fails bash "$GENERATE" \
  --name bad-bool \
  --type pc \
  --test-scope unit \
  --pinia maybe \
  --skills false \
  --username tester \
  --output "$TMP_DIR"

bash "$GENERATE" \
  --name demo-pc \
  --type pc \
  --test-scope unit \
  --pinia false \
  --skills false \
  --username 'tester/name&team' \
  --version 9.9.9 \
  --output "$TMP_DIR"

PC="$TMP_DIR/demo-pc"
assert_file "$PC/package.json"
assert_file "$PC/.env"
assert_file "$PC/.claude/settings.json"
assert_file "$PC/.claude/settings.local.json"
assert_file "$PC/src/main.ts"
assert_file "$PC/src/views/Home.vue"
assert_file "$PC/src/views/Home.test.ts"
assert_absent "$PC/src/main.pinia.ts"
assert_absent "$PC/src/stores"
assert_absent "$PC/playwright.config.ts"
assert_no_placeholders "$PC"
assert_single_version_section "$PC"
assert_package_lacks "$PC" '"pinia"'
assert_package_lacks "$PC" '@playwright/test'
grep -q '^.claude/settings.local.json$' "$PC/.gitignore" || fail "settings.local.json must be ignored"
grep -q 'ElementPlusResolver' "$PC/vite.config.ts" || fail "PC template must auto-import Element Plus components"
cmp -s "$PC/.env.example" "$PC/.env" || fail ".env must be created from .env.example"
git -C "$PC" init -q
git -C "$PC" check-ignore -q .env || fail ".env must be ignored in generated projects"
git -C "$PC" check-ignore -q .claude/settings.local.json || fail "settings.local.json must be ignored in generated projects"
assert_not_git_ignored "skills/fast-to-template/references/types/pc/.claude/settings.json"

bash "$GENERATE" \
  --name demo-both \
  --type both \
  --test-scope full \
  --pinia true \
  --skills true \
  --username tester \
  --version 9.9.9 \
  --output "$TMP_DIR"

BOTH="$TMP_DIR/demo-both"
assert_file "$BOTH/src/main.ts"
assert_file "$BOTH/src/stores/index.ts"
assert_file "$BOTH/src/pc/views/Home.vue"
assert_file "$BOTH/src/h5/views/Home.vue"
assert_file "$BOTH/playwright.config.ts"
assert_file "$BOTH/e2e/flows/home.spec.ts"
assert_file "$BOTH/.claude/skills/kit-zyb-docs/SKILL.md"
assert_file "$BOTH/.claude/commands/commit.md"
grep -q 'bunx playwright install chromium' "$BOTH/README.md" || fail "README must document E2E browser install"
grep -q 'ElementPlusResolver' "$BOTH/vite.config.ts" || fail "both template must auto-import Element Plus components"
assert_no_placeholders "$BOTH"
assert_single_version_section "$BOTH"

echo "generate.sh smoke tests passed"
