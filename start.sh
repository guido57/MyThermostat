#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority

# wait until X is ready
until xset q &>/dev/null; do
    sleep 1
done


# allow the pi user to access X
xhost +SI:localuser:pi

cd /home/pi/thermostat
exec python3 /home/pi/thermostat/MultiPage.py

