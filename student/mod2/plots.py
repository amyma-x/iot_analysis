import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# wczytanie danych
df = pd.read_csv("data.csv")

# konwersja czasu
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# 🔥 przeliczenie jednostki (Wh → kWh)
df["Appliances_kWh"] = df["Appliances"] / 1000

# 🔥 usunięcie szumów (agregacja + wygładzenie)
df_hourly = df.resample("1H").mean()

# -----------------------
# 1. Wykres energii
# -----------------------
df_hourly["Appliances_kWh"].rolling(5).mean().plot(figsize=(10,5))
plt.title("Zużycie energii [kWh]")
plt.ylabel("kWh")
plt.xlabel("Czas")
plt.savefig("energy.png")
plt.close()

# -----------------------
# 2. Temperatura
# -----------------------
df_hourly["T1"].rolling(5).mean().plot(figsize=(10,5))
plt.title("Temperatura [°C]")
plt.ylabel("°C")
plt.xlabel("Czas")
plt.savefig("temp.png")
plt.close()

# -----------------------
# 3. Histogram energii
# -----------------------
df["Appliances_kWh"].hist()
plt.title("Histogram zużycia energii [kWh]")
plt.xlabel("kWh")
plt.ylabel("Liczba wystąpień")
plt.savefig("hist.png")
plt.close()

# -----------------------
# 4. Korelacje
# -----------------------
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Macierz korelacji")
plt.savefig("heatmap.png")
plt.close()