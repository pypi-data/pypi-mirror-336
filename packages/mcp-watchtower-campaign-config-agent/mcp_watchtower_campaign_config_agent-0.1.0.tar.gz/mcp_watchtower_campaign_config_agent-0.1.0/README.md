# mcp-watchtower-campaign-config-agent MCP server

An agent for managing campaign configurations and channel bindings in the MCP ecosystem.

## Components

### Tools

The server implements three tools:

- get-campaign-info: Retrieves detailed campaign information
  - Takes either "campaignId" or "campaignName" as input
  - Returns comprehensive campaign details

- bind-campaign-channel: Binds a campaign to a specified channel
  - Requires "channelName", "campaignId", and "campaignName"
  - Updates campaign-channel binding and confirms success

- list-c-type-campaigns: Lists all C-type campaigns
  - No input required
  - Returns detailed information for each campaign including name, ID, channel, partner, creator, and timestamps

## Configuration

The agent requires the following environment variables:

- MCP_HOST: MCP server host (default: localhost)
- MCP_PORT: MCP server port (default: 8080)
- MCP_API_KEY: Authentication key for MCP server access
- MCP_PUBLIC_KEY: Public key for secure communication

Create a `.env` file in the project root with these variables:

```env
MCP_HOST=localhost
MCP_PORT=8080
MCP_API_KEY=your_api_key
MCP_PUBLIC_KEY=your_public_key
```

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-watchtower-campaign-config-agent": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/user/Documents/projects/mcp-server/mcp-watchtower-campaign-config-agent",
        "run",
        "mcp-watchtower-campaign-config-agent"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-watchtower-campaign-config-agent": {
      "command": "uvx",
      "args": [
        "mcp-watchtower-campaign-config-agent"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/user/Documents/projects/mcp-server/mcp-watchtower-campaign-config-agent run mcp-watchtower-campaign-config-agent
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.