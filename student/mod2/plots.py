import pandas as pd
import matplotlib.pyplot as plt
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

# -----------------------
# 1. Wykres energii
# -----------------------
plt.figure(figsize=(12, 5))
plt.plot(smoothed.index, smoothed["Appliances_kWh"], color="tab:blue", linewidth=2)
plt.title("Średnie zużycie energii [kWh] po resamplingu i wygładzeniu")
plt.xlabel("Data i godzina")
plt.ylabel("Zużycie energii [kWh]")
plt.grid(alpha=0.35)
plt.tight_layout()
plt.savefig("energy.png", dpi=150)
plt.close()

# -----------------------
# 2. Temperatura
# -----------------------
plt.figure(figsize=(12, 5))
plt.plot(smoothed.index, smoothed["T1"], color="tab:red", linewidth=2)
plt.title("Temperatura T1 po resamplingu i wygładzeniu")
plt.xlabel("Data i godzina")
plt.ylabel("Temperatura [°C]")
plt.grid(alpha=0.35)
plt.tight_layout()
plt.savefig("temp.png", dpi=150)
plt.close()

# -----------------------
# 3. Histogram energii
# -----------------------
plt.figure(figsize=(10, 5))
plt.hist(resampled["Appliances_kWh"].dropna(), bins=30, color="tab:blue", edgecolor="black", alpha=0.8)
plt.title("Histogram zużycia energii [kWh] po agregacji")
plt.xlabel("Zużycie energii [kWh]")
plt.ylabel("Liczba obserwacji")
plt.tight_layout()
plt.savefig("hist.png", dpi=150)
plt.close()

# -----------------------
# 4. Korelacje
# -----------------------
plt.figure(figsize=(12, 10))
heatmap = sns.heatmap(
    resampled.corr(),
    cmap="coolwarm",
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    cbar_kws={"shrink": 0.8},
    square=True,
)
heatmap.set_title("Macierz korelacji zmiennych po resamplingu")
plt.tight_layout()
plt.savefig("heatmap.png", dpi=150)
plt.close()