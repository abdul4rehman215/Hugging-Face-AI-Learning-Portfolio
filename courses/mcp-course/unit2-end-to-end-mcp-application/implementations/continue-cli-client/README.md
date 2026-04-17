# Continue CLI Client

This folder contains the Continue CLI configuration used to adapt the course's IDE-focused lesson to a terminal-based EC2 workflow.

## What it demonstrates
- local model configuration through Ollama
- MCP server registration through an SSE endpoint
- a coding-assistant style client that can discover and call MCP tools

## Usage notes
- replace `YOUR_SERVER_PRIVATE_IP` in `config.yaml`
- ensure Ollama is running locally on the client machine
- start Continue CLI with:
```bash
cn --config ./config.yaml
```

## Why this matters
The course page is written around Continue in an IDE environment, but the core idea is the same:
register the MCP server, let the model discover the tool, and observe the tool call flow.
