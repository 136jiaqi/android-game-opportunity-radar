from __future__ import annotations
import math
def coverage_score(evidence_count: int, known_metrics: int) -> tuple[float, str]:
    coverage = min(1.0, known_metrics / 4)
    confidence = "high" if evidence_count >= 3 and coverage >= .75 else "low" if coverage < .5 else "medium"
    return coverage, confidence
def opportunity(heat, demand, commercial, promotion):
    vals = [heat, demand, commercial, promotion]
    if any(v is None for v in vals): return None
    return round(heat*.30 + demand*.35 + commercial*.25 + promotion*.10, 1)
