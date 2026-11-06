"""Collect public source data into auditable CSV snapshots. Safe to run without keys."""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
sys.path.insert(0, str(Path(__file__).parents[1]))
from services.discovery import run_discovery
from services.normalization import canonical_name

ROOT = Path(__file__).parents[1]; DATA = ROOT / "data"
def main():
    DATA.mkdir(exist_ok=True)
    results = run_discovery(); now = datetime.now(timezone.utc).isoformat()
    games, logs, evidence = [], [], []
    for result in results:
        logs.append({"collected_at": result.collected_at, "source": result.source, "status": result.status, "message": result.message, "records": len(result.records)})
        for r in result.records:
            r["game_id"] = r.get("package_name") or f"steam:{r.get('steam_appid')}"
            r["canonical_name"] = canonical_name(r.get("name", "")); r["collected_at"] = now
            games.append(r)
            evidence.append({"evidence_id": f"{r['game_id']}:{result.source}", "game_id": r["game_id"], "source": result.source, "url": r.get("google_play_url") or r.get("steam_url"), "claim": "discovery/public metadata", "collected_at": now, "confidence": "medium"})
    if games:
        df = pd.DataFrame(games).drop_duplicates("game_id", keep="last")
        df.to_csv(DATA / "games.csv", index=False)
    pd.DataFrame(logs).to_csv(DATA / "collection_log.csv", index=False)
    pd.DataFrame(evidence).to_csv(DATA / "evidence.csv", index=False)
    print(pd.DataFrame(logs).to_string(index=False))
if __name__ == "__main__": main()
