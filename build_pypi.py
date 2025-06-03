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
    
    dirs_to_remove = ["build", "dist", "minecraft_mcp_server.egg-info"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已删除 {dir_name}")

def build_package():
    """构建PyPI包"""
    print("🔨 构建PyPI包...")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "build"],
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
    
    try:
        cmd = f"{sys.executable} -m twine upload {repo_url} dist/*"
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