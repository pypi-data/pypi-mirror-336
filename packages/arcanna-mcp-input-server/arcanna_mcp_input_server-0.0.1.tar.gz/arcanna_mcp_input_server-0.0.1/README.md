# Arcanna MCP Input Server

The Arcanna MCP Inpyt server allows user to send data and feedback to  AI use cases through the Model Context Protocol (MCP).

## Usage with Claude Desktop or other MCP Clients

### Option 1 - uvx
#### Prerequisites
- uv - https://docs.astral.sh/uv/getting-started/installation/#installation-methods

#### Configuration
Add the following entry to the `mcpServers` section in your MCP client config file (`claude_desktop_config.json` for Claude
Desktop).

```json
{
  "mcpServers": {
    "arcanna-mcp-input-server": {
      "command": "uvx",
      "args": [
        "arcanna-mcp-input-server"
      ],
      "env": {
        "ARCANNA_INPUT_API_KEY": "YOUR_ARCANNA_INPUT_API_KEY",
        "ARCANNA_HOST": "YOUR_ARCANNA_HOST",
        "ARCANNA_USER": "YOUR_USERNAME"
      }
    }
  }
}
```

### Option 2 - Building local image from this repository
#### Prerequisites
- Docker - https://docs.docker.com/engine/install/

#### Configuration
1. Change directory to the directory where the Dockerfile is.
2. Run ```docker build -t arcanna/arcanna-mcp-input-server. --progress=plain --no-cache```
3. Add the configuration bellow to your claude desktop config.
```json
{
  "mcpServers": {
    "arcanna-mcp-input-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "ARCANNA_INPUT_API_KEY",
        "-e",
        "ARCANNA_HOST",
        "-e",
        "ARCANNA_USER",
        "mcp/arcanna-mcp-input-server"
      ],
      "env": {
        "ARCANNA_INPUT_API_KEY": "<YOUR_ARCANNA_API_KEY_HERE>",
        "ARCANNA_HOST": "<YOUR_ARCANNA_HOST_HERE>",
        "ARCANNA_USER": "<YOUR_USERNAME_HERE>"
      }
    }
  }
}
```

