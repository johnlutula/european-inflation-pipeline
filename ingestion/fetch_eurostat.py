import requests
import pandas as pd

print("Fetching data from Eurostat...")

# API Eurostat (inflation - HICP)
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_midx?geo=LU&coicop=CP00"

response = requests.get(url)

data = response.json()

print(data.keys())
#print(data)

print("Raw data received")

# Extraction des valeurs
values = data.get("value", {})
print(len(values))

# Extraction du temps (dates)
time_labels = data["dimension"]["time"]["category"]["label"]

times = list(time_labels.values())

rows = []
for i, value in enumerate(values.values()):
    time = times[i % len(times)]
    rows.append((time,value))

#Création DataFrame
df = pd.DataFrame(
    rows,
    columns = ["time","valeur"]
    )

print(df.head(20))
print(len(df))

from sqlalchemy import create_engine

# Connexion à PostegreSQL
engine = create_engine("postgresql+psycopg2://postgres:postgre123@localhost:5432/financial_db")

# Envoi du DataFrame vers la table
df.to_sql("inflation_eu", engine, if_exists="append", index=False)

print("Données envoyées dans PostgreSQL")

import matplotlib.pyplot as plt

# Convertir en datetime
df["time"] = pd.to_datetime(df["time"])

# Trier par date
df = df.sort_values("time")
df["valeur_lisse"] = df["valeur"].rolling(window=12).mean()

# Plot
plt.figure()
plt.plot(df["time"], df["valeur"], alpha=0.2, label="Raw data")
plt.plot(df["time"], df["valeur_lisse"], label="Smoothed", linewidth=2)
plt.legend()
plt.title("Inflation in Europe over time")
plt.xlabel("Time")
plt.ylabel("Inflation (HICP)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()