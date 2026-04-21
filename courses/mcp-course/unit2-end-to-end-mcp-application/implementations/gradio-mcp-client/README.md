# Gradio MCP Client

This folder contains the Unit 2 client-side Gradio app.

## What it does
- connects to a remote MCP server through `MCPClient`
- loads the exposed tools
- uses `CodeAgent` + `InferenceClientModel`
- provides a chat-style Gradio UI for interaction

## Environment variables
- `HUGGINGFACE_API_TOKEN` — required
- `MCP_SERVER_SSE_URL` — optional; defaults to a localhost-style example

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export HUGGINGFACE_API_TOKEN="YOUR_TOKEN"
export MCP_SERVER_SSE_URL="http://YOUR_SERVER_PRIVATE_IP:7860/gradio_api/mcp/sse"
python app.py
```

## Notes
This is the public-repo-safe version of the app.  
The endpoint is provided through an environment variable instead of hardcoding a private EC2 address.
