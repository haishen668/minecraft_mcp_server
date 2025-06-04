# Minecraft MCP Server Configuration Tool

[中文版](README.md)

A modern Minecraft MCP (Model Context Protocol) server management tool that provides a beautiful web interface for configuring environment variables and supports integration with Trae IDE.

## 🌟 Features

- 🎨 **Modern Web Interface** - Responsive design, supports mobile devices
- ⚙️ **Environment Variable Configuration** - Visual configuration of Minecraft server connection parameters
- 🔧 **Real-time Connection Testing** - One-click server connection status testing
- 💾 **Automatic Configuration Saving** - Configurations are automatically saved to environment variables
- 🚀 **Trae IDE Integration** - Automatically synchronize configurations to Trae's MCP server configuration
- 🛡️ **Input Validation** - Complete form validation and error prompts
- 📱 **Responsive Design** - Perfect adaptation to various device screens
- 🔌 **RCON Communication** - Communicate with Minecraft servers via RCON protocol

## 📦 Installation Dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Configuration Instructions

The following parameters need to be configured in the web interface:

| Parameter | Environment Variable | Default Value | Description |
|------|----------|--------|------|
| Server Address | `MC_HOST` | `localhost` | Minecraft server IP address or domain name |
| RCON Port | `MC_RCON_PORT` | `25575` | RCON service port number |
| RCON Password | `MC_RCON_PASSWORD` | - | RCON management password (required) |



## 🚀 MCP Client Integration

This tool provides two ways to integrate with MCP clients:

### Method 1: Using Web Configuration Tool (Only supports Trae IDE)

1. Run `minecraft_web_config.exe`
2. Configure server Rcon parameters in the web interface
3. Click "Save Configuration" to automatically synchronize the configuration to Trae
4. You can then directly use the MCP server functionality in Trae IDE

### Method 2: Manually Add MCP Configuration

Add MCP configuration file through MCP clients (Claude, Cursor, Trae, etc.):

- **Configuration Format**:
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

## 🛠️ MCP Server Functionality

This MCP server provides the following tools:

### Minecraft Server Management
- **send_command** - Execute any command in the Minecraft server backend
- **broadcast_message** - Send an announcement to all players

### Plugin Management
- **search_minecraft_plugins** - Search for Minecraft plugins on plugin communities
- **download_file** - Download files from specified URLs to local paths

### Web Content Retrieval
- **fetch_web_content** - Fetch website content from URLs

## 📁 Project Structure

```
minecraft_mcp_server/
├── main.py                 # MCP server main program
├── web_config.py           # Web configuration interface service
├── start_web_config.py     # Web configuration startup script
├── config.py               # Configuration management module
├── build.py                # Packaging build script
├── requirements.txt        # Project dependencies
├── icon.ico                # Application icon
├── static/                 # Static resources
│   ├── script.js           # Frontend JavaScript
│   └── style.css           # Frontend styles
├── templates/              # HTML templates
│   └── config.html         # Configuration page template
└── tools/                  # MCP tool modules
    ├── __init__.py         # Tool registration
    ├── command_execute.py  # Command execution tool
    ├── file_download.py    # File download tool
    ├── plugin_search.py    # Plugin search tool
    └── web_fetch.py        # Web content retrieval tool
```

## 🔨 Building Standalone Application

This project can be packaged into standalone executable files using PyInstaller:

```bash
python build.py
```

The packaged files will be located in the `dist` directory.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contribution

Issue reports and feature requests are welcome!