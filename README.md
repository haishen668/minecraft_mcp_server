# Minecraft MCP 服务器配置工具

[English Version](README_EN.md)

一个现代化的 Minecraft MCP (Model Context Protocol) 服务器管理工具，提供美观的Web界面用于配置环境变量，并支持与Trae IDE集成。

## 🌟 特性

- 🎨 **现代美观的Web界面** - 响应式设计，支持移动端
- ⚙️ **环境变量配置** - 可视化配置Minecraft服务器连接参数
- 🔧 **实时连接测试** - 一键测试服务器连接状态
- 💾 **自动保存配置** - 配置自动保存到环境变量
- 🚀 **Trae IDE 集成** - 自动同步配置到 Trae 的 MCP 服务器配置
- 🛡️ **输入验证** - 完整的表单验证和错误提示
- 📱 **响应式设计** - 完美适配各种设备屏幕
- 🔌 **RCON通信** - 通过RCON协议与Minecraft服务器通信

## 🎮 配置说明

在Web界面中需要配置以下参数：

| 参数 | 环境变量 | 默认值 | 说明 |
|------|----------|--------|------|
| 服务器地址 | `MC_HOST` | `localhost` | Minecraft服务器IP地址或域名 |
| RCON端口 | `MC_RCON_PORT` | `25575` | RCON服务端口号 |
| RCON密码 | `MC_RCON_PASSWORD` | - | RCON管理密码（必填） |

## 🚀 MCP客户端 集成

本工具提供两种方式与Trae IDE集成：

### 方法1: 使用Web配置工具（仅仅支持Trae IDE）

1. 运行 `minecraft_web_config.exe`
2. 在Web界面中配置服务器Rcon参数
3. 点击"保存配置"，配置会自动同步到Trae
4. 在Trae IDE中即可直接使用MCP服务器功能

### 方法2: 手动添加MCP配置

通过MCP客户但添加MCP配置文件(Claude、Cursor、Trae等)：

- **配置格式**:
  ```json
  {
    "mcpServers": {
      "minecraft": {
        "command": "uvx",
        "args": [
          "minecraft-mcp-server"
        ],
        "env": {
          "MC_HOST": "localhost",
          "MC_RCON_PORT": "25575",
          "MC_RCON_PASSWORD": "your_password"
        }
      }
    }
  }
  ```


## 🛠️ MCP服务器功能

本MCP服务器提供以下工具：

### Minecraft服务器管理
- **send_command** - 在Minecraft服务器后台执行任意命令
- **broadcast_message** - 向所有玩家发送一条公告

### 插件管理
- **search_minecraft_plugins** - 搜索插件社区上的Minecraft插件
- **download_file** - 从指定URL下载文件到本地路径

### 网页内容获取
- **fetch_web_content** - 从URL抓取网站内容

## 📁 项目结构

```
minecraft_mcp_server/
├── main.py                 # MCP服务器主程序
├── web_config.py           # Web配置界面服务
├── start_web_config.py     # Web配置启动脚本
├── config.py               # 配置管理模块
├── build.py                # 打包构建脚本
├── requirements.txt        # 项目依赖
├── icon.ico                # 应用图标
├── static/                 # 静态资源
│   ├── script.js           # 前端JavaScript
│   └── style.css           # 前端样式
├── templates/              # HTML模板
│   └── config.html         # 配置页面模板
└── tools/                  # MCP工具模块
    ├── __init__.py         # 工具注册
    ├── command_execute.py  # 命令执行工具
    ├── file_download.py    # 文件下载工具
    ├── plugin_search.py    # 插件搜索工具
    └── web_fetch.py        # 网页内容获取工具
```

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交问题报告和功能请求！