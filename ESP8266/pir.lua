       outpin=7             -- Select output pin - D7 
       gpio.mode(outpin,gpio.OUTPUT)

       inpin=6                        -- Select input pin - D6
       gpio.mode(inpin,gpio.INT,gpio.PULLUP)  -- attach interrupt to inpin

       pulse1 = tmr.now()

       function motion(level,pulse)
          print("level="..level.." pulse lasted="..(pulse-pulse1)/1000000 .." secs")
          pulse1 = pulse  
          if(level == 1) then
            print("Motion Detection : ON!") 
            gpio.write(outpin,gpio.HIGH)  -- Led ON - Motion detected
          else
            print("Motion Detection : OFF!") 
            gpio.write(outpin,gpio.LOW)  -- Led ON - Motion detected
          end  
       end

       gpio.trig(inpin,"both",motion)  -- trigger on rising edge
