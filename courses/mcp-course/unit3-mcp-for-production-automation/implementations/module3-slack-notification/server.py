from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pr-agent-notify")

BASE_DIR = Path(__file__).resolve().parent
EVENTS_FILE = BASE_DIR / "github_events.json"


def _to_json(data: Any) -> str:
    return json.dumps(data, indent=2)


async def _get_working_dir() -> str:
    try:
        context = mcp.get_context()
        session = getattr(context, "session", None)

        if session and hasattr(session, "list_roots"):
            roots_result = await session.list_roots()
            roots = getattr(roots_result, "roots", None) or []

            if roots:
                first_root = roots[0]
                uri = getattr(first_root, "uri", None)

                if hasattr(uri, "path") and getattr(uri, "path", None):
                    return uri.path

                if isinstance(uri, str):
                    if uri.startswith("file://"):
                        return uri.replace("file://", "", 1)
                    return uri
    except Exception:
        pass

    return str(Path.cwd())


def _run_git(args: list[str], cwd: str) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )

    stdout = getattr(result, "stdout", "") or ""
    stderr = getattr(result, "stderr", "") or ""
    returncode = getattr(result, "returncode", 0)

    if isinstance(returncode, int) and returncode != 0:
        raise RuntimeError(stderr.strip() or stdout.strip() or f"git {' '.join(args)} failed")

    return stdout.strip()


def _read_events() -> list[dict]:
    if not EVENTS_FILE.exists():
        return []

    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


# ---------- Module 1 tools ----------

@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500,
) -> str:
    try:
        working_dir = await _get_working_dir()

        files_result = _run_git(["diff", "--name-status", f"{base_branch}...HEAD"], working_dir)
        stat_result = _run_git(["diff", "--stat", f"{base_branch}...HEAD"], working_dir)

        diff_content = ""
        truncated = False
        total_diff_lines = 0

        if include_diff:
            diff_result = _run_git(["diff", f"{base_branch}...HEAD"], working_dir)
            diff_lines = diff_result.split("\n")
            total_diff_lines = len(diff_lines)

            if len(diff_lines) > max_diff_lines:
                diff_content = "\n".join(diff_lines[:max_diff_lines])
                diff_content += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
                truncated = True
            else:
                diff_content = diff_result

        commits_result = _run_git(["log", "--oneline", f"{base_branch}..HEAD"], working_dir)

        return _to_json(
            {
                "working_dir": working_dir,
                "base_branch": base_branch,
                "files_changed": files_result,
                "statistics": stat_result,
                "commits": commits_result,
                "diff": diff_content if include_diff else "",
                "truncated": truncated,
                "total_diff_lines": total_diff_lines,
            }
        )
    except Exception as e:
        return _to_json({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    templates = [
        {
            "filename": "bug.md",
            "type": "Bug Fix",
            "content": "# Bug Fix\n\n## Summary\nDescribe the bug fix.\n",
        },
        {
            "filename": "feature.md",
            "type": "Feature",
            "content": "# Feature\n\n## Summary\nDescribe the feature.\n",
        },
        {
            "filename": "docs.md",
            "type": "Documentation",
            "content": "# Documentation\n\n## Summary\nDescribe the docs update.\n",
        },
        {
            "filename": "refactor.md",
            "type": "Refactor",
            "content": "# Refactor\n\n## Summary\nDescribe the refactor.\n",
        },
    ]
    return _to_json(templates)


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    mapping = {
        "bug": "bug.md",
        "fix": "bug.md",
        "feature": "feature.md",
        "enhancement": "feature.md",
        "docs": "docs.md",
        "documentation": "docs.md",
        "refactor": "refactor.md",
        "cleanup": "refactor.md",
    }

    template_file = mapping.get(change_type.lower(), "feature.md")

    return _to_json(
        {
            "recommended_template": template_file,
            "reasoning": f"Based on '{changes_summary}', this looks like a {change_type} change.",
        }
    )


# ---------- Module 2 tools ----------

@mcp.tool()
async def get_recent_actions_events(limit: int = 10) -> str:
    events = _read_events()
    if not events:
        return _to_json([])

    recent = events[-limit:]
    recent.reverse()
    return _to_json(recent)


@mcp.tool()
async def get_workflow_status(workflow_name: Optional[str] = None) -> str:
    events = _read_events()

    workflow_events = []
    for event in events:
        if event.get("event_type") == "workflow_run" and event.get("workflow_run"):
            wr = event["workflow_run"]
            name = wr.get("name")

            if workflow_name and name != workflow_name:
                continue

            workflow_events.append(
                {
                    "name": name,
                    "status": wr.get("status"),
                    "conclusion": wr.get("conclusion"),
                    "event": wr.get("event"),
                    "html_url": wr.get("html_url"),
                    "run_number": wr.get("run_number"),
                    "head_branch": wr.get("head_branch"),
                    "repository": event.get("repository"),
                    "timestamp": event.get("timestamp"),
                }
            )

    workflow_events.sort(key=lambda x: x.get("timestamp") or "", reverse=True)

    latest_by_name: dict[str, dict] = {}
    for item in workflow_events:
        if item["name"] not in latest_by_name:
            latest_by_name[item["name"]] = item

    return _to_json(
        {
            "workflow_count": len(latest_by_name),
            "workflows": list(latest_by_name.values()),
        }
    )


# ---------- Module 3 tool ----------

@mcp.tool()
def send_slack_notification(message: str) -> str:
    """
    Send a formatted notification to the team Slack channel.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return "Error: SLACK_WEBHOOK_URL environment variable not set"

    try:
        payload = {
            "text": message,
            "mrkdwn": True,
        }

        response = requests.post(webhook_url, json=payload, timeout=15)

        if response.status_code == 200:
            return "Slack notification sent successfully"
        return f"Slack API error: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error sending message: {str(e)}"


# ---------- Module 2 prompts ----------

@mcp.prompt()
async def analyze_ci_results() -> str:
    return (
        "Analyze recent CI/CD results for this project.\n"
        "1. Use get_recent_actions_events() to inspect recent events.\n"
        "2. Use get_workflow_status() to summarize workflow states.\n"
        "3. Identify failures or incomplete runs.\n"
        "4. Return a concise, actionable summary."
    )


@mcp.prompt()
async def create_deployment_summary() -> str:
    return (
        "Create a team-friendly deployment summary from recent GitHub Actions activity.\n"
        "Use get_recent_actions_events() and get_workflow_status().\n"
        "Summarize successful/failed runs and mention the important links."
    )


@mcp.prompt()
async def generate_pr_status_report() -> str:
    return (
        "Generate a PR status report.\n"
        "1. Use analyze_file_changes().\n"
        "2. Use get_workflow_status().\n"
        "3. Summarize code changes, risks, CI status, and PR readiness."
    )


@mcp.prompt()
async def troubleshoot_workflow_failure() -> str:
    return (
        "Troubleshoot a failing GitHub Actions workflow.\n"
        "1. Use get_recent_actions_events().\n"
        "2. Use get_workflow_status().\n"
        "3. Explain the likely issue and suggest debugging steps."
    )


# ---------- Module 3 prompts ----------

@mcp.prompt()
def format_ci_failure_alert() -> str:
    return """Format this GitHub Actions failure as a Slack message:

Use this template:
:rotating_light: *CI Failure Alert* :rotating_light:

A CI workflow has failed:
*Workflow*: workflow_name
*Branch*: branch_name
*Status*: Failed
*View Details*: <LOGS_LINK|View Logs>

Please check the logs and address any issues.
Use Slack markdown formatting and keep it concise for quick team scanning."""


@mcp.prompt()
def format_ci_success_summary() -> str:
    return """Format this successful GitHub Actions run as a Slack message:

Use this template:
:white_check_mark: *Deployment Successful* :white_check_mark:

Deployment completed successfully for [Repository Name]
*Changes:*
- Key feature or fix 1
- Key feature or fix 2

*Links:*
<PR_LINK|View Changes>

Keep it celebratory but informative. Use Slack markdown formatting."""


if __name__ == "__main__":
    mcp.run(transport="stdio")