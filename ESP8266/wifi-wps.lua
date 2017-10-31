
function startWPS()
     wifi.setmode(wifi.STATION) -- in STATIONAP it doesn't work
     wps.enable()
     wps.start(function(status)
         if status == wps.SUCCESS then
             -- now the AP I stored in flash
             wpsstatus = "WPS Success"
             wifi.sta.connect() 
         elseif status == wps.FAILED then
             wpsstatus = "WPS Failed"
         elseif status == wps.TIMEOUT then
             wpsstatus = "WPS Timeout"
         elseif status == wps.WEP then
             wpsstatus = "WEP not supported"
         elseif status == wps.SCAN_ERR then
             wpsstatus = "WPS AP not found"
         else 
             wpsstatus = "WPS error "..tostring(status)
         end
         print(wpsstatus)         
         wps.disable()
         
     end)
end

function printSSIDs()

--print stored access point info(formatted)
         local x=wifi.sta.getapinfo()
         local y=wifi.sta.getapindex()
         print("\n Number of APs stored in flash:", x.qty)
         print(string.format("  %-6s %-32s %-64s %-18s", "index:", "SSID:", "Password:", "BSSID:")) 
         for i=1, (x.qty), 1 do
              print(string.format(" %s%-6d %-32s %-64s %-18s",(i==y and ">" or " "), i, x[i].ssid, x[i].pwd and x[i].pwd or type(nil), x[i].bssid and x[i].bssid or type(nil)))
         end
end

function getCurrentSSID()
         local ap_info=wifi.sta.getapinfo()
         local ap_index=wifi.sta.getapindex()
         if(ap_info == nil) then return "" end
         local ap_current = ap_info[ap_index]
         if(ap_current == nil) then return "" end
         local ssid = ap_current.ssid   
         if(ssid == nil) then return "" end
         return ssid
end
-- ------------------------------------------------------
print("wifi-wps started")
connstat = "connnecting to SSID"
wpsstatus = ""
firsttime = true
TRY = 0 
MAXTRIES = 7

 -- 
 -- STEP 1: try the stored SSID and PWD
 -- STEP 2: try WPS
 -- repeat

wifi.setmode(wifi.STATION)

if(wslib == nil) then
     dofile("ws2812lib.lua") -- wslib functions
     wslib.init()
end

if(pir == nil) then
     dofile("pir.lua") -- pir motion detector
     
end


wifi.sta.connect()
print("Connecting to "..getCurrentSSID())
-- this alarm runs forever
tmr.alarm(0, 1000, 1, function ()

      local ip = wifi.sta.getip()
      if ip then
            if(connstat ~= "connected") then
              --  print("ESP8266 mode is: " .. wifi.getmode())
              --  print("The module MAC address is: " .. wifi.ap.getmac())
                print("Config done, IP is "..wifi.sta.getip())
                print("Connected to SSID:"..getCurrentSSID())
                connstat = "connected"
                dofile("ws2812lib.lua")
                wslib.SetRow(1,{"G","G","G","G","G","G","G","G"})
                sntp.sync()
            end     
            -- print date and time
            tm = rtctime.epoch2cal(rtctime.get())
            print(string.format("%04d/%02d/%02d %02d:%02d:%02d", tm["year"], tm["mon"], tm["day"], tm["hour"], tm["min"], tm["sec"]))
            
            print("before calling http.main")
            print("garbage="..collectgarbage("count")*1024)
            print("heap="..node.heap())
            dofile("http.lua")
            tmr.interval(0,40 * 60 * 1000) -- repeat after 40 minutes
            tmr.start(1)
            TRY = 0
      else 
            -- no ip obtained 
            -- try MAXTRIES to connect to the stored SSID (if any)
            -- and once by WPS
            if(connstat == "connected") then
                wifi.sta.connect()
                connstat = "connecting"
                print("Lost previous connection: now connecting to "..getCurrentSSID())    
            end
            
            -- uart.write(0,tostring(TRY))
            if TRY <= MAXTRIES then
                TRY = TRY + 1 
                wslib.set8x8(1,TRY,0,0,32)
            else
               -- try WPS 
               if(wpsstatus~="started" then 
                   print("press the WPS button of your router")
                   startWPS()
                   wpsstatus = "started"
                   wslib.SetRow(1,{"-","-","-","-","-","-","-","-"})
                   wslib.set8x8(1,1,0,0,32)
                   TRY = 1
               end                 
            end     
 
            tmr.interval(0,1000)
            tmr.start(1)
      end             
 
end)
-- -----------------------------------------------------------
