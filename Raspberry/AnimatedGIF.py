#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import PhotoImage
from tkinter import Button
from PIL import Image, ImageTk
    
class AnimatedGIF(Button):

    def __init__(self, master, path, forever=True, subsample=1, zoom=1):
        self._master = master
        self._loc = 0
        self._forever = forever
        self._is_running = False
        
        self.load_frames(path=path,subsample=subsample,zoom=zoom)

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 1000

        self._callback_id = None

        self.image = self._frames[0]
        super().__init__(master,text="ciao", image=self._frames[0],borderwidth=0)
        
    def load_frames(self,path,zoom,subsample):

        self._frames = []
        i = 0
        try:
            while i < 100:
                fformat = "gif -index " + str(i)
                photoframe = PhotoImage(file=path,format=fformat)
                photoframe = photoframe.zoom(zoom)
                photoframe = photoframe.subsample(subsample)
                self._frames.append(photoframe)
                i += 1
        except Exception as inst:
            if(inst.args[0] == 'no image data for this index'):
                pass
        
        self._last_index = len(self._frames) 
 
    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self.configure(image=self._frames[self._loc])
        self.image = self._frames[self._loc]
        self._loc += 1

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)
        
    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)
        
    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)
        
    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)


