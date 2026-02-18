# MyThermostat
A home wifi thermostat with a Raspberry PI-3 with TFT screen reading the room temperature from Home Assistant.  

### Overview
The wifi thermostat software runs on a Raspberry with TFT 3.5" Touchscreen.
The room temperature is measured by a sensor connnected to Home Assistant. 
The thermostat SW running on the Raspberry PI reads sensor.temperature_sensor from Home Assistant.
Then it compares the received temperature and consequently turn on or off the relay.
The thermostat has the following states:
- Off. The relay is always off

[![](https://github.com/guido57/MyThermostat/blob/master/off.PNG)](https://github.com/guido57/MyThermostat/blob/master/off.PNG)
- Manual. The relay is on if the room temperature is below the set temperature

[![](https://github.com/guido57/MyThermostat/blob/master/manual.PNG)](https://github.com/guido57/MyThermostat/blob/master/manual.PNG)
- Thermostat. The relay is on if the room temperature is below the set temperature at that time range.

[![](https://github.com/guido57/MyThermostat/blob/master/thermostat.PNG)](https://github.com/guido57/MyThermostat/blob/master/thermostat.PNG)

See the logic diagram below also.

### Prepare your Raspberry
0. I used a [Raspberry PI 3 Model B Scheda madre CPU 1.2 GHz Quad Core, 1 GB RAM](https://www.amazon.it/gp/product/B01CD5VC92/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) bought at Amazon
1. Start from a clean sd: I tested 8M and 32M SD Samsung cards.
2. Download and install Raspberry PI OS Bullseye

when installed, activate WiFi, VNC and SSH then:   

```
pip3 install pillow
```

### Autostart the Python3 program on Raspbian
1. Place thermostat folder into /home/pi
2. Add this line to ~/.config/lxsession/LXDE-pi/autostart file
```
...
@sh /home/pi/thermostat/start.sh
```
### Install a TFT 3.5" Touchscreen
1. I used a [Elegoo 3.5 Inch 480x320 TFT LCD Display Touch Screen Monitor](https://www.amazon.it/gp/product/B01N2N86HB/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) 
2. Install the software inputting these commands one by one: 
 
```
sudo apt-mark hold raspberrypi-bootloader 
sudo apt-get update 
sudo apt-get upgrade  
git clone https://github.com/goodtft/LCD-show.git  
chmod -R 755 LCD-show  
cd LCD-show/  
sudo ./LCD35-show 
```
3. Calibrate the screen 
Optional, but useful. Follow instructions at 3.1 here [ELEGOO 3.5" TFT Touchscreen](https://github.com/guido57/MyThermostat/blob/master/3.5inch%20touch%20screen%20user%20manual%EF%BC%88Arduino-EN%EF%BC%89V1.00.2017.04.14.pdf)

Alternatively to the steps above, you can download and install the ready made sd card image.
https://github.com/guido57/MyThermostat/releases/tag/sd_card_image

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
