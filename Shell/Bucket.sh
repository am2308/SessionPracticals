#!/bin/bash

# Check if bucket name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <bucket-name>"
  exit 1
fi

echo $1
echo $2
echo $@
echo $#

BUCKET_NAME=$1
INTERVIEW_FOLDER="$HOME/Documents/Interview"
TARBALL_NAME="Interview_backup.tar.gz"

# Create a tarball of the Interview folder
tar -czvf "$TARBALL_NAME" "$INTERVIEW_FOLDER"

if [ $? -eq 0 ]; then
  echo "Tarball '$TARBALL_NAME' created successfully."
else
  echo "Failed to create tarball of the Interview folder."
  exit 1
fi

# Create S3 bucket
aws s3api create-bucket --bucket "$BUCKET_NAME" --region us-east-1 --profile sandbox

if [ $? -eq 0 ]; then
  echo "Bucket '$BUCKET_NAME' created successfully."
  # Upload the tarball to the S3 bucket
  aws s3 cp "$TARBALL_NAME" "s3://$BUCKET_NAME/$TARBALL_NAME" --region us-east-1 --profile sandbox
  if [ $? -eq 0 ]; then
    echo "Tarball '$TARBALL_NAME' uploaded successfully to bucket '$BUCKET_NAME'."
  else
    echo "Failed to upload tarball to bucket '$BUCKET_NAME'."
  fi
else
  echo "Failed to create bucket '$BUCKET_NAME'."
fi