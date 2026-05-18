#!/usr/bin/env python3
"""
获取帮帮文档内容的简化脚本
整合浏览器自动化和文档导出功能
"""

import sys
import os
import asyncio
import json
import time
import requests
from pathlib import Path

# 导入浏览器自动化模块
sys.path.append(str(Path(__file__).parent))
try:
    from browser_automation import BrowserAutomation
    from cookie_manager import CookieManager
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装依赖: pip install -r requirements.txt")
    sys.exit(1)

class DocContentFetcher:
    """文档内容获取器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.cookie_manager = CookieManager()
        self.session = requests.Session()
        self.setup_session_headers()
    
    def setup_session_headers(self):
        """设置会话头"""
        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'docs-skill-version': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        })
    
    def log(self, message: str):
        """日志输出"""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def error(self, message: str):
        """错误输出"""
        print(f"[ERROR] {message}", file=sys.stderr)
    
    def get_cookie(self) -> str:
        """获取Cookie，如果没有则自动登录获取"""
        # 1. 尝试从加密文件获取
        cookie = self.cookie_manager.get_cookie('docs.zuoyebang.cc')
        if cookie:
            self.log("从加密文件获取到Cookie")
            return cookie
        
        # 2. 需要登录
        self.log("未找到有效Cookie，需要登录")
        return None
    
    async def login_and_get_cookie(self, url: str) -> str:
        """使用浏览器自动化登录并获取Cookie"""
        self.log("使用playwright进行浏览器自动化登录...")
        
        automation = BrowserAutomation(headless=False, verbose=self.verbose)
        
        try:
            # 执行登录流程
            result = await automation.login_and_get_cookie(url)
            
            if result and result[0]:
                cookie, file_id = result
                self.log(f"登录成功，获取到fileId: {file_id}")
                
                # 加密保存Cookie到本地文件
                self.cookie_manager.save_cookie('docs.zuoyebang.cc', cookie)
                
                return cookie
            else:
                self.error("浏览器自动化登录失败")
                return None
                
        except Exception as e:
            self.error(f"登录流程异常: {e}")
            return None
        finally:
            # 确保清理资源
            await automation.cleanup()
    
    def create_export_task(self, file_id: str, cookie: str) -> str:
        """创建导出任务"""
        url = "https://docs.zuoyebang.cc/document-application/api/v2/file/export"
        
        headers = self.session.headers.copy()
        headers['Cookie'] = cookie
        
        data = {
            "fileId": file_id,
            "exportType": "markdown"
        }
        
        try:
            self.log(f"创建导出任务，fileId: {file_id}")
            response = self.session.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == 0 and result.get('data', {}).get('taskId'):
                task_id = result['data']['taskId']
                self.log(f"导出任务创建成功，taskId: {task_id}")
                return task_id
            elif result.get('code') == 8000:
                self.log("Cookie无效或未登录 (code=8000)")
                return None
            else:
                self.error(f"创建导出任务失败: {result.get('msg', '未知错误')}")
                return None
                
        except Exception as e:
            self.error(f"创建导出任务异常: {e}")
            return None
    
    def check_export_progress(self, task_id: str, cookie: str):
        """检查导出进度"""
        url = f"https://docs.zuoyebang.cc/document-application/api/v2/file/export/progress?taskId={task_id}"
        
        headers = self.session.headers.copy()
        headers['Cookie'] = cookie
        headers['x-zyb-trace-id'] = f"{int(time.time() * 1000)}"
        
        try:
            self.log(f"检查导出进度，taskId: {task_id}")
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            code = result.get('code')
            task_status = result.get('data', {}).get('taskStatus')
            
            if code == 0 and task_status == 1:
                # 导出成功
                download_url = result['data'].get('downloadUrl')
                if download_url:
                    self.log(f"导出成功，下载链接: {download_url}")
                    return download_url, True
                else:
                    self.error("导出成功但未找到下载链接")
                    return None, False
            elif code == 0 and task_status == 0:
                # 正在导出
                self.log("正在导出中...")
                return None, True
            else:
                # 导出失败
                self.error(f"导出失败，状态码: {code}, 任务状态: {task_status}")
                return None, False
                
        except Exception as e:
            self.error(f"检查导出进度异常: {e}")
            return None, False
    
    def download_and_read_content(self, download_url: str) -> str:
        """下载并读取内容"""
        try:
            self.log(f"开始下载文件: {download_url}")
            response = self.session.get(download_url, timeout=60)
            response.raise_for_status()
            
            # 获取内容
            content = response.text
            self.log(f"文件内容获取成功，大小: {len(content)} 字符")
            
            return content
            
        except Exception as e:
            self.error(f"下载文件异常: {e}")
            return None
    
    async def fetch_content(self, doc_url: str) -> str:
        """获取文档内容的主函数"""
        # 1. 提取fileId
        if 'fileId=' not in doc_url:
            self.error(f"URL格式错误，未找到fileId: {doc_url}")
            return None
        
        start = doc_url.find('fileId=') + 7
        end = doc_url.find('&', start)
        if end == -1:
            end = len(doc_url)
        file_id = doc_url[start:end]
        
        if not file_id:
            self.error("无法提取fileId")
            return None
        
        self.log(f"提取到fileId: {file_id}")
        
        # 2. 获取Cookie
        cookie = self.get_cookie()
        need_login = False
        
        # 3. 创建导出任务
        task_id = None
        if cookie:
            task_id = self.create_export_task(file_id, cookie)
            if not task_id:
                need_login = True
        
        # 4. 如果需要登录
        if not cookie or need_login:
            self.log("需要登录获取新Cookie")
            cookie = await self.login_and_get_cookie(doc_url)
            if not cookie:
                return None
            
            # 重新尝试创建导出任务
            task_id = self.create_export_task(file_id, cookie)
            if not task_id:
                return None
        
        # 5. 轮询导出进度
        max_retries = 20
        wait_seconds = 2
        
        for i in range(max_retries):
            download_url, should_continue = self.check_export_progress(task_id, cookie)
            
            if download_url:
                # 导出成功，下载文件
                break
            
            if not should_continue:
                # 导出失败
                return None
            
            # 正在导出，等待后继续
            self.log(f"等待 {wait_seconds} 秒后重试... ({i+1}/{max_retries})")
            time.sleep(wait_seconds)
        else:
            self.error(f"导出任务超时，已达到最大重试次数: {max_retries}")
            return None
        
        # 6. 下载并读取内容
        content = self.download_and_read_content(download_url)
        return content

async def main_async():
    """主函数（异步版本）"""
    if len(sys.argv) < 2:
        print("用法: python get_doc_content.py <文档URL> [--verbose]")
        return 1
    
    url = sys.argv[1]
    verbose = '--verbose' in sys.argv
    
    print("=" * 60)
    print(f"获取帮帮文档内容: {url}")
    print("=" * 60)
    
    fetcher = DocContentFetcher(verbose=verbose)
    content = await fetcher.fetch_content(url)
    
    if content:
        print("\n" + "=" * 60)
        print("✅ 文档内容获取成功！")
        print("=" * 60)
        print(content[:500] + "..." if len(content) > 500 else content)
        print(f"\n总字符数: {len(content)}")
        
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ 文档内容获取失败")
        print("=" * 60)
        return 1

def main():
    """主函数入口"""
    return asyncio.run(main_async())

if __name__ == '__main__':
    sys.exit(main())
