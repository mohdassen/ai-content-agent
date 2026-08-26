from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Scene:
    start: float
    end: float
    narration: str
    visual_prompt: str
    on_screen_text: str


def saudi_ai_datacenter_story() -> dict:
    # Creative Engine V2: short spoken beats, immediate hook, one idea per scene.
    hook = "السعودية رفعت قدرة مراكز البيانات من 68 إلى 467 ميغاواط. لماذا هذا الرقم مهم؟"
    scenes: List[Scene] = [
        Scene(0, 4, hook, "Saudi Arabia modern data center server racks", "68 → 467 MW"),
        Scene(4, 8, "لأن الذكاء الاصطناعي لا يعيش في التطبيق فقط. خلفه آلاف الخوادم تعمل بلا توقف.", "AI GPU data center servers", "الـAI يحتاج حوسبة"),
        Scene(8, 12, "ومركز البيانات يتحول من مخزن للملفات إلى مصنع حوسبة للذكاء الاصطناعي.", "hyperscale GPU server data center", "AI FACTORY"),
        Scene(12, 16, "وهذا يرفع الطلب على الرقائق والكهرباء والتبريد والألياف الضوئية.", "semiconductor chips power cooling fiber optic", "رقائق • طاقة • تبريد"),
        Scene(16, 20, "ومنذ 2016 تجاوزت استثمارات مراكز البيانات في المملكة 16 مليار ريال.", "Saudi Riyadh technology investment skyline", "+16 مليار ريال"),
        Scene(20, 24, "لذلك السباق القادم ليس على التطبيقات فقط، بل على من يملك قدرة الحوسبة التي تشغلها.", "hyperscale data center infrastructure computing", "من يملك الحوسبة؟"),
        Scene(24, 29, "إذا استمر النمو، قد تصبح السعودية عقدة رئيسية للحوسبة والذكاء الاصطناعي في المنطقة.", "Riyadh futuristic technology skyline realistic", "SAUDI AI HUB?"),
        Scene(29, 34, "فهل تصبح الحوسبة أصلاً استراتيجياً مثل الطاقة؟", "Saudi Arabia digital infrastructure night", "الطاقة + الحوسبة"),
    ]
    return {
        "title": "القصة خلف سباق مراكز البيانات والذكاء الاصطناعي في السعودية",
        "hook": hook,
        "scenes": [asdict(s) for s in scenes],
        "caption": "السباق على الذكاء الاصطناعي لا يبدأ من التطبيق… يبدأ من القدرة على تشغيله. 🇸🇦 هل تصبح الحوسبة أصلاً استراتيجياً مثل الطاقة؟",
        "hashtags": ["السعودية", "الذكاء_الاصطناعي", "مراكز_البيانات", "تقنية", "رؤية_2030"],
        "ai_disclosure": True,
        "source_topic": "data/seeds/saudi_ai_datacenters_2026.json"
    }
