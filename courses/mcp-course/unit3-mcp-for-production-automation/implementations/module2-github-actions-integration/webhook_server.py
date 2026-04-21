from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
EVENTS_FILE = BASE_DIR / "github_events.json"
WEBHOOK_PATH = "/webhook/github"

app = FastAPI(title="GitHub Webhook Capture Server")


def _load_events() -> list[dict[str, Any]]:
    if not EVENTS_FILE.exists():
        return []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_events(events: list[dict[str, Any]]) -> None:
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "message": "GitHub webhook server is running"}


@app.post(WEBHOOK_PATH)
async def github_webhook(request: Request) -> dict[str, Any]:
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event", "unknown")

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "action": payload.get("action"),
        "workflow_run": payload.get("workflow_run"),
        "check_run": payload.get("check_run"),
        "repository": (payload.get("repository") or {}).get("full_name"),
        "sender": (payload.get("sender") or {}).get("login"),
    }

    events = _load_events()
    events.append(entry)
    _save_events(events)

    return {
        "ok": True,
        "stored_events": len(events),
        "event_type": event_type,
        "repository": entry["repository"],
    }


if __name__ == "__main__":
    print("🚀 Starting webhook server on http://localhost:8080")
    print(f"🗂️ Events will be saved to: {EVENTS_FILE}")
    print(f"🔗 Webhook URL: http://localhost:8080{WEBHOOK_PATH}")
    print("======== Running on http://localhost:8080 ========")
    print("(Press CTRL+C to quit)")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")
