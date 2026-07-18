#!/bin/bash

echo
echo "========== Git =========="

cd ~/SPOTING

git log --oneline -5

echo
echo "========== Backend =========="

curl http://127.0.0.1:8000/health

echo
echo "========== Apache =========="

curl http://127.0.0.1/api/health

echo
echo "========== Services =========="

systemctl is-active spoting

systemctl is-active apache2

echo
echo "========== IP =========="

hostname -I