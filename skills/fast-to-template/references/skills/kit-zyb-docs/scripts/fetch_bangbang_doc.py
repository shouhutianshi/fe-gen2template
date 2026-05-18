#!/usr/bin/env python3
"""
帮帮文档获取工具
用于从docs.zuoyebang.cc获取文档内容
"""

import os
import sys
import json
import time
import requests
import argparse
import tempfile
import webbrowser
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# 添加父目录到路径，以便导入cookie_manager
sys.path.append(str(Path(__file__).parent.parent))
from scripts.cookie_manager import CookieManager

class BangbangDocFetcher:
    """帮帮文档获取器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.cookie_manager = CookieManager()
        self.session = requests.Session()
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
    
    def extract_file_id(self, url: str) -> Optional[str]:
        """从URL中提取fileId"""
        try:
            parsed = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed.query)
            file_id = query_params.get('fileId', [None])[0]
            
            if file_id:
                self.log(f"从URL提取到fileId: {file_id}")
                return file_id
            
            # 尝试从路径中提取
            if 'fileId=' in url:
                start = url.find('fileId=') + 7
                end = url.find('&', start)
                if end == -1:
                    end = len(url)
                file_id = url[start:end]
                self.log(f"从URL中提取fileId: {file_id}")
                return file_id
            
            self.error(f"无法从URL提取fileId: {url}")
            return None
            
        except Exception as e:
            self.error(f"提取fileId失败: {e}")
            return None
    
    def get_cookie(self) -> Optional[str]:
        """从加密文件获取Cookie"""
        try:
            cookie = self.cookie_manager.get_cookie('docs.zuoyebang.cc')
            if cookie:
                self.log("从加密文件获取到Cookie")
                return cookie
            else:
                self.log("加密文件中没有找到Cookie")
                return None
        except Exception as e:
            self.error(f"获取Cookie失败: {e}")
            return None
    
    def save_cookie(self, cookie: str):
        """加密保存Cookie到本地文件"""
        try:
            self.cookie_manager.save_cookie('docs.zuoyebang.cc', cookie)
            self.log("Cookie已加密保存到本地文件")
        except Exception as e:
            self.error(f"保存Cookie失败: {e}")
    
    def open_browser_for_login(self, url: str) -> Optional[str]:
        """在浏览器中打开文档，引导用户登录"""
        self.log("开始浏览器登录流程...")
        
        try:
            # 导入浏览器自动化模块
            from scripts.browser_automation import BrowserAutomation
            import asyncio
            
            # 创建浏览器自动化实例
            self.log("初始化playwright浏览器自动化...")
            automation = BrowserAutomation(headless=False, verbose=self.verbose)
            
            # 运行登录流程
            async def run_login():
                return await automation.login_and_get_cookie(url)
            
            # 执行异步任务
            self.log("执行登录流程...")
            result = asyncio.run(run_login())
            
            if result and result[0]:
                cookie, file_id = result
                self.log(f"✅ 登录成功")
                self.log(f"  获取到fileId: {file_id}")
                self.log(f"  Cookie长度: {len(cookie)} 字符")
                
                # 加密保存Cookie到本地文件
                self.save_cookie(cookie)
                
                return cookie
            else:
                self.error("❌ 浏览器自动化登录失败")
                return None
                
        except ImportError as e:
            self.log("⚠️ playwright未安装: {e}")
            self.log("使用传统手动登录方法...")
            print("=" * 60)
            print("请在浏览器中登录帮帮文档账号...")
            print("=" * 60)
            
            # 打开浏览器
            webbrowser.open(url)
            
            # 等待用户登录
            try:
                input("登录完成后，按Enter键继续...")
            except EOFError:
                self.error("非交互式环境，无法等待用户输入")
                return None
            
            # 提示用户获取Cookie
            print("\n" + "=" * 60)
            print("请按照以下步骤获取Cookie:")
            print("1. 在浏览器中按F12打开开发者工具")
            print("2. 切换到Network标签页")
            print("3. 刷新页面")
            print("4. 找到任意一个docs.zuoyebang.cc的请求")
            print("5. 在Request Headers中找到Cookie")
            print("6. 复制完整的Cookie字符串")
            print("=" * 60)
            
            try:
                cookie = input("\n请输入Cookie: ").strip()
                if cookie:
                    self.save_cookie(cookie)
                    self.log(f"✅ 手动登录成功，Cookie长度: {len(cookie)} 字符")
                    return cookie
                else:
                    self.error("❌ 未提供Cookie")
                    return None
            except EOFError:
                self.error("❌ 非交互式环境，无法获取Cookie输入")
                return None
        except Exception as e:
            self.error(f"❌ 登录流程异常: {e}")
            return None
    
    def create_export_task(self, file_id: str, cookie: str) -> Optional[str]:
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
            self.log(f"创建任务响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
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
                
        except requests.exceptions.RequestException as e:
            self.error(f"网络请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            self.error(f"JSON解析失败: {e}")
            return None
    
    def check_export_progress(self, task_id: str, cookie: str) -> Tuple[Optional[str], bool]:
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
            self.log(f"进度检查响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
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
                
        except requests.exceptions.RequestException as e:
            self.error(f"网络请求失败: {e}")
            return None, False
        except json.JSONDecodeError as e:
            self.error(f"JSON解析失败: {e}")
            return None, False
    
    def download_file(self, download_url: str, cookie: str = None) -> Optional[str]:
        """使用curl命令下载文件到临时目录
        Args:
            download_url: 下载链接
            cookie: Cookie字符串（可选）
        Returns:
            临时文件路径，或者None表示失败
        """
        # 直接使用curl下载，避免requests的URL编码问题
        return self._download_with_curl(download_url, cookie)
    
    def _download_with_curl(self, download_url: str, cookie: str = None) -> Optional[str]:
        """使用curl命令下载文件（解决requests编码问题）
        Args:
            download_url: 下载链接
            cookie: Cookie字符串（可选）
        Returns:
            临时文件路径，或者None表示失败
        """
        self.log(f"使用curl下载文件: {download_url[:100]}...")
        
        import subprocess
        import tempfile
        import os
        
        # 创建curl命令
        curl_cmd = ['curl', '-s', '-L', '--max-time', '60']
        
        # 添加headers
        curl_cmd.extend(['-H', 'accept: */*'])
        curl_cmd.extend(['-H', 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'])
        curl_cmd.extend(['-H', 'referer: https://docs.zuoyebang.cc/'])
        
        if cookie:
            curl_cmd.extend(['-H', f'Cookie: {cookie}'])
        
        # 添加URL
        curl_cmd.append(download_url)
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(
            mode='wb',
            suffix='.md',
            delete=False,
            prefix='bangbang_doc_curl_'
        )
        temp_file.close()
        
        # 执行curl命令，输出到临时文件
        curl_cmd.extend(['-o', temp_file.name])
        
        try:
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.error(f"curl命令失败，返回码: {result.returncode}")
                if result.stderr:
                    self.error(f"错误信息: {result.stderr[:200]}")
                return None
            
            # 检查文件大小
            file_size = os.path.getsize(temp_file.name)
            if file_size < 100:
                self.error(f"下载的内容过短: {file_size} 字节")
                os.unlink(temp_file.name)
                return None
            
            self.log(f"curl下载成功，文件大小: {file_size} 字节")
            return temp_file.name
            
        except subprocess.TimeoutExpired:
            self.error("curl下载超时")
            return None
        except Exception as e:
            self.error(f"curl下载异常: {e}")
            return None
    
    def read_file_content(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.log(f"文件内容读取成功，大小: {len(content)} 字符")
            return content
        except Exception as e:
            self.error(f"读取文件失败: {e}")
            return None
        finally:
            # 删除临时文件
            try:
                os.unlink(file_path)
                self.log(f"临时文件已删除: {file_path}")
            except:
                pass
    
    def fetch_document(self, url: str) -> Optional[str]:
        """获取文档内容的主函数"""
        # 1. 提取fileId
        file_id = self.extract_file_id(url)
        if not file_id:
            return None
        
        # 2. 获取Cookie并尝试创建导出任务
        cookie = self.get_cookie()
        task_id = None
        
        if cookie:
            # 先尝试使用现有Cookie
            self.log("尝试使用现有Cookie创建导出任务...")
            task_id = self.create_export_task(file_id, cookie)
            
            # 如果任务创建失败，说明Cookie可能已过期
            if not task_id:
                self.log("⚠️ 现有Cookie可能已过期，需要重新登录...")
        
        # 3. 如果任务创建失败（Cookie无效或不存在），进行登录
        if not task_id:
            self.log("🔐 需要用户登录获取新Cookie...")
            print("\n" + "="*60)
            print("即将打开浏览器进行登录...")
            print("请确保您有帮帮文档的访问权限")
            print("登录后浏览器会自动关闭")
            print("="*60 + "\n")
            
            cookie = self.open_browser_for_login(url)
            if not cookie:
                self.error("❌ 登录失败")
                return None
            
            self.log("✅ 登录成功，使用新Cookie创建导出任务...")
            task_id = self.create_export_task(file_id, cookie)
            if not task_id:
                self.error("❌ 使用新Cookie创建任务失败")
                return None
        
        # 4. 轮询导出进度
        max_retries = 20
        wait_seconds = 2
        
        for i in range(max_retries):
            download_url, should_continue = self.check_export_progress(task_id, cookie)
            
            if download_url:
                # 导出成功
                self.log("✅ 导出任务完成，获取到下载链接")
                self.log(f"下载链接: {download_url[:150]}...")
                break
            
            if not should_continue:
                # 导出失败
                self.error("❌ 导出任务失败")
                return None
            
            # 正在导出，等待后继续
            if i % 5 == 0:  # 每5次报告一次
                self.log(f"⏳ 正在导出中... ({i+1}/{max_retries})")
            time.sleep(wait_seconds)
        else:
            self.error(f"❌ 导出任务超时，已达到最大重试次数: {max_retries}")
            return None
        
        # 5. 使用curl直接下载文件
        self.log("📥 开始下载文档文件...")
        temp_file = self.download_file(download_url, cookie)
        if not temp_file:
            self.error("❌ 文件下载失败")
            return None
        
        # 6. 读取内容并自动清理临时文件
        self.log("📖 读取文档内容...")
        content = self.read_file_content(temp_file)
        if content:
            self.log(f"✅ 文档内容获取成功，大小: {len(content)} 字符")
        else:
            self.error("❌ 读取文件内容失败")
            
        return content

def main():
    parser = argparse.ArgumentParser(description='获取帮帮文档内容')
    parser.add_argument('--url', required=True, help='帮帮文档URL')
    parser.add_argument('--output', help='输出文件路径（可选）')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("开始获取帮帮文档内容")
    print(f"文档URL: {args.url}")
    print("=" * 70)
    
    fetcher = BangbangDocFetcher(verbose=args.verbose)
    content = fetcher.fetch_document(args.url)
    
    if content:
        print("\n" + "=" * 70)
        print("✅ 文档内容获取成功！")
        print("=" * 70)
        
        # 显示文档标题预览
        lines = content.split('\n')
        title = lines[0] if lines else "未找到标题"
        print(f"文档标题: {title}")
        print(f"文档大小: {len(content)} 字符")
        print(f"行数: {len(lines)}")
        
        # 只在指定 --output 参数时保存到文件
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 内容已保存到: {args.output}")
            except Exception as e:
                print(f"❌ 保存文件失败: {e}")
        
        # 总是显示内容预览
        preview = content[:500]
        if len(content) > 500:
            preview += "..."
        print(f"\n内容预览:\n{preview}")
        
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ 文档内容获取失败")
        print("=" * 70)
        
        print("\n建议:")
        print("1. 检查文档URL是否正确")
        print("2. 确认您有文档的访问权限")
        print("3. 尝试手动在浏览器中访问文档")
        print("4. 检查网络连接")
        print("5. 使用 --verbose 参数查看详细错误信息")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
