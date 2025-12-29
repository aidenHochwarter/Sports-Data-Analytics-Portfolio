import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from nba_api.stats.endpoints import shotchartdetail

# ===== SETTINGS =====
PLAYER_ID = 1627759
GAME_ID = "0022500426"
SEASON = "2025-26"

# How many free throws to display
NUM_FREE_THROWS = 2

# ===== 1. GET SHOT DATA =====
shots = shotchartdetail.ShotChartDetail(
    team_id=0,
    player_id=PLAYER_ID,
    game_id_nullable=GAME_ID,
    season_nullable=SEASON,
    context_measure_simple="FGA"
)

df = shots.get_data_frames()[0]

df["PLOT_X"] = -df["LOC_X"]
df["PLOT_Y"] = df["LOC_Y"].abs()

makes = df[df["SHOT_MADE_FLAG"] == 1]
misses = df[df["SHOT_MADE_FLAG"] == 0]

# ===== FREE THROW DOTS =====
if NUM_FREE_THROWS > 0:
    np.random.seed(1)
    angles = np.linspace(-0.12, 0.12, NUM_FREE_THROWS)
    ft_x = 15 * np.sin(angles)
    ft_y = np.full(NUM_FREE_THROWS, 150) + np.random.normal(0, 2, NUM_FREE_THROWS)
else:
    ft_x = np.array([])
    ft_y = np.array([])


# ===== COURT DRAW =====
def draw_half_court(ax):
    hoop = plt.Circle((0, 0), 7.5, linewidth=1.5, fill=False)
    ax.add_patch(hoop)

    ax.plot([-30, 30], [-7.5, -7.5], linewidth=1.5)
    ax.add_patch(plt.Rectangle((-80, -47.5), 160, 190, linewidth=1.5, fill=False))
    ax.add_patch(plt.Circle((0, 142.5), 60, linewidth=1.5, fill=False))
    ax.add_patch(plt.Circle((0, 0), 40, linewidth=1.5, fill=False))
    ax.add_patch(plt.Circle((0, 0), 237.5, linewidth=1.5, fill=False))

    ax.plot([-220, -220], [-47.5, 92.5], linewidth=1.5)
    ax.plot([220, 220], [-47.5, 92.5], linewidth=1.5)

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    ax.set_aspect(1)
    ax.axis("off")


# ===== PLOT =====
fig, ax = plt.subplots(figsize=(6.5, 11))
draw_half_court(ax)

# Field goals
ax.scatter(misses["PLOT_X"], misses["PLOT_Y"], 
           s=45, edgecolors="black", facecolors="red", label="Miss")

ax.scatter(makes["PLOT_X"], makes["PLOT_Y"], 
           s=45, edgecolors="black", facecolors="lime", label="Make")

# Free throws
if NUM_FREE_THROWS > 0:
    ax.scatter(ft_x, ft_y, 
               s=60, edgecolors="black", facecolors="dodgerblue", label="Free Throws")


# ===== TITLE =====
ax.set_title(
    "Jaylen Brown Shot Chart Vs Indiana — 12/27/25",
    fontsize=14,
    pad=18
)

# ===== LEFT-SIDE STAT BOX =====
stats_text = (
    "2/3 = 67% 3P\n"
    "11/17 = 65% FG\n"
    "13/20 = 65% Total FG\n"
    "2/2 = 100% FT"
)

ax.text(
    -245, 400,          # position (top-left area)
    stats_text,
    fontsize=11,
    verticalalignment="top",
    bbox=dict(
        facecolor="white",
        edgecolor="black",
        boxstyle="round,pad=0.5"
    )
)

# ===== LEGEND (RIGHT SIDE) =====
ax.legend(loc="upper right", fontsize=9)

plt.tight_layout()
plt.show()
