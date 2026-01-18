import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


id_age_year = pd.read_csv("athlete_events.csv")


id_age_year["Age"] = pd.to_numeric(id_age_year["Age"], errors="coerce")
id_age_year["Year"] = pd.to_numeric(id_age_year["Year"], errors="coerce")


id_age_year = id_age_year[id_age_year["Year"] >= 1900].copy()


per_athlete_year = (
    id_age_year.dropna(subset=["ID", "Year"])
               .sort_values(["ID", "Year", "Age"])
               .groupby(["ID", "Year"], as_index=False)["Age"]
               .first()
)


mean_age_by_year = (
    per_athlete_year.groupby("Year", as_index=False)["Age"]
                    .mean()
                    .rename(columns={"Age": "mean_age"})
                    .sort_values("Year")
)


year_min = max(1900, int(mean_age_by_year["Year"].min()))
year_max = int(mean_age_by_year["Year"].max())

all_years = pd.DataFrame({"Year": range(year_min, year_max + 1)})


series = all_years.merge(mean_age_by_year, on="Year", how="left")


series["mean_age_interp"] = series["mean_age"].interpolate(method="linear")

fig, ax = plt.subplots(figsize=(14, 6))

ax.axvspan(1900, 1950, alpha=0.15, color='#6CA6CD', zorder=0)

ax.axvspan(1950, 1980, alpha=0.15, color='#FFB6C1', zorder=0)

ax.axvspan(1980, year_max, alpha=0.15, color='#90EE90', zorder=0)

ax.plot(series["Year"], series["mean_age_interp"], 
        color='#4682B4', linewidth=2, alpha=0.8, zorder=2)

oly = series.dropna(subset=["mean_age"])
ax.scatter(oly["Year"], oly["mean_age"], 
          color='#2F4F4F', s=35, alpha=0.7, zorder=3, edgecolors='black', linewidth=0.5)

ax.axvline(x=1950, color='black', linewidth=2.5, linestyle='-', alpha=0.8, zorder=1)
ax.axvline(x=1980, color='black', linewidth=2.5, linestyle='-', alpha=0.8, zorder=1)

ax.text(1925, 25.5, 'fluctuating', fontsize=14, ha='center', 
        style='italic', color='#2F4F4F', weight='normal')

ax.annotate('decrease', xy=(1965, 24.7), xytext=(1958, 26.8),
            fontsize=13, ha='center', style='italic', color='#2F4F4F',
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F4F4F'))

ax.annotate('increase', xy=(2015, 26.3), xytext=(2008, 27.2),
            fontsize=13, ha='center', style='italic', color='#2F4F4F',
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F4F4F'))

ax.set_title("Mean Athlete Age by Year (>=1900) — Points = Olympic years", 
            fontsize=14, weight='bold', pad=15)
ax.set_xlabel("Year", fontsize=12, weight='bold')
ax.set_ylabel("Mean Age", fontsize=12, weight='bold')

ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.5)

ax.set_ylim(24, 31)
ax.set_xlim(1900, 2020)

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

plt.tight_layout()

plt.savefig("mean_age_trend_graph.png", dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Graph saved: mean_age_trend_graph.png")

plt.show()