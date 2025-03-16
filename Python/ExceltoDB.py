import pandas as pd
import mysql.connector
from mysql.connector import Error

# Configuration details
excel_file_path = ''  # Replace with your Excel file path
mysql_host = 'localhost'  # Replace with your MySQL host
mysql_user = ''       # Replace with your MySQL username
mysql_codereplace = input("Enter codereplace:")  # Replace with your MySQL codereplace
database_name = ''  # Replace with your desired database name
table_name = ''  # Replace with your desired table name

# Step 1: Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Step 2: Create MySQL connection
try:
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        codereplace=mysql_codereplace,
        auth_plugin='mysql_native_codereplace'
    )

    if connection.is_connected():
        print("Connected to MySQL Server successfully.")
        cursor = connection.cursor()

        # Step 3: Create the database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")

        # Step 4: Create table schema based on DataFrame columns
        column_definitions = []
        for column_name, dtype in zip(df.columns, df.dtypes):
            # Mapping pandas dtypes to MySQL types
            if 'int' in str(dtype):
                mysql_type = 'INT'
            elif 'float' in str(dtype):
                mysql_type = 'FLOAT'
            elif 'datetime' in str(dtype):
                mysql_type = 'DATETIME'
            else:
                mysql_type = 'VARCHAR(255)'  # Default to VARCHAR for strings and other types

            column_definitions.append(f"`{column_name}` {mysql_type}")

        # Create the table with the generated column definitions
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(column_definitions)}
        )
        """
        cursor.execute(create_table_query)
        print(f"Table {table_name} created successfully in {database_name} database.")

        # Step 5: Insert DataFrame data into MySQL table
        # Converting NaN to None to handle NULL values in MySQL
        df = df.where(pd.notnull(df), None)

        for index, row in df.iterrows():
            # Prepare insert statement dynamically based on the DataFrame columns
            columns = ', '.join([f"`{col}`" for col in df.columns])
            values = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(insert_query, tuple(row))

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")
        
except Error as e:
    print(f"Error: {e}")

'''
finally:
    if connection.is_connected():
        #cursor.close()
        #connection.close()
        print("MySQL connection closed.")
'''