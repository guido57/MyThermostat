# MyThermostat
A home wifi thermostat with a Raspberry PI-3 with TFT screen and an ESP32 measuring the room temperature and sending it to Raspberry via wifi.  

ciao

### Overview
The wifi thermostat software runs on a Raspberry with TFT 3.5" Touchscreen.
The room temperature is measured by a sensor connnected to an ESP32. 
Every 30 seconds the ESP32 sends the room temperature to the Raspberry via wifi.
The thermostat SW running on the Raspberry PI compare the received temperature and consequently turn on or off the relay.
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
2. Install "Raspian Jessie with Desktop" or "Raspbian Stretch with Desktop", I tested:
   - Stretch "2017-11-29-raspbian-stretch.img" downloaded and with "installation guide" at [Download Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)
   - Jessie "2017-04-10-raspbian-jessie.img"
   - Jessie "2016-11-25-raspbian-jessie.img"
3. (Optional, if you don't have screen, keyboard and mouse) Prepare the SD you just created for headless operations following these instructions. [
Raspbian Stretch Headless Setup Procedure](https://www.raspberrypi.org/forums/viewtopic.php?t=191252) 
4. Install the python PIL module with the command. In newest Raspberry PI OS it should be there already.
   
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
