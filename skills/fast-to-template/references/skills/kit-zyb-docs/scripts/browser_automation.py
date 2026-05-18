#!/usr/bin/env python3
"""
浏览器自动化工具
使用playwright自动登录帮帮文档并获取Cookie
"""

import asyncio
import json
import time
import subprocess
import sys
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

try:
    from playwright.async_api import async_playwright, Page, BrowserContext
except ImportError:
    print("警告: playwright未安装，请运行: pip install playwright && playwright install")
    raise

class BrowserAutomation:
    """浏览器自动化类"""
    
    def __init__(self, headless: bool = False, verbose: bool = False):
        self.headless = headless
        self.verbose = verbose
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def log(self, message: str):
        """日志输出"""
        if self.verbose:
            print(f"[BROWSER] {message}")
    
    def error(self, message: str):
        """错误输出"""
        import sys
        print(f"[BROWSER ERROR] {message}", file=sys.stderr)
    
    async def _check_chromium_installed(self) -> bool:
        """检查Chromium浏览器是否已安装"""
        try:
            from playwright.async_api import async_playwright
            # 尝试创建playwright实例并检查chromium
            async with async_playwright() as p:
                # 检查chromium是否可用
                try:
                    await p.chromium.launch(headless=True)
                    return True
                except Exception:
                    return False
        except Exception:
            return False
    
    async def _install_chromium(self) -> bool:
        """安装Chromium浏览器"""
        try:
            self.log("正在安装Chromium浏览器，这可能需要一些时间...")
            
            # 方法1: 使用playwright的CLI命令
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                self.log("Chromium浏览器安装成功")
                return True
            else:
                self.error(f"安装失败: {result.stderr}")
                
                # 方法2: 尝试使用pip安装playwright包
                self.log("尝试重新安装playwright包...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "playwright"],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    # 再次尝试安装chromium
                    result = subprocess.run(
                        [sys.executable, "-m", "playwright", "install", "chromium"],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if result.returncode == 0:
                        self.log("✅ Chromium浏览器安装成功")
                        return True
                    else:
                        self.error(f"第二次安装失败: {result.stderr}")
                        return False
                else:
                    self.error(f"重新安装playwright失败: {result.stderr}")
                    return False
                    
        except subprocess.TimeoutExpired:
            self.error("Chromium安装超时，请手动运行: playwright install chromium")
            return False
        except Exception as e:
            self.error(f"安装Chromium时发生异常: {e}")
            return False
    
    async def setup(self):
        """设置浏览器"""
        try:
            # 检查Chromium是否已安装，如果未安装则自动安装
            if not await self._check_chromium_installed():
                self.log("Chromium浏览器未安装，正在自动安装...")
                if not await self._install_chromium():
                    self.error("Chromium浏览器安装失败，请手动运行: playwright install chromium")
                    return False
                self.log("✅ Chromium浏览器安装完成")
            
            self.playwright = await async_playwright().start()
            
            # 使用Chromium浏览器
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                ]
            )
            
            # 创建上下文
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
                ignore_https_errors=True
            )
            
            self.page = await self.context.new_page()
            
            self.log("浏览器设置完成")
            return True
            
        except Exception as e:
            self.error(f"浏览器设置失败: {e}")
            return False
    
    async def navigate_to_doc(self, url: str) -> bool:
        """导航到文档页面"""
        try:
            self.log(f"导航到: {url}")
            await self.page.goto(url, wait_until='networkidle', timeout=60000)
            
            # 检查当前URL
            current_url = self.page.url
            self.log(f"当前URL: {current_url}")
            
            # 检查当前URL
            current_url = self.page.url
            self.log(f"当前URL: {current_url}")
            
            # 方法1：检查URL是否匹配登录页面模式
            login_page_patterns = [
                'ips.zuoyebang.cc/static/cas-fe/',
                'ips.zuoyebang.cc',
                'login.zuoyebang.cc',
                '/cas/login',
                'service=https%3A%2F%2Fdocs.zuoyebang.cc',
                'document-application/api/ips/login/callback'
            ]
            
            for pattern in login_page_patterns:
                if pattern in current_url:
                    self.log(f"检测到登录页面（URL模式）: {pattern}")
                    return False  # 需要登录
            
            # 方法2：检查页面元素判断是否为登录页面
            try:
                # 检查页面标题
                page_title = await self.page.title()
                if page_title and ('内部系统登录' in page_title or '登录' in page_title or 'Login' in page_title.lower()):
                    self.log(f"检测到登录页面（标题）: {page_title}")
                    return False  # 需要登录
                
                # 检查页面内容中的登录元素
                login_selectors = [
                    'text=内部操作系统',
                    'text=员工登录',
                    'text=访客登录',
                    'text=邮箱前缀',
                    'text=密码',
                    'text=钉钉扫码',
                    'input[type="password"]',
                    '.login',
                    '.login-board',
                    '.el-form',
                    '.login-container'
                ]
                
                for selector in login_selectors:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            self.log(f"检测到登录页面（元素: {selector}）")
                            return False  # 需要登录
                    except:
                        continue
                
            except Exception as e:
                self.log(f"检查页面元素时出错: {e}")
            
            # 方法3：检查是否已登录并进入文档页面
            if 'docs.zuoyebang.cc' in current_url and 'fileId=' in current_url:
                self.log("已进入文档页面")
                return True  # 已登录
            
            # 方法4：检查是否跳转到文档页面但可能没有fileId参数
            if 'docs.zuoyebang.cc' in current_url:
                self.log(f"已进入帮帮文档域名: {current_url}")
                # 进一步检查页面内容确认不是登录页面
                try:
                    page_title = await self.page.title()
                    if page_title and '登录' not in page_title and 'Login' not in page_title:
                        self.log(f"页面标题不包含登录字样: {page_title}，可能已登录")
                        return True
                    
                    # 检查是否有用户信息元素
                    user_elements = await self.page.query_selector_all('.user-info, .user-name, .avatar')
                    if len(user_elements) > 0:
                        self.log(f"检测到用户信息元素，确认已登录")
                        return True
                    
                    # 检查是否为文档页面（分享、演示按钮等）
                    if await self._is_document_page():
                        self.log("检测到文档页面特征元素，确认已登录")
                        return True
                        
                except:
                    pass
            
            # 如果以上方法都无法判断，默认需要进一步判断
            self.log(f"无法确定页面状态，需要进一步判断: {current_url}")
            return False
            
        except Exception as e:
            self.error(f"导航失败: {e}")
            return False
    
    async def wait_for_login(self, timeout: int = 120) -> bool:
        """等待用户登录完成"""
        self.log("等待用户登录...")
        print("\n" + "="*60)
        print("请完成以下登录步骤:")
        print("1. 使用钉钉账号登录（可能需要扫码）")
        print("2. 登录成功后页面会自动跳转")
        print("3. 检测到登录成功后会自动继续流程")
        print("="*60 + "\n")
        
        start_time = time.time()
        last_url = ""
        login_attempts = 0
        
        try:
            while time.time() - start_time < timeout:
                current_url = self.page.url
                
                # 检测URL变化
                if current_url != last_url:
                    self.log(f"URL变化: {current_url[:150]}...")
                    last_url = current_url
                    login_attempts += 1
                
                # 方法1：检查当前是否在登录页面（基于元素）
                is_on_login_page = await self._is_login_page_by_elements()
                if is_on_login_page:
                    # 仍然在登录页面
                    if login_attempts % 5 == 0:  # 每5次检查报告一次
                        self.log("仍在登录页面，等待用户操作...")
                else:
                    # 不再在登录页面，可能登录成功
                    self.log("✅ 检测到已离开登录页面，可能登录成功")
                    
                    # 检查是否进入文档页面
                    if 'docs.zuoyebang.cc' in current_url:
                        self.log(f"✅ 已进入帮帮文档页面: {current_url[:100]}...")
                        
                        # 进一步确认登录成功
                        if await self._confirm_login_success():
                            return True
                    
                    # 检查是否为文档页面（即使不在docs.zuoyebang.cc域名）
                    if await self._is_document_page():
                        self.log("✅ 检测到文档页面特征元素（分享、演示等）")
                        return True
                
                # 方法2：检查明确的成功URL模式
                success_indicators = [
                    ('docs.zuoyebang.cc/doc?fileId=', '已登录并进入文档页面'),
                    ('docs.zuoyebang.cc/doc/', '已登录并进入文档页面'),
                    ('docs.zuoyebang.cc/edit', '已登录并进入编辑页面'),
                    ('docs.zuoyebang.cc/d/', '已登录并进入文档查看页面'),
                    ('docs.zuoyebang.cc/spaces', '已登录，进入空间列表'),
                    ('docs.zuoyebang.cc/home', '已登录，进入首页'),
                ]
                
                for pattern, message in success_indicators:
                    if pattern in current_url:
                        self.log(f"✅ {message}")
                        
                        # 等待页面加载
                        try:
                            await self.page.wait_for_load_state('domcontentloaded', timeout=10000)
                        except:
                            pass  # 超时可忽略
                        
                        self.log("✅ 登录成功确认")
                        return True
                
                # 检查是否出现登录错误
                error_selectors = [
                    'text=登录失败',
                    'text=账号或密码错误',
                    'text=验证码错误',
                    'text=验证失败',
                    'text=扫码失败',
                    '.error-message',
                    '.login-error',
                    '.ant-message-error',
                    '.el-message--error',
                    '.el-message-box__error'
                ]
                
                for selector in error_selectors:
                    try:
                        error_element = await self.page.query_selector(selector)
                        if error_element:
                            error_text = await error_element.text_content()
                            self.error(f"❌ 登录错误: {error_text}")
                            return False
                    except:
                        pass
                
                # 每10次检查报告一次状态
                if login_attempts % 10 == 0:
                    status = "登录页面" if is_on_login_page else "可能已登录"
                    self.log(f"登录检测中... 状态: {status}, 检查次数: {login_attempts}")
                
                # 等待2秒后再次检查
                await asyncio.sleep(2)
            
            self.error(f"❌ 登录超时 ({timeout}秒)")
            self.log(f"最终URL: {last_url[:150]}...")
            self.log(f"检测次数: {login_attempts}")
            return False
            
        except Exception as e:
            self.error(f"❌ 等待登录时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _is_login_page_by_elements(self) -> bool:
        """通过页面元素判断是否在登录页面"""
        try:
            # 检查页面标题
            page_title = await self.page.title()
            if page_title and ('内部系统登录' in page_title or '登录' in page_title or 'Login' in page_title.lower()):
                self.log(f"检测到登录页面（标题）: {page_title}")
                return True
            
            # 检查页面内容中的登录元素
            login_selectors = [
                'text=内部操作系统',
                'text=员工登录',
                'text=访客登录',
                'text=邮箱前缀',
                'text=密码',
                'text=钉钉扫码',
                'input[type="password"]',
                '.login',
                '.login-board',
                '.el-form',
                '.login-container'
            ]
            
            for selector in login_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        # 如果是文本元素，检查是否可见
                        if selector.startswith('text='):
                            is_visible = await element.is_visible()
                            if is_visible:
                                self.log(f"检测到登录页面元素（可见: {selector}）")
                                return True
                        else:
                            self.log(f"检测到登录页面元素（{selector}）")
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.log(f"检查登录页面元素时出错: {e}")
            return False
    
    async def _confirm_login_success(self) -> bool:
        """确认登录成功"""
        try:
            # 检查页面标题不包含登录字样
            page_title = await self.page.title()
            if page_title:
                login_keywords = ['登录', 'Login', 'Sign In', '认证', '验证', '内部系统登录']
                has_login_keyword = any(keyword in page_title for keyword in login_keywords)
                
                if not has_login_keyword:
                    self.log(f"✅ 页面标题不含登录字样: {page_title[:50]}")
                    
                    # 检查是否有用户信息元素
                    user_elements = await self.page.query_selector_all('.user-info, .user-name, .avatar, .ant-avatar, .el-avatar')
                    if len(user_elements) > 0:
                        self.log(f"✅ 检测到用户信息元素 ({len(user_elements)}个)")
                        return True
                    
                    # 检查是否有文档内容元素
                    doc_elements = await self.page.query_selector_all('.document-content, .doc-content, .editor-content, .prosemirror')
                    if len(doc_elements) > 0:
                        self.log(f"✅ 检测到文档内容元素 ({len(doc_elements)}个)")
                        return True
                    
                    # 检查是否有导航栏或菜单
                    nav_elements = await self.page.query_selector_all('.nav, .navbar, .menu, .sidebar')
                    if len(nav_elements) > 0:
                        self.log(f"✅ 检测到导航元素 ({len(nav_elements)}个)")
                        return True
                    
                    # 检查是否有文档页面特征元素（分享、演示按钮）
                    if await self._is_document_page():
                        self.log("✅ 检测到文档页面特征元素")
                        return True
            
            return False
            
        except Exception as e:
            self.log(f"确认登录成功时出错: {e}")
            return False
    
    async def _is_document_page(self) -> bool:
        """检查是否为文档页面（根据分享、演示span等特征元素）"""
        try:
            # 检查是否包含"分享"或"演示"的span或按钮
            share_demo_selectors = [
                'text=分享',
                'text=演示',
                'span:has-text("分享")',
                'span:has-text("演示")',
                '.share-button',
                '.demo-button',
                'button:has-text("分享")',
                'button:has-text("演示")'
            ]
            
            for selector in share_demo_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        self.log(f"检测到文档页面元素: {selector}")
                        return True
                except:
                    continue
            
            # 检查是否包含文档编辑器相关元素
            editor_selectors = [
                '.doc-editor',
                '.editor-wrapper',
                '.document-editor',
                '[contenteditable="true"]',
                '.ql-editor',
                '.w-e-text',
                '.ProseMirror'
            ]
            
            for selector in editor_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        self.log(f"检测到文档编辑器元素: {selector}")
                        return True
                except:
                    continue
            
            # 检查是否包含文档功能相关元素
            doc_function_selectors = [
                'text=编辑',
                'text=预览',
                'text=导出',
                'text=历史',
                'text=协作',
                '.doc-toolbar',
                '.doc-menu',
                '.doc-actions'
            ]
            
            for selector in doc_function_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        self.log(f"检测到文档功能元素: {selector}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.log(f"检查文档页面时出错: {e}")
            return False
    
    async def get_cookies(self) -> Optional[str]:
        """获取当前页面的Cookie"""
        try:
            # 获取所有Cookie
            cookies = await self.context.cookies()
            
            # 过滤出docs.zuoyebang.cc的Cookie
            doc_cookies = []
            for cookie in cookies:
                if 'docs.zuoyebang.cc' in cookie.get('domain', '') or 'zuoyebang.cc' in cookie.get('domain', ''):
                    doc_cookies.append(f"{cookie['name']}={cookie['value']}")
            
            if not doc_cookies:
                self.error("未找到docs.zuoyebang.cc的Cookie")
                return None
            
            # 组合Cookie字符串
            cookie_string = '; '.join(doc_cookies)
            
            # 验证Cookie是否包含必要字段
            cookie_dict = self._parse_cookie_string(cookie_string)
            required_fields = ['doc_atoken', 'x_dingtalk_doc_signature']
            
            for field in required_fields:
                if field not in cookie_dict:
                    self.error(f"Cookie缺少必要字段: {field}")
                    return None
            
            self.log(f"获取到Cookie，包含 {len(doc_cookies)} 个字段")
            if self.verbose:
                self.log(f"Cookie预览: {cookie_string[:200]}...")
            
            return cookie_string
            
        except Exception as e:
            self.error(f"获取Cookie失败: {e}")
            return None
    
    def _parse_cookie_string(self, cookie_string: str) -> Dict[str, str]:
        """解析Cookie字符串为字典"""
        cookie_dict = {}
        items = cookie_string.split(';')
        
        for item in items:
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookie_dict[key.strip()] = value.strip()
        
        return cookie_dict
    
    async def extract_file_id(self) -> Optional[str]:
        """从当前页面提取fileId"""
        try:
            current_url = self.page.url
            
            # 从URL中提取fileId
            if 'fileId=' in current_url:
                start = current_url.find('fileId=') + 7
                end = current_url.find('&', start)
                if end == -1:
                    end = len(current_url)
                file_id = current_url[start:end]
                
                self.log(f"从URL提取到fileId: {file_id}")
                return file_id
            
            # 尝试从页面中提取
            file_id_selectors = [
                '[data-file-id]',
                '.file-id',
                'input[name="fileId"]',
                'meta[name="fileId"]'
            ]
            
            for selector in file_id_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        file_id = await element.get_attribute('data-file-id') or await element.get_attribute('value') or await element.get_attribute('content')
                        if file_id:
                            self.log(f"从页面元素提取到fileId: {file_id}")
                            return file_id
                except:
                    pass
            
            self.error("无法提取fileId")
            return None
            
        except Exception as e:
            self.error(f"提取fileId失败: {e}")
            return None
    
    async def cleanup(self):
        """清理资源"""
        try:
            if self.page:
                await self.page.close()
                self.log("页面已关闭")
            
            if self.context:
                await self.context.close()
                self.log("上下文已关闭")
            
            if self.browser:
                await self.browser.close()
                self.log("浏览器已关闭")
            
            if self.playwright:
                await self.playwright.stop()
                self.log("playwright已停止")
                
        except Exception as e:
            self.error(f"清理资源时出错: {e}")
    
    async def login_and_get_cookie(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """完整的登录流程，返回Cookie和fileId"""
        try:
            # 1. 设置浏览器
            if not await self.setup():
                return None, None
            
            # 2. 导航到文档页面
            if not await self.navigate_to_doc(url):
                # 需要登录
                self.log("需要用户登录")
                
                # 3. 等待用户登录
            # 3. 等待用户登录（减少超时时间）
            if not await self.wait_for_login():
                self.error("用户登录失败或超时")
                await self.cleanup()
                return None, None
            
            # 4. 等待页面稳定，确认已登录
            self.log("等待页面稳定...")
            try:
                await self.page.wait_for_timeout(3000)  # 等待3秒让页面完全稳定
            except:
                pass
            
            # 5. 获取Cookie
            cookie = await self.get_cookies()
            if not cookie:
                self.error("无法获取Cookie，可能登录未成功")
                await self.cleanup()
                return None, None
            
            # 6. 提取fileId
            file_id = await self.extract_file_id()
            if not file_id:
                self.log("⚠️ 无法从当前页面提取fileId，尝试从URL提取")
                # 从原始URL提取
                if 'fileId=' in url:
                    start = url.find('fileId=') + 7
                    end = url.find('&', start)
                    if end == -1:
                        end = len(url)
                    file_id = url[start:end]
            
            if not file_id:
                self.error("❌ 无法获取fileId")
                await self.cleanup()
                return None, None
            
            self.log(f"✅ 登录成功")
            self.log(f"  获取到fileId: {file_id}")
            self.log(f"  获取到Cookie长度: {len(cookie)} 字符")
            
            # 7. 关闭浏览器（用户已登录完成）
            await self.cleanup()
            
            return cookie, file_id
            
        except Exception as e:
            self.error(f"登录流程失败: {e}")
            await self.cleanup()
            return None, None
    
    async def quick_login_test(self, url: str) -> Optional[str]:
        """快速登录测试（不保留浏览器）"""
        try:
            # 1. 设置浏览器
            if not await self.setup():
                return None
            
            # 2. 导航到文档页面
            if not await self.navigate_to_doc(url):
                # 需要登录
                self.log("需要用户登录")
                
                # 3. 等待用户登录
                if not await self.wait_for_login():
                    await self.cleanup()
                    return None
            
            # 4. 获取Cookie
            cookie = await self.get_cookies()
            
            # 5. 清理资源
            await self.cleanup()
            
            return cookie
            
        except Exception as e:
            self.error(f"快速登录测试失败: {e}")
            await self.cleanup()
            return None

def main():
    """测试函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python browser_automation.py <文档URL> [--headless] [--verbose]")
        return 1
    
    url = sys.argv[1]
    headless = '--headless' in sys.argv
    verbose = '--verbose' in sys.argv
    
    async def run():
        automation = BrowserAutomation(headless=headless, verbose=verbose)
        cookie = await automation.quick_login_test(url)
        
        if cookie:
            print(f"\n✅ 登录成功！获取到Cookie:")
            print(cookie[:200] + "..." if len(cookie) > 200 else cookie)
            return 0
        else:
            print("\n❌ 登录失败")
            return 1
    
    return asyncio.run(run())

if __name__ == '__main__':
    import sys
    sys.exit(main())
