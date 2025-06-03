#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft MCP Server 打包脚本
使用 PyInstaller 将 Python 应用打包为独立的 EXE 文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查 PyInstaller 是否已安装"""
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                                encoding='utf-8', errors='ignore')
            print("✓ PyInstaller 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 安装失败")
            return False

def build_mcp_server():
    """打包 MCP 服务器"""
    print("\n🔨 开始打包 MCP 服务器...")
    
    # PyInstaller 命令参数
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--console",                   # 保留控制台窗口（MCP服务器需要stdio通信）
        "--name", "minecraft_mcp_server",  # 输出文件名
        "--icon", "icon.ico",          # 图标文件（如果存在）
        "--add-data", "resources;resources",  # 添加资源文件夹
        "--add-data", "tools;tools",          # 添加工具文件夹
        "--add-data", "config.py;.",          # 添加配置文件
        "--hidden-import", "mcrcon",          # 隐式导入
        "--hidden-import", "requests",        # 隐式导入
        "--hidden-import", "json",            # 隐式导入
        "--hidden-import", "asyncio",         # 隐式导入asyncio
        "--hidden-import", "mcp.server.stdio", # 隐式导入MCP stdio
        "--clean",                            # 清理临时文件
        "main.py"                             # 主程序文件
    ]
    
    # 如果图标文件不存在，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon")
        cmd.remove("icon.ico")
        print("⚠️  未找到 icon.ico 文件，将使用默认图标")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("✓ MCP 服务器打包成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ MCP 服务器打包失败: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def build_web_config():
    """打包 Web 配置界面"""
    print("\n🔨 开始打包 Web 配置界面...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "minecraft_web_config",
        "--icon", "icon.ico",
        "--add-data", "templates;templates",
        "--add-data", "static;static",
        "--add-data", "web_config.py;.",
        "--hidden-import", "flask",
        "--hidden-import", "mcrcon",
        "--clean",
        "start_web_config.py"
    ]
    
    # 如果图标文件不存在，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon")
        cmd.remove("icon.ico")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("✓ Web 配置界面打包成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Web 配置界面打包失败: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def create_release_package():
    """创建发布包"""
    print("\n📦 创建发布包...")
    
    # 创建发布目录
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制可执行文件
    dist_dir = Path("dist")
    if dist_dir.exists():
        for exe_file in dist_dir.glob("*.exe"):
            shutil.copy2(exe_file, release_dir)
            print(f"✓ 复制 {exe_file.name}")
    
    # 复制配置文件和说明
    files_to_copy = [
        "README.md",
        "requirements.txt"
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, release_dir)
            print(f"✓ 复制 {file_name}")
    
    # 创建使用说明
    usage_text = """Minecraft MCP Server 使用说明
================================

文件说明：
- minecraft_mcp_server.exe: MCP 服务器主程序
- minecraft_web_config.exe: Web 配置界面

使用方法：
1. 双击运行 minecraft_web_config.exe 打开配置界面
2. 在浏览器中访问 http://localhost:5000 进行配置
3. 配置完成后，在 Trae IDE 的 mcp.json 中添加服务器配置

配置示例：
{
  "mcpServers": {
    "minecraft-server": {
      "command": "path/to/minecraft_mcp_server.exe",
      "args": [],
      "env": {
        "MC_HOST": "localhost",
        "MC_RCON_PORT": "25575",
        "MC_RCON_PASSWORD": "your_password"
      }
    }
  }
}

注意事项：
- 确保 Minecraft 服务器已启用 RCON
- 配置正确的服务器地址和端口
- 密码必须与服务器 RCON 密码一致
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(usage_text)
    
    print(f"✓ 发布包创建完成: {release_dir.absolute()}")

def cleanup():
    """清理临时文件"""
    print("\n🧹 清理临时文件...")
    
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["*.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 删除 {dir_name}")
    
    import glob
    for pattern in files_to_remove:
        for file_path in glob.glob(pattern):
            os.remove(file_path)
            print(f"✓ 删除 {file_path}")

def main():
    """主函数"""
    print("🚀 Minecraft MCP Server 打包工具")
    print("=" * 40)
    
    # 检查 PyInstaller
    if not check_pyinstaller():
        return False
    
    # 检查必要文件
    required_files = ["main.py", "start_web_config.py"]
    for file_name in required_files:
        if not os.path.exists(file_name):
            print(f"❌ 缺少必要文件: {file_name}")
            return False
    
    success = True
    
    # 打包 MCP 服务器
    if not build_mcp_server():
        success = False
    
    # 打包 Web 配置界面
    if not build_web_config():
        success = False
    
    if success:
        # 创建发布包
        create_release_package()
        
        # 清理临时文件
        cleanup()
        
        print("\n🎉 打包完成！")
        print("📁 发布文件位于 release 目录")
    else:
        print("\n❌ 打包过程中出现错误")
    
    return success

if __name__ == "__main__":
    main()