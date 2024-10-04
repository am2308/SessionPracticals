import json
import pymysql
import boto3
from botocore.exceptions import ClientError

def get_db_credentials(secret_name, region_name):
    """Fetch database credentials from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        # Parse the secret's content
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            return secret
        else:
            raise Exception("Secret is not a valid JSON string.")
    except ClientError as e:
        raise Exception(f"Error retrieving secret from Secrets Manager: {e}")

def create_table(connection):
    """Create a sample table in the MySQL database."""
    
    print("Table Created Successfully")

def lambda_handler(event, context):
    secret_name = "mysql_database"  # Replace with your Secrets Manager secret name
    region_name = "ap-south-1"  # Replace with your AWS region

    # Step 1: Fetch database credentials from Secrets Manager
    secret = get_db_credentials(secret_name, region_name)
    print(secret)
    create_table(secret)

    # Step 2: Establish database connection
