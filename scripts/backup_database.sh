#!/bin/bash

BACKUP_DIR="$HOME/db_backups"

mkdir -p "$BACKUP_DIR"

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

sudo -u postgres pg_dump spoting > "$BACKUP_DIR/spoting_$DATE.sql"

echo
echo "Backup Created:"
echo "$BACKUP_DIR/spoting_$DATE.sql"