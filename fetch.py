import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "YOUR_API_KEY"
CITY = "Chennai"
UNITS = "metric"  # or "imperial"
URL = "https://api.openweathermap.org/data/2.5/forecast"  # 5‑day forecast endpoint

params = {
    "q": CITY,
    "appid": API_KEY,
    "units": UNITS,
    "cnt": 40  # typically 40 records for 5‑day with 3‑hour intervals
}

resp = requests.get(URL, params=params)
resp.raise_for_status()
data = resp.json()

# Flatten list of forecasts into a DataFrame
records = []
for entry in data["list"]:
    records.append({
        "datetime": entry["dt_txt"],
        "temp": entry["main"]["temp"],
        "humidity": entry["main"]["humidity"],
        "wind_speed": entry["wind"]["speed"],
        "description": entry["weather"][0]["description"]
    })

df = pd.DataFrame(records)
df["datetime"] = pd.to_datetime(df["datetime"])

# Plot temperature over time
plt.figure(figsize=(12, 6))
sns.lineplot(x="datetime", y="temp", data=df, marker="o")
plt.title(f"Temperature Forecast for {CITY}")
plt.xlabel("Date and Time")
plt.ylabel(f"Temperature ({'°C' if UNITS=='metric' else '°F'})")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Optionally: humidity bar chart
plt.figure(figsize=(12, 4))
sns.barplot(x="datetime", y="humidity", data=df)
plt.title(f"Humidity Forecast for {CITY}")
plt.xlabel("Date and Time")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
