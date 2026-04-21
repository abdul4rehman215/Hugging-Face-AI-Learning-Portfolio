# ☁️ EC2 Practice Setup Summary — Unit 3

This file condenses the practical setup flow used during Unit 3.

---

# 1. Machine Roles

## MCP client EC2
This was the main Unit 3 machine.
It hosted:
- Claude Code
- the Unit 3 `server.py` files
- the local webhook server
- Cloudflare Tunnel
- the cloned GitHub test repository
- the Slack webhook environment variable

## MCP server EC2
Not required for the Unit 3 modules.

---

# 2. Module 1 — Build MCP Server

On the MCP client EC2:

```bash
sudo apt update
sudo apt install -y git curl unzip ca-certificates build-essential python3 python3-venv python3-pip
curl -LsSf https://astral.sh/uv/install.sh | sh
exec bash -l
uv --version

curl -fsSL https://claude.ai/install.sh | bash
exec bash -l
claude --version
claude doctor
```

Then use the files in:
- `implementations/module1-build-mcp-server/`

Main validation step:

```bash
uv run pytest test_server.py -v
```

---

# 3. Module 2 — GitHub Actions Integration

On the MCP client EC2, keep three terminals:

## Terminal A — webhook server
```bash
cd implementations/module2-github-actions-integration
python webhook_server.py
```

## Terminal B — Cloudflare tunnel
```bash
cloudflared tunnel --url http://localhost:8080
```

## Terminal C — Claude Code workflow server
```bash
claude mcp add pr-agent-actions -- uv --directory "$PWD/implementations/module2-github-actions-integration" run server.py
```

Use a real GitHub repository for webhook testing.
A local-only Git repository is not enough for GitHub Actions + webhook verification.

---

# 4. Module 3 — Slack Notification

Add the Slack incoming webhook URL on the MCP client EC2:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

Then re-register the Claude MCP server so the correct environment is visible:

```bash
claude mcp remove pr-agent-notify
claude mcp add pr-agent-notify -- uv --directory "$PWD/implementations/module3-slack-notification" run server.py
```

Manual verification before Claude:

```bash
curl -X POST -H 'Content-type: application/json'       --data '{"text":"Hello from MCP Course Module 3!"}'       "$SLACK_WEBHOOK_URL"
```

---

# 5. Practical Summary

Unit 3 was effectively a **single-machine workflow-server lab** running on the MCP client EC2, with external integrations to:
- GitHub
- Cloudflare Tunnel
- Slack
- Claude Code
