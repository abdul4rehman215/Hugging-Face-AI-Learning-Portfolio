# Module 3 — Slack Notification

This folder contains the final Unit 3 workflow server that added Slack delivery on top of the GitHub Actions integration.

## Included
- `server.py` — Slack-enabled MCP workflow server
- `webhook_server.py` — local webhook capture service reused for event intake
- `requirements.txt` — minimal dependency hint
- `github_events.sample.json` — sanitized event example
- `manual-test-workflow-run-failure.json` — sample payload for local curl testing
- `slack-webhook.env.example` — example env export for Slack webhook setup
- `slack-message-examples.md` — example messages used during verification

## What this module demonstrated
- reading recent workflow failures
- formatting Slack-ready alerts through MCP prompts / Claude reasoning
- sending real Slack notifications through `send_slack_notification`
