from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

import requests


STATE_PATH = Path("data/state/telegram_state.json")
APPROVAL_PATH = Path("data/state/approval.json")


def _load_json(path: Path, default: Dict) -> Dict:
    if not path.exists():
        return dict(default)
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def poll_latest_decision(token: Optional[str] = None, chat_id: Optional[str] = None) -> Dict:
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = str(chat_id or os.getenv("TELEGRAM_CHAT_ID") or "")
    if not token or not chat_id:
        return {"decision": "not_configured", "changed": False}

    state = _load_json(STATE_PATH, {"last_update_id": 0})
    last_update_id = int(state.get("last_update_id", 0))
    api = f"https://api.telegram.org/bot{token}"
    response = requests.get(
        f"{api}/getUpdates",
        params={"offset": last_update_id + 1, "timeout": 5, "allowed_updates": json.dumps(["callback_query"])},
        timeout=15,
    )
    response.raise_for_status()
    updates = response.json().get("result", [])

    decision = "none"
    changed = False
    processed_update = last_update_id

    for update in updates:
        update_id = int(update.get("update_id", 0))
        processed_update = max(processed_update, update_id)
        callback = update.get("callback_query") or {}
        message = callback.get("message") or {}
        callback_chat = str((message.get("chat") or {}).get("id", ""))
        data = callback.get("data")
        if callback_chat != chat_id or data not in {"approve_latest", "reject_latest"}:
            continue

        approved = data == "approve_latest"
        decision = "approved" if approved else "rejected"
        approval = {
            "status": decision,
            "approved": approved,
            "publishing_allowed": approved,
            "telegram_update_id": update_id,
            "telegram_message_id": message.get("message_id"),
        }
        _save_json(APPROVAL_PATH, approval)
        changed = True

        callback_id = callback.get("id")
        if callback_id:
            requests.post(
                f"{api}/answerCallbackQuery",
                data={"callback_query_id": callback_id, "text": "Approved ✅" if approved else "Rejected ❌"},
                timeout=10,
            )

    if processed_update > last_update_id:
        _save_json(STATE_PATH, {"last_update_id": processed_update})

    return {"decision": decision, "changed": changed, "last_update_id": processed_update}
