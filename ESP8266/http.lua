
ht = {}

function ht.main()
    
    local function listap(t) -- (SSID : Authmode, RSSI, BSSID, Channel)
        wifiaps = ""
 --       url = "http://192.168.1.124/httpclient/owm.aspx"
       url = "http://www.dogsally.com/owm.aspx"
        for bssid,v in pairs(t) do
            local ssid, rssi, authmode, channel = string.match(v, "([^,]+),([^,]+),([^,]+),([^,]*)")
            wifiaps = wifiaps
                ..bssid..","..rssi.."\r\n" 
        end
        print(wifiaps)
        http.post(url,
          'Content-Type: application/json\r\n',
            wifiaps,
             function(code, data)
               if (code < 0) then
                  print("code="..code)
                  print("HTTP request failed")
                else
               --   print(code, data)
                  -- get weather
                  table_weather = {}
                  i = 0
                  sep = "\r\n"
                  for str in string.gmatch(data, "([^"..sep.."]+)") do
                     print("i:"..i.." str:"..str)
                     local str_w = string.sub(str,1,2)
                     if(i==0) then
                        -- get localtime
                        lt_dd,lt_MM,lt_yy,lt_hh,lt_mm,lt_ss = string.match(str, "Your local time is: ([^/]+)/([^/]+)/([^ ]+) ([^:]+):([^:]+):([^ ]+) ")
                     elseif(i==1) then
                        table_weather[1]= str_w      
                     elseif(i==3) then
                        table_weather[2]= str_w      
                     elseif(i==4) then
                        table_weather[3]= str_w      
                     elseif(i==6) then
                        table_weather[4]= str_w      
                     elseif(i==7) then
                        table_weather[5]= str_w      
                     elseif(i==9) then
                        table_weather[6]= str_w      
                     end
                     i = i + 1
                  end
                  dofile("weather.lua")
                  wt.setWeather(table_weather)
                 end
             end)
    end
    wifi.sta.getap(1, listap)
end

ht.main()
    
