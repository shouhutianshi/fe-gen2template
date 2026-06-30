#!/usr/bin/env python3
"""
Cookie管理器
用于安全地存储和获取Cookie到加密的本地文件
"""

import sys
import json
import os
import argparse
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

@dataclass
class CookieInfo:
    """Cookie信息"""
    cookie_string: str
    domain: str
    created_at: str
    expires_at: Optional[str] = None
    is_valid: bool = True

class CookieManager:
    """Cookie管理器类"""
    
    SERVICE_NAME = "bangbang-doc-fetcher"
    
    def __init__(self, storage_dir: Optional[str] = None):
        """初始化Cookie管理器
        
        Args:
            storage_dir: 存储目录，默认为 ~/.bangbang-doc-fetcher
        """
        self.service = self.SERVICE_NAME
        self.storage_dir = Path(storage_dir) if storage_dir else Path.home() / '.bangbang-doc-fetcher'
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._key = self._get_or_create_encryption_key()
        self._cipher = Fernet(self._key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """获取或创建加密密钥

        使用随机生成的密钥，更安全
        """
        key_file = self.storage_dir / '.key'

        if key_file.exists():
            # 从文件读取密钥（已经是正确的格式，无需解码）
            return key_file.read_bytes()

        # 直接生成随机密钥（更安全）
        key = Fernet.generate_key()

        # 保存密钥
        key_file.write_bytes(key)
        key_file.chmod(0o600)  # 仅所有者可读写

        return key
    
    def _get_machine_id(self) -> str:
        """获取机器唯一标识"""
        import platform
        
        # 组合多个机器特征生成唯一标识
        identifiers = [
            platform.node(),  # 主机名
            platform.system(),  # 操作系统
            platform.machine(),  # 机器架构
        ]
        
        return '|'.join(identifiers)
    
    def _make_key(self, domain: str) -> str:
        """生成存储键名"""
        return f"cookie_{domain}"
    
    def _get_cookie_file_path(self, domain: str) -> Path:
        """获取Cookie文件路径"""
        safe_domain = domain.replace('.', '_').replace('-', '_')
        return self.storage_dir / f"{safe_domain}.enc"
    
    def _encrypt_data(self, data: str) -> bytes:
        """加密数据
        
        Args:
            data: 明文字符串
            
        Returns:
            加密后的字节
        """
        return self._cipher.encrypt(data.encode('utf-8'))
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """解密数据
        
        Args:
            encrypted_data: 加密的字节
            
        Returns:
            解密后的字符串
        """
        return self._cipher.decrypt(encrypted_data).decode('utf-8')
    
    def save_cookie(self, domain: str, cookie_string: str, expires_hours: int = 720):
        """加密保存Cookie到本地文件
        
        Args:
            domain: 域名，如 'docs.yukework.com'
            cookie_string: Cookie字符串
            expires_hours: 过期时间（小时），默认30天
        """
        try:
            # 创建Cookie信息对象
            created_at = datetime.now().isoformat()
            expires_at = None
            
            if expires_hours > 0:
                expires_at = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
            
            cookie_info = CookieInfo(
                cookie_string=cookie_string,
                domain=domain,
                created_at=created_at,
                expires_at=expires_at,
                is_valid=True
            )
            
            # 转换为JSON字符串
            cookie_json = json.dumps(cookie_info.__dict__)
            
            # 加密数据
            encrypted_data = self._encrypt_data(cookie_json)
            
            # 保存到加密文件
            cookie_file = self._get_cookie_file_path(domain)
            cookie_file.write_bytes(encrypted_data)
            cookie_file.chmod(0o600)  # 仅所有者可读写
            
            print(f"[SUCCESS] Cookie已加密保存到文件: {cookie_file}")
            print(f"          域名: {domain}")
            print(f"          创建时间: {created_at}")
            if expires_at:
                print(f"          过期时间: {expires_at}")
                
        except Exception as e:
            print(f"[ERROR] 保存Cookie失败: {e}")
            raise
    
    def get_cookie(self, domain: str) -> Optional[str]:
        """从加密文件获取并解密Cookie
        
        Args:
            domain: 域名
            
        Returns:
            Cookie字符串，如果不存在或已过期则返回None
        """
        try:
            # 读取加密文件
            cookie_file = self._get_cookie_file_path(domain)
            
            if not cookie_file.exists():
                print(f"[INFO] 未找到{domain}的Cookie文件")
                return None
            
            # 读取加密数据
            encrypted_data = cookie_file.read_bytes()
            
            # 解密数据
            cookie_json = self._decrypt_data(encrypted_data)
            
            # 解析Cookie信息
            cookie_dict = json.loads(cookie_json)
            cookie_info = CookieInfo(**cookie_dict)
            
            # 检查是否过期
            if cookie_info.expires_at:
                expires_at = datetime.fromisoformat(cookie_info.expires_at)
                if datetime.now() > expires_at:
                    print(f"[WARNING] Cookie已过期: {domain}")
                    print(f"          过期时间: {cookie_info.expires_at}")
                    # 删除过期Cookie
                    self.delete_cookie(domain)
                    return None
            
            if not cookie_info.is_valid:
                print(f"[WARNING] Cookie标记为无效: {domain}")
                return None
            
            print(f"[SUCCESS] 从文件获取到{domain}的Cookie")
            print(f"          存储文件: {cookie_file}")
            print(f"          创建时间: {cookie_info.created_at}")
            if cookie_info.expires_at:
                print(f"          过期时间: {cookie_info.expires_at}")
            
            return cookie_info.cookie_string
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] 解析Cookie JSON失败: {e}")
            # 删除损坏的Cookie
            self.delete_cookie(domain)
            return None
        except Exception as e:
            print(f"[ERROR] 获取Cookie失败: {e}")
            return None
    
    def delete_cookie(self, domain: str) -> bool:
        """从本地文件删除Cookie
        
        Args:
            domain: 域名
            
        Returns:
            是否成功删除
        """
        try:
            cookie_file = self._get_cookie_file_path(domain)
            
            if cookie_file.exists():
                cookie_file.unlink()
                print(f"[SUCCESS] 已删除{domain}的Cookie文件")
                return True
            else:
                print(f"[INFO] {domain}的Cookie文件不存在")
                return False
                
        except Exception as e:
            print(f"[ERROR] 删除Cookie失败: {e}")
            return False
    
    def list_cookies(self) -> list:
        """列出所有保存的Cookie
        
        Returns:
            Cookie信息列表
        """
        cookies = []
        try:
            # 扫描存储目录中的所有加密文件
            for file_path in self.storage_dir.glob('*.enc'):
                # 跳过密钥文件
                if file_path.name.startswith('.'):
                    continue
                
                # 从文件名恢复域名
                domain = file_path.stem.replace('_', '.').replace('_', '-')
                
                # 检查Cookie是否存在
                cookie = self.get_cookie(domain)
                if cookie:
                    cookies.append({
                        'domain': domain,
                        'has_cookie': True,
                        'file': str(file_path)
                    })
            
            return cookies
            
        except Exception as e:
            print(f"[ERROR] 列出Cookie失败: {e}")
            return []
    
    def validate_cookie(self, domain: str, cookie_string: str) -> bool:
        """验证Cookie是否有效
        
        Args:
            domain: 域名
            cookie_string: Cookie字符串
            
        Returns:
            Cookie是否有效
        """
        # 这里可以添加更复杂的验证逻辑
        # 例如：检查Cookie是否包含必要的字段
        
        required_fields = [
            'doc_atoken',
            'x_dingtalk_doc_signature',
            'doc_corp_id'
        ]
        
        cookie_dict = self._parse_cookie_string(cookie_string)
        
        for field in required_fields:
            if field not in cookie_dict:
                print(f"[WARNING] Cookie缺少必要字段: {field}")
                return False
        
        print(f"[SUCCESS] Cookie验证通过: {domain}")
        return True
    
    def _parse_cookie_string(self, cookie_string: str) -> dict:
        """解析Cookie字符串为字典
        
        Args:
            cookie_string: Cookie字符串
            
        Returns:
            Cookie字典
        """
        cookie_dict = {}
        items = cookie_string.split(';')
        
        for item in items:
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookie_dict[key.strip()] = value.strip()
        
        return cookie_dict
    
    def update_cookie_expiry(self, domain: str, expires_hours: int = 720) -> bool:
        """更新Cookie的过期时间
        
        Args:
            domain: 域名
            expires_hours: 新的过期时间（小时）
            
        Returns:
            是否成功更新
        """
        try:
            # 读取加密文件
            cookie_file = self._get_cookie_file_path(domain)
            
            if not cookie_file.exists():
                print(f"[ERROR] 未找到{domain}的Cookie")
                return False
            
            # 读取并解密
            encrypted_data = cookie_file.read_bytes()
            cookie_json = self._decrypt_data(encrypted_data)
            
            # 解析并更新过期时间
            cookie_dict = json.loads(cookie_json)
            
            if expires_hours > 0:
                expires_at = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
                cookie_dict['expires_at'] = expires_at
            else:
                cookie_dict['expires_at'] = None
            
            # 加密并保存更新后的Cookie
            updated_json = json.dumps(cookie_dict)
            updated_encrypted = self._encrypt_data(updated_json)
            cookie_file.write_bytes(updated_encrypted)
            
            print(f"[SUCCESS] 已更新{domain}的Cookie过期时间")
            if expires_hours > 0:
                print(f"          新的过期时间: {cookie_dict['expires_at']}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] 更新Cookie过期时间失败: {e}")
            return False

def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='Cookie管理器')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # save命令
    save_parser = subparsers.add_parser('save', help='保存Cookie')
    save_parser.add_argument('--domain', required=True, help='域名')
    save_parser.add_argument('--cookie', required=True, help='Cookie字符串')
    save_parser.add_argument('--expires', type=int, default=720, help='过期时间（小时）')
    
    # get命令
    get_parser = subparsers.add_parser('get', help='获取Cookie')
    get_parser.add_argument('--domain', required=True, help='域名')
    
    # delete命令
    delete_parser = subparsers.add_parser('delete', help='删除Cookie')
    delete_parser.add_argument('--domain', required=True, help='域名')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出所有Cookie')
    
    # validate命令
    validate_parser = subparsers.add_parser('validate', help='验证Cookie')
    validate_parser.add_argument('--domain', required=True, help='域名')
    validate_parser.add_argument('--cookie', required=True, help='Cookie字符串')
    
    # update-expiry命令
    update_parser = subparsers.add_parser('update-expiry', help='更新过期时间')
    update_parser.add_argument('--domain', required=True, help='域名')
    update_parser.add_argument('--expires', type=int, default=720, help='过期时间（小时）')
    
    args = parser.parse_args()
    
    manager = CookieManager()
    
    if args.command == 'save':
        manager.save_cookie(args.domain, args.cookie, args.expires)
    
    elif args.command == 'get':
        cookie = manager.get_cookie(args.domain)
        if cookie:
            print(f"\nCookie for {args.domain}:")
            print(cookie)
        else:
            print(f"\n未找到{args.domain}的Cookie")
    
    elif args.command == 'delete':
        success = manager.delete_cookie(args.domain)
        if success:
            print(f"\n已删除{args.domain}的Cookie")
        else:
            print(f"\n删除{args.domain}的Cookie失败")
    
    elif args.command == 'list':
        cookies = manager.list_cookies()
        print("\n保存的Cookie列表:")
        for cookie_info in cookies:
            status = "✓ 已保存" if cookie_info['has_cookie'] else "✗ 未保存"
            print(f"  {cookie_info['domain']}: {status}")
    
    elif args.command == 'validate':
        is_valid = manager.validate_cookie(args.domain, args.cookie)
        if is_valid:
            print(f"\n{args.domain}的Cookie验证通过")
        else:
            print(f"\n{args.domain}的Cookie验证失败")
    
    elif args.command == 'update-expiry':
        success = manager.update_cookie_expiry(args.domain, args.expires)
        if success:
            print(f"\n已更新{args.domain}的Cookie过期时间")
        else:
            print(f"\n更新{args.domain}的Cookie过期时间失败")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
