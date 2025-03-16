import pandas as pd

# Load dataset
df = pd.read_excel("financial_data.xlsx")

# Sort by Account_ID for better analysis
df = df.sort_values(by=["Account_ID"])

# Calculate moving average balance over past transactions (simulated)
df["Predicted_Balance"] = df["Balance"].rolling(window=3, min_periods=1).mean()

# Save the predictions
df.to_excel("predicted_balances.xlsx", index=False)

print("📈 Predicted balances saved as 'predicted_balances.xlsx'")