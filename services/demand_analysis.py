from __future__ import annotations
import yaml
from pathlib import Path
WORDS = yaml.safe_load((Path(__file__).parents[1] / "config/keywords.yaml").read_text(encoding="utf-8"))
def classify(text: str) -> list[str]:
    text = (text or "").lower()
    return [kind for kind, terms in WORDS.items() if any(term in text for term in terms)]
