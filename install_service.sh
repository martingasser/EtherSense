#!/bin/bash

sudo cp ethersense.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ethersense.service
sudo systemctl start ethersense.service