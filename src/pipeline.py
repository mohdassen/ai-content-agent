from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import json

from src.quality import Evidence, evaluate
from src.scoring import TopicSignals, viral_score


def build_demo_package() -> dict:
    topic = "كيف يمكن لقرار تجاري واحد أن يغيّر مصير شركة؟"
    signals = TopicSignals(
        curiosity=9.0,
        emotion=8.0,
        shareability=8.5,
        freshness=7.5,
        monetization=8.5,
        market_relevance=8.0,
        competition=5.0,
    )
    score = viral_score(signals)

    # Demo evidence placeholders deliberately do not claim real facts.
    evidence = [
        Evidence("demo://source-1", "Replace with primary/authoritative source", ["core claim"]),
        Evidence("demo://source-2", "Replace with independent corroborating source", ["core claim"]),
    ]

    hook = "قرار واحد قد يصنع شركة بمليارات... أو يمحوها من السوق."
    script = (
        "قرار واحد قد يصنع شركة بمليارات... أو يمحوها من السوق. "
        "في حلقات خلف الرقم لن نكتفي بالنتيجة؛ سنرجع إلى القرار نفسه، "
        "نراجع المصادر، ونفهم لماذا اتُّخذ وما الذي حدث بعده. "
        "كل رقم مهم سيظهر فقط عندما نجد له دليلاً موثوقاً. "
        "وفي النهاية سنترك لك السؤال: لو كنت مكان صاحب القرار، هل كنت ستفعل الشيء نفسه؟"
    )

    quality = evaluate(script, evidence, score)
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "brand": "خلف الرقم | Behind The Number",
        "topic": topic,
        "signals": asdict(signals),
        "viral_score": score,
        "hook": hook,
        "script": script,
        "evidence": [asdict(x) for x in evidence],
        "quality": asdict(quality),
        "publishing": {"status": "approval_required", "ai_disclosure": True},
    }


def save_package(package: dict, output_dir: str = "data/output") -> Path:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "latest_content_package.json"
    path.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
