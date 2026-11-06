from __future__ import annotations
from collectors.steam import discover
from collectors.google_play import probe
def run_discovery():
    return [discover(), probe()]
