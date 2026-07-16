#!/bin/bash

###############################################################################
# SPOTING Automatic Installer
###############################################################################

set -e

########################################
# Do not run as root
########################################

if [ "$EUID" -eq 0 ]; then
    echo
    echo "Please run as a normal user with sudo privileges."
    exit 1
fi

########################################
# Script location
########################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

########################################
# Load configuration
########################################

CONFIG_FILE="$SCRIPT_DIR/config.env"

if [ ! -f "$CONFIG_FILE" ]; then
    echo
    echo "ERROR: config.env not found."
    exit 1
fi

source "$CONFIG_FILE"

########################################
# Validate configuration
########################################

for VAR in \
DB_NAME \
DB_USER \
DB_PASSWORD \
NODE_VERSION \
SITE_NAME \
BACKEND_PORT
do
    if [ -z "${!VAR}" ]; then
        echo
        echo "ERROR: $VAR missing from config.env"
        exit 1
    fi
done

########################################
# Internet
########################################

echo
echo "Checking Internet Connection..."

if ! ping -c 1 github.com >/dev/null 2>&1; then
    echo
    echo "ERROR: Internet connection unavailable."
    exit 1
fi

echo "Internet OK."

echo
echo "=============================================="
echo "     SPOTING Automatic Installer"
echo "=============================================="

###############################################################################
# Ubuntu Packages
###############################################################################

echo
echo "[1/10] Installing Ubuntu packages..."

sudo apt update

sudo apt install -y \
git \
curl \
wget \
apache2 \
python3 \
python3-pip \
python3-venv \
software-properties-common \
ca-certificates \
gnupg \
lsb-release

###############################################################################
# PostgreSQL 18
###############################################################################

echo
echo "[2/10] Installing PostgreSQL 18..."

if ! command -v psql >/dev/null || ! psql --version | grep -q "18"; then

    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    | sudo gpg --dearmor --yes \
    -o /usr/share/keyrings/postgresql.gpg

    echo \
"deb [signed-by=/usr/share/keyrings/postgresql.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
| sudo tee /etc/apt/sources.list.d/pgdg.list >/dev/null

    sudo apt update

    sudo apt install -y \
    postgresql-18 \
    postgresql-client-18

fi

echo
echo "Installed PostgreSQL Version:"

psql --version

if ! psql --version | grep -q "18"; then
    echo
    echo "ERROR: PostgreSQL 18 installation failed."
    exit 1
fi

###############################################################################
# NodeJS
###############################################################################

echo
echo "[3/10] Installing NodeJS ${NODE_VERSION}..."

if ! command -v node >/dev/null; then

    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x \
    | sudo -E bash -

    sudo apt install -y nodejs

fi

echo

node -v
npm -v

###############################################################################
# Apache
###############################################################################

echo

###############################################################################
# Remove Nginx (if installed)
###############################################################################

echo
echo "Checking for Nginx..."

if systemctl list-unit-files | grep -q nginx.service; then

    echo "Nginx detected."

    sudo systemctl stop nginx || true

    sudo systemctl disable nginx || true

    sudo apt purge -y nginx nginx-common || true

    sudo apt autoremove -y

else

    echo "Nginx not installed."

fi
echo "[4/10] Configuring Apache..."

sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite

###############################################################################
# PostgreSQL Configuration
###############################################################################

echo
echo "[5/10] Configuring PostgreSQL..."

sudo systemctl enable postgresql
sudo systemctl start postgresql

sleep 3

if ! systemctl is-active --quiet postgresql; then
    echo
    echo "ERROR: PostgreSQL failed to start."
    exit 1
fi

sudo -u postgres psql <<EOF
ALTER USER postgres PASSWORD '${DB_PASSWORD}';
EOF

###############################################################################
# Database
###############################################################################

echo
echo "[6/10] Creating database..."

sudo -u postgres psql <<EOF

SELECT 'CREATE DATABASE ${DB_NAME}'
WHERE NOT EXISTS
(
SELECT
FROM pg_database
WHERE datname='${DB_NAME}'
)\gexec

EOF

###############################################################################
# Restore
###############################################################################

echo
echo "[7/10] Restoring database..."

BACKUP_FILE="$SCRIPT_DIR/backup.sql"

if [ ! -f "$BACKUP_FILE" ]; then

    echo
    echo "ERROR: backup.sql not found."

    echo

    echo "$BACKUP_FILE"

    exit 1

fi

cp "$BACKUP_FILE" /tmp/spoting_backup.sql

chmod 644 /tmp/spoting_backup.sql

sudo -u postgres psql \
-v ON_ERROR_STOP=1 \
-d "$DB_NAME" \
-f /tmp/spoting_backup.sql

rm -f /tmp/spoting_backup.sql

echo
echo "Database restored successfully."

###############################################################################
# PART 2 STARTS HERE
###############################################################################
###############################################################################
# Backend
###############################################################################

echo
echo "[8/10] Setting up Backend..."

cd "$PROJECT_DIR/backend"

echo "Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo
echo "Installing Python packages..."

pip install --upgrade pip

pip install -r requirements.txt

echo
echo "Creating backend .env..."

cat > .env <<EOF
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}
EOF

###############################################################################
# Frontend
###############################################################################

echo
echo "[9/10] Setting up Frontend..."

cd "$PROJECT_DIR/frontend"

echo
echo "Installing npm packages..."

npm install

SERVER_IP=$(hostname -I | awk '{print $1}')

echo
echo "Creating frontend .env..."

cat > .env <<EOF
VITE_API_URL=http://${SERVER_IP}/api
EOF

echo
echo "Building frontend..."

npm run build

###############################################################################
# Deploy Frontend
###############################################################################

echo
echo "Deploying frontend..."

sudo rm -rf /var/www/html/*

sudo cp -r dist/* /var/www/html/

###############################################################################
# Apache Configuration
###############################################################################

echo
echo "Creating Apache configuration..."

sudo tee /etc/apache2/sites-available/${SITE_NAME}.conf > /dev/null <<EOF
<VirtualHost *:80>

    ServerAdmin admin@localhost

    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPreserveHost On

    ProxyPass /api/ http://127.0.0.1:${BACKEND_PORT}/
    ProxyPassReverse /api/ http://127.0.0.1:${BACKEND_PORT}/

    RewriteEngine On

    RewriteCond %{REQUEST_URI} !^/api/
    RewriteCond %{REQUEST_URI} !^/assets/

    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d

    RewriteRule ^ /index.html [L]

    ErrorLog \${APACHE_LOG_DIR}/${SITE_NAME}_error.log
    CustomLog \${APACHE_LOG_DIR}/${SITE_NAME}_access.log combined

</VirtualHost>
EOF

sudo a2dissite 000-default.conf || true

sudo a2ensite ${SITE_NAME}.conf

sudo systemctl restart apache2

###############################################################################
# Backend Service
###############################################################################

echo
echo "[10/10] Creating Backend Service..."

CURRENT_USER=$(whoami)

sudo tee /etc/systemd/system/spoting.service > /dev/null <<EOF
[Unit]
Description=SPOTING Backend
After=network.target

[Service]
User=${CURRENT_USER}
WorkingDirectory=/home/${CURRENT_USER}/SPOTING/backend
Environment="PATH=/home/${CURRENT_USER}/SPOTING/backend/venv/bin"
ExecStart=/home/${CURRENT_USER}/SPOTING/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

sudo systemctl enable spoting

sudo systemctl restart spoting

sleep 5

###############################################################################
# Health Check
###############################################################################

echo
echo "======================================="
echo "Running Health Checks..."
echo "======================================="

echo
echo "Backend Service:"
systemctl is-active spoting

echo
echo "Apache:"
systemctl is-active apache2

echo
echo "Backend Health:"
curl -s http://127.0.0.1:${BACKEND_PORT}/health
echo

echo
echo "Apache Proxy:"
curl -s http://127.0.0.1/api/health
echo

echo
echo "Git Version:"
cd "$PROJECT_DIR"
git log --oneline -1

echo
echo "Server IP:"
echo "http://${SERVER_IP}"

echo
echo "======================================="
echo " SPOTING Installation Complete!"
echo "======================================="
echo
echo "Open your browser at:"
echo
echo "http://${SERVER_IP}"
echo
echo "Default login:"
echo "Username: superadmin"
echo "Password: 123456"
echo
