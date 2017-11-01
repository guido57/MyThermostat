---------------------------------------
--- Get MAC address -------------------
---------------------------------------
mymac = wifi.sta.getmac()
---------------------------------------
--- Get Temperature -------------------
---------------------------------------
alt=320 -- altitude of the measurement place


-- tmr.alarm(0, 5000, 1, function ()

-- encoder module is needed only for debug output; lines can be removed if no
-- debug output is needed and/or encoder module is missing

   t = require("ds18b20")
   pin = 3 -- gpio0 = 3, gpio2 = 4

   -- a red led is connected to D4
   led_pin = 4  
   -- set led pin to LOW 
   gpio.mode(led_pin,gpio.OUTPUT)
   gpio.write(led_pin,gpio.LOW)

   function pin_flash(msec_on,msec_off,times,deep_sleep_sec)
            led_time = 0
            led_times = times
            led_on = true
            gpio.write(led_pin,gpio.HIGH)
            tmr.alarm(0, msec_on, tmr.ALARM_SEMI, function()
                -- print(string.format("led_time=%i",led_time))
                if led_time < led_times then
                    
                    if(led_on) then
                        gpio.write(led_pin,gpio.LOW)
                        led_on = false
                        led_time = led_time + 1
                        tmr.interval(0,msec_off)    
                    else
                        gpio.write(led_pin,gpio.HIGH)
                        led_on = true
                        tmr.interval(0,msec_on)    
                    end    
                    tmr.start(0)
                else
                    if(deep_sleep_sec>0) then
                        print(string.format("go to sleep for %i secs",deep_sleep_sec))
                        rtctime.dsleep(deep_sleep_sec*1000000)
                    end     
                end
            end)
   end        
        
   function readout(temp)
          for addr, temp in pairs(temp) do
            -- print(string.format("Sensor %s: %s 'C", addr, temp))
            print(string.format("Sensor %s: %s °C", encoder.toHex(addr), temp)) -- readable address with base64 encoding is preferred when encoder module is available
            print(string.format("sending %s",temp))
            SendTempToThermostat(temp)
          end
        
          -- Module can be released when it is no longer needed
          t = nil
          package.loaded["ds18b20"]=nil
   end
        
   -- t:readTemp(readout) -- default pin value is 3
   t:readTemp(readout, pin)
   if t.sens then
          print("Total number of DS18B20 sensors: "..table.getn(t.sens))
          for i, s in ipairs(t.sens) do
            -- print(string.format("  sensor #%d address: %s%s", i, s.addr, s.parasite == 1 and " (parasite)" or ""))
            print(string.format("  sensor #%d address: %s%s",  i, encoder.toHex(s.addr), s.parasite == 1 and " (parasite)" or "")) -- readable address with base64 encoding is preferred when encoder module is available
          end
   end


   function SendTempToThermostat(Tstr) 
        ---------------------------------------
        --- Send data to Thermostat -----------
        ---------------------------------------
        myjson = '{"temp": "' .. Tstr .. '","macAddress": "'..mymac..'"}'
        print (myjson)
        
        url = "http://192.168.1.69:2048"
       -- url = "http://192.168.1.93:2048"
        
        http.post(url,
                  'Content-Type: application/json\r\n',
                    myjson,
                     function(code, data)
                       if (code < 0) then
                          print("code="..code)
                          print("HTTP request failed")
                          pin_flash(10,1000,1,5) -- it flashes 1 time and go to sleep for 5 secs
                        else
                          pin_flash(10,1000,3,30) -- it flashes 3 times and go to sleep for 30 secs
                          print(code, data)
                        end
                     end)
    end
