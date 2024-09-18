#!/bin/bash

# Define the log file
LOG_FILE="http_error_logs.log"

# Define the number of logs to generate
NUM_LOGS=100

# Define a list of HTTP error codes
ERROR_CODES=("400" "401" "403" "404" "500" "502" "503" "504")

# Generate logs
for ((i=1; i<=NUM_LOGS; i++))
do
  # Randomly select an error code
  ERROR_CODE=${ERROR_CODES[$RANDOM % ${#ERROR_CODES[@]}]}
  
  # Generate a random timestamp
  TIMESTAMP=$(date -d "$((RANDOM % 365)) days ago" +"%Y-%m-%d %H:%M:%S")
  
  # Write the log entry to the file
  echo "$TIMESTAMP - ERROR $ERROR_CODE - Some error message" >> "$LOG_FILE"
done

echo "Generated $NUM_LOGS HTTP error logs in $LOG_FILE"

