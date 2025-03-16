#!/bin/bash

# Variables
DB_USER="root"
read -sp "Enter your codereplace: " codereplace
DB_NAME="test_db"
BACKUP_DIR="backups"
mkdir $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db-backup-$TIMESTAMP.sql"
touch $BACKUP_FILE
# Create Backup
mysqldump -u $DB_USER -p$codereplace $DB_NAME | gzip > $BACKUP_FILE

# Remove Old Backups (older than 7 days)
find $BACKUP_DIR -type f -mtime +7 -exec rm {} \;

echo "Database backup completed: $BACKUP_FILE."
