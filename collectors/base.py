from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass
class CollectionResult:
    source: str
    records: list[dict[str, Any]]
    status: str
    message: str
    collected_at: str = datetime.now(timezone.utc).isoformat()
