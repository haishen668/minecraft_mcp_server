# Minecraft MCP 服务器

一个现代化的 Minecraft MCP (Model Context Protocol) 服务器管理工具，提供美观的Web界面用于配置环境变量，并支持与Trae IDE集成。

## 安装

### 使用pip安装

```bash
pip install minecraft-mcp-server
```

### 使用uvx直接运行（推荐）

```bash
uvx minecraft-mcp-server
```

或者启动Web配置界面：

```bash
uvx minecraft-web-config
```

## 功能特性

- 🎨 **现代美观的Web界面** - 响应式设计，支持移动端
- ⚙️ **环境变量配置** - 可视化配置Minecraft服务器连接参数
- 🔧 **实时连接测试** - 一键测试服务器连接状态
- 💾 **自动保存配置** - 配置自动保存到环境变量
- 🚀 **Trae IDE 集成** - 自动同步配置到 Trae 的 MCP 服务器配置
- 🛡️ **输入验证** - 完整的表单验证和错误提示
- 📱 **响应式设计** - 完美适配各种设备屏幕
- 🔌 **RCON通信** - 通过RCON协议与Minecraft服务器通信

## 使用方法

### 配置服务器

1. 启动Web配置界面：
   ```bash
   uvx minecraft-web-config
   ```

2. 在浏览器中访问 `http://localhost:5000` 进行配置

3. 填写Minecraft服务器连接信息并保存

### 运行MCP服务器

```bash
uvx minecraft-mcp-server
```

## Trae IDE 集成

本工具已集成 Trae IDE 支持，配置会自动同步到 Trae 的 MCP 服务器配置文件。

### 配置示例

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

## 许可证

本项目采用MIT许可证。