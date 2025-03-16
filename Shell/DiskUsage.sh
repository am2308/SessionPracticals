#!/bin/bash

# Variables
THRESHOLD=80
EMAIL=""
HOSTNAME=$(hostname)

# Check Disk Usage
disk_usage=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')

# Define CloudWatch namespace and metric names
namespace="DiskUsageMetricsMac"
used_metric_name="UsedSpace"

# Push metrics to CloudWatch
aws cloudwatch put-metric-data --metric-name $used_metric_name --namespace $namespace --value $disk_usage --unit Percent --region us-east-1 --profile test
if [ $? -eq 0 ]; then
  echo "Disk space usage metrics pushed to CloudWatch successfully."
else
  echo "Failed to push disk space usage metrics to CloudWatch."
fi

if [ "$DISK_USAGE" -gt "$THRESHOLD" ]; then
    echo "Disk usage on $HOSTNAME is above threshold: ${DISK_USAGE}%" | mail -s "Disk Usage Alert" $EMAIL
    echo "Alert sent to $EMAIL."
else
    echo "Disk usage on $HOSTNAME is within limits: ${DISK_USAGE}%."
fi
