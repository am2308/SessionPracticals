import pandas as pd

# Load the dataset
df = pd.read_excel("financial_data.xlsx")

# Aggregate financial metrics by location
summary = df.groupby("Location").agg(
    Total_Credit=("Credit", "sum"),
    Total_Debit=("Debit", "sum"),
    Avg_Balance=("Balance", "mean"),
    Total_Transactions=("Transaction_Count", "sum")
).reset_index()

# Save the summary report
summary.to_excel("financial_summary.xlsx", index=False)

print("📊 Financial summary report saved as 'financial_summary.xlsx'")