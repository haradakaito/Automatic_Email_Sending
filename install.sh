#!/bin/bash

echo "=== Installing python libraries ==="
pip install --break-system-packages -r requirements.txt || pip install -r requirements.txt

echo "=== Copying files ==="
cp ./service/* /etc/systemd/system/
mkdir -p /usr/local/bin/auto_mail_send
cp -r ./config/ /usr/local/bin/auto_mail_send/config
cp -r ./lib/ /usr/local/bin/auto_mail_send/lib

echo "=== Setting up service ==="
systemctl daemon-reload
systemctl enable --now mail_send.service
systemctl enable --now mail_send.timer
systemctl daemon-reload

echo "=== Installation complete ==="