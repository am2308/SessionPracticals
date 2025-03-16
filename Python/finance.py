import pandas as pd
import random

# Generate sample financial data
num_rows = 10000

data = {
    "Account_ID": [f"ACC{str(i).zfill(6)}" for i in range(1, num_rows + 1)],
    "Location": [random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]) for _ in range(num_rows)],
    "Credit": [round(random.uniform(1000, 50000), 2) for _ in range(num_rows)],
    "Debit": [round(random.uniform(1000, 50000), 2) for _ in range(num_rows)],
    "Balance": [round(random.uniform(10000, 200000), 2) for _ in range(num_rows)],
    "Transaction_Count": [random.randint(1, 500) for _ in range(num_rows)],
    "Account_Type": [random.choice(["Savings", "Current", "Business"]) for _ in range(num_rows)],
    "Currency": ["INR" for _ in range(num_rows)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
file_path = "financial_data.xlsx"
df.to_excel(file_path, index=False, engine='openpyxl')

print(f"Excel file saved as {file_path}")
