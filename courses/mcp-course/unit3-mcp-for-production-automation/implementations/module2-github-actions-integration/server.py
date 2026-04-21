#!/usr/bin/env python3
"""
Module 2: GitHub Actions Integration
Extends the PR Agent with webhook handling and MCP Prompts for CI/CD workflows.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional, Any

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent-actions")

BASE_DIR = Path(__file__).resolve().parent

# PR template directory (shared between starter and solution)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

# File where webhook_server.py stores events
EVENTS_FILE = Path(__file__).parent / "github_events.json"

# Default PR templates
DEFAULT_TEMPLATES = {
    "bug.md": "Bug Fix",
    "feature.md": "Feature",
    "docs.md": "Documentation",
    "refactor.md": "Refactor",
    "test.md": "Test",
    "performance.md": "Performance",
    "security.md": "Security",
}

# Type mapping for PR templates
TYPE_MAPPING = {
    "bug": "bug.md",
    "fix": "bug.md",
    "feature": "feature.md",
    "enhancement": "feature.md",
    "docs": "docs.md",
    "documentation": "docs.md",
    "refactor": "refactor.md",
    "cleanup": "refactor.md",
    "test": "test.md",
    "testing": "test.md",
    "performance": "performance.md",
    "optimization": "performance.md",
    "security": "security.md",
}


def _to_json(data: Any) -> str:
    return json.dumps(data, indent=2)


async def _get_working_dir() -> str:
    """
    Use Claude roots when available; otherwise fall back to current directory.
    """
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


def _load_templates() -> list[dict[str, str]]:
    templates: list[dict[str, str]] = []

    for filename, template_type in DEFAULT_TEMPLATES.items():
        path = TEMPLATES_DIR / filename
        if path.exists():
            content = path.read_text(encoding="utf-8")
        else:
            content = f"# {template_type}\n\nTemplate file not found."
        templates.append(
            {
                "filename": filename,
                "type": template_type,
                "content": content,
            }
        )

    return templates


def _read_events() -> list[dict]:
    if not EVENTS_FILE.exists():
        return []

    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


# ===== Module 1 Tools =====

@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500,
) -> str:
    """
    Get the full diff and list of changed files in the current git repository.
    """
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
                diff_content += "\n... Use max_diff_lines parameter to see more ..."
                truncated = True
            else:
                diff_content = diff_result

        commits_result = _run_git(["log", "--oneline", f"{base_branch}..HEAD"], working_dir)

        analysis = {
            "working_dir": working_dir,
            "base_branch": base_branch,
            "files_changed": files_result,
            "statistics": stat_result,
            "commits": commits_result,
            "diff": diff_content if include_diff else "Diff not included (set include_diff=true to see full diff)",
            "truncated": truncated,
            "total_diff_lines": total_diff_lines,
        }
        return _to_json(analysis)

    except Exception as e:
        return _to_json({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """
    List available PR templates with their content.
    """
    return _to_json(_load_templates())


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """
    Suggest the most appropriate PR template for a change.
    """
    templates = _load_templates()

    template_file = TYPE_MAPPING.get(change_type.lower(), "feature.md")
    selected_template = next(
        (t for t in templates if t["filename"] == template_file),
        templates[0],
    )

    suggestion = {
        "recommended_template": selected_template,
        "reasoning": f"Based on the summary '{changes_summary}', this appears to be a {change_type} change.",
        "template_content": selected_template["content"],
        "usage_hint": "Claude can help fill this template based on the code changes and CI status.",
    }
    return _to_json(suggestion)


# ===== Module 2: GitHub Actions Tools =====

@mcp.tool()
async def get_recent_actions_events(limit: int = 10) -> str:
    """
    Get recent GitHub webhook events received by webhook_server.py.
    """
    events = _read_events()

    if not events:
        return _to_json([])

    recent = events[-limit:]
    recent.reverse()  # newest first
    return _to_json(recent)


@mcp.tool()
async def get_workflow_status(workflow_name: Optional[str] = None) -> str:
    """
    Get latest status for GitHub Actions workflows from workflow_run webhook events.
    """
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

    result = {
        "workflow_count": len(latest_by_name),
        "workflows": list(latest_by_name.values()),
    }
    return _to_json(result)


# ===== Module 2: MCP Prompts =====

@mcp.prompt()
async def analyze_ci_results() -> str:
    return (
        "Analyze recent CI/CD results for this project.\n"
        "Steps:\n"
        "1. Use get_recent_actions_events() to inspect the latest webhook events.\n"
        "2. Use get_workflow_status() to summarize the latest workflow states.\n"
        "3. Identify failures, incomplete runs, or suspicious patterns.\n"
        "4. Explain what failed, where it failed, and what the likely next action should be.\n"
        "5. Keep the final response concise and actionable."
    )


@mcp.prompt()
async def create_deployment_summary() -> str:
    return (
        "Create a team-friendly deployment summary based on recent GitHub Actions activity.\n"
        "Steps:\n"
        "1. Use get_recent_actions_events() and get_workflow_status().\n"
        "2. Summarize the most recent workflow outcomes.\n"
        "3. Highlight any failed or cancelled runs.\n"
        "4. Mention repository, workflow, branch, and current deployment confidence.\n"
        "5. Format the final answer like a message you would send to the team."
    )


@mcp.prompt()
async def generate_pr_status_report() -> str:
    return (
        "Generate a full PR status report.\n"
        "Steps:\n"
        "1. Use analyze_file_changes() to inspect code changes.\n"
        "2. Use get_workflow_status() to inspect CI/CD state.\n"
        "3. Use suggest_template() if needed to recommend the right PR template.\n"
        "4. Produce a report with: code summary, risk areas, CI/CD summary, and PR readiness.\n"
        "5. Clearly state whether the PR is ready for review or needs fixes first."
    )


@mcp.prompt()
async def troubleshoot_workflow_failure() -> str:
    return (
        "Troubleshoot a failing GitHub Actions workflow.\n"
        "Steps:\n"
        "1. Use get_recent_actions_events() to find the latest relevant failures.\n"
        "2. Use get_workflow_status() to identify the workflow name, conclusion, and branch.\n"
        "3. Explain the likely failure point and what information is missing.\n"
        "4. Suggest concrete next debugging steps for the developer.\n"
        "5. Keep the response practical and ordered."
    )


if __name__ == "__main__":
    mcp.run()