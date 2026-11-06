"""Public Steam Store adapter. Steam signals are explicitly not Android metrics."""
from __future__ import annotations
import requests
from .base import CollectionResult

BASE = "https://store.steampowered.com/api"

def discover(limit: int = 20, timeout: int = 20) -> CollectionResult:
    """Discover upcoming Steam games. They are candidate PC→Android opportunities only."""
    try:
        response = requests.get(f"{BASE}/featuredcategories", timeout=timeout,
                                headers={"User-Agent": "AndroidGameOpportunityRadar/1.0"})
        response.raise_for_status()
        items = response.json().get("coming_soon", {}).get("items", [])[:limit]
        records = [{"steam_appid": str(x.get("id")), "name": x.get("name"),
                    "steam_url": f"https://store.steampowered.com/app/{x.get('id')}/",
                    "release_date": x.get("release_date", ""), "platform": "Steam",
                    "android_status": "unknown", "source": "Steam featured coming soon"} for x in items]
        return CollectionResult("steam", records, "ok", f"Discovered {len(records)} public coming-soon records")
    except Exception as exc:
        return CollectionResult("steam", [], "error", f"{type(exc).__name__}: {exc}")

def app_details(appid: str, timeout: int = 20) -> CollectionResult:
    try:
        response = requests.get(f"{BASE}/appdetails?appids={appid}", timeout=timeout,
                                headers={"User-Agent": "AndroidGameOpportunityRadar/1.0"})
        response.raise_for_status(); payload = response.json().get(str(appid), {})
        if not payload.get("success"): return CollectionResult("steam", [], "error", "Steam returned no app details")
        d = payload["data"]
        record = {"steam_appid": str(appid), "name": d.get("name"), "developer": ", ".join(d.get("developers", [])),
                  "genres": ", ".join(x.get("description", "") for x in d.get("genres", [])),
                  "steam_url": f"https://store.steampowered.com/app/{appid}/", "release_date": d.get("release_date", {}).get("date", ""),
                  "is_free": d.get("is_free"), "header_image": d.get("header_image", ""), "platform": "Steam",
                  "android_status": "unknown", "source": "Steam Store API"}
        return CollectionResult("steam", [record], "ok", "Public app details retrieved")
    except Exception as exc: return CollectionResult("steam", [], "error", f"{type(exc).__name__}: {exc}")
