import pandas as pd

# Load the dataset
df = pd.read_excel("financial_data.xlsx")

# Identify accounts with anomalies
anomalies = df[(df["Debit"] > df["Credit"]) | (df["Balance"] < 0)]

# Save the anomaly report
anomalies.to_excel("anomalies.xlsx", index=False)

print(f"⚠️ {len(anomalies)} anomalies detected. Saved to 'anomalies.xlsx'")