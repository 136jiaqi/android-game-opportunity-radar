"""Google Play public-page discovery adapter.

The chart endpoint is public HTML.  Details are subsequently read from public
app pages via google-play-scraper; no private Play API or login is used.
"""
from __future__ import annotations
import re
import requests
from google_play_scraper import app as play_app
from .base import CollectionResult

# The app-collection endpoint is more consistently available than /store/games
# across regions.  Each candidate is filtered using its public ``genre`` field.
CHART_URL = "https://play.google.com/store/apps/collection/topselling_free?hl={lang}&gl={country}"
PACKAGE_PATTERN = re.compile(r"\bcom\.[A-Za-z0-9._]+\b")

def discover_top_games(country: str = "us", lang: str = "en", limit: int = 8,
                       timeout: int = 12) -> CollectionResult:
    """Discover current free-game chart candidates, then normalize public details.

    Google does not expose an official general-purpose chart API.  This adapter
    therefore treats the chart as a discovery signal and stores its URL/time as
    evidence; it does not infer current download volume from the ranking.
    """
    chart_url = CHART_URL.format(country=country.upper(), lang=lang)
    try:
        response = requests.get(chart_url, timeout=timeout,
                                headers={"User-Agent": "Mozilla/5.0 (compatible; AndroidGameOpportunityRadar/1.0)"})
        response.raise_for_status()
        packages = []
        for package in PACKAGE_PATTERN.findall(response.text):
            if package not in packages:
                packages.append(package)
            if len(packages) >= limit:
                break
        if not packages:
            return CollectionResult("google_play_chart", [], "partial", "Chart page loaded but no package IDs could be parsed")
        records, failures = [], 0
        for chart_rank, package in enumerate(packages, start=1):
            try:
                item = play_app(package, lang=lang, country=country)
                # The public global chart contains non-game apps too. Keep only
                # records whose details identify a game category.
                if "game" not in str(item.get("genreId", "")).lower() and "game" not in str(item.get("genre", "")).lower():
                    continue
                records.append({
                    "package_name": package, "name": item.get("title"), "developer": item.get("developer"),
                    "genres": item.get("genre"), "google_play_url": item.get("url"), "header_image": item.get("headerImage"),
                    "rating": item.get("score"), "rating_count": item.get("ratings"), "installs_public_band": item.get("installs"),
                    "updated_timestamp": item.get("updated"), "is_free": item.get("free"), "price": item.get("price"),
                    "platform": "Android", "android_status": "released", "country": country.upper(),
                    "chart_rank": chart_rank, "discovery_method": "Google Play free games chart public HTML",
                    "source": "Google Play public chart + public app page",
                })
            except Exception:
                failures += 1
        status = "ok" if records else "error"
        return CollectionResult("google_play_chart", records, status,
            f"Parsed {len(packages)} chart candidates; enriched {len(records)} public app records; {failures} detail requests failed")
    except Exception as exc:
        return CollectionResult("google_play_chart", [], "error", f"{type(exc).__name__}: {exc}")

def probe(package: str = "com.supercell.clashroyale", timeout: int = 20) -> CollectionResult:
    url = f"https://play.google.com/store/apps/details?id={package}&hl=en&gl=US"
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (compatible; AndroidGameOpportunityRadar/1.0)"})
        response.raise_for_status()
        title = re.search(r'<meta property="og:title" content="([^"]+)', response.text)
        image = re.search(r'<meta property="og:image" content="([^"]+)', response.text)
        if not title: return CollectionResult("google_play", [], "partial", "Page reached but public metadata schema changed")
        return CollectionResult("google_play", [{"package_name": package, "name": title.group(1).replace(" - Apps on Google Play", ""),
          "google_play_url": url, "header_image": image.group(1) if image else "", "platform": "Android", "android_status": "released",
          "source": "Google Play public HTML metadata"}], "partial", "Public metadata retrieved; installs and historical downloads are not supplied by this probe")
    except Exception as exc: return CollectionResult("google_play", [], "error", f"{type(exc).__name__}: {exc}")
