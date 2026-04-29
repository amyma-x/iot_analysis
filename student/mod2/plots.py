import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
sns.set_context("talk")

DATA_PATH = Path(__file__).resolve().parent / "data.csv"


RESAMPLE_FREQ = "12h"
ROLLING_WINDOW = 20

# Load data
df = pd.read_csv(DATA_PATH)

# Time index
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.sort_index(inplace=True)

#
df["Appliances_kWh"] = df["Appliances"] / 1000

# 
resampled = df.resample("1D").mean()

# 
smoothed = resampled.rolling(window=7, min_periods=1).mean()

# Oś czasu
def format_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
# -----------------------
# 1. Energy consumption
# -----------------------
# -----------------------
# 1. Energia vs temperatura
# -----------------------
fig, ax1 = plt.subplots(figsize=(14,6))

# energia
ax1.plot(smoothed.index, smoothed["Appliances_kWh"], color="tab:blue", label="Energia [kWh]")
ax1.set_ylabel("Energia [kWh]", color="tab:blue")

# druga oś (temperatura)
ax2 = ax1.twinx()
ax2.plot(smoothed.index, smoothed["T1"], color="tab:red", label="Temperatura [°C]")
ax2.set_ylabel("Temperatura [°C]", color="tab:red")

# tytuł i styl
ax1.set_title("Zużycie energii w zależności od temperatury")
ax1.set_xlabel("Data")

fig.tight_layout()
plt.savefig("energy_temp.png", dpi=150)
plt.close()

# -----------------------
# 2. Temperature
# -----------------------
# -----------------------
# Dni tygodnia (po polsku)
# -----------------------

dni_map = {
    "Monday": "Poniedziałek",
    "Tuesday": "Wtorek",
    "Wednesday": "Środa",
    "Thursday": "Czwartek",
    "Friday": "Piątek",
    "Saturday": "Sobota",
    "Sunday": "Niedziela"
}

# zamiana na polskie dni
resampled["dzien_tygodnia"] = resampled.index.day_name().map(dni_map)

# średnia
avg = resampled.groupby("dzien_tygodnia")["Appliances_kWh"].mean()

# kolejność dni
kolejnosc = [
    "Poniedziałek", "Wtorek", "Środa",
    "Czwartek", "Piątek", "Sobota", "Niedziela"
]

avg = avg.reindex(kolejnosc)

# wykres
avg.plot(kind="bar")

plt.title("Średnie zużycie energii według dnia tygodnia")
plt.xlabel("Dzień tygodnia")
plt.ylabel("Zużycie energii [kWh]")

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("day.png", dpi=150)
plt.close()

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
