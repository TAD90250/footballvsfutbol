"""
FFL Football vs Futbol (dynasty, Sleeper only) -- the ONE place league-specific settings live.

Every script in this folder imports from here. Nothing in this folder reads
or writes the Camaradas League or FFL Magnificos files -- the guard at the
bottom stops any script cold if a path ever points into either folder.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------ fill these in
LEAGUE_NAME = "FFL Football vs Futbol"

# Sleeper-only league: no Yahoo seasons. Leave this empty.
YAHOO_LEAGUE_KEYS = {}

# Current Sleeper league ID (the URL number on sleeper.com/leagues/<ID>).
# Used by the weekly update.
SLEEPER_SEED_LEAGUE_ID = "1320694452435558400"   # 2026

# Every season's Sleeper league ID. The dynasty was restarted after 2023 with a
# start-from-zero draft, so the 2021-2023 leagues aren't linked to 2024+ on
# Sleeper -- they're listed here so both eras are pulled. When a new season
# rolls over, add its ID here and update SLEEPER_SEED_LEAGUE_ID.
SLEEPER_LEAGUE_IDS = {
    # Original dynasty
    2021: "718334747297771520",
    2022: "784358017742266368",
    2023: "921906680370114560",
    # Restarted dynasty (startup draft in 2024)
    2024: "1049548640748605440",
    2025: "1180584276680388608",
    2026: "1320694452435558400",
}
DYNASTY_RESTART_YEAR = 2024

# Real names / nicknames per OwnerID. OwnerIDs are created on the first pull
# from each Sleeper display name (see owner_map.json). Fill these in afterwards.
#   "OWNERID": ("Full Name", "Nickname"),
OWNER_NAMES = {
    "ROBERTO": ("Roberto", "Rooney"),
    "ALEXAODE": ("Alejandro", "Lopez"),   # Sleeper: alexaodesouza
    "PUENTETU": ("Amir", "Amir"),          # Sleeper: puentetunechi   # Sleeper: JustGiveMeTheMoney / JustGiveMeDaMoney / hueroelchampion
}

# ------------------------------------------------------------ files (this folder only)
OAUTH_PATH = os.path.join(HERE, "oauth2.json")            # this league's own copy
WORKBOOK_PATH = os.path.join(HERE, "FFL_Football_vs_Futbol_Database.xlsx")
OWNER_MAP_PATH = os.path.join(HERE, "owner_map.json")
DEBUG_DIR = os.path.join(HERE, "debug_dumps")
SITE_DIR = os.path.join(HERE, "site")

# ------------------------------------------------------------ isolation guard
_PROTECTED = [
    r"C:\Users\jchap\fantasy_env\ffl_pull",
    r"C:\Users\jchap\Python\Yahoo\Camaradas_League_parquet",
    r"C:\Users\jchap\Python\Yahoo\FFL_Magnificos",
]


def _norm(p):
    return os.path.normcase(os.path.abspath(p)).rstrip("\\/")


def assert_isolated(*paths):
    """Raise if any path is inside the Camaradas or Magnificos folders."""
    for p in paths:
        np_ = _norm(p)
        for prot in _PROTECTED:
            npr = _norm(prot)
            if np_ == npr or np_.startswith(npr + os.sep):
                raise SystemExit(f"STOP: {p} is inside another league's folder ({prot}). "
                                 "Football vs Futbol scripts must run from their own folder.")


def require_league_ids(need_yahoo=False, need_sleeper=True):
    missing = []
    if need_yahoo and not YAHOO_LEAGUE_KEYS:
        missing.append("YAHOO_LEAGUE_KEYS")
    if need_sleeper and not SLEEPER_SEED_LEAGUE_ID:
        missing.append("SLEEPER_SEED_LEAGUE_ID")
    if missing:
        raise SystemExit("Fill in " + " and ".join(missing) + " in league_config.py first "
                         "(the number in sleeper.com/leagues/<ID>).")


assert_isolated(HERE, OAUTH_PATH, WORKBOOK_PATH, OWNER_MAP_PATH, DEBUG_DIR, SITE_DIR)
