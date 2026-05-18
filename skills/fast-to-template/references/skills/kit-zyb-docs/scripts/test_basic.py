#!/usr/bin/env python3
"""
基本功能测试脚本
用于验证技能的基本功能
"""

import sys
import os
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import requests
        print("✓ requests 导入成功")
    except ImportError:
        print("✗ requests 导入失败")
        return False
    
    try:
        import cryptography
        print("✓ cryptography 导入成功")
    except ImportError:
        print("✗ cryptography 导入失败")
        print("  请运行: pip install cryptography")
        return False
    
    try:
        # 测试本地模块导入
        sys.path.append(str(Path(__file__).parent))
        import cookie_manager
        print("✓ cookie_manager 导入成功")
        
        import fetch_bangbang_doc
        print("✓ fetch_bangbang_doc 导入成功")
    except ImportError as e:
        print(f"✗ 本地模块导入失败: {e}")
        return False
    
    return True

def test_file_structure():
    """测试文件结构"""
    print("\n测试文件结构...")
    
    skill_dir = Path(__file__).parent.parent
    
    required_files = [
        ('SKILL.md', True),
        ('README.md', True),
        ('scripts/fetch_bangbang_doc.py', True),
        ('scripts/cookie_manager.py', True),
        ('scripts/requirements.txt', True),
        ('references/api_documentation.md', True),
        ('references/workflow_diagram.md', True),
        ('assets/', False),  # 目录
    ]
    
    all_ok = True
    for file_path, is_file in required_files:
        full_path = skill_dir / file_path
        exists = full_path.exists()
        
        if is_file:
            is_ok = exists and full_path.is_file()
        else:
            is_ok = exists and full_path.is_dir()
        
        status = "✓" if is_ok else "✗"
        print(f"{status} {file_path}")
        
        if not is_ok:
            all_ok = False
    
    return all_ok

def test_skill_md():
    """测试SKILL.md文件内容"""
    print("\n测试SKILL.md文件...")
    
    skill_dir = Path(__file__).parent.parent
    skill_md_path = skill_dir / 'SKILL.md'
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查YAML frontmatter
        if 'name: bangbang-doc-fetcher' in content:
            print("✓ 技能名称正确")
        else:
            print("✗ 技能名称不正确")
            return False
        
        if 'description:' in content:
            print("✓ 描述信息存在")
        else:
            print("✗ 描述信息缺失")
            return False
        
        # 检查关键内容
        required_sections = [
            '使用时机',
            '核心功能',
            '工作流程',
            '接口说明',
            '脚本使用'
        ]
        
        for section in required_sections:
            if section in content:
                print(f"✓ 包含'{section}'部分")
            else:
                print(f"✗ 缺少'{section}'部分")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ 读取SKILL.md失败: {e}")
        return False

def test_scripts():
    """测试脚本文件"""
    print("\n测试脚本文件...")
    
    scripts_dir = Path(__file__).parent
    
    # 测试fetch_bangbang_doc.py
    try:
        with open(scripts_dir / 'fetch_bangbang_doc.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_classes = ['BangbangDocFetcher']
        required_methods = ['fetch_document', 'create_export_task', 'check_export_progress']
        
        for class_name in required_classes:
            if f'class {class_name}' in content:
                print(f"✓ 包含类: {class_name}")
            else:
                print(f"✗ 缺少类: {class_name}")
                return False
        
        # 检查命令行参数解析
        if 'argparse.ArgumentParser' in content:
            print("✓ 包含命令行参数解析")
        else:
            print("✗ 缺少命令行参数解析")
            return False
        
    except Exception as e:
        print(f"✗ 读取fetch_bangbang_doc.py失败: {e}")
        return False
    
    # 测试cookie_manager.py
    try:
        with open(scripts_dir / 'cookie_manager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class CookieManager' in content:
            print("✓ 包含CookieManager类")
        else:
            print("✗ 缺少CookieManager类")
            return False
        
        required_methods = ['save_cookie', 'get_cookie', 'delete_cookie']
        for method in required_methods:
            if f'def {method}' in content:
                print(f"✓ 包含方法: {method}")
            else:
                print(f"✗ 缺少方法: {method}")
                return False
        
    except Exception as e:
        print(f"✗ 读取cookie_manager.py失败: {e}")
        return False
    
    return True

def test_references():
    """测试参考文献"""
    print("\n测试参考文献...")
    
    ref_dir = Path(__file__).parent.parent / 'references'
    
    try:
        # 测试api_documentation.md
        api_doc_path = ref_dir / 'api_documentation.md'
        with open(api_doc_path, 'r', encoding='utf-8') as f:
            api_content = f.read()
        
        if '创建导出任务接口' in api_content:
            print("✓ api_documentation.md 包含接口文档")
        else:
            print("✗ api_documentation.md 缺少接口文档")
            return False
        
        # 测试workflow_diagram.md
        workflow_path = ref_dir / 'workflow_diagram.md'
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_content = f.read()
        
        if 'graph TD' in workflow_content or '流程图' in workflow_content:
            print("✓ workflow_diagram.md 包含流程图")
        else:
            print("✗ workflow_diagram.md 缺少流程图")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 读取参考文献失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("帮帮文档获取技能测试")
    print("=" * 60)
    
    tests = [
        ("模块导入测试", test_imports),
        ("文件结构测试", test_file_structure),
        ("SKILL.md测试", test_skill_md),
        ("脚本文件测试", test_scripts),
        ("参考文献测试", test_references),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "通过" if success else "失败"
        symbol = "✓" if success else "✗"
        print(f"{symbol} {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！技能结构完整。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
