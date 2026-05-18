---
name: kit-zyb-docs
description: 该技能用于获取帮帮文档（docs.zuoyebang.cc）内容，支持自动登录、Cookie管理、文档导出和内容提取功能。
---

# 帮帮文档获取技能

## 使用时机

当用户需要读取帮帮文档链接、提取文档内容、或批量处理帮帮文档时使用此技能。

## 核心功能

1. **Cookie管理**：加密存储docs.zuoyebang.cc的Cookie到本地文件，使用Fernet对称加密
2. **登录处理**：当Cookie无效或未登录时，自动在浏览器中打开文档并引导用户登录
3. **文档导出**：通过API创建导出任务，将文档导出为markdown格式
4. **内容提取**：下载导出的文档并提取文本内容

## 工作流程

1. 从本地加密文件中获取docs.zuoyebang.cc的Cookie（自动解密）
2. 如果获取成功，使用Cookie创建导出任务
3. 如果获取失败或Cookie为空，在浏览器中打开文档引导用户登录
4. 用户登录后，获取Cookie并加密保存到本地文件
5. 使用Cookie创建导出任务，获取taskId
6. 轮询导出进度，等待导出完成
7. 导出成功后，从downloadUrl下载文件
8. 读取文件内容，完成后删除本地文件

## 接口说明

### 创建导出任务
- **接口地址**：`https://docs.zuoyebang.cc/document-application/api/v2/file/export`
- **请求方法**：POST
- **请求头**：需要包含Cookie和content-type: application/json
- **请求体**：`{"fileId": "文件ID", "exportType": "markdown"}`
- **成功判断**：code == 0 && data.taskId不为空

### 获取导出进度
- **接口地址**：`https://docs.zuoyebang.cc/document-application/api/v2/file/export/progress?taskId={taskId}`
- **请求方法**：GET
- **请求头**：需要包含Cookie
- **状态判断**：
  - 导出成功：code = 0 && data.taskStatus = 1
  - 正在导出：code = 0 && data.taskStatus = 0
  - 导出失败：code != 0 || data.taskStatus = 2

## 文件ID提取

从文档链接中提取fileId：
- 文档链接格式：`https://docs.zuoyebang.cc/doc?fileId={fileId}`
- 登录页面格式：包含重定向参数，最终会跳转到上述格式

## 脚本使用

### fetch_bangbang_doc.py
主脚本，提供完整功能：
```bash
# 获取文档内容（仅显示预览，不保存文件）
python scripts/fetch_bangbang_doc.py --url "https://docs.zuoyebang.cc/doc?fileId=2003342689400123394"

# 获取并保存到指定文件
python scripts/fetch_bangbang_doc.py --url "文档URL" --output "output.md"
```

### cookie_manager.py
Cookie管理工具，用于keychain操作：
```bash
python scripts/cookie_manager.py --action get --domain docs.zuoyebang.cc
python scripts/cookie_manager.py --action save --domain docs.zuoyebang.cc --cookie "your_cookie_here"
```

### browser_automation.py
浏览器自动化工具，使用playwright自动登录：
```bash
# 测试登录功能
python scripts/browser_automation.py "https://docs.zuoyebang.cc/doc?fileId=2003342689400123394" --verbose
```

## 依赖包

确保以下Python包已安装：
```bash
pip install requests cryptography beautifulsoup4 playwright
# 安装playwright浏览器
playwright install chromium
```

## 浏览器自动化功能

当Cookie无效或不存在时，技能会自动使用playwright打开浏览器进行登录：

### 自动化流程
1. **检测Cookie状态**：检查本地加密文件中是否有有效Cookie
2. **打开浏览器**：使用Chromium浏览器打开文档链接
3. **等待用户登录**：显示提示信息，等待用户手动输入账号密码
4. **检测登录成功**：监听页面跳转，检测是否成功进入文档页面
5. **获取Cookie**：从浏览器上下文中提取登录后的Cookie
6. **保存Cookie**：将获取的Cookie加密保存到本地文件
7. **继续导出流程**：使用新Cookie创建导出任务

### 优势
- **无需手动操作**：自动处理浏览器打开和Cookie获取
- **安全可靠**：使用Fernet对称加密安全存储Cookie到本地文件
- **跨平台支持**：支持macOS、Linux、Windows
- **灵活配置**：可配置headless模式或无头模式

## 错误处理

1. **Cookie无效或过期**：自动打开浏览器引导重新登录
2. **导出任务失败**：返回错误信息，建议重新尝试
3. **网络问题**：重试机制，最多重试3次
4. **文件下载失败**：检查网络连接和权限
5. **浏览器自动化失败**：回退到传统登录方式

## 最佳实践

1. 对于批量处理，建议先测试单个文档
2. Cookie会自动加密保存到 ~/.bangbang-doc-fetcher 目录
3. 定期检查Cookie有效性
4. 处理大文档时，注意网络超时设置

## 输出格式

默认输出markdown格式内容，也可通过参数指定其他格式：
```bash
python scripts/fetch_bangbang_doc.py --url "文档链接" --output-format html
```

## 注意事项

1. 需要用户有帮帮文档的访问权限
2. Cookie安全性：使用Fernet对称加密保存到本地文件 (~/.bangbang-doc-fetcher/)
3. 导出任务可能有并发限制，建议合理控制请求频率
4. 下载的文件会在读取后自动删除，确保隐私安全
