#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.name == 'posix':
    # on raspberry
    print("ptvsd.enable_attach('my_secret')")
    import ptvsd
    ptvsd.enable_attach('my_secret')

# import for the GUI
from tkinter import Tk, Button, PhotoImage, messagebox
from tkinter.ttk import Frame,  Label, Entry, Style
# import for the HTTP Server
import threading, json, time
from queue import Queue, Empty
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from Settings import Settings
from AnimatedGIF import AnimatedGIF

TITLE_FONT = ("Helvetica", 18, "bold")
RELAY_PIN = 40

class SampleApp(Tk):

    def save_settings(self_SampleApp):

        self_SampleApp.settings.OnOff = self_SampleApp.frames["MainPage"].OffBtn["text"]
        self_SampleApp.settings.SetTemp = self_SampleApp.frames["MainPage"].SetTemp["text"]
        self_SampleApp.settings.Temp1 = self_SampleApp.frames["PagePrg"].Temp1["text"]
        self_SampleApp.settings.Temp2 = self_SampleApp.frames["PagePrg"].Temp2["text"]
        self_SampleApp.settings.Temp3 = self_SampleApp.frames["PagePrg"].Temp3["text"]
        self_SampleApp.settings.Time1 = self_SampleApp.frames["PagePrg"].Time1["text"]
        self_SampleApp.settings.Time2 = self_SampleApp.frames["PagePrg"].Time2["text"]
        self_SampleApp.settings.Time3 = self_SampleApp.frames["PagePrg"].Time3["text"]

        self_SampleApp.settings.Save()        

    def on_closing(self):
        self.save_settings()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
   

    def __init__(self, server_queue ):
        Tk.__init__(self)
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
      
        if os.name == 'nt':
            # on windows
            self.geometry("480x320+200+200")
        elif(os.name == 'posix') :
            # on raspberry
            # hide mouse cursor
            self.config(cursor="none")

            # go fullscreen
            self.geometry("{0}x{1}+0+0".format(
                self.winfo_screenwidth(), self.winfo_screenheight()))
            self.overrideredirect(1)

            # set pin 40 as outpot to command the 220V relay
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(RELAY_PIN,GPIO.OUT)
            GPIO.output(RELAY_PIN,GPIO.HIGH)

        # Load Settings
        self.settings = Settings()
        self.settings.Load()
        self.frames = {}
        self.frames["PagePrg"] = PagePrg(parent=container, controller=self, queue=server_queue)
        self.frames["PagePrg"].Temp1["text"] = self.settings.Temp1
        self.frames["PagePrg"].Temp2["text"] = self.settings.Temp2
        self.frames["PagePrg"].Temp3["text"] = self.settings.Temp3
        self.frames["PagePrg"].Time1["text"] = self.settings.Time1
        self.frames["PagePrg"].Time2["text"] = self.settings.Time2
        self.frames["PagePrg"].Time3["text"] = self.settings.Time3
        self.frames["MainPage"] = MainPage(parent=container, controller=self, queue=server_queue)
        self.frames["MainPage"].SetTemp["text"] = self.settings.SetTemp
        self.frames["MainPage"].OffBtn["text"] = self.settings.OnOff

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        self.frames["PagePrg"].grid(row=0, column=0, sticky="nsew")
        self.frames["MainPage"].grid(row=0, column=0, sticky="nsew")
 
        self.show_frame("MainPage")
        # clicking 3 times enables the right settings 
        self.frames["MainPage"].OffBtnClick()
        self.frames["MainPage"].OffBtnClick()
        self.frames["MainPage"].OffBtnClick()

        Tk.protocol(self,"WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class PagePrg(Frame):
    
    def __init__(self, parent, controller, queue):
        Frame.__init__(self, parent)
        self.controller = controller
        self.queue = queue

        def UpTempBtnClick(lbl):
            temp = float(lbl["text"][:-1])
            lbl["text"] = str(temp+1.0) + "°" 
 
        def DnTempBtnClick(lbl):
            temp = float(lbl["text"][:-1])
            lbl["text"] = str(temp-1.0) + "°"

        def UpTimeBtnClick(lbl):
           hh = lbl["text"][0:2]
           mm = lbl["text"][3:5]
           hh_int = int(hh) + 1
           if(hh_int == 24): hh_int = 0 
           hh = str(hh_int)
           if(len(hh)==1) : hh="0" + hh
           lbl["text"] = hh + ":" + mm 

        def DnTimeBtnClick(lbl):
           hh = lbl["text"][0:2]
           mm = lbl["text"][3:5]
           hh_int = int(hh) - 1
           if(hh_int == -1): hh_int = 23 
           hh = str(hh_int)
           if(len(hh)==1) : hh="0" + hh
           lbl["text"] = hh + ":" + mm 
     
        def PlaceBtn(imgfile,_row,_col, _callback,lbl):
            photo1 = PhotoImage(file=imgfile)
            photo1 = photo1.zoom(3)
            photo1 = photo1.subsample(5)
            btn = Button(self, text="Up",command = lambda: _callback(lbl), image=photo1, borderwidth=0)
            btn.image = photo1
            btn.grid(row=_row, column=_col) 
            
        def PlaceTime(_text, _row,_col):
            timeStyle = Style ()
            timeStyle.configure("PrgTime.TLabel", font = ('Helvetica','16','bold'))
            TimeLbl = Label(self, text=_text, style="PrgTime.TLabel")
            TimeLbl.grid(row=_row,column=_col)
            return TimeLbl

        def PlaceTemp(_text, _row,_col):
            tempStyle = Style ()
            tempStyle.configure("PrgTemp.TLabel", font = ('Helvetica','16','bold'), foreground="blue")
            TempLbl = Label(self, text=_text, style="PrgTemp.TLabel")
            TempLbl.grid(row=_row,column=_col)
            return TempLbl

        ''' COLUMN 1 '''
        Time1 = PlaceTime("09:00",5,1)
        PlaceBtn("up.gif",4,1,UpTimeBtnClick,Time1)
        PlaceBtn("dn.gif",6,1,DnTimeBtnClick,Time1)
        self.Time1 = Time1

        ''' COLUMN 2 '''
        TempLbl1 = PlaceTemp("20.0°",1,2)
        PlaceBtn("up.gif",0,2,UpTempBtnClick, TempLbl1)
        PlaceBtn("dn.gif",2,2,DnTempBtnClick, TempLbl1)
        self.Temp1 = TempLbl1

        ''' COLUMN 3 '''
        Time2 = PlaceTime("10:00",5,3)
        PlaceBtn("up.gif",4,3,UpTimeBtnClick,Time2)
        PlaceBtn("dn.gif",6,3,DnTimeBtnClick,Time2)
        self.Time2 = Time2

        ''' COLUMN 4 '''
        TempLbl2 = PlaceTemp("20.0°",1,4)
        PlaceBtn("up.gif",0,4,UpTempBtnClick, TempLbl2)
        PlaceBtn("dn.gif",2,4,DnTempBtnClick, TempLbl2)
        self.Temp2 = TempLbl2

        ''' COLUMN 5 '''
        Time3 = PlaceTime("12:00",5,5)
        PlaceBtn("up.gif",4,5,UpTimeBtnClick,Time3)
        PlaceBtn("dn.gif",6,5,DnTimeBtnClick,Time3)
        self.Time3 = Time3

        ''' COLUMN 6 '''
        TempLbl3 = PlaceTemp("20.0°",1,6)
        PlaceBtn("up.gif",0,6,UpTempBtnClick, TempLbl3)
        PlaceBtn("dn.gif",2,6,DnTempBtnClick, TempLbl3)
        self.Temp3 = TempLbl3

        ''' COLUMN 7 '''
        photo1 = PhotoImage(file="rightarrow.gif")
        photo1 = photo1.subsample(3)
        btn = Button(self, text="Up",command = lambda: controller.show_frame("MainPage"), image=photo1, borderwidth=0)
        btn.image = photo1
        btn.grid(row=6,column=7) 


class MainPage(Frame):
 
    def __init__(self, parent, controller, queue):
        Frame.__init__(self, parent)
        self.controller = controller
        self.queue = queue
        self.display_time_count = 0
        self.WIFI_on = False
        self.last_temp_reading = -100

        ''' when Off Manual Program Thermostat is clicked  ''' 
        def OffBtnClick():
           
            if (OffBtn["text"] == "Off"):
                OffBtn["text"] = "Manual"
                UpTempBtn["state"]="normal"
                DnTempBtn["state"]="normal"
                SetTempLbl["state"]="normal"
                PrgBtn["state"]="disabled"
            elif OffBtn["text"] == "Manual":
                OffBtn["text"] = "Thermostat"
                UpTempBtn["state"]="disabled"
                DnTempBtn["state"]="disabled"
                SetTempLbl["state"]="normal"
                PrgBtn["state"]="normal"
            elif OffBtn["text"] == "Thermostat":
                OffBtn["text"] = "Off"
                UpTempBtn["state"]="disabled"
                DnTempBtn["state"]="disabled"
                SetTempLbl["state"]="normal"
                PrgBtn["state"]="disabled"
            FunctLbl["text"] = OffBtn["text"] 

        self.OffBtnClick = OffBtnClick

        ''' when Program Button is clicked  ''' 
        def PrgBtnClick():
            controller.show_frame("PagePrg")

        def UpTempBtnClick():
            temp = float(SetTempLbl["text"][:-1])
            SetTempLbl["text"] = str(temp+1.0) + "°" 
 
        def DnTempBtnClick():
            temp = float(SetTempLbl["text"][:-1])
            SetTempLbl["text"] = str(temp-1.0) + "°"

        def PlaceTimeNow(_text, _row,_col):
            timeStyle = Style ()
            timeStyle.configure("Time.TLabel", font = ('Helvetica','15','bold'))
            TimeLbl = Label(self, text=_text, style="Time.TLabel")
            TimeLbl.grid(row=_row,column=_col)
            return TimeLbl

        ''' SepLbl - First Row '''
        sepStyle = Style ()
        sepStyle.configure("Sep.TLabel", font = ('Helvetica','15','bold'))
        SepLbl = Label(self, text=" ", width=2, style = "Sep.TLabel")
        SepLbl.grid(row=0, column=0) 
       
        ''' OffBtn '''
        photo1 = PhotoImage(file="rightarrow.gif")
        photo1 = photo1.zoom(2)
        photo1 = photo1.subsample(5)
        OffBtn = Button(self, text="Thermostat", image=photo1, borderwidth=0, command=OffBtnClick)
        OffBtn.image = photo1
        OffBtn.grid(row=1, column=1 ) 
        self.OffBtn = OffBtn

        ''' FunctLbl '''
        functStyle = Style ()
        functStyle.configure("funct.TLabel", font = ('Helvetica','14','bold'), foreground="black")
        FunctLbl = Label(self, text="  ", width=10, style="funct.TLabel")
        FunctLbl["text"] = OffBtn["text"]
        FunctLbl.grid(row=1, column=2, columnspan=2) 

        tempStyle = Style ()
        tempStyle.configure("Temp.TLabel", font = ('Helvetica','40','bold'), foreground="red")
        TempLbl = Label(self, text="20.0°", style="Temp.TLabel")
        TempLbl.grid(row=2,column=2,columnspan=2) 
        self.Temp = TempLbl # to be used by read_sensor

        ''' Flame '''
        flameImg = PhotoImage(file="flame.gif")
        flameImg = flameImg.subsample(4)
        flameBtn = Button(self, text="Up", image=flameImg, borderwidth=0)
      #  flameBtn.grid(row=3, column=2) 
        flameBtn.image = flameImg
        self.flameBtn = flameBtn

        ''' Animated Flame '''
        ani_flame_icon = AnimatedGIF(master=self, path = "ani_flame.gif",zoom=2, subsample=5)
        ani_flame_icon._delay = 100 # update every 100 msec
       # ani_flame_icon.grid(row=3,column=1)
        self.ani_flame_icon = ani_flame_icon

        ''' Animated Flame2 '''
        ani_flame_icon2 = AnimatedGIF(master=self, path = "ani_flame.gif",zoom=2, subsample=5)
        ani_flame_icon2._delay = 100 # update every 100 msec
        ani_flame_icon2.grid(row=3,column=2)
        self.ani_flame_icon2 = ani_flame_icon2

        ''' Animated Flame3 '''
        ani_flame_icon3 = AnimatedGIF(master=self, path = "ani_flame.gif",zoom=2, subsample=5)
        ani_flame_icon3._delay = 100 # update every 100 msec
       # ani_flame_icon3.grid(row=3,column=3)
        self.ani_flame_icon3 = ani_flame_icon3
        
        ''' SepLbl '''
        SepLbl = Label(self, text="  ", width=2)
        SepLbl.grid(row=3, column=4) 

        ''' UpTempBtn '''
        photo1 = PhotoImage(file="up.gif")
        photo1 = photo1.zoom(4)
        photo1 = photo1.subsample(5)
        UpTempBtn = Button(self, text="Up", command=UpTempBtnClick, image=photo1, borderwidth=0)
        UpTempBtn.grid(row=1, column=5) 
        UpTempBtn.image = photo1

        ''' DnTempBtn '''
        photo2 = PhotoImage(file="dn.gif")
        photo2 = photo2.zoom(4)
        photo2 = photo2.subsample(5)
        DnTempBtn = Button(self, text="Dno", command=DnTempBtnClick, image=photo2, borderwidth=0)
        DnTempBtn.grid(row=3, column=5) 
        DnTempBtn.image = photo2

        ''' SetTempLbl '''	
        SetTempStyle = Style ()
        SetTempStyle.configure("SetTemp.TLabel", font = ('Helvetica','20','bold'), foreground="blue")
        SetTempLbl = Label(self, text="22.0°", style="SetTemp.TLabel")
        SetTempLbl.grid(row=2,column=5) 
        self.SetTemp = SetTempLbl
        
        ''' SepLbl '''	
        SetTempStyle = Style ()
        SetTempStyle.configure("SetTemp.TLabel", font = ('Helvetica','20','bold'), foreground="blue")
        SepRowLbl = Label(self, text="  ", style="SetTemp.TLabel")
        SepRowLbl.grid(row=4,column=3) 
        
        ''' PrgBtn '''
        photo3 = PhotoImage(file="settings.gif")
        photo3 = photo3.zoom(3)
        photo3 = photo3.subsample(5)
        PrgBtn = Button(self, text="Prg", command=PrgBtnClick, image=photo3, borderwidth=0)
        PrgBtn.grid(row=2, column=6) 
        PrgBtn.image = photo3
        self.PrgBtn = PrgBtn
        
        ''' WIFI '''
        WIFI_icon = AnimatedGIF(master=self, path = "WIFI_red.gif", subsample=8)
        WIFI_icon.grid(row=4,column=6)
        self.WIFI_icon = WIFI_icon
        
        ''' Time '''    
        placeTimeNow = PlaceTimeNow(time.strftime("%H:%M:%S"), 4,2)
        placeTimeNow.after(1000, self.display_time) # every second
        self.placeTimeNow = placeTimeNow
        
        self.read_sensor()

    def display_time(self):
        try:
            # display time now
            self.placeTimeNow["text"] = time.strftime("%H:%M:%S")

            if(self.OffBtn["text"]=="Thermostat"):
                # if Thermostat set SetTempLbl according to the actual time
                pagePrg = self.controller.frames["PagePrg"]
                templbl1 = self.controller.frames["PagePrg"].Temp1["text"]
                templbl2 = self.controller.frames["PagePrg"].Temp2["text"]
                templbl3 = self.controller.frames["PagePrg"].Temp3["text"]
                time1 = self.controller.frames["PagePrg"].Time1["text"]
                time2 = self.controller.frames["PagePrg"].Time2["text"]
                time3 = self.controller.frames["PagePrg"].Time3["text"]
                timenow = time.strftime("%H:%M")
                if(timenow<time1):
                    self.SetTemp["text"] = templbl3
                elif(timenow<time2):
                    self.SetTemp["text"] = templbl1
                elif(timenow<time3):
                    self.SetTemp["text"] = templbl2
                elif(timenow>=time3):
                    self.SetTemp["text"] = templbl3

            # Turn On/Off Flame
            temp = float(self.Temp["text"][:-1])
            settemp = float( self.SetTemp["text"][:-1])

            if(temp > settemp or self.OffBtn["text"]=="Off"):
                self.FlameOn = False
                # self.flameBtn.grid_remove()
                self.ani_flame_icon.grid_remove()
                self.ani_flame_icon2.grid_remove()
                self.ani_flame_icon3.grid_remove()
                
            else:
                self.FlameOn = True
              #  self.ani_flame_icon.grid(row=3, column=1)
                self.ani_flame_icon2.grid(row=3, column=2)
              #  self.ani_flame_icon3.grid(row=3, column=3)

            # turn RELAY On / Off 
            if(os.name == 'posix') :
                 import RPi.GPIO as GPIO
                 if(self.FlameOn):
                    GPIO.output(RELAY_PIN,GPIO.LOW)
                 else:
                    GPIO.output(RELAY_PIN,GPIO.HIGH)
                     
            # Turn WIFI red / green
            if(time.time() > 60 + self.last_temp_reading):
                self.WIFI_icon.load_frames(path="WIFI_red.gif",zoom=1,subsample=8)
            else:
                self.WIFI_icon.load_frames(path="WIFI_green.gif",zoom=1,subsample=8)
        
        except Empty:
            pass

        # save settings every 30 seconds
        if(self.display_time_count%30 == 0):
            self.controller.save_settings()
        self.display_time_count = self.display_time_count + 1

        self.Temp.after(1000, self.display_time) # read every 1000 msecs
        

   
    def read_sensor(self):
        try:
            # self.lbl["text"] = self.queue.get_nowait()
            str = self.queue.get_nowait()
            self.Temp["text"] = str + "°"
            self.last_temp_reading = time.time()
        except Empty:
            str= ""
            pass

        self.Temp.after(500, self.read_sensor) # read every 500 msecs

    def initUI(self):
      
        self.parent.title("Simple")
        self.style=Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
 
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-length'])
        request_bytes = self.rfile.read(length)
        request_str = request_bytes.decode("utf-8") 
        try:
            jsonobj = json.loads(request_str)
            str_temp = jsonobj["temp"] # get item "temp" which is the temperature as string formatted like 20.3
            self.server.queue.put(str_temp)
        except ee:
            pass

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        wfile_str = "<html><body><h1>POST " +request_str + "</h1></body></html>"
        wfile_encoded = wfile_str.encode()
        self.wfile.write(wfile_encoded)
      #  self.wfile.write("<html><body><h1>POST " + "</h1></body></html>")

    """Respond to a GET request."""
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    # the HTTP Server listening on the IP address at port 1024
    # server = ThreadedHTTPServer(('192.168.1.36', 1024), RequestHandler) # listen on the given IP at port 1024
    server = ThreadedHTTPServer(('', 2048), RequestHandler) # listen on any IP at port 2048
    # this is the Queue to communicate between the GUI and the HTTP Server
    server.queue = Queue()
    print ('Starting server, use <Ctrl-C> to stop')
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # root-
    
    app = SampleApp(server.queue)
    app.mainloop()
    # if mainloop exits -> shut down the server
    server.shutdown()

 