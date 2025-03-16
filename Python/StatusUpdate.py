import pandas as pd

def update_repo_action(repo_txt_path, excel_path, output_path):
    try:
        # Read repository names from the .txt file
        with open(repo_txt_path, 'r') as file:
            repo_names = {line.strip() for line in file if line.strip()}
        
        # Load the Excel file into a DataFrame
        df = pd.read_excel(excel_path, engine='openpyxl')
        
        # Check if required columns exist
        if 'repo_name' not in df.columns or 'action' not in df.columns:
            raise ValueError("The Excel file must contain 'repo_name' and 'action' columns.")
        
        # Update the "action" column for matching repo names
        df['action'] = df.apply(
            lambda row: 'Critical' if row['repo_name'] in repo_names else row['action'],
            axis=1
        )
        
        # Save the updated DataFrame to a new Excel file
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"File updated successfully! Saved as: {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
repo_txt_path = 'repo.txt'  # Path to the .txt file containing repository names
excel_path = '../../repo-migration-sanity-check/repositories.xlsx'  # Path to the input Excel file
output_path = '../../../Downloads/updated_repositories.xlsx'  # Path to save the updated Excel file

# Call the function
update_repo_action(repo_txt_path, excel_path, output_path)
