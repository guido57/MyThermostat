#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser


class Settings:

    def Save(self):

        config = ConfigParser()
        config.read('persist.ini')
        try:
            config.add_section('main')
        except:
            pass # the main section already exists
        config.set('main', 'SetTemp', self.SetTemp[:-1]) # skip ° at the right
        config.set('main', 'Temp1', self.Temp1[:-1])
        config.set('main', 'Temp2', self.Temp2[:-1])
        config.set('main', 'Temp3', self.Temp3[:-1])
        config.set('main', 'Time1', self.Time1)
        config.set('main', 'Time2', self.Time2)
        config.set('main', 'Time3', self.Time3)
        config.set('main', 'OnOff', self.OnOff)

        with open('persist.ini', 'w') as f:
            config.write(f)


    def Load(self):

        config = ConfigParser()
    
        ret = config.read('persist.ini')
        if(ret == []): # the file doesn't exist
            # default Values
            self.SetTemp = "20.0°"
            self.Temp1 = "19.0°"
            self.Temp2 = "20.0°"
            self.Temp3 = "21.0°"
            self.Time1 = "09:00"
            self.Time2 = "17:00"
            self.Time3 = "20:00"
            self.OnOff = "Off"
            return        

        self.SetTemp = config.get('main', 'SetTemp')+"°" # -> "value1"
        self.Temp1 = config.get('main', 'Temp1') +"°"
        self.Temp2 = config.get('main', 'Temp2') +"°"
        self.Temp3 = config.get('main', 'Temp3') +"°"
        self.Time1 = config.get('main', 'Time1') 
        self.Time2 = config.get('main', 'Time2') 
        self.Time3 = config.get('main', 'Time3') 
        self.OnOff = config.get('main', 'OnOff') 
    


