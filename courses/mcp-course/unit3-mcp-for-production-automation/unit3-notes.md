# 📝 Unit 3 Notes — MCP for Production Automation

This file captures the practical ideas, implementation choices, and friction points from my Unit 3 work in the Hugging Face MCP Course.

---

# 1. Why Unit 3 Felt Different From Unit 1 and Unit 2

Unit 1 was about understanding MCP.
Unit 2 was about proving that an MCP server and different clients could talk to each other.
Unit 3 moved into a much more **workflow-oriented** space.

Instead of building a small example tool, the unit focused on a full **developer-automation use case**:

- pull requests
- CI/CD monitoring
- team notification

That made the protocol feel more production-adjacent than the earlier units.

---

# 2. Core Design Idea Of The Unit

The most important design lesson from this unit was:

> do not try to hard-code all workflow intelligence into the MCP server itself.

The server should expose structured capabilities:
- tools that fetch or transform data
- prompts that standardize workflows

Then **Claude Code** becomes the reasoning layer that decides what to do with that data.

That principle showed up clearly in all three modules.

---

# 3. Module 1 — Build MCP Server

## What mattered most
Module 1 was not just “write a server.”
It was really about learning how to expose **useful raw development data** to Claude.

The three tools made that clear:
- `analyze_file_changes`
- `get_pr_templates`
- `suggest_template`

## What I learned from the implementation

### A. Raw Git data is more useful than rigid rules
The server did not try to generate the entire PR writeup itself.
Instead, it returned structured git diff information, changed files, summary stats, and template options.

Claude then used that data to reason about the right template and summary.

### B. Claude roots / working directory really matter
One of the practical details was making sure the MCP tool operated on the **repo Claude was actually opened in**, not just the folder where the server lived.

Using Claude roots through the FastMCP context solved that problem.

### C. Response size matters
Git diffs can get large quickly.
Adding diff truncation was not just a convenience — it made the tool safer and more reliable inside Claude Code.

### D. Small demo repos are useful for validation
The safe local demo repo was a good first testing path before switching to a real GitHub repository.

---

# 4. Module 2 — GitHub Actions Integration

## What changed in this module
Module 2 introduced the first real “outside world” integration in Unit 3.

The server no longer only looked at git diffs. It also needed to react to **live GitHub Actions workflow events**.

## What mattered most

### A. Webhook capture is a bridge between GitHub and MCP
The local webhook server became the bridge between GitHub and Claude Code.

It received webhook payloads and wrote them to `github_events.json`, which the MCP tools later read.

That made the architecture very understandable:
- GitHub sends events
- local webhook server stores them
- Claude uses MCP tools to read and summarize them

### B. Cloudflare Tunnel solved the development exposure problem
Since the webhook server ran locally on EC2, GitHub needed a public HTTPS endpoint.

Cloudflare Tunnel solved that neatly for development/testing.

One practical lesson here was that **quick tunnel URLs change**, so GitHub webhook settings must be updated when the tunnel URL changes.

### C. A local-only Git repo is not enough for real webhook tests
That became very clear during practice.

A local repo worked fine for Module 1 PR analysis, but Module 2 needed a **real GitHub repo** because webhooks and GitHub Actions only fire from GitHub-hosted events.

### D. Prompts are very strong for standardized workflows
Module 2 added prompts such as:
- `analyze_ci_results`
- `create_deployment_summary`
- `generate_pr_status_report`
- `troubleshoot_workflow_failure`

The real value of these prompts was not complexity. It was consistency.
They turned messy event data into reusable team-oriented workflow guidance.

---

# 5. Module 3 — Slack Notification

## Why this module mattered
Module 3 made the workflow feel complete because it added the final outward action:
**team notification**.

Until this point, the system could analyze and summarize.
Module 3 made it communicate.

## Important lessons

### A. The Slack problem was not channel setup — it was environment consistency
During practice, the biggest issue was not Slack itself.
The real issue was making sure the correct `SLACK_WEBHOOK_URL` was actually visible to the MCP server process used by Claude Code.

That reinforced a simple but important operational lesson:
environment variables and process restarts matter as much as the code.

### B. Manual curl verification is invaluable
Sending a direct test message to Slack before relying on Claude helped isolate whether the problem was:
- Slack setup
- the webhook URL
- or the MCP server environment

That made debugging much faster.

### C. End-to-end automation feels different from isolated tool tests
Once the workflow status was summarized, formatted, and then delivered into Slack, the unit stopped feeling like a tutorial and started feeling like a reusable automation pattern.

---

# 6. Why Claude Code Was Central In Unit 3

Claude Code was not just a testing surface here.
It was the actual reasoning environment that made the workflow server useful.

The server provided:
- raw git information
- template lists
- captured GitHub events
- workflow prompts
- Slack delivery capability

Claude turned that into:
- a PR recommendation
- a CI summary
- a failure alert
- a Slack-ready team message

That was the clearest real-world demonstration so far of why MCP matters.

---

# 7. Practical Friction Points That Showed Up

## A. Claude access / authentication
The course expects Claude Code testing, so access method mattered.
In practice, this meant using a valid Claude account or API-backed workflow.

## B. Cloudflare quick tunnel URL changes
A changing tunnel URL can silently break GitHub webhook delivery if the repo settings are not updated.

## C. GitHub repo requirements
A real GitHub repo with a remote and a workflow file was needed to test the webhook flow properly.

## D. Slack webhook environment drift
A direct curl test can succeed while Claude fails if the MCP server was launched with an older or different webhook value.

## E. Prompt discoverability vs prompt usefulness
At one point Claude reported that the formatting prompt was not exposed as a normal listable resource. That did not break the actual workflow outcome, but it was a useful reminder that prompts and resources are distinct MCP concepts.

---

# 8. What I Actually Demonstrated By The End

By the end of Unit 3, I had demonstrated:

- a working FastMCP server for Claude Code
- working PR-analysis tools
- working GitHub Actions event capture through webhook delivery
- working Cloudflare Tunnel-based webhook exposure
- working MCP prompts for CI/CD summarization
- working Slack notification delivery from Claude Code through MCP
- an end-to-end automation flow backed by screenshots and code artifacts

---

# 9. Public Repository Choices Made Here

For GitHub/portfolio safety, this folder intentionally:

- keeps secrets out of code
- stores Slack webhook setup as an example env file only
- uses a sample GitHub workflow file rather than dumping a private repo wholesale
- keeps webhook event examples sanitized
- uses renamed screenshots to make the story readable without publishing raw setup clutter

---

# 10. Best Summary Of This Unit

Unit 3 moved MCP from “tool connectivity” into **team workflow automation** by combining Claude Code, FastMCP tools, GitHub Actions webhooks, Cloudflare Tunnel, and Slack notifications into one practical pull-request assistant workflow.
