import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
sns.set_context("talk")

DATA_PATH = Path(__file__).resolve().parent / "data.csv"

# 🔥 lepsze parametry (mniej szumu)
RESAMPLE_FREQ = "12h"
ROLLING_WINDOW = 20

# Load data
df = pd.read_csv(DATA_PATH)

# Time index
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.sort_index(inplace=True)

# 🔥 jednostki (Wh → kWh)
df["Appliances_kWh"] = df["Appliances"] / 1000

# 🔥 mocna redukcja szumu (dane dzienne)
resampled = df.resample("1D").mean()

# 🔥 wygładzenie tygodniowe
smoothed = resampled.rolling(window=7, min_periods=1).mean()

# 🔥 lepsza oś czasu
def format_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# -----------------------
# 1. Energy consumption
# -----------------------
fig, ax = plt.subplots(figsize=(14, 6))

# 🔥 lekka linia danych surowych
ax.plot(resampled.index, resampled["Appliances_kWh"], alpha=0.3, linewidth=1)

# 🔥 główna wygładzona linia
ax.plot(smoothed.index, smoothed["Appliances_kWh"], linewidth=3)

ax.set_title("Zużycie energii [kWh] (po agregacji i wygładzeniu)")
ax.set_xlabel("Data")
ax.set_ylabel("kWh")
ax.grid(alpha=0.3)

format_time_axis(ax)
fig.tight_layout()
fig.savefig("energy.png", dpi=150)
plt.close(fig)

# -----------------------
# 2. Temperature
# -----------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(smoothed.index, smoothed["T1"], color="tab:red", linewidth=3)

ax.set_title("Temperatura T1 [°C] (po wygładzeniu)")
ax.set_xlabel("Data")
ax.set_ylabel("°C")
ax.grid(alpha=0.3)

format_time_axis(ax)
fig.tight_layout()
fig.savefig("temp.png", dpi=150)
plt.close(fig)

# -----------------------
# 3. Histogram
# -----------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(
    resampled["Appliances_kWh"].dropna(),
    bins=25,
    color="tab:blue",
    edgecolor="black",
    alpha=0.8
)

ax.set_title("Histogram zużycia energii [kWh]")
ax.set_xlabel("kWh")
ax.set_ylabel("Liczba pomiarów")
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("hist.png", dpi=150)
plt.close(fig)

# -----------------------
# 4. Korelacje
# -----------------------
fig, ax = plt.subplots(figsize=(12, 10))

sns.heatmap(
    resampled.corr(),
    cmap="coolwarm",
    annot=False,   # 🔥 mniej chaosu
    linewidths=0.5,
    cbar_kws={"shrink": 0.8},
    ax=ax
)

ax.set_title("Macierz korelacji")
fig.tight_layout()
fig.savefig("heatmap.png", dpi=150)
plt.close(fig)