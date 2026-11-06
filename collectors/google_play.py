"""Google Play feasibility probe; only public page metadata, no undocumented private API."""
from __future__ import annotations
import re
import requests
from .base import CollectionResult

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
