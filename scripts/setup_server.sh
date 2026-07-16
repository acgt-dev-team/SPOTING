#!/bin/bash

sudo apt update

sudo apt upgrade -y

sudo apt install -y \
git \
python3 \
python3-pip \
python3-venv \
apache2 \
postgresql \
postgresql-contrib \
curl

curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

sudo apt install -y nodejs

sudo a2enmod proxy

sudo a2enmod proxy_http

sudo a2enmod rewrite

git clone https://github.com/acgt-dev-team/SPOTING.git

cd SPOTING/backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cd ../frontend

npm install

echo
echo "Setup Finished."