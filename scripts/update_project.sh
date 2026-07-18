#!/bin/bash

set -e

PROJECT_DIR="$HOME/SPOTING"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "======================================="
echo " SPOTING Deployment Script"
echo "======================================="

echo
echo "Updating Git..."

cd "$PROJECT_DIR"

git fetch origin
git pull origin main

echo
echo "Updating Backend..."

cd "$BACKEND_DIR"

source venv/bin/activate

pip install -r requirements.txt

echo
echo "Updating Frontend..."

cd "$FRONTEND_DIR"

npm install

echo
echo "Building Frontend..."

npm run build

echo
echo "Deploying Frontend..."

sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/

echo
echo "Restarting Services..."

sudo systemctl daemon-reload

sudo systemctl restart spoting

sudo systemctl restart apache2

echo
echo "Running Health Checks..."

curl http://127.0.0.1:8000/health

echo

curl http://127.0.0.1/api/health

echo
echo "======================================="
echo " Deployment Completed Successfully!"
echo "======================================="