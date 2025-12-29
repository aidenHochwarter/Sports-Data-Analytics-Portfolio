import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashplayerstats

# ========== SETTINGS ==========
TEAM_NAME = "Brooklyn Nets"        # full team name as nba_api uses it

SEASON_24_25 = "2024-25"
SEASON_25_26 = "2025-26"

OUTPUT_FILE = r"C:\Users\aiden\OneDrive\Documents\BKnetsAnalysis.xlsx"
SHEET_25_26 = "Nets_2025_26"
SHEET_24_25 = "Nets_2024_25"

# ========== HELPERS ==========

def get_team_id(team_full_name: str) -> int:
    """Return NBA team ID given full team name, e.g. 'Brooklyn Nets'."""
    all_teams = teams.get_teams()
    for t in all_teams:
        if t["full_name"] == team_full_name:
            return t["id"]
    raise ValueError(f"Team not found: {team_full_name}")


def get_team_player_stats(season: str, team_full_name: str) -> pd.DataFrame:
    """
    Get per-game stats for all players on a team in a given season.
    Uses LeagueDashPlayerStats from nba_api.
    """
    team_id = get_team_id(team_full_name)

    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star="Regular Season",   # only regular season
        per_mode_detailed="PerGame",
        team_id_nullable=team_id
    )

    df = stats.get_data_frames()[0]

    # Keep a subset of useful, ESPN-like columns (no PLUS_MINUS)
    keep_cols = [
        "PLAYER_NAME",
        "GP", "MIN",
        "PTS", "REB", "AST",
        "STL", "BLK", "TOV",
        "FG_PCT", "FG3_PCT", "FT_PCT"
    ]

    df = df[keep_cols].sort_values("MIN", ascending=False).reset_index(drop=True)


    return df


# ========== MAIN ==========

# --- 2024–25 Nets (kept for later use, but not printed or written) ---
nets_24_25 = get_team_player_stats(SEASON_24_25, TEAM_NAME)
   # If you ever want to see it, uncomment:
print(f"\n=== {TEAM_NAME} {SEASON_24_25} Per-Game Stats ===") #TERMINAL PRINT
print(nets_24_25)


# --- 2025–26 Nets (ACTIVE) ---
nets_25_26 = get_team_player_stats(SEASON_25_26, TEAM_NAME)

#print(f"\n=== {TEAM_NAME} {SEASON_25_26} Per-Game Stats ===")
#print(nets_25_26)


# ===== WRITE ONLY 2025–26 TO EXCEL =====
from openpyxl.utils import get_column_letter
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    nets_25_26.to_excel(writer, sheet_name=SHEET_25_26, index=False)

    wb = writer.book
    ws = wb[SHEET_25_26]

    # Make the PLAYER_NAME column (A) wider so names fit nicely
    ws.column_dimensions['A'].width = 28  # adjust if you want wider/narrower

#with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
 #   nets_24_25.to_excel(writer, sheet_name=SHEET_24_25, index=False)

  #  wb = writer.book
   # ws = wb[SHEET_24_25]

    # Make the PLAYER_NAME column (A) wider so names fit nicely
    #ws.column_dimensions['A'].width = 28  # adjust if you want wider/narrower

print(f"\nSaved ONLY Nets {SEASON_25_26} stats to:")
print(OUTPUT_FILE)
