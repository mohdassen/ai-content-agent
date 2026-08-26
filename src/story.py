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
    # Short, punchy sentences on purpose. Final timings are recalculated from the
    # generated audio so narration is never clipped.
    hook = "تخيل أن استهلاك الذكاء الاصطناعي يبدأ هنا... داخل مبانٍ مليئة بآلاف الخوادم."
    scenes: List[Scene] = [
        Scene(0, 4, hook, "data center server racks lights", "الـAI يبدأ هنا"),
        Scene(4, 8, "في السعودية، قدرة مراكز البيانات قفزت من 68 إلى 467 ميغاواط خلال نحو خمس سنوات.", "Riyadh skyline night technology", "68 → 467 MW"),
        Scene(8, 12, "لكن الرقم ليس القصة. التحول الحقيقي هو أن مركز البيانات لم يعد مجرد مكان لتخزين الملفات.", "modern data center corridor servers", "ليس مجرد تخزين"),
        Scene(12, 16, "مع الذكاء الاصطناعي، هذه المراكز تتحول إلى مصانع حوسبة تعمل ليل نهار.", "GPU servers artificial intelligence data center", "AI Factory"),
        Scene(16, 20, "وهذا يعني طلباً هائلاً على الرقائق، الكهرباء، التبريد، والألياف الضوئية.", "computer chips power grid fiber optic", "رقائق + طاقة + شبكات"),
        Scene(20, 24, "ومنذ 2016، تجاوزت استثمارات مراكز البيانات في المملكة 16 مليار ريال بحسب بيانات منشورة في 2026.", "Saudi business investment technology city", "+16 مليار ريال"),
        Scene(24, 28, "والسباق لم يعد على التطبيقات فقط... بل على من يملك البنية التحتية التي تشغل الذكاء نفسه.", "hyperscale data center aerial technology", "من يملك الحوسبة؟"),
        Scene(28, 32, "إذا استمر هذا النمو، قد تصبح السعودية واحدة من أهم عقد الحوسبة والذكاء الاصطناعي في المنطقة.", "Riyadh futuristic skyline realistic", "Saudi AI Hub?"),
        Scene(32, 36, "السؤال: بعد خمس سنوات، هل ستكون قوة الدول في النفط فقط... أم في الحوسبة أيضاً؟", "Saudi Arabia city night digital infrastructure", "النفط أم الحوسبة؟"),
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
