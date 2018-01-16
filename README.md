# MyThermostat
A home wifi thermostat with a Raspberry PI-3 with LCD screen and an ESP8266  measuring the room temperature and sending it to Raspberry via wifi.  

### Overview

### Prepare your Raspberry
0. I used a [Raspberry PI 3 Model B Scheda madre CPU 1.2 GHz Quad Core, 1 GB RAM](https://www.amazon.it/gp/product/B01CD5VC92/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) bought at Amazon
1. Start from a clean sd: I tested 8M and 32M SD Samsung cards.
2. Install "Raspian Jessie with Desktop" or "Raspbian Stretch with Desktop", I tested:
   - Stretch "2017-11-29-raspbian-stretch.img" downloaded and with "installation guide" at [Download Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)
   - Jessie "2017-04-10-raspbian-jessie.img"
   - Jessie "2016-11-25-raspbian-jessie.img"
3. (Optional, if you don't have screen, keyboard and mouse) Prepare the SD you just created for headless operations following these instructions. [
Raspbian Stretch Headless Setup Procedure](https://www.raspberrypi.org/forums/viewtopic.php?t=191252) 

### Autostart the Python3 program on Raspbian
1. Place thermostat folder into /home/pi
1. Add this line to ~/.config/lxsession/LXDE/autostart file
```
...
@sh /home/pi/thermostat/start.sh
```

### Highlights
 
 
### Screenshots
These are the pages shown by the MyThermostat python3 programs:
- MutiPage.py
- Setting.py

[![N|Solid](https://github.com/guido57/MyThermostat/blob/master/Raspberry/MyThermostat.PNG)](https://github.com/guido57/MyThermostat/blob/master/Raspberry/MyThermostat.PNG)


### Logic Diagram 
[![N|Solid](https://github.com/guido57/MyThermostat/blob/master/Logic%20Diagram%20And%20Schematic%20v1.PNG)](https://github.com/guido57/MyThermostat/blob/master/Logic%20Diagram%20And%20Schematic%20v1.PNG)

### 220V relay connection to Raspberry PI Schematic
See these lines of code inside MultiPage.py
```
 # set pin 40 as output to command the 220V relay
 RELAY_PIN = 40
 ...
 import RPi.GPIO as GPIO
 GPIO.setmode(GPIO.BOARD)
 GPIO.setup(RELAY_PIN,GPIO.OUT)
 GPIO.output(RELAY_PIN,GPIO.HIGH)
```            
