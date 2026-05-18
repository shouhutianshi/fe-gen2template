---
name: kit-zyb-pms
description: 查询作业帮 PMS 系统中某个需求（Story）下的所有 Bug/缺陷列表。当用户说"查一下需求下的所有 bug"、"获取 story 的缺陷列表"、"需求 ID XXX 有哪些 bug"、"查看需求关联的 bug"时必须使用此 skill。
---

# kit-zyb-pms

从 PMS 接口拉取指定需求下的所有 Bug 数据，结构化解析后标注到上下文，支持批量查看和统计分析。

---

## 第一步：提取需求 ID

从用户输入中提取需求 ID（Story ID）：

| 输入示例 | 提取的 REQ_ID |
|---|---|
| "查一下需求 12345 的所有 bug" | 12345 |
| "获取 story 67890 的缺陷" | 67890 |
| "需求 ID S-2024-001 有哪些问题" | S-2024-001 |
| "PRD-1234 关联的 bug" | PRD-1234 |

如无法提取，询问用户：
> 请提供需求 ID（Story ID），例如：12345 或 S-2024-001

---

## 第二步：生成验签 sign

**必须优先执行**，发起请求前必须计算 `sign` 参数。

### 全局时间戳 ⚠️【关键】

> **警告：时间戳不一致是导致验签失败的最常见原因！**

在计算 sign **之前**，先生成一个全局时间戳，后续所有步骤（sign 计算和实际请求）**必须复用同一个值**，确保两者完全一致：

```bash
# Shell：生成全局时间戳（Unix 秒级整数）
TIMESTAMP=$(python3 -c "import time; print(int(time.time()))")
```

```python
# Python：生成全局时间戳
import time
TIMESTAMP = int(time.time())   # 全局复用，不要在 sign 和请求中分别调用 time.time()
```

> **关键警告**：
> - `TIMESTAMP` 必须在调用 `get_sign` 和发起 HTTP 请求时使用**同一个变量**
> - **禁止**在两处分别调用 `time.time()`，即使是毫秒级的时间差也会导致 `验签失败`
> - 如果签名验证失败返回 `{"errNo":1,"errstr":"参数错误: 验签失败"}`，首先检查时间戳是否一致

### 验签算法

| 步骤 | 操作 |
|---|---|
| 1 | 收集所有请求参数（不含 `sign` 本身），按 key 字母序排序 |
| 2 | 拼接为 `key1=val1&key2=val2&...` 格式字符串 |
| 3 | 整体转为大写 |
| 4 | 对大写字符串取 MD5（十六进制，小写） |

### 执行步骤

使用 `scripts/get_sign.py` 中的 `get_sign` 方法计算签名：

```bash
# 将业务参数以 JSON 传入，输出 sign 值（time 使用全局 TIMESTAMP）
SIGN=$(python3 scripts/get_sign.py "{\"page\":\"1\",\"page_size\":\"100\",\"source\":\"QI\",\"reqid\":\"${REQ_ID}\",\"status\":\"open,handling\",\"time\":\"${TIMESTAMP}\"}")
```

或在 Python 中直接调用：

```python
import sys
sys.path.insert(0, "scripts")
from get_sign import get_sign

params = {
    "page": "1",
    "page_size": "100",
    "source": "QI",
    "reqid": REQ_ID,
    "status": "open,handling",
    "time": str(TIMESTAMP),   # 使用全局时间戳，与请求参数保持一致
}
sign = get_sign(params)
```

### 依赖安装

```bash
pip install hashlib  # hashlib 为 Python 内置，无需额外安装
```

---

## 第三步：发起接口请求

### 接口信息

| 字段 | 值 |
|---|---|
| URL | `https://pms.zuoyebang.cc/testplatapi/api/getbuglist` |
| Method | POST |
| Content-Type | `application/x-www-form-urlencoded` |
| 认证方式 | 验签（`sign` 参数，见第二步） |
| 请求参数 | `page=1&page_size=100&source=QI&reqid={需求ID}&status=open,handling&time={时间戳}&sign={sign}` |

```bash
# 完整查询命令：生成时间戳 → 计算 sign → curl 请求 → 解析结果
TIMESTAMP=$(python3 -c "import time; print(int(time.time()))") && \
SIGN=$(python3 scripts/get_sign.py "{\"page\":\"1\",\"page_size\":\"100\",\"source\":\"QI\",\"reqid\":\"${REQ_ID}\",\"status\":\"open,handling\",\"time\":\"${TIMESTAMP}\"}") && \
curl -s --insecure \
  'https://pms.zuoyebang.cc/testplatapi/api/getbuglist' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw "page=1&page_size=100&source=QI&reqid=${REQ_ID}&status=open,handling&time=${TIMESTAMP}&sign=${SIGN}" | \
python3 scripts/parse_bugs.py
```

### 查询条件说明

本 skill 默认只查询**待办**和**处理中**状态的 Bug：

| 参数 | 值 | 说明 |
|---|---|---|
| `page` | `1` | 页码，默认第 1 页 |
| `page_size` | `100` | 每页条数，最大 100 |
| `source` | `QI` | 请求来源标识 |
| `reqid` | `{需求ID}` | 需求 ID |
| `status` | `open,handling` | 状态：待办、处理中 |
| `time` | `{时间戳}` | 全局时间戳（Unix 秒级），需与 sign 计算时一致 |
| `sign` | `{sign}` | 验签，见第二步 |

如需查询所有状态（包括已解决、已关闭等），移除 `status` 参数即可。

### 分页处理

如果 `total > 100`，需要多页请求：

```bash
# 计算总页数
TOTAL_PAGES=$(( (TOTAL + 99) / 100 ))

# 循环获取所有页
for PAGE in $(seq 2 $TOTAL_PAGES); do
  RESPONSE=$(curl -s ... --data-raw "...page=${PAGE}...")
  # 追加到结果集
done
```

### 异常处理

| 情况 | 处理方式 |
|---|---|
| HTTP 非 200 | 告知状态码，提示 sign 计算是否正确 |
| `code != 0` | 展示 `message` / `msg` 字段 |
| 响应为空 | 提示网络问题或接口地址变更 |
| JSON 解析失败 | 输出原始响应前 500 字符 |

---

## 第四步：解析响应数据

所有字符串字段做 Unicode 解码和 HTML 实体还原后展示。

### 响应结构

| JSON 字段 | 含义 | 备注 |
|---|---|---|
| `code` | 状态码 | 0 表示成功 |
| `message` / `msg` | 消息 | |
| `data` | 数据对象 | 包含实际数据 |
| `data.totalItem` | Bug 总数 | 整数 |
| `data.data` | Bug 列表 | JsonArray |

### Bug 列表字段

| JSON 字段 | 含义 | 备注 |
|---|---|---|
| `bugid` / `id` | Bug ID | |
| `summary` / `title` | Bug 标题 | Unicode 转义，需解码 |
| `description` | 问题描述 | HTML + Unicode 混合，需解码 |
| `status` | 当前状态 | 如：open、handling、resolved、closed、rejected |
| `statusName` | 状态中文名 | 如：开放、处理中、已解决、已关闭、已拒绝 |
| `pLevel` | 严重程度 | 如：P1、P2、P3、P4 |
| `assignee` | 经办人 | 对象，包含 `displayName` 和 `name` |
| `reporter` | 创建人 | 对象，包含 `displayName` 和 `name` |
| `created` | 创建时间 | 格式：YYYY-MM-DD HH:MM:SS |
| `attachment` | 附件列表 | JsonArray，`content` 字段为下载地址 |

### 按状态分类统计

解析 `data.data` 数组，按状态统计数量：

```
open      → 开放
handling  → 处理中
resolved  → 已解决
closed    → 已关闭
notbug    → 非问题
```

### 按严重程度分类统计

```
P0  → 致命/Blocker
P1  → 严重/Critical
P2  → 一般/Major
P3  → 提示/Minor
```

### 解析命令示例

响应数据通过 `scripts/parse_bugs.py` 解析，直接管道调用：

```bash
curl -s --insecure ... | python3 scripts/parse_bugs.py
```

---

## 第五步：展示 Bug 列表

以详细列表形式展示每个 Bug 的完整信息：

```
========================================================================================================================
Bug ID: 1093597
标题: 群发消息时，如果某个老师资产不在线时 不提示发送失败，只展示了发送成功的老师
严重程度: P2 | 状态: open | 经办人: 陈毅恒
附件: -
描述: 群发催摸底测消息时 有两个lpc老师企微。其中一个老师资产在线，一个不在线...
------------------------------------------------------------------------------------------------------------------------
```

### 展示字段说明

| 字段 | 说明 |
|---|---|
| **Bug ID** | Bug 唯一标识 |
| **标题** | Bug 标题（summary） |
| **严重程度** | P1/P2/P3/P4 |
| **状态** | open/handling/resolved/closed/rejected |
| **经办人** | 当前处理人 displayName |
| **附件** | 附件 URL 列表，多个用逗号分隔；无附件展示 `-` |
| **描述** | 问题描述，去除 HTML 标签后完整展示 |

### 统计摘要

展示 Bug 总数及分布统计：

```
共 13 个 Bug

按严重程度： P1: 5 | P2: 8
按状态：     open: 10 | handling: 3
```

---

## 文件结构

```
kit-zyb-pms-
├── SKILL.md                 # 本技能文档
├── scripts/
│   ├── get_sign.py          # 验签生成脚本
│   ├── parse_bugs.py        # Bug 数据解析脚本
```

---

## 接口说明

本 skill 使用 PMS 系统的 `buglist` 接口，通过 `reqid` 参数筛选指定需求下的所有 Bug。
