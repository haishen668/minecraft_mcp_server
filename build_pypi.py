#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft MCP Server PyPI包构建脚本
用于构建和发布PyPI包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查构建依赖是否已安装"""
    dependencies = ["setuptools", "wheel", "twine", "build"]
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        print(f"⚠️ 缺少以下依赖: {', '.join(missing)}")
        print("🔧 正在安装缺失的依赖...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing,
                encoding='utf-8', errors='ignore'
            )
            print("✅ 依赖安装成功")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败")
            return False
    
    return True

def clean_build_files():
    """清理旧的构建文件"""
    print("🧹 清理旧的构建文件...")
    
    # 确保只清理PyPI相关的构建文件，不清理PyInstaller生成的.exe文件
    dirs_to_remove = ["build", "dist/*.whl", "dist/*.tar.gz", "*.egg-info"]
    
    for dir_pattern in dirs_to_remove:
        if "*" in dir_pattern:
            import glob
            for path in glob.glob(dir_pattern):
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"✅ 已删除 {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✅ 已删除 {path}")
        elif os.path.exists(dir_pattern):
            shutil.rmtree(dir_pattern)
            print(f"✅ 已删除 {dir_pattern}")

def build_package():
    """构建PyPI包"""
    print("🔨 构建PyPI包...")
    
    try:
        # 直接使用setup.py构建包，避免与本地build.py冲突
        # 构建wheel包
        subprocess.check_call(
            [sys.executable, "setup.py", "bdist_wheel"],
            encoding='utf-8', errors='ignore'
        )
        # 构建源码包
        subprocess.check_call(
            [sys.executable, "setup.py", "sdist"],
            encoding='utf-8', errors='ignore'
        )
        print("✅ 包构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 包构建失败: {e}")
        return False

def upload_to_pypi(test=True):
    """上传包到PyPI"""
    if test:
        print("🚀 上传包到TestPyPI...")
        repo_url = "--repository-url https://test.pypi.org/legacy/"
    else:
        print("🚀 上传包到PyPI...")
        repo_url = ""
    
    # 确保只上传PyPI包文件（.whl和.tar.gz），不上传.exe文件
    try:
        # 检查是否有PyPI包文件
        import glob
        pypi_files = glob.glob("dist/*.whl") + glob.glob("dist/*.tar.gz")
        if not pypi_files:
            print("❌ 没有找到PyPI包文件（.whl或.tar.gz）")
            return False
            
        cmd = f"{sys.executable} -m twine upload {repo_url} dist/*.whl dist/*.tar.gz"
        subprocess.check_call(cmd, shell=True)
        print("✅ 包上传成功")
        
        if test:
            print("\n📦 安装命令:")
            print("pip install --index-url https://test.pypi.org/simple/ minecraft-mcp-server")
        else:
            print("\n📦 安装命令:")
            print("pip install minecraft-mcp-server")
            print("\n🚀 使用uvx运行:")
            print("uvx minecraft-mcp-server")
            print("uvx minecraft-web-config")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 包上传失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Minecraft MCP Server PyPI包构建工具")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    # 清理旧的构建文件
    clean_build_files()
    
    # 构建包
    if not build_package():
        return False
    
    # 询问是否上传
    upload = input("\n是否上传到PyPI? (y/n/test): ").strip().lower()
    
    if upload == "y":
        upload_to_pypi(test=False)
    elif upload == "test":
        upload_to_pypi(test=True)
    else:
        print("\n✅ 构建完成，包位于 dist/ 目录")
    
    return True

if __name__ == "__main__":
    main()