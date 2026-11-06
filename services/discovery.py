from __future__ import annotations
from collectors.steam import discover
from collectors.google_play import discover_top_games, probe
def run_discovery():
    return [discover_top_games(), discover(), probe()]
