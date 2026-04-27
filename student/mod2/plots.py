import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

# czas
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# wykres energii
df["Appliances_kWh"].rolling(50).mean().plot(figsize=(10,5))
plt.title("Zużycie energii [kWh]")
plt.ylabel("kWh")
plt.savefig("energy.png")
plt.close()

# temperatura
df["T1"].rolling(50).mean().plot()
plt.title("Temperatura [°C]")
plt.ylabel("°C")
plt.savefig("temp.png")
plt.close()

# histogram
df["Appliances_kWh"].hist()
plt.title("Histogram zużycia energii [kWh]")
plt.xlabel("kWh")
plt.savefig("hist.png")
plt.close()

# korelacje
sns.heatmap(df.corr())
plt.savefig("heatmap.png")
plt.close()