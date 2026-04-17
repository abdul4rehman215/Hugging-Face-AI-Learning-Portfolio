# ☁️ EC2 Practice Setup Summary

This file condenses the basic setup flow used during the Unit 2 practice.

---

# 1. Server EC2 — Gradio MCP Server

```bash
mkdir -p ~/huggingface-mcp/unit2/mcp-sentiment
cd ~/huggingface-mcp/unit2/mcp-sentiment

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install "gradio[mcp]" textblob
```

Add the `app.py` from:
- `implementations/gradio-mcp-server/app.py`

Run:

```bash
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"
python app.py
```

Useful checks:

```bash
curl http://127.0.0.1:7860/gradio_api/mcp/schema
```

---

# 2. Client EC2 — Basic Config Test

```bash
mkdir -p ~/huggingface-mcp/unit2/client
cd ~/huggingface-mcp/unit2/client

sudo apt update
sudo apt install -y curl jq git python3 python3-venv python3-pip unzip
```

Create the config files using the templates in:
- `implementations/client-configs/`

Connectivity tests:

```bash
curl http://YOUR_SERVER_PRIVATE_IP:7860/gradio_api/mcp/schema
timeout 5 curl -iN http://YOUR_SERVER_PRIVATE_IP:7860/gradio_api/mcp/sse
```

---

# 3. Continue CLI Path

Install local model tooling and Continue CLI on the client machine, then use:
- `implementations/continue-cli-client/config.yaml`

---

# 4. Gradio MCP Client Path

Use:
- `implementations/gradio-mcp-client/app.py`
- `implementations/gradio-mcp-client/requirements.txt`

---

# 5. Tiny Agents Path

Use:
- `implementations/tiny-agents-client/agent.json`
- `implementations/tiny-agents-client/package-notes.md`

---

# Important Public Repo Note

This summary intentionally uses:
- placeholders
- environment-driven config
- no real IPs
- no tokens or secrets

That keeps it safe to publish while preserving the practical workflow.
