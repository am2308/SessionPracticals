import pandas as pd

# Load Excel files
excel1 = "assignee.xlsx"  # Replace with your first Excel file
excel2 = "MigrationSanityCheckReport19thDec.xlsx"  # Replace with your second Excel file

# Read data into DataFrames
df1 = pd.read_excel(excel1)  # File 1 with "repo_name" and "Assignee"
df2 = pd.read_excel(excel2)  # File 2 with "repo_name"

# Merge DataFrames based on "repo_name"
merged_df = df2.merge(df1[['repo_name', 'Assignee']], on='repo_name', how='left')

# Add default assignee name if there is no match
merged_df['Assignee'] = merged_df['Assignee'].fillna("Michelle - Automated")

# Save the updated DataFrame back to Excel
output_file = "MigrationSanityCheckReport19thDec.xlsx"
merged_df.to_excel(output_file, index=False)

print(f"Updated file saved as {output_file}")
