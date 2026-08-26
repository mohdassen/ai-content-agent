from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Scene:
    start: int
    end: int
    narration: str
    visual_prompt: str
    on_screen_text: str


def saudi_ai_datacenter_story() -> dict:
    hook = "خلال خمس سنوات تقريباً، قفزت قدرة مراكز البيانات في السعودية من 68 إلى 467 ميغاواط. لكن القصة ليست تخزين بيانات فقط."
    scenes: List[Scene] = [
        Scene(0, 5, hook, "Cinematic aerial of Riyadh at night, digital infrastructure lines, vertical 9:16", "68 → 467 MW"),
        Scene(5, 13, "مراكز البيانات التقليدية كانت تخزن وتعالج المعلومات. الآن، مع الذكاء الاصطناعي، تتحول إلى بنية تولّد الذكاء على نطاق واسع.", "Modern hyperscale data center, GPU racks, realistic documentary style, no logos", "من Data Center إلى AI Factory"),
        Scene(13, 22, "وبحسب بيانات منشورة في 2026، تجاوزت استثمارات قطاع مراكز البيانات في المملكة 16 مليار ريال منذ 2016.", "Saudi technology investment visualization, data center construction, realistic, no fake documents", "+16 مليار ريال"),
        Scene(22, 32, "والسعودية مرشحة لاستقطاب الحصة الأكبر من استثمارات مراكز بيانات الذكاء الاصطناعي في الشرق الأوسط.", "Middle East map with Saudi Arabia highlighted, compute network visualization, clean editorial graphic", "سباق البنية التحتية للـ AI"),
        Scene(32, 43, "السبب؟ الطلب على الحوسبة يتسارع، والذكاء الاصطناعي يحتاج طاقة، رقائق، شبكات ومراكز بيانات ضخمة قبل أن يحتاج تطبيقاً على هاتفك.", "GPU compute closeups, power infrastructure, fiber networks, fast documentary montage", "AI يبدأ من البنية التحتية"),
        Scene(43, 50, "السؤال الآن: هل تصبح السعودية مركز الحوسبة والذكاء الاصطناعي الأهم في المنطقة؟", "Futuristic but realistic Riyadh skyline, subtle AI infrastructure, premium documentary ending", "هل تصبح السعودية AI Hub؟"),
    ]
    return {
        "title": "لماذا تتحول مراكز البيانات السعودية إلى مصانع ذكاء اصطناعي؟",
        "hook": hook,
        "scenes": [asdict(s) for s in scenes],
        "caption": "الذكاء الاصطناعي لا يبدأ من التطبيق… بل من البنية التحتية التي تشغله. 🇸🇦 ما رأيك: هل تصبح السعودية مركز الـAI الأهم في المنطقة؟",
        "hashtags": ["السعودية", "الذكاء_الاصطناعي", "مراكز_البيانات", "تقنية", "رؤية_2030"],
        "ai_disclosure": True,
        "source_topic": "data/seeds/saudi_ai_datacenters_2026.json"
    }
