#!/bin/bash
# this statement checks if there is an instance of the EtherSenseServer running
if [[ ! `ps -eaf | grep "python EtherSenseServer.py" | grep -v grep` ]]; then
    python EtherSenseServer.py
fi
