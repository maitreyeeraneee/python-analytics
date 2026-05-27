import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Style
sns.set_style("whitegrid")

# Load Dataset
df = pd.read_csv("netflix_titles.csv")

# -----------------------------
# BASIC DATA CLEANING
# -----------------------------

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill missing values
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')

# Convert date column
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# -----------------------------
# 1. MOVIES VS TV SHOWS
# -----------------------------

plt.figure(figsize=(6,5))
sns.countplot(x='type', data=df)
plt.title("Movies vs TV Shows on Netflix")
plt.savefig("plots/movies_vs_tvshows.png")
plt.show()

# -----------------------------
# 2. TOP 10 COUNTRIES
# -----------------------------

top_countries = df['country'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top 10 Countries on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.savefig("plots/top_countries.png")
plt.show()

# -----------------------------
# 3. TOP 10 RATINGS
# -----------------------------

top_ratings = df['rating'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_ratings.index, y=top_ratings.values)
plt.title("Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.savefig("plots/ratings_distribution.png")
plt.show()

# -----------------------------
# 4. CONTENT ADDED OVER YEARS
# -----------------------------

df['year_added'] = df['date_added'].dt.year

content_by_year = df['year_added'].value_counts().sort_index()

plt.figure(figsize=(12,6))
plt.plot(content_by_year.index, content_by_year.values)
plt.title("Content Added Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.savefig("plots/content_over_years.png")
plt.show()

# -----------------------------
# 5. MOVIE DURATION ANALYSIS
# -----------------------------

movies = df[df['type'] == 'Movie'].copy()

movies['duration'] = movies['duration'].str.replace(' min', '')
movies['duration'] = pd.to_numeric(movies['duration'], errors='coerce')

plt.figure(figsize=(10,6))
sns.histplot(movies['duration'], bins=30)
plt.title("Movie Duration Distribution")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Count")
plt.savefig("plots/movie_duration.png")
plt.show()

# -----------------------------
# INSIGHTS
# -----------------------------

print("\n===== BASIC INSIGHTS =====")

print("1. Movies dominate Netflix content.")
print("2. United States has the highest number of titles.")
print("3. Netflix content increased rapidly after 2016.")
print("4. TV-MA is one of the most common ratings.")
print("5. Most movies are around 90-120 minutes long.")