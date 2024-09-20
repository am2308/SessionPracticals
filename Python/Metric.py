import boto3
import psutil
import time

# AWS CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')  # Replace 'your-region' with your AWS region, e.g., 'us-east-1'

# Function to get disk space utilization
def get_disk_usage():
    # Get disk usage details for the root ('/') partition
    disk_usage = psutil.disk_usage('/')
    # Calculate the percentage of disk used
    disk_usage_percent = disk_usage.percent
    return disk_usage_percent

# Function to send the metric to CloudWatch
def send_metric_to_cloudwatch(disk_usage_percent):
    response = cloudwatch.put_metric_data(
        Namespace='Custom/ServerMetrics',  # Namespace for custom metrics
        MetricData=[
            {
                'MetricName': 'RootDiskUtilization',  # Custom metric name
                'Dimensions': [
                    {
                        'Name': 'Path',
                        'Value': '/'
                    },
                    {
                        'Name': 'InstanceId',  # Optional: You can tag metrics with instance ID or other relevant dimensions
                        'Value': 'server-identifier'  # Replace with actual instance ID or server identifier if required
                    }
                ],
                'Value': disk_usage_percent,  # The metric value (disk utilization %)
                'Unit': 'Percent'  # Unit of the metric
            },
        ]
    )
    print(f"Metric sent to CloudWatch: {disk_usage_percent}%")
    return response

# Main execution loop to continuously monitor and send disk utilization metrics
def main():
  for i in range(10):
    try:
          # Get disk utilization percentage
          disk_usage_percent = get_disk_usage()
          # Send the metric to CloudWatch
          send_metric_to_cloudwatch(disk_usage_percent)
          # Sleep for 60 seconds before sending the next metric
          time.sleep(60)
    except Exception as e:
          print(f"Error: {e}")
  '''
    while True:
        try:
            # Get disk utilization percentage
            disk_usage_percent = get_disk_usage()
            # Send the metric to CloudWatch
            send_metric_to_cloudwatch(disk_usage_percent)
            # Sleep for 60 seconds before sending the next metric
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
'''
if __name__ == "__main__":
    main()
