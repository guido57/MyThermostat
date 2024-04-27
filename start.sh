#!/bin/bash
cd /home/pi/thermostat
sudo killall -9 python3
export DISPLAY=:0.0
python3 -u  MultiPage.py>>thermostat.log 2>>thermostat.log

