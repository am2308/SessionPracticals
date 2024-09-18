#/bin/bash
COUNT=0
while IFS= read -r line; do
  # Check if the line contains the keyword
  if echo "$line" | grep -0 -I -q "ERROR"; then
    # Increment count
    COUNT=$((COUNT + 1))
  fi
done < http_error_logs.log

echo "Total no of HTTP Error is $COUNT"
