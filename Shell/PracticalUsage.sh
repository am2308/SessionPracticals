#!/bin/bash

# Variables
THRESHOLD=80
EMAIL="b110020510@gmail.com"
HOSTNAME=$(hostname)

# Check Disk Usage
DISK_USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')

if [ "$DISK_USAGE" -gt "$THRESHOLD" ]; then
    echo "Disk usage on $HOSTNAME is above threshold: ${DISK_USAGE}%" | mail -s "Disk Usage Alert" $EMAIL
    echo "Alert sent to $EMAIL."
else
    echo "Disk usage on $HOSTNAME is within limits: ${DISK_USAGE}%."
fi
