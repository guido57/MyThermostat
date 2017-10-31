wslib = {}

wslib.brightness = 256

wslib.buffer = ws2812.newBuffer(64, 3)

function wslib.init()
    ws2812.init(ws2812.MODE_SINGLE)
end

function wslib.set8x8(row,col,green,red,blue)

    local inv = 1-(row)%2 -- row=i inv=0; row=2 inv=1; row=3 inv=0 
    wslib.buffer:set( inv*9 + (1-2*inv)*col  + row*8-8,(green*wslib.brightness)/256,(red*wslib.brightness)/256,(blue*wslib.brightness)/256)
    ws2812.write(wslib.buffer)
end

function wslib.SetRow(row,cc) -- cc array 1 to 8

    local red
    local green
    local blue
    
    for i=1,8,1 do
    
        red,green,blue = wslib.getRGB(cc[i]) 
--    print("red="..red.." green="..green.." blue="..blue)
        wslib.set8x8(row,i,green,red,blue)
    end    
end

function wslib.getRGB(colorname)
    
    local W = 1
    local R = 2
    local G = 3
    local B = 4
    local Y = 5

    if(colorname==W or colorname =="W") then
        return 32,32,32
    elseif(colorname==B or colorname =="B") then
        return 0,0,64
    elseif(colorname==R or colorname =="R") then
        return 16,0,0
    elseif(colorname==G or colorname =="G") then
        return 0,16,0
    elseif(colorname==Y or colorname =="Y") then
        return 16,16,0
    else
        return 0,0,0
    end    
end



