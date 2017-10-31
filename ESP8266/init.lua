
print("time to rename init.lua into init.old before starting wifi-wps")

tmr.alarm(0, 10000, 1, function ()
    -- time to rename init.lua into init.old to 
    dofile("wifi-wps.lua")    
end)

