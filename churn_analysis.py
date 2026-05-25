import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Style
sns.set_style("whitegrid")

# Load Dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# -----------------------------
# BASIC INFO
# -----------------------------

print(df.head())
print(df.info())
print(df.isnull().sum())

# -----------------------------
# CHURN DISTRIBUTION
# -----------------------------

plt.figure(figsize=(6,5))
sns.countplot(x='Churn', data=df)
plt.title("Customer Churn Distribution")
plt.savefig("plots/churn_distribution.png")
plt.show()

# -----------------------------
# GENDER VS CHURN
# -----------------------------

plt.figure(figsize=(6,5))
sns.countplot(x='gender', hue='Churn', data=df)
plt.title("Gender vs Churn")
plt.savefig("plots/gender_vs_churn.png")
plt.show()

# -----------------------------
# CONTRACT TYPE ANALYSIS
# -----------------------------

plt.figure(figsize=(8,5))
sns.countplot(x='Contract', hue='Churn', data=df)
plt.title("Contract Type vs Churn")
plt.xticks(rotation=10)
plt.savefig("plots/contract_vs_churn.png")
plt.show()

# -----------------------------
# INTERNET SERVICE ANALYSIS
# -----------------------------

plt.figure(figsize=(8,5))
sns.countplot(x='InternetService', hue='Churn', data=df)
plt.title("Internet Service vs Churn")
plt.savefig("plots/internet_vs_churn.png")

plt.show()

# -----------------------------
# MONTHLY CHARGES ANALYSIS
# -----------------------------

plt.figure(figsize=(10,6))
sns.histplot(data=df, x='MonthlyCharges', hue='Churn', bins=30)
plt.title("Monthly Charges Distribution")
plt.savefig("plots/monthly_charges.png")
plt.show()

# -----------------------------
# TENURE ANALYSIS
# -----------------------------

plt.figure(figsize=(10,6))
sns.histplot(data=df, x='tenure', hue='Churn', bins=30)
plt.title("Customer Tenure Analysis")
plt.savefig("plots/tenure_analysis.png")
plt.show()

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------

numeric_df = df.select_dtypes(include=['int64', 'float64'])

plt.figure(figsize=(8,6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.savefig("plots/correlation_heatmap.png")
plt.show()

# -----------------------------
# SENIOR CITIZEN ANALYSIS
# -----------------------------

plt.figure(figsize=(6,5))
sns.countplot(x='SeniorCitizen', hue='Churn', data=df)
plt.title("Senior Citizen vs Churn")
plt.savefig("plots/seniorcitizen_vs_churn.png")
plt.show()

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------

print("\n===== BUSINESS INSIGHTS =====")

churn_rate = (df['Churn'].value_counts(normalize=True)['Yes']) * 100

print(f"Overall churn rate: {churn_rate:.2f}%")
print("Month-to-month customers churn the most.")
print("Customers with higher monthly charges are more likely to churn.")
print("Long-term customers are more loyal.")
print("Fiber optic users show higher churn rates.")
print("Contract type strongly affects churn.")