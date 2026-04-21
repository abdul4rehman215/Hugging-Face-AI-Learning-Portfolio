# Module 1 — Build MCP Server

This folder contains the working `server.py` used for the Unit 3 Module 1 PR Agent setup.

## Included
- `server.py` — the FastMCP workflow server used with Claude Code
- `requirements.txt` — minimal dependency hint for the server
- `templates/` — PR template files used by the agent
- `demo-repo-sample/` — safe local repository structure used for early Claude testing

## What this module demonstrated
- reading git diffs and changed files
- listing available PR templates
- letting Claude suggest the best PR template from raw change context

## Notes
- the real workflow used Claude Code on the MCP client EC2
- the demo repo sample is included only as a safe reconstruction of the test structure
