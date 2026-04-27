import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
sns.set_context("talk")

DATA_PATH = Path(__file__).resolve().parent / "data.csv"
RESAMPLE_FREQ = "3H"
ROLLING_WINDOW = 6

# Load data and prepare time index
ninja = pd.read_csv(DATA_PATH)
ninja["date"] = pd.to_datetime(ninja["date"])
ninja.set_index("date", inplace=True)
ninja.sort_index(inplace=True)

# Convert energy from Wh to kWh
if "Appliances" not in ninja.columns:
    raise KeyError("Column 'Appliances' not found in data.csv")
ninja["Appliances_kWh"] = ninja["Appliances"] / 1000

# Resample to reduce high-frequency noise and then smooth
resampled = ninja.resample(RESAMPLE_FREQ).mean()
smoothed = resampled.rolling(window=ROLLING_WINDOW, min_periods=1, center=True).mean()

# Helper for time axis formatting
def format_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# -----------------------
# 1. Energy consumption
# -----------------------
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(smoothed.index, smoothed["Appliances_kWh"], color="tab:blue", linewidth=2)
ax.set_title("Średnie zużycie energii [kWh] po resamplingu i wygładzeniu")
ax.set_xlabel("Data i godzina")
ax.set_ylabel("Zużycie energii [kWh]")
ax.grid(alpha=0.35)
format_time_axis(ax)
fig.tight_layout()
fig.savefig("energy.png", dpi=150)
plt.close(fig)

# -----------------------
# 2. Temperature
# -----------------------
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(smoothed.index, smoothed["T1"], color="tab:red", linewidth=2)
ax.set_title("Temperatura T1 [°C] po resamplingu i wygładzeniu")
ax.set_xlabel("Data i godzina")
ax.set_ylabel("Temperatura [°C]")
ax.grid(alpha=0.35)
format_time_axis(ax)
fig.tight_layout()
fig.savefig("temp.png", dpi=150)
plt.close(fig)

# -----------------------
# 3. Energy histogram
# -----------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(resampled["Appliances_kWh"].dropna(), bins=30, color="tab:blue", edgecolor="black", alpha=0.8)
ax.set_title("Histogram zużycia energii [kWh] po agregacji")
ax.set_xlabel("Zużycie energii [kWh]")
ax.set_ylabel("Liczba obserwacji")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig("hist.png", dpi=150)
plt.close(fig)

# -----------------------
# 4. Korelacje
# -----------------------
fig, ax = plt.subplots(figsize=(14, 11))
heatmap = sns.heatmap(
    resampled.corr(),
    cmap="coolwarm",
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    cbar_kws={"shrink": 0.8},
    square=True,
    ax=ax,
)
heatmap.set_title("Macierz korelacji zmiennych po resamplingu")
fig.tight_layout()
fig.savefig("heatmap.png", dpi=150)
plt.close(fig)