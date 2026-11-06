"""Generate rankings only where metrics support an explicit score; never invents values."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).parents[1]; DATA = ROOT / "data"
def main():
    games_path = DATA / "games.csv"
    if not games_path.exists(): raise SystemExit("Run scripts/collect.py first")
    games = pd.read_csv(games_path).fillna("")
    rows=[]
    for _, g in games.iterrows():
        stage = "S3-S5" if g.get("android_status") == "released" else "S1"
        rows.append({"game_id":g.game_id,"name":g.name,"lifecycle":stage,"heat_score":"", "demand_score":"", "commercial_score":"", "promotion_score":"", "opportunity_score":"", "confidence":"low", "rating_status":"数据不足，暂不可评级", "reason":"当前仅有发现/基础元数据；缺少近30天下载、增长、真实需求与商业化证据。"})
    pd.DataFrame(rows).to_csv(DATA / "rankings.csv", index=False)
    print(f"Wrote {len(rows)} transparent unranked records")
if __name__ == "__main__": main()
