# Gradio MCP Server

This folder contains the server-side app used for the Unit 2 practice flow.

## What it does
- exposes a sentiment analysis function through a normal Gradio UI
- also exposes the same function as an MCP tool
- returns structured JSON with:
  - polarity
  - subjectivity
  - assessment

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"
python app.py
```

## Notes
- `mcp_server=True` is the key piece that turns the Gradio app into an MCP server
- for public repositories, this file is safe because no private IPs or secrets are hardcoded
