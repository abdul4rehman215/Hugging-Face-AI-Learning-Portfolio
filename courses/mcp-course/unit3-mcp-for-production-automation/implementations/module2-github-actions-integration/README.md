# Module 2 — GitHub Actions Integration

This folder contains the Module 2 workflow server and helper files used to capture GitHub Actions events and summarize them inside Claude Code.

## Included
- `server.py` — the GitHub Actions-aware MCP workflow server
- `webhook_server.py` — local webhook capture service for `/webhook/github`
- `requirements.txt` — minimal dependency hint
- `github_events.sample.json` — sanitized example of stored webhook data
- `sample-github-repo/` — minimal workflow/sample files used to trigger webhook events

## What this module demonstrated
- receiving GitHub webhook payloads locally
- using Cloudflare Tunnel for development-grade webhook exposure
- storing events in `github_events.json`
- exposing MCP prompts for workflow summaries and troubleshooting
