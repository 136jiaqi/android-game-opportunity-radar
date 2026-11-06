from __future__ import annotations
import re
def canonical_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())
