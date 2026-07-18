sudo apt update
sudo apt upgrade -y
sudo apt install git -y
git --version
cd ~
git clone https://github.com/acgt-dev-team/SPOTING.git
cd scripts
chmod +x setup_server.sh
./setup_server.sh