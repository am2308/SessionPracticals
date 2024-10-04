import boto3

def list_s3_buckets():
    # Create a session using boto3
    session = boto3.session.Session(profile_name="")
    
    # Create an S3 client
    s3_client = session.client('s3')
    
    # List buckets
    try:
        # List buckets
        response = s3_client.list_buckets()
    except Exception as e:
        print(f"Error listing S3 buckets: {str(e)}")
        # Handle the exception here

    response = s3_client.list_buckets()
    print (response)
    
    # Print bucket names
    print("S3 Buckets:")
    for bucket in response['Buckets']:
        print(f" - {bucket['Name']}")

if __name__ == "__main__":
    list_s3_buckets()