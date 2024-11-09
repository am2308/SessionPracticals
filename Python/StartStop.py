import boto3
from datetime import datetime

# AWS clients
ec2_client = boto3.client('ec2')
dynamodb_client = boto3.resource('dynamodb')

# Configuration variables
DYNAMODB_TABLE_NAME = 'EC2InstanceStatus'  # DynamoDB table name
INSTANCE_ID = 'i-02f439094bbf19ae8'  # Replace with your EC2 instance ID

def get_desired_state(instance_id):
    """
    Retrieves the desired state of an EC2 instance from DynamoDB.
    """
    try:
        table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)
        response = table.get_item(Key={'InstanceID': instance_id})
        if 'Item' in response:
            return response['Item'].get('DesiredState', 'unknown').lower()
        else:
            return 'unknown'
    except Exception as e:
        print(f"Error fetching desired state from DynamoDB: {e}")
        return 'unknown'

def update_dynamodb_state(instance_id, desired_state):
    """
    Updates the desired state of the EC2 instance in DynamoDB.
    """
    try:
        table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)
        table.put_item(
            Item={
                'InstanceID': instance_id,
                'DesiredState': desired_state,
                'LastUpdated': datetime.utcnow().isoformat()
            }
        )
        print(f"DynamoDB updated with new state: {desired_state} for instance {instance_id}.")
    except Exception as e:
        print(f"Error updating DynamoDB: {e}")

def get_instance_status(instance_id):
    """
    Retrieves the current status of the EC2 instance.
    """
    try:
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
        if response['InstanceStatuses']:
            state = response['InstanceStatuses'][0]['InstanceState']['Name']
            return state
        else:
            # If no status is returned, the instance is likely stopped
            return 'stopped'
    except Exception as e:
        print(f"Error getting instance status: {e}")
        return 'unknown'

def stop_ec2_instance(instance_id):
    """
    Stops the EC2 instance.
    """
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance {instance_id}...")
        ec2_client.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} stopped successfully.")
        return True
    except Exception as e:
        print(f"Error stopping instance: {e}")
        return False

def start_ec2_instance(instance_id):
    """
    Starts the EC2 instance.
    """
    try:
        ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Starting instance {instance_id}...")
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} started successfully.")
        return True
    except Exception as e:
        print(f"Error starting instance: {e}")
        return False

def lambda_handler(event, context):
    """
    Main Lambda function handler.
    """
    try:
        # Fetch the desired state from DynamoDB
        desired_state = get_desired_state(INSTANCE_ID)
        current_status = get_instance_status(INSTANCE_ID)
        
        # Determine action based on the desired state or current instance status
        if desired_state == 'stop':
            if current_status != 'running':
                if start_ec2_instance(INSTANCE_ID):
                    update_dynamodb_state(INSTANCE_ID, 'start')
        elif desired_state == 'start':
            if current_status != 'stopped':
                print("stopped")
                if stop_ec2_instance(INSTANCE_ID):
                    update_dynamodb_state(INSTANCE_ID, 'stop')
        elif desired_state == 'unknown':
            # Toggle based on current instance status if no desired state is found
            if current_status == 'running':
                if stop_ec2_instance(INSTANCE_ID):
                    update_dynamodb_state(INSTANCE_ID, 'stop')
            elif current_status == 'stopped':
                if start_ec2_instance(INSTANCE_ID):
                    update_dynamodb_state(INSTANCE_ID, 'start')
            else:
                print(f"Unable to determine action for instance {INSTANCE_ID}. Current status: {current_status}")
        else:
            print(f"Unknown desired state: {desired_state}. No action taken.")
    except Exception as e:
        print(f"Error in Lambda handler: {e}")

