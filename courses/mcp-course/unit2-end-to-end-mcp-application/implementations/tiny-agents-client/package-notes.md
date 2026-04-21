# Tiny Agents Package Notes

During the original hands-on flow:

- `npx` was already available through modern Node/npm
- `mcp-remote` was used to bridge the remote MCP server into a stdio-compatible flow
- Tiny Agents then loaded the tool and executed it successfully

## Install pattern
```bash
npm install mcp-remote
npm install @huggingface/tiny-agents
```

## Run
```bash
npx @huggingface/tiny-agents run ./agent.json
```

## Important
Before publishing publicly, replace private endpoint values with placeholders.  
That is why this repository version does **not** contain the original EC2 IPs.
