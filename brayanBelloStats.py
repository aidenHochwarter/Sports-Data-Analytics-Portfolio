import pandas as pd

# --- FILES ---
file_2024 = r"C:\Users\aiden\Downloads\Bello2024.csv"
file_2025 = r"C:\Users\aiden\Downloads\Bello2025.csv"

BELLO_ID = 678394

# Load CSVs
df24 = pd.read_csv(file_2024)
df25 = pd.read_csv(file_2025)

# --- Filter ONLY Bello if player_id exists ---
if "player_id" in df24.columns:
    df24 = df24[df24["player_id"] == BELLO_ID]
if "player_id" in df25.columns:
    df25 = df25[df25["player_id"] == BELLO_ID]

# --- ALL STATS YOU ORIGINALLY LISTED ---
all_stats = [
    "p_formatted_ip", "pa", "strikeout", "walk", "batting_avg", "p_era",
    "p_earned_run", "p_run", "k_percent", "bb_percent", "f_strike_percent",  
    "hit", "home_run", "slg_percent", "on_base_percent", "on_base_plus_slg", 
    "barrel_batted_rate", "poorlyweak_percent", "hard_hit_percent",
    "z_swing_miss_percent", "oz_swing_percent", "whiff_percent",
]

# --- PITCH USAGE (separate) ---
pitch_cols = [
    "n_ff_formatted", "n_sl_formatted", "n_ch_formatted",
    "n_si_formatted", "n_fc_formatted", "n_st_formatted"
]

# Cleaned names for pretty output
clean_names = {
    "p_formatted_ip": "IP",
    "pa": "BF",
    "hit": "Hits",
    "home_run": "HR",
    "strikeout": "SO",
    "walk": "BB",
    "k_percent": "SO%",
    "bb_percent": "BB%",
    "slg_percent": "oSLG",
    "on_base_percent": "OBPa",
    "on_base_plus_slg": "OPSa",
    "p_earned_run": "ER",
    "p_run": "Runs",
    "p_era": "ERA",
    "batting_avg": "oBA",
    "barrel_batted_rate": "Barrel %",
    "poorlyweak_percent": "Poor/Weak %",
    "hard_hit_percent": "Hard Hit %",
    "z_swing_miss_percent": "Z-Whiff %",
    "oz_swing_percent": "Chase %",
    "whiff_percent": "Whiff %",
    "f_strike_percent": "First Strike %",
    "n_ff_formatted": "4-Seam %",
    "n_sl_formatted": "Slider %",
    "n_ch_formatted": "Changeup %",
    "n_si_formatted": "Sinker %",
    "n_fc_formatted": "Cutter %",
    "n_st_formatted": "Sweeper %",
}

# Pull stat values
stats24 = df24.iloc[0][all_stats]
stats25 = df25.iloc[0][all_stats]

pitches24 = df24.iloc[0][pitch_cols]
pitches25 = df25.iloc[0][pitch_cols]

# Build comparison table
combined = pd.DataFrame({
    "Stat": [clean_names[s] for s in all_stats],
    "2024": list(stats24),
    "2025": list(stats25)
}).set_index("Stat")

# --- Highlight rules ---
lower_better = {"ERA", "Runs", "BB", "oBA", "Hard Hit %", "Barrel %", 
                "Hits", "BB%", "oSLG", "OPSa", "ER", "HR", "OBPa"}

highlight_df = pd.DataFrame("", index=combined.index, columns=combined.columns)

for stat in combined.index:
    v24 = combined.loc[stat, "2024"]
    v25 = combined.loc[stat, "2025"]
    if stat in lower_better:
        if v24 < v25:
            highlight_df.loc[stat, "2024"] = "background-color: lightgreen"
        else:
            highlight_df.loc[stat, "2025"] = "background-color: lightgreen"
    else:
        if v24 > v25:
            highlight_df.loc[stat, "2024"] = "background-color: lightgreen"
        else:
            highlight_df.loc[stat, "2025"] = "background-color: lightgreen"

styled = combined.style.apply(lambda _: highlight_df, axis=None)

# -------- PRINT OUTPUT --------
print("\n================ BELLO 2024 vs 2025 =================\n")
print(combined)

print("\n------------ 2024 Pitch Usage -------------")
for col in pitch_cols:
    print(f"{clean_names[col]}: {pitches24[col]}")

print("\n------------ 2025 Pitch Usage -------------")
for col in pitch_cols:
    print(f"{clean_names[col]}: {pitches25[col]}")

styled.to_html("bello_2024_2025_comparison.html")
print("\nSaved table as: bello_2024_2025_comparison.html")
