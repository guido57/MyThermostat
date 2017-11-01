print("time to rename init.lua into init.old before starting wifi-wps")

tmr.alarm(0, 3000, 1, function ()
    -- time to rename init.lua into init.old to 
    dofile("thermo.lua")    
end)
