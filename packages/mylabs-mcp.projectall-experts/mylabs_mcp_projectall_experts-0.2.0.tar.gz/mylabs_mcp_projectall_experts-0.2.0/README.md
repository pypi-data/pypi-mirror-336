# projectall-experts

All Model Context Protocol (MCP) servers

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python using `uv python install 3.13`

## Installation

Install the MCP server:
```bash
uv tool install mylabs-mcp.projectall-experts --force 
```

Add the server to your MCP client config (e.g. `~/.cursor-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "mylabs_mcp.projectfour_expert": {
      "command": "uvx",
      "args": [
        "--from",
        "mylabs-mcp-projectall-experts",
        "projectfour-expert"
      ],
      "env": {
        "SHELL": "/usr/bin/zsh"
      },
      "disabled": false,
      "autoApprove": []
    },    
    "mylabs_mcp.projectsix_expert": {
      "command": "uvx",
      "args": [
        "--from",
        "mylabs-mcp-projectall-experts",
        "projectsix-expert"
      ],
      "env": {
        "SHELL": "/usr/bin/zsh"
      },
      "disabled": false,
      "autoApprove": []
    },
    "mylabs_mcp.projectten_expert": {
      "command": "uvx",
      "args": [
        "--from",
        "mylabs-mcp-projectall-experts",
        "projectten-expert"
      ],
      "env": {
        "SHELL": "/usr/bin/zsh"
      },
      "disabled": false,
      "autoApprove": []
    }

  }
}
```

## Development

1. Set up the development environment:
```bash
uv sync --all-groups
```

2. Install pre-commit hooks:
```bash
GIT_CONFIG=/dev/null pre-commit install
```
