#!/usr/bin/env python3
"""
测试下载功能
"""

import sys
import requests

def test_download():
    """测试下载功能"""
    # 使用您提供的curl中的URL
    download_url = "https://zyb-saas-info-document-alidocs.oss-cn-beijing.aliyuncs.com/export/tempres/markdown/aKdnl1JJEWe1x5bZ/3559333955628/D0Bdoo4WNHozdqKj?Expires=1774358324&OSSAccessKeyId=LTAI5t8KEoEQ2vTqsvMNnXDw&Signature=lkfeBOQR9UQghZaTh3raX1GxZiM%3D&response-content-disposition=attachment%3Bfilename%3D%25E5%259C%25A8%25E6%2595%25B0%25E6%258D%25AE%25E5%25BA%2593%25E4%25B8%25AD%25E9%2585%258D%25E7%25BD%25AE%25E8%2599%259A%25E6%258B%259F%25E8%25B4%25A6%25E5%258F%25B7.markdown"
    
    print("测试下载URL:")
    print(download_url)
    print("\n" + "="*80)
    
    # 方法1：最简单的方式
    print("方法1: 直接使用requests.get")
    try:
        response = requests.get(download_url, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)} 字符")
        print(f"内容类型: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("✅ 下载成功！")
            # 显示前200个字符
            preview = response.text[:200]
            print(f"内容预览: {preview}...")
            
            # 保存到文件
            filename = "test_download.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"✅ 内容已保存到: {filename}")
            return True
        else:
            print(f"❌ 下载失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 方法1异常: {e}")
    
    print("\n" + "="*80)
    
    # 方法2：模拟curl的默认行为
    print("方法2: 模拟curl默认行为")
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'curl/7.81.0',
            'Accept': '*/*',
        })
        
        response = session.get(download_url, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)} 字符")
        
        if response.status_code == 200:
            print("✅ 使用curl模拟下载成功！")
            return True
        else:
            print(f"❌ 下载失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 方法2异常: {e}")
    
    print("\n" + "="*80)
    
    # 方法3：使用urllib（更底层）
    print("方法3: 使用urllib")
    try:
        import urllib.request
        import urllib.error
        
        req = urllib.request.Request(download_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            print(f"状态码: {response.getcode()}")
            print(f"内容长度: {len(content)} 字符")
            
            if response.getcode() == 200:
                print("✅ 使用urllib下载成功！")
                
                # 保存到文件
                filename = "test_urllib.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 内容已保存到: {filename}")
                return True
                
    except Exception as e:
        print(f"❌ 方法3异常: {e}")
    
    return False

def main():
    """主函数"""
    print("开始测试下载功能...")
    print("="*80)
    
    success = test_download()
    
    if success:
        print("\n" + "="*80)
        print("✅ 所有下载测试完成！")
        return 0
    else:
        print("\n" + "="*80)
        print("❌ 下载测试失败")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 检查URL是否有有效期限制")
        print("3. 尝试使用curl命令验证URL有效性")
        return 1

if __name__ == '__main__':
    sys.exit(main())
