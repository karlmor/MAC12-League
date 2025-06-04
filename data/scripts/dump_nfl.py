#!/usr/bin/env python3
"""
NFL Fantasy one-shot data dump
------------------------------
• Works for both public *and* private leagues.
• Private league:  export NFL_COOKIE='sid=…; jwt=…; nfl_token=…'
• Requires:  python -m pip install httpx tqdm   (inside your venv)
"""

from __future__ import annotations
import json
import os
import time
import pathlib
import httpx
from tqdm import tqdm

# ────────────  EDIT ONCE EACH SEASON  ────────────
LEAGUE_ID = 9050048       # ← your leagueId
SEASON = 2024          # season you’re dumping
WEEKS = 17            # set 18 if you play Week 18
# ────────────────────────────────────────────────

BASE_URL = "https://api.fantasy.nfl.com/v1"
OUT_DIR = pathlib.Path("data")
OUT_DIR.mkdir(exist_ok=True)

# add Cookie: header only if it exists in the environment
HEADERS = {"cookie": os.environ["NFL_COOKIE"]
           } if "NFL_COOKIE" in os.environ else {}


def grab(endpoint: str, **params) -> dict:
    """GET JSON helper – raises on HTTP errors."""
    resp = httpx.get(
        f"{BASE_URL}/{endpoint}",
        params={**params, "format": "json"},
        headers=HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def dump_json(filename: str, obj: dict):
    path = OUT_DIR / filename
    path.write_text(json.dumps(obj, indent=2))
    print(f" • wrote {path}")


def main():
    print(f"📦 Dumping season {SEASON} for league {LEAGUE_ID} → {OUT_DIR}/")

    # 1) League meta – choose endpoint style based on cookie presence
    if "NFL_COOKIE" in os.environ:
        # PRIVATE league: query-string version *with* season param
        league_meta = grab(
            "league",
            leagueId=LEAGUE_ID,
            season=SEASON,
        )
    else:
        # PUBLIC league: path version (must omit season param)
        league_meta = grab(f"league/{LEAGUE_ID}")

    dump_json(f"{SEASON}_league.json", league_meta)

    # 2) Final standings
    standings = grab(
        "standings",
        leagueId=LEAGUE_ID,
        season=SEASON,
    )
    dump_json(f"{SEASON}_standings.json", standings)

    # 3) Weekly scoreboards
    for wk in tqdm(range(1, WEEKS + 1), desc="Weekly scoreboards"):
        sb = grab(
            "scoreboard",
            leagueId=LEAGUE_ID,
            season=SEASON,
            week=wk,
        )
        dump_json(f"{SEASON}_week{wk:02}.json", sb)
        time.sleep(0.3)   # polite delay

    print("✅  All done!  Commit the files in /data and push to GitHub.")


if __name__ == "__main__":
    main()
