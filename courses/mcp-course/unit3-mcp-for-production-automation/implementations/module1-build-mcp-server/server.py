from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pr-agent")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


def _to_json(data: Any) -> str:
    return json.dumps(data, indent=2)


async def _get_working_dir() -> str:
    """
    Try to use Claude/host roots when available.
    Fall back to the current working directory, then BASE_DIR.
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

                # Handle common URI object case
                if hasattr(uri, "path") and getattr(uri, "path", None):
                    return uri.path

                # Handle string URI case
                if isinstance(uri, str):
                    if uri.startswith("file://"):
                        return uri.replace("file://", "", 1)
                    return uri

    except Exception:
        pass

    try:
        cwd = os.getcwd()
        if cwd:
            return cwd
    except Exception:
        pass

    return str(BASE_DIR)


def _run_git(args: list[str], cwd: str) -> str:
    """
    Run git safely.
    Important: tests mock subprocess.run with partial MagicMock objects,
    so this helper must be tolerant of missing/odd attributes.
    """
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

    # In mocked pytest cases, returncode may be a MagicMock instead of int.
    if isinstance(returncode, int) and returncode != 0:
        raise RuntimeError(
            stderr.strip()
            or stdout.strip()
            or f"git {' '.join(args)} failed"
        )

    return stdout.strip()


def _load_templates() -> list[dict[str, str]]:
    templates: list[dict[str, str]] = []

    if not TEMPLATES_DIR.exists():
        return templates

    for path in sorted(TEMPLATES_DIR.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            content = ""

        templates.append(
            {
                "name": path.stem,
                "content": content,
                "preview": content[:300],
            }
        )

    return templates


def _detect_patterns(paths: list[str], diff_text: str = "") -> list[str]:
    patterns = set()
    diff_lower = (diff_text or "").lower()

    for raw_path in paths:
        path = (raw_path or "").lower()

        if path.endswith((".md", ".rst", ".txt")) or "docs/" in path or "/docs/" in path:
            patterns.add("docs")

        if "test" in path:
            patterns.add("tests")

        if path.endswith((".yml", ".yaml", ".toml", ".ini", ".json")) or ".github/" in path:
            patterns.add("config")

        if "refactor" in path or "cleanup" in path:
            patterns.add("refactor")

    if any(word in diff_lower for word in ["fix", "bug", "error", "exception", "hotfix"]):
        patterns.add("bug")

    if any(word in diff_lower for word in ["feature", "add", "implement", "new"]):
        patterns.add("feature")

    return sorted(patterns)


@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500,
) -> str:
    """
    Analyze current git changes against a base branch and return structured JSON.
    """
    try:
        working_dir = await _get_working_dir()

        # Keep these calls tolerant because tests mock subprocess.run globally.
        current_branch = _run_git(["branch", "--show-current"], working_dir)
        name_status = _run_git(["diff", "--name-status", f"{base_branch}...HEAD"], working_dir)
        numstat = _run_git(["diff", "--numstat", f"{base_branch}...HEAD"], working_dir)
        stats = _run_git(["diff", "--stat", f"{base_branch}...HEAD"], working_dir)

        files_changed: list[dict[str, str]] = []

        for line in name_status.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                status = parts[0].strip()
                path = parts[-1].strip()
            else:
                # fallback if mocked output is unusual
                status = "M"
                path = line.strip()

            files_changed.append(
                {
                    "status": status,
                    "path": path,
                }
            )

        lines_added = 0
        lines_removed = 0

        for line in numstat.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 3:
                added, removed, _path = parts[0], parts[1], parts[2]

                if added.isdigit():
                    lines_added += int(added)
                if removed.isdigit():
                    lines_removed += int(removed)

        raw_paths = [item["path"] for item in files_changed]

        extensions: dict[str, int] = {}
        for path in raw_paths:
            suffix = Path(path).suffix.lower() or "[no_extension]"
            extensions[suffix] = extensions.get(suffix, 0) + 1

        diff_text = ""
        total_diff_lines = 0
        diff_truncated = False

        if include_diff:
            diff_text = _run_git(["diff", f"{base_branch}...HEAD"], working_dir)
            diff_lines = diff_text.splitlines()
            total_diff_lines = len(diff_lines)

            if len(diff_lines) > max_diff_lines:
                diff_text = "\n".join(diff_lines[:max_diff_lines])
                diff_text += (
                    f"\n\n... Output truncated. Showing {max_diff_lines} "
                    f"of {len(diff_lines)} lines ..."
                )
                diff_truncated = True

        patterns = _detect_patterns(raw_paths, diff_text)

        result = {
            # primary fields
            "working_dir": working_dir,
            "current_branch": current_branch,
            "base_branch": base_branch,
            "files_changed": files_changed,
            "diff": diff_text if include_diff else "",
            # extra compatible aliases / summary fields
            "files": raw_paths,
            "changes": files_changed,
            "file_count": len(files_changed),
            "extensions": extensions,
            "patterns": patterns,
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "stats": stats,
            "total_diff_lines": total_diff_lines,
            "diff_truncated": diff_truncated,
        }

        return _to_json(result)

    except Exception as e:
        return _to_json({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """
    Return available PR templates as a JSON list.
    """
    try:
        templates = _load_templates()

        if not templates:
            return _to_json({"error": f"No templates found in {TEMPLATES_DIR}"})

        return _to_json(templates)

    except Exception as e:
        return _to_json({"error": str(e)})


@mcp.tool()
async def suggest_template(change_summary: str, template_hint: str = "") -> str:
    """
    Suggest the best PR template based on a change summary and optional hint.
    """
    try:
        summary = (change_summary or "").lower()
        hint = (template_hint or "").lower()

        suggested = "feature"
        confidence = "medium"
        reasoning: list[str] = []

        if "bug" in hint or any(word in summary for word in ["bug", "fix", "fixed", "error", "issue", "auth"]):
            suggested = "bug"
            confidence = "high" if "bug" in hint else "medium"
            reasoning.append("Detected bug-fix style language.")
        elif "docs" in hint or any(word in summary for word in ["docs", "documentation", "readme"]):
            suggested = "docs"
            confidence = "high" if "docs" in hint else "medium"
            reasoning.append("Detected documentation-related change.")
        elif "refactor" in hint or any(word in summary for word in ["refactor", "cleanup", "rename", "restructure"]):
            suggested = "refactor"
            confidence = "high" if "refactor" in hint else "medium"
            reasoning.append("Detected refactor/cleanup style change.")
        else:
            suggested = "feature"
            confidence = "medium"
            reasoning.append("Defaulted to feature for general code changes.")

        result = {
            "suggested_template": suggested,
            "template": suggested,
            "confidence": confidence,
            "reasoning": reasoning,
            "input_summary": change_summary,
            "template_hint": template_hint,
        }

        return _to_json(result)

    except Exception as e:
        return _to_json({"error": str(e)})


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()