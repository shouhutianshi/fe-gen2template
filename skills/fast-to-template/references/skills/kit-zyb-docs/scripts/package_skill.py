#!/usr/bin/env python3
"""
技能打包脚本
将技能打包成zip文件，便于分发
"""

import os
import sys
import json
import zipfile
import shutil
import tempfile
import argparse
import yaml
from pathlib import Path
from datetime import datetime

def read_yaml_frontmatter(file_path):
    """读取YAML frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                return yaml.safe_load(frontmatter)
        
        return None
    except Exception as e:
        print(f"读取YAML frontmatter失败: {e}")
        return None

def validate_skill(skill_dir):
    """验证技能结构"""
    print("验证技能结构...")
    
    skill_dir = Path(skill_dir)
    
    # 检查必需的文件
    required_files = [
        ('SKILL.md', True, "主技能文档"),
        ('README.md', False, "说明文档"),
    ]
    
    required_dirs = [
        ('scripts/', False, "脚本目录"),
        ('references/', False, "参考文献目录"),
        ('assets/', False, "资源目录"),
    ]
    
    errors = []
    warnings = []
    
    # 检查文件
    for file_name, required, description in required_files:
        file_path = skill_dir / file_name
        if not file_path.exists():
            if required:
                errors.append(f"缺少必需文件: {file_name} ({description})")
            else:
                warnings.append(f"缺少可选文件: {file_name} ({description})")
        elif not file_path.is_file():
            errors.append(f"{file_name} 不是文件")
    
    # 检查目录
    for dir_name, required, description in required_dirs:
        dir_path = skill_dir / dir_name
        if not dir_path.exists():
            if required:
                errors.append(f"缺少必需目录: {dir_name} ({description})")
            else:
                warnings.append(f"缺少可选目录: {dir_name} ({description})")
        elif not dir_path.is_dir():
            errors.append(f"{dir_name} 不是目录")
    
    # 检查SKILL.md的YAML frontmatter
    skill_md_path = skill_dir / 'SKILL.md'
    if skill_md_path.exists():
        frontmatter = read_yaml_frontmatter(skill_md_path)
        if not frontmatter:
            errors.append("SKILL.md缺少YAML frontmatter")
        else:
            # 检查必需字段
            if 'name' not in frontmatter:
                errors.append("SKILL.md frontmatter缺少'name'字段")
            if 'description' not in frontmatter:
                errors.append("SKILL.md frontmatter缺少'description'字段")
            
            # 检查字段内容
            if 'name' in frontmatter and not frontmatter['name']:
                errors.append("'name'字段不能为空")
            if 'description' in frontmatter and not frontmatter['description']:
                errors.append("'description'字段不能为空")
    
    # 输出结果
    if warnings:
        print("\n警告:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    
    if errors:
        print("\n错误:")
        for error in errors:
            print(f"  ❌ {error}")
        print(f"\n验证失败，发现 {len(errors)} 个错误")
        return False
    
    print(f"✓ 技能结构验证通过")
    if warnings:
        print(f"  发现 {len(warnings)} 个警告（不影响打包）")
    return True

def create_zip_file(skill_dir, output_path):
    """创建zip文件"""
    print(f"\n创建zip文件: {output_path}")
    
    skill_dir = Path(skill_dir)
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加所有文件和目录
            for root, dirs, files in os.walk(skill_dir):
                # 跳过隐藏文件
                files = [f for f in files if not f.startswith('.')]
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(skill_dir)
                    zipf.write(file_path, arcname)
                    print(f"  ✓ 添加: {arcname}")
        
        # 检查zip文件大小
        zip_size = os.path.getsize(output_path)
        print(f"✓ Zip文件创建成功")
        print(f"  文件大小: {zip_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建zip文件失败: {e}")
        return False

def create_manifest(skill_dir, output_dir):
    """创建清单文件"""
    print("\n创建清单文件...")
    
    skill_dir = Path(skill_dir)
    manifest_path = output_dir / 'manifest.json'
    
    try:
        # 读取SKILL.md信息
        skill_md_path = skill_dir / 'SKILL.md'
        frontmatter = read_yaml_frontmatter(skill_md_path)
        
        # 统计文件
        file_count = 0
        dir_count = 0
        
        for root, dirs, files in os.walk(skill_dir):
            # 跳过隐藏文件
            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            file_count += len(files)
            dir_count += len(dirs)
        
        # 创建清单
        manifest = {
            'skill_name': frontmatter.get('name', 'unknown') if frontmatter else 'unknown',
            'description': frontmatter.get('description', '') if frontmatter else '',
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'file_count': file_count,
            'directory_count': dir_count,
            'files': []
        }
        
        # 添加文件列表
        for root, dirs, files in os.walk(skill_dir):
            # 跳过隐藏文件
            files = [f for f in files if not f.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(skill_dir)
                
                manifest['files'].append({
                    'path': str(rel_path),
                    'size': os.path.getsize(file_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
        
        # 写入清单文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 清单文件已创建: {manifest_path}")
        return True
        
    except Exception as e:
        print(f"❌ 创建清单文件失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='技能打包工具')
    parser.add_argument('skill_dir', help='技能目录路径')
    parser.add_argument('-o', '--output', help='输出目录（默认: 当前目录）')
    parser.add_argument('--no-validate', action='store_true', help='跳过验证')
    parser.add_argument('--no-manifest', action='store_true', help='不创建清单文件')
    
    args = parser.parse_args()
    
    # 解析路径
    skill_dir = Path(args.skill_dir).absolute()
    if not skill_dir.exists():
        print(f"❌ 技能目录不存在: {skill_dir}")
        return 1
    
    if not skill_dir.is_dir():
        print(f"❌ 不是目录: {skill_dir}")
        return 1
    
    # 设置输出目录
    if args.output:
        output_dir = Path(args.output).absolute()
    else:
        output_dir = Path.cwd()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("技能打包工具")
    print("=" * 60)
    print(f"技能目录: {skill_dir}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 验证技能
    if not args.no_validate:
        if not validate_skill(skill_dir):
            return 1
    else:
        print("⚠️  跳过验证")
    
    # 获取技能名称
    skill_md_path = skill_dir / 'SKILL.md'
    frontmatter = read_yaml_frontmatter(skill_md_path)
    skill_name = frontmatter.get('name', 'unknown') if frontmatter else 'unknown'
    
    # 清理技能名称
    safe_name = skill_name.lower().replace(' ', '-').replace('_', '-')
    zip_filename = f"{safe_name}.zip"
    zip_path = output_dir / zip_filename
    
    # 创建zip文件
    if not create_zip_file(skill_dir, zip_path):
        return 1
    
    # 创建清单文件
    if not args.no_manifest:
        create_manifest(skill_dir, output_dir)
    
    print("\n" + "=" * 60)
    print("打包完成!")
    print("=" * 60)
    print(f"技能名称: {skill_name}")
    print(f"Zip文件: {zip_path}")
    print(f"文件大小: {os.path.getsize(zip_path) / 1024:.1f} KB")
    
    # 显示使用说明
    print("\n使用说明:")
    print(f"1. 分发: {zip_filename}")
    print(f"2. 安装: 解压到 .codebuddy/skills/ 目录")
    print(f"3. 使用: Claude会自动检测并加载技能")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
