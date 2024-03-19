#!/bin/bash

echo "=== Installing python libraries ==="
pip install --break-system-packages -r requirements.txt || pip install -r requirements.txt

echo "=== Copying files ==="
cp ./service/* /etc/systemd/system/
mkdir -p /usr/local/bin/auto_mail_send
cp -r ./config/ /usr/local/bin/auto_mail_send/
cp -r ./lib/ /usr/local/bin/auto_mail_send/

echo "=== Setting up service ==="
systemctl daemon-reload
systemctl enable mail_send.service
systemctl enable mail_send.timer

echo "=== Installation complete ==="