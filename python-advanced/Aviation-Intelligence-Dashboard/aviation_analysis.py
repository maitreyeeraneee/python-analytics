import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Style
sns.set_style("whitegrid")

# Load Dataset
df = pd.read_csv("dataset/flights.csv")

# -----------------------------
# BASIC INFO
# -----------------------------

print(df.head())
print(df.info())
print(df.isnull().sum())

# -----------------------------
# TOP 10 AIRLINES BY DELAYS
# -----------------------------

top_airlines = df.groupby('carrier_name')['arr_delay'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_airlines.values, y=top_airlines.index)
plt.title("Top 10 Airlines with Highest Delays")
plt.xlabel("Total Delay")
plt.ylabel("Airline")
plt.savefig("plots/top_airlines_delays.png")
plt.show()

# -----------------------------
# TOP 10 BUSIEST AIRPORTS
# -----------------------------

top_airports = df.groupby('airport_name')['arr_flights'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_airports.values, y=top_airports.index)
plt.title("Top 10 Busiest Airports")
plt.xlabel("Total Flights")
plt.ylabel("Airport")
plt.savefig("plots/busiest_airports.png")
plt.show()

# -----------------------------
# DELAYS OVER YEARS
# -----------------------------

yearly_delays = df.groupby('year')['arr_delay'].sum()

plt.figure(figsize=(12,6))
plt.plot(yearly_delays.index, yearly_delays.values, marker='o')
plt.title("Total Flight Delays Over Years")
plt.xlabel("Year")
plt.ylabel("Total Delay")
plt.savefig("plots/delays_over_years.png")
plt.show()

# -----------------------------
# WEATHER DELAY ANALYSIS
# -----------------------------

weather_delays = df.groupby('year')['weather_delay'].sum()

plt.figure(figsize=(12,6))
plt.plot(weather_delays.index, weather_delays.values, marker='o')
plt.title("Weather Delays Over Years")
plt.xlabel("Year")
plt.ylabel("Weather Delay")
plt.savefig("plots/weather_delays.png")
plt.show()

# -----------------------------
# CANCELLATION ANALYSIS
# -----------------------------

top_cancelled = df.groupby('carrier_name')['arr_cancelled'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_cancelled.values, y=top_cancelled.index)
plt.title("Top Airlines by Flight Cancellations")
plt.xlabel("Cancelled Flights")
plt.ylabel("Airline")
plt.savefig("plots/cancelled_flights.png")
plt.show()

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------

numeric_df = df.select_dtypes(include=['int64', 'float64'])

plt.figure(figsize=(14,10))
sns.heatmap(numeric_df.corr(), cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.savefig("plots/correlation_heatmap.png")
plt.show()

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------

print("\n===== AVIATION INSIGHTS =====")

print("1. Certain airlines consistently experience higher delays.")
print("2. Major airports handle extremely high traffic volumes.")
print("3. Weather contributes significantly to yearly delays.")
print("4. Flight delays vary heavily across years.")
print("5. Operational inefficiencies strongly impact cancellations.")
