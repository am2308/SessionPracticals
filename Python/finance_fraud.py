import pandas as pd

# Load dataset
df = pd.read_excel("financial_data.xlsx")

# Detect suspicious accounts with very high credits or debits
suspicious = df[(df["Credit"] > 45000) | (df["Debit"] > 45000)]

# Save fraud report
suspicious.to_excel("fraud_accounts.xlsx", index=False)

print(f"🚨 {len(suspicious)} suspicious transactions detected. Report saved as 'fraud_accounts.xlsx'")
