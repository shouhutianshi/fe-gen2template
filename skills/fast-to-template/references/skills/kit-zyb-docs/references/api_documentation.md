# 帮帮文档API接口文档

## 概述

本文档详细说明帮帮文档（docs.yukework.com）的API接口，用于文档导出和内容获取。

## 接口端点

### 1. 创建导出任务接口

**URL**: `https://docs.yukework.com/document-application/api/v2/file/export`

**方法**: POST

**请求头**:
```http
accept: */*
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
content-type: application/json
pragma: no-cache
priority: u=1, i
sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
docs-skill-version: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Cookie: [完整的Cookie字符串]
```

**请求体**:
```json
{
    "fileId": "2003342689400123394",
    "exportType": "markdown"
}
```

**参数说明**:
- `fileId`: 文档的唯一标识符，从文档URL中提取
- `exportType`: 导出格式，支持的值：`markdown`、`html`、`pdf`等

**响应示例（成功）**:
```json
{
    "msg": "成功",
    "code": 0,
    "data": {
        "taskId": "183009_n4yLWzvXr4O1GmgE",
        "fileId": "2003342689400123394"
    },
    "requestId": "d064ae368e418eb9:bf1c90ce1b61d655:d064ae368e418eb9:1",
    "errNo": 0,
    "errStr": "成功"
}
```

**响应字段说明**:
- `code`: 响应码，0表示成功
- `data.taskId`: 导出任务ID，用于查询进度
- `data.fileId`: 文件ID，与请求一致

**成功判断条件**:
- `code == 0`
- `data.taskId`不为空

### 2. 获取导出进度接口

**URL**: `https://docs.yukework.com/document-application/api/v2/file/export/progress`

**方法**: GET

**查询参数**:
- `taskId`: 导出任务ID

**请求头**:
```http
accept: */*
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
content-type: application/json
pragma: no-cache
priority: u=1, i
sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
docs-skill-version: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
x-zyb-trace-id: [随机生成]
Cookie: [完整的Cookie字符串]
```

**响应示例**:
```json
{
    "msg": "成功",
    "code": 0,
    "data": {
        "taskId": "183009_n4yLWzvXr4O1GmgE",
        "taskStatus": 1,
        "downloadUrl": "https://zyb-saas-info-document-common.oss-cn-beijing.aliyuncs.com/export/tempres/markdown/n4yLWzvXr4O1GmgE/44965945486563/PaAd0vvODsGXR0wB?Expires=1774345204&OSSAccessKeyId=LTAI5t9kDnXNR4GfnVmuUr19&Signature=VLbyEEDfSWE%2BSihUS5szyX0l0jo%3D&response-content-disposition=attachment%3Bfilename%3D%25E6%2597%25A0%25E6%25A0%2587%25E9%25A2%2598.markdown",
        "fileId": "2003342689400123394"
    },
    "requestId": "eb35d805c8fae84a:d4e8eb2a87f3797e:62889859b8860711:1",
    "errNo": 0,
    "errStr": "成功"
}
```

**响应字段说明**:
- `code`: 响应码，0表示成功
- `data.taskStatus`: 任务状态
  - `0`: 正在导出
  - `1`: 导出成功
  - `2`: 导出失败
- `data.downloadUrl`: 下载链接（当taskStatus=1时有效）
- `data.taskId`: 任务ID

**状态判断逻辑**:
1. **导出成功**: `code == 0 && data.taskStatus == 1`
2. **正在导出**: `code == 0 && data.taskStatus == 0`
3. **导出失败**: `code != 0 || data.taskStatus == 2`

## Cookie管理

### Cookie结构
帮帮文档使用多个Cookie字段，主要包括：
- `doc_atoken`: 认证令牌
- `x_dingtalk_doc_signature`: 钉签签名
- `doc_corp_id`: 企业ID
- `ZYBIPSCAS`: CAS认证信息
- `ZYBIPSUN`: 用户名
- 其他会话相关Cookie

### Cookie获取方式
1. **自动获取**: 用户登录后，浏览器会自动设置Cookie
2. **手动获取**: 通过浏览器开发者工具查看Network请求
3. **Keychain存储**: 使用系统keychain安全存储Cookie

### Cookie有效期
- 认证令牌通常有较长的有效期（如30天）
- 会话Cookie在浏览器关闭后可能失效
- 建议定期检查Cookie有效性

## 错误码说明

### 常见错误码
- `0`: 成功
- `8000`: Cookie无效或未登录
- `4001`: 参数错误
- `4003`: 权限不足
- `5000`: 服务器内部错误
- `5001`: 导出任务创建失败

### 错误处理建议
1. **code=8000**: 重新登录获取新的Cookie
2. **code=4003**: 检查文档权限
3. **code=5000/5001**: 稍后重试

## URL格式解析

### 文档URL
```
https://docs.yukework.com/doc?fileId=2036002822277443586
```
- 提取`fileId`: `2036002822277443586`

### 登录页面URL
```
https://ips.yukework.com/static/cas-fe/?version=2.0&sdk=java&sid=document&service=https%3A%2F%2Fdocs.yukework.com%2Fdocument-application%2Fapi%2Fips%2Flogin%2Fcallback%3Fpath%3Dhttps%253A%252F%252Fdocs.yukework.com%252Fdoc%253FfileId%253D2036002822277443586#/
```
- 包含重定向逻辑
- 最终会跳转到文档URL

## 请求频率限制

### 限制规则
1. 导出任务创建：建议间隔至少5秒
2. 进度查询：建议间隔2秒
3. 并发任务：最多同时处理3个任务

### 最佳实践
1. 使用合理的等待时间
2. 实现指数退避重试
3. 监控响应时间，避免超时

## 安全注意事项

1. **Cookie保护**: 不要将Cookie硬编码在代码中
2. **HTTPS**: 所有请求都使用HTTPS
3. **数据清理**: 下载的文件读取后立即删除
4. **权限控制**: 仅访问有权限的文档
