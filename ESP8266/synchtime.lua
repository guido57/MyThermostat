st = {}


function st.getDeltaDay(t1,t2)

    return (t2/1440/60 - t1/1440/60)

end


function st.getUTCtime()
    -- synch to NTP server
    -- sntp.sync()
    -- get ESP8266 Real Time Clock time in UNIX Epoch (seconds since 01/01/1970)
    local epochtime = rtctime.get()
    -- convert UNIX epoch time to UTC time
    local tm = rtctime.epoch2cal(epochtime)

    return tm

end

function st.getUTCtimeString()

    local tm = st.getUTCtime()
    return string.format("%04d/%02d/%02d %02d:%02d:%02d", tm["year"], tm["mon"], tm["day"], tm["hour"], tm["min"], tm["sec"])
    
end

function st.getTimeString(epochtime)

    if epochtime == nil then return "" end
    local tm = rtctime.epoch2cal(epochtime)
    
    return string.format("%04d/%02d/%02d %02d:%02d:%02d", tm["year"], tm["mon"], tm["day"], tm["hour"], tm["min"], tm["sec"])
    
end

