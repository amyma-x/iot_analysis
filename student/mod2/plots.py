import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

# czas
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# wykres energii
df["Appliances"].plot(figsize=(10,5))
plt.title("Zużycie energii")
plt.savefig("energy.png")
plt.close()

# temperatura
df["T1"].plot()
plt.savefig("temp.png")
plt.close()

# histogram
df["Appliances"].hist()
plt.savefig("hist.png")
plt.close()

# korelacje
sns.heatmap(df.corr())
plt.savefig("heatmap.png")
plt.close()