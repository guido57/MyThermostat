-- module("weather", package.seeall)

wt = {}


local mattino = 0
local pomeriggio = 1

local function sereno(day,matt_pom) 
       row = day*3+1 + matt_pom 
       for col=1,8,1 do
          wslib.set8x8(row,col,8,0,32)
       end  
end

local function poconuvoloso(day,matt_pom,init)
    if(init) then
        pn_col1 = 2
        pn_col2 = 1
    end
    
    row = day*3+1+matt_pom 
    -- all blue 
    for col=1,8,1 do
          wslib.set8x8(row,col,4,0,32)
    end  
    wslib.set8x8(row,pn_col1,16,16,16)
    wslib.set8x8(row,pn_col2,0,0,0)
end  

local function nuvoloso(day,matt_pom)
       local row = day*3+1+matt_pom 
       for col=1,8,1 do
          wslib.set8x8(row,col,16,16,16)
       end  
end

local function pioggia(day,matt_pom,init)
    if(init) then
        pioggia_col1 = 1
        pioggia_col2 = 3
    end
    
    local row = day*3+1+matt_pom 
    -- all white 
    for col=1,8,1 do
          wslib.set8x8(row,col,16,16,16)
    end  
    wslib.set8x8(row,pioggia_col1,16,16,0)
    wslib.set8x8(row,pioggia_col2,16,16,0)
end 

local function pioggiaschiarite(day,matt_pom,init)
    if(init) then
        pioggiaschiarite_col1 = 1
       
    end
    
    local row = day*3+1+matt_pom 
    -- all white 
    for col=1,1,1 do
          wslib.set8x8(row,col,16,16,16)
    end  
    -- clear blue sky at col 2
    wslib.set8x8(row,2,0,0,16)
    -- all white 
    for col=3,4,1 do
          wslib.set8x8(row,col,16,16,16)
    end  
    -- clear blue sky at col 5
    wslib.set8x8(row,5,0,0,16)
    for col=6,8,1 do
          wslib.set8x8(row,col,16,16,16)
    end  

    wslib.set8x8(row,pioggiaschiarite_col1,16,16,0)
end 

local function neve(day,matt_pom,init)
        if(init) then
            neve_col1 = 1
        end

       local row = day*3+1+matt_pom 
       -- all white 
       for col=1,8,1 do
          wslib.set8x8(row,col,2,2,2)
       end  
       wslib.set8x8(row,neve_col1,16,16,16)
end 


function wt.setWeather(table_weather)

    -- this is called by ht.displayweather
    -- it is time to destroy httplamma.lua to save memory
    ht = nil

    print(collectgarbage("count")*1024)
    collectgarbage("collect")            

    if(wslib == nil) then
        dofile("ws2812lib.lua") -- wslib functions
        wslib.init()
    end
    
    -- clear all 8x8    
    for col=1,8,1 do 
        wslib.SetRow(col,"-","-","-","-","-","-","-","-")
    end
    
    for ndx=1,6,1 do
        print("table_weather["..ndx.."]="..table_weather[ndx])
        if(table_weather[ndx] == "se") then
            sereno((ndx-1)/2,(ndx-1)%2)
        elseif(table_weather[ndx] == "pn")then
            poconuvoloso((ndx-1)/2,(ndx-1)%2,true)
        elseif(table_weather[ndx] == "nu")then
            nuvoloso((ndx-1)/2,(ndx-1)%2)
        elseif(table_weather[ndx] == "pi")then
            pioggia((ndx-1)/2,(ndx-1)%2,true)
        elseif(table_weather[ndx] == "ne")then
            neve((ndx-1)/2,(ndx-1)%2,true)
        elseif(table_weather[ndx] == "ps")then
            pioggiaschiarite((ndx-1)/2,(ndx-1)%2,true)
        end
        timer_msecs = 0 
    end

    timer_timeout = 100
    
    tmr.alarm(2, timer_timeout, tmr.ALARM_SEMI, function ()
        timer_msecs = timer_msecs + timer_timeout
        
        -- handle brightness: hour 7:00-20:59->256   21:01-06:59->16  
     --   if(lt_hh ~= nil) then
       if(pir ~= nil) then
       --      if(tonumber(lt_hh)>=7 and tonumber(lt_hh)<21) then
             if (pir.motion) then
                     wslib.brightness = 256
             else
                     wslib.brightness = 16    
             end
       end 

        -- animate

       if(timer_msecs%1000 == 0 ) then 
            -- 1 moving yellow drop at col1 
           if(pioggiaschiarite_col1 ~= nil) then 
                pioggiaschiarite_col1=pioggiaschiarite_col1-1
                if(pioggiaschiarite_col1<1) then pioggiaschiarite_col1 = 8 end
           end 
           if(pn_col1 ~= nil) then 
            -- 1 moving cloud at col1 
                pn_col1=pn_col1-1
                if(pn_col1<1) then pn_col1 = 8 end
           end 
           if(pn_col2 ~= nil) then 
                -- 1 dark cloud at col2 
                pn_col2=pn_col2-1
                if(pn_col2<1) then pn_col2 = 8 end
           end 
       end 
       if(timer_msecs%500 == 0 ) then 
           if(neve_col1 ~= nil) then 
               neve_col1=neve_col1-1
               if(neve_col1<1) then neve_col1 = 8 end
           end     
       end 
       
       if(timer_msecs%100 == 0) then
            -- 1 moving yellow drop at col1 
           if (pioggia_col1 ~= nil) then 
                pioggia_col1=pioggia_col1-1
                if(pioggia_col1<1) then pioggia_col1 = 8 end
           end
           -- 1 moving yellow drop at col2 
           if(pioggia_col2 ~= nil) then 
                pioggia_col2=pioggia_col2-1
                if(pioggia_col2<1) then pioggia_col2 = 8 end
           end
       end 
       
        for ndx=1,6,1 do
            if(table_weather[ndx] == "se") then
               if(timer_msecs%1000 == 0) then
                   sereno((ndx-1)/2,(ndx-1)%2)
               end 
            elseif(table_weather[ndx] == "pn")then
                if(timer_msecs%1000 == 0) then
                    poconuvoloso((ndx-1)/2,(ndx-1)%2,false)
                end
            elseif(table_weather[ndx] == "nu")then
                if(timer_msecs%1000 == 0) then
                    nuvoloso((ndx-1)/2,(ndx-1)%2)
                end
            elseif(table_weather[ndx] == "pi")then
                if(timer_msecs%100 == 0) then
                    --every 100 msecs 
                    pioggia((ndx-1)/2,(ndx-1)%2,false)
                end
            elseif(table_weather[ndx] == "ps")then
                if(timer_msecs%100 == 0) then
                    --every 100 msecs 
                    pioggiaschiarite((ndx-1)/2,(ndx-1)%2,false)
                end
            elseif(table_weather[ndx] == "ne")then
                if(timer_msecs%500 == 0) then
                    neve((ndx-1)/2,(ndx-1)%2,false)
                end    
            end
        end
        -- restart timer
        tmr.start(2)
    end)

end
