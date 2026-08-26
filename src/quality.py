from dataclasses import dataclass, field
from typing import List


@dataclass
class Evidence:
    url: str
    title: str
    supports: List[str] = field(default_factory=list)


@dataclass
class QualityResult:
    passed: bool
    score: float
    reasons: List[str]


def evaluate(script: str, evidence: List[Evidence], viral_score: float, min_viral_score: float = 7.5) -> QualityResult:
    reasons: List[str] = []
    score = 10.0

    if viral_score < min_viral_score:
        reasons.append(f"Viral score {viral_score} is below {min_viral_score}")
        score -= 3
    if len(evidence) < 2:
        reasons.append("At least two evidence sources are required")
        score -= 4
    if len(script.strip()) < 120:
        reasons.append("Script is too short for a useful short-form story")
        score -= 2
    if not script.strip():
        reasons.append("Script is empty")
        score = 0

    score = max(0.0, round(score, 1))
    return QualityResult(passed=not reasons, score=score, reasons=reasons)
