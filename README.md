[README.md](https://github.com/user-attachments/files/33854104/README.md)
# FFL Football vs Futbol — League Database & Website

Dynasty league, **Sleeper only**, 2021 onward. History, stats and website data, cloned from the Magnificos setup.

| Era | Seasons |
|---|---|
| Original dynasty | 2021, 2022, 2023 |
| Restarted dynasty (start-from-zero draft) | 2024, 2025, 2026 |

All six league IDs are listed in `SLEEPER_LEAGUE_IDS` in `league_config.py`. The two eras aren't linked
on Sleeper, so the list is what makes both get pulled. Owner records carry across both eras.

Folder: `C:\Users\jchap\Python\Yahoo\FFL_Football_vs_Futbol`

---

## Kept separate from the other leagues

- All settings are in **`league_config.py`** (league name, Sleeper ID, owner names, file paths).
- Every script stops with `STOP:` if a path points into `fantasy_env\ffl_pull`,
  `Camaradas_League_parquet` or `FFL_Magnificos`.
- Own workbook (`FFL_Football_vs_Futbol_Database.xlsx`), `owner_map.json`, player cache, money settings and rules.
- **Always `cd` into this folder before running a script.**
- Publish to its **own GitHub repo** (e.g. `ffl-football-vs-futbol`), never the Camaradas or Magnificos repo.

---

## One-time setup

1. League IDs are already filled in. Run:

```
C:\Users\jchap\fantasy_env\Scripts\activate
cd C:\Users\jchap\Python\Yahoo\FFL_Football_vs_Futbol
pip install -r requirements.txt
python ffl_extract.py discover        # lists every Sleeper season it found
python sleeper_backfill.py            # full pull: teams, scores, playoffs, drafts, lineups, players
python export_site_data.py            # website data
```

2. Open `owner_map.json`. Each Sleeper user got an OwnerID from their display name.
   Rename any you want (e.g. `JESUS`), then add real names and nicknames to `OWNER_NAMES` in `league_config.py`.
   Run `sleeper_backfill.py` and `export_site_data.py` again.
3. The first export creates `league_settings.json` (money, all zeros) and `league_rules.md`. Edit them and export again.

Optional: `python build_owner_sheets.py` adds per-owner Excel tabs.

---

## Weekly routine (during the season)

```
C:\Users\jchap\fantasy_env\Scripts\activate
cd C:\Users\jchap\Python\Yahoo\FFL_Football_vs_Futbol
python sleeper_backfill.py weekly
python export_site_data.py
```

Then on GitHub: **Add file → Upload files**, drag in the `site\data` folder and commit.

**Every Thursday (Power Rankings):** before the new week starts, pull Sleeper's projections for the
weeks still to play, then export:

```
python fetch_projections.py
python export_site_data.py
```

The Power score mixes projected best lineup (65%), recent form (10%: scoring rank in each of the last 3
weeks played, averaged), bench depth (5%), record and standings (15%) and points scored (5%); the Playoffs
table is 90% projected lineup and 10% recent form. Change the weights with `powerWeights` in
`league_settings.json`. Starting slots (2 flex here) come from the league's Sleeper settings; taxi and IR
players are left out.

**New season:** add the new league ID to `SLEEPER_LEAGUE_IDS` and set it as `SLEEPER_SEED_LEAGUE_ID`.

---

## Website

- `site\` holds the website (plain HTML/CSS/JS plus JSON data). Nothing to build.
- Preview locally: `cd site`, `python -m http.server 8000`, open http://localhost:8000.
- GitHub Pages setup: create a new public repo, upload everything *inside* `site`,
  then Settings → Pages → Deploy from branch `main`, folder `/ (root)`.
- **Photos:** `python prepare_photos.py --public "C:\path\to\photos"` (or `--private`). Name files like `2025_draft day.jpg`.
  Needs `pip install pillow cryptography` once.
- **Renamed owners:** delete `site\data\owner` before exporting, and delete the old owner file from the GitHub repo.

---

## Scripts

| Script | What it does |
|---|---|
| `league_config.py` | All league settings and the isolation guard |
| `sleeper_backfill.py` | Pulls every Sleeper season: scores, playoffs, drafts, lineups (incl. taxi), players (`weekly` = current season only) |
| `ffl_extract.py` | `discover` lists the seasons found; the Sleeper helpers live here (Yahoo parts are skipped) |
| `link_players.py` | Cleans up player records |
| `build_owner_sheets.py` | Owner tabs, leaderboard, head-to-head matrix and records in the workbook |
| `fetch_projections.py` | Pulls Sleeper projections and current rosters for the Power Rankings (`power_projections.json`) |
| `export_site_data.py` | Turns the workbook into the website's JSON files in `site\data` |
| `prepare_photos.py` | Shrinks public photos and encrypts private ones |

Every script backs up the workbook before changing it. All of them are safe to re-run.

## Dynasty notes

- Each season's draft is the first draft Sleeper lists for it (the startup draft in year one, rookie drafts after).
  A second draft in the same season is skipped with a message.
- Trades and roster moves aren't tracked yet.
