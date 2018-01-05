# MyThermostat
A home wifi thermostat with a Raspberry PI-3 with LCD screen and an ESP8266  measuring the room temperature and sending it to Raspberry via wifi.  

### Overview



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
[![N|Solid](https://github.com/guido57/MyThermostat/blob/master/Logic%20Diagram.PNG)](https://github.com/guido57/MyThermostat/blob/master/Logic%20Diagram.PNG)

### 220V relay connection to Raspberry PI 
See these lines ofo code inside MultiPage.py
```
 # set pin 40 as output to command the 220V relay
 RELAY_PIN = 40
 
 import RPi.GPIO as GPIO
 GPIO.setmode(GPIO.BOARD)
 GPIO.setup(RELAY_PIN,GPIO.OUT)
 GPIO.output(RELAY_PIN,GPIO.HIGH)
```            
