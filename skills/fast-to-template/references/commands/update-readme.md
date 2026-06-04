同步 README.md 和 CLAUDE.md 与项目真实状态。

## 1. 收集信息

运行以下命令收集项目现状：

```bash
# 基本信息
cat package.json
ls -d src/*/  2>/dev/null
ls -d e2e/  2>/dev/null
ls -d .claude/skills/  2>/dev/null

# 验证命令是否可用
cat package.json | python3 -c "import json,sys; s=json.load(sys.stdin).get('scripts',{}); [print(k) for k in s]"
```

## 2. 更新 README.md

根据收集到的信息，更新 README.md 中以下章节（只修改与现状不一致的部分，保持已有风格）：

### 必须核对的内容

| 章节 | 数据来源 |
| --- | --- |
| 项目描述 | `package.json` name、dependencies |
| 快速开始命令 | `package.json` scripts |
| 命令表 | `package.json` scripts，只列有意义的项目（跳过内部脚本） |
| E2E 依赖 | `e2e/` 目录是否存在 |
| Python 依赖 | `.claude/skills/kit-zyb-docs/` 或 `kit-zyb-pms/` 是否存在 |
| 文档链接 | `docs/` 下实际存在的文件 |

### 不修改的部分

- 用户手动添加的自定义章节（如 API 说明、部署流程等）
- 已有的 README 标题和整体结构

## 3. 更新 CLAUDE.md

CLAUDE.md 是 Claude Code 的项目指令文件，**保守更新**——只修改以下内容：

| 检查项 | 规则 |
| --- | --- |
| 技术栈 | 与 `package.json` dependencies 实际一致 |
| 验证门禁命令表 | 与 `package.json` scripts 实际一致（有才列，没有就去掉对应行） |
| 插件版本号 | 如果 `CLAUDE.md` 末尾有版本号行，保持原样或按用户要求更新 |

**不要修改**：行为准则、规范加载表、路径分流、高风险变更、工作方式等章节——这些由 `/scaffold-sync` 管理。

## 4. 输出

更新完成后，输出变更摘要：

```
README.md: 更新了 <列出修改的章节>
CLAUDE.md: 更新了 <列出修改的部分>
```

未做修改的文件不要输出。
