#!/bin/bash

if [ "$EUID" -eq 0 ]; then
    echo "Do not run this script as root."
    echo "Run it as a normal user with sudo privileges."
    exit 1
fi




set -e

########################################
# SPOTING Automatic Installer
########################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$SCRIPT_DIR/config.env" ]; then
    echo "config.env not found!"
    exit 1
fi

source "$SCRIPT_DIR/config.env"

########################################
# Internet Check
########################################

echo "Checking Internet Connection..."

if ! ping -c 1 github.com >/dev/null 2>&1; then
    echo "ERROR: No Internet Connection."
    exit 1
fi

echo "Internet OK."
echo

echo
echo "====================================="
echo " SPOTING Automatic Installer"
echo "====================================="
echo


########################################
# Install Packages
########################################

echo "[1/9] Installing Ubuntu packages..."

sudo apt update

sudo apt install -y \
git \
curl \
wget \
apache2 \
postgresql \
postgresql-contrib \
python3 \
python3-pip \
python3-venv \
software-properties-common


echo
########################################
# Validate Configuration
########################################

if [ -z "$DB_NAME" ]; then
    echo "DB_NAME missing in config.env"
    exit 1
fi

if [ -z "$DB_USER" ]; then
    echo "DB_USER missing in config.env"
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    echo "DB_PASSWORD missing in config.env"
    exit 1
fi

if [ -z "$NODE_VERSION" ]; then
    echo "NODE_VERSION missing in config.env"
    exit 1
fi
echo "[2/9] Installing NodeJS..."

if [ -z "$NODE_VERSION" ]; then
    echo "NODE_VERSION not found in config.env"
    exit 1
fi

curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -

sudo apt install -y nodejs

echo

echo "[3/9] Configuring Apache..."

sudo a2enmod proxy

sudo a2enmod proxy_http

sudo a2enmod rewrite

echo

echo "[4/9] Configuring PostgreSQL..."


sudo systemctl enable postgresql
sudo systemctl start postgresql
if ! systemctl is-active --quiet postgresql; then
    echo "PostgreSQL failed to start."
    exit 1
fi

sleep 3

sudo -u postgres psql <<EOF

ALTER USER postgres PASSWORD '${DB_PASSWORD}';

EOF

echo

echo "Creating database..."

sudo -u postgres psql <<EOF

SELECT 'CREATE DATABASE ${DB_NAME}'
WHERE NOT EXISTS (
SELECT FROM pg_database
WHERE datname='${DB_NAME}'
)\gexec

EOF

echo

echo "[5/9] Restoring Database..."

if [ -f "$SCRIPT_DIR/backup.sql" ]; then

    sudo -u postgres psql \
        -d "$DB_NAME" \
        -f "$SCRIPT_DIR/backup.sql"

else

    echo
    echo "ERROR: backup.sql not found!"
    echo "Expected:"
    echo "$SCRIPT_DIR/backup.sql"
    exit 1

fi