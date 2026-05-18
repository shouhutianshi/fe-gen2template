执行本地验证清单，收集验证证据。

按以下顺序执行验证，记录每项结果：

1. **检查变更范围**
   ```
   git status --short
   git diff --stat
   ```

2. **依赖检查**（仅当有依赖变更时）
   ```
   bun install
   ```

3. **Lint**
   ```
   bun run lint
   ```

4. **Typecheck**
   ```
   bun run typecheck
   ```

5. **Unit Test**
   ```
   bun run test
   ```

6. **Build**
   ```
   bun run build
   ```

验证结果格式：

| 验证项 | 状态 | 备注 |
| --- | --- | --- |
| 依赖安装 | ✅/❌/跳过 | |
| Lint | ✅/❌ | 0 error / N errors |
| Typecheck | ✅/❌ | 0 error / N errors |
| Test | ✅/❌ | N passed, 0 failed |
| Build | ✅/❌ | 产物大小 |

如有任何项失败，给出失败原因和修复建议，不要继续后续验证步骤。
全部通过后，提示用户可以执行 `/commit` 提交。
