from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

import requests


class TelegramApprovalGate:
    """Send a review package to Telegram and default to a safe non-publishing state.

    Expected environment variables:
      TELEGRAM_BOT_TOKEN
      TELEGRAM_CHAT_ID

    If either variable is missing, an approval request JSON file is written locally
    and the pipeline continues without publishing.
    """

    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def request_approval(self, story: Dict, video_path: Path, output_dir: str = "data/output") -> Dict:
        payload = {
            "status": "approval_required",
            "title": story.get("title"),
            "caption": story.get("caption"),
            "hashtags": story.get("hashtags", []),
            "ai_disclosure": bool(story.get("ai_disclosure", True)),
            "video": str(video_path),
            "approved": False,
            "publishing_allowed": False,
        }

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        approval_file = out / "approval_request.json"
        approval_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        if not self.configured:
            payload["delivery"] = "local_only"
            return payload

        keyboard = {
            "inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": "approve_latest"},
                {"text": "❌ Reject", "callback_data": "reject_latest"},
            ]]
        }
        text = (
            f"🎬 {story.get('title', 'New Reel')}\n\n"
            f"{story.get('caption', '')}\n\n"
            "Status: approval required\n"
            "Publishing is blocked until approval."
        )

        api = f"https://api.telegram.org/bot{self.token}"
        with video_path.open("rb") as video_file:
            response = requests.post(
                f"{api}/sendVideo",
                data={
                    "chat_id": self.chat_id,
                    "caption": text[:1024],
                    "reply_markup": json.dumps(keyboard),
                    "supports_streaming": "true",
                },
                files={"video": video_file},
                timeout=120,
            )
        response.raise_for_status()
        payload["delivery"] = "telegram"
        payload["telegram_message"] = response.json().get("result", {}).get("message_id")
        approval_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload
