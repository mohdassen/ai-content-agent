from pathlib import Path

from src.telegram_gate import TelegramApprovalGate


def test_gate_defaults_to_local_and_blocks_publishing(tmp_path):
    video = tmp_path / "demo.mp4"
    video.write_bytes(b"not-a-real-video")
    story = {
        "title": "Demo",
        "caption": "Demo caption",
        "hashtags": ["demo"],
        "ai_disclosure": True,
    }

    gate = TelegramApprovalGate(token="", chat_id="")
    result = gate.request_approval(story, video, output_dir=str(tmp_path))

    assert result["delivery"] == "local_only"
    assert result["approved"] is False
    assert result["publishing_allowed"] is False
    assert (tmp_path / "approval_request.json").exists()
