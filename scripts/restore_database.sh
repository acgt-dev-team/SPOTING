#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage:"
    echo "./restore_database.sh backup.sql"
    exit 1
fi

BACKUP_FILE=$1

sudo -u postgres psql -d spoting -f "$BACKUP_FILE"

echo
echo "Database Restored."