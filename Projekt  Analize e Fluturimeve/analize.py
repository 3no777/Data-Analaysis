import pandas as pd
import matplotlib.pyplot as plt

# 1. Leximi i dataset-it dhe shfaqja e 10 rreshtave te para
df = pd.read_csv("flight_delays_dataset.csv")

print("10 rreshtat e pare:")
print(df.head(10))

# 2. Pastrimi i te dhenave - heqim fluturimet e anuluara dhe vlerat null
df_clean = df[df["arr_cancelled"] == 0].dropna()
print(f"\nPas pastrimit mbeten {df_clean.shape[0]} rreshta")

# 3. Bar chart - vonesa mesatare sipas shkakut
shkaqet = ["carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"]
labels  = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
mesataret = [df_clean[k].mean() for k in shkaqet]

plt.figure()
plt.bar(labels, mesataret, color="steelblue")
plt.title("Vonesa mesatare sipas shkakut")
plt.xlabel("Shkaku")
plt.ylabel("Minuta")
plt.savefig("bar_chart_vonesa.png")
plt.show()

# 4. Histogram per ArrDelay
plt.figure()
plt.hist(df_clean["arr_delay"], bins=30, color="orange")
plt.title("Shperndarja e ArrDelay")
plt.xlabel("Vonesa (min)")
plt.ylabel("Frekuenca")
plt.show()

# 5. Scatter plot - arr_flights vs arr_delay
plt.figure()
plt.scatter(df_clean["arr_flights"], df_clean["arr_delay"], alpha=0.3, s=10)
plt.title("Numri i fluturimeve vs Vonesa")
plt.xlabel("Numri i fluturimeve")
plt.ylabel("Vonesa totale (min)")
plt.show()

# 6. Line plot - vonesa mesatare mujore
vonesa_mujore = df_clean.groupby("month")["arr_delay"].mean()

plt.figure()
plt.plot(vonesa_mujore.index, vonesa_mujore.values, marker="o")
plt.title("Vonesa mesatare sipas muajit")
plt.xlabel("Muaji")
plt.ylabel("Vonesa mesatare (min)")
plt.xticks(range(1, 13))
plt.show()

# 7. Analiza
# Muaji me vonesen me te larte
muaji_max = vonesa_mujore.idxmax()
print(f"\nMuaji me vonesen me te larte: muaji {muaji_max} ({vonesa_mujore[muaji_max]:.1f} min)")

# Shkaku me i zakonshem
totalet = {k: df_clean[k].sum() for k in shkaqet}
shkaku_max = max(totalet, key=totalet.get)
print(f"Shkaku me i zakonshem: {shkaku_max} ({totalet[shkaku_max]:,.0f} min totale)")

# A kane me shume vonesa fluturimet me te ngarkuara?
median_f = df_clean["arr_flights"].median()
v_larte  = df_clean[df_clean["arr_flights"] >= median_f]["arr_delay"].mean()
v_ulet   = df_clean[df_clean["arr_flights"] <  median_f]["arr_delay"].mean()
print(f"Vonesa mesatare - ngarkese e larte: {v_larte:.1f} min")
print(f"Vonesa mesatare - ngarkese e ulet:  {v_ulet:.1f} min")
if v_larte > v_ulet:
    print("Fluturimet me te ngarkuara kane me shume vonesa.")
else:
    print("Aeroportet me ngarkese te larte dhe te ulet kane vonesa te ngjashme.")