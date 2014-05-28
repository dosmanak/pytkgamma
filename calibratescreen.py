#!/usr/bin/env python
"""
Calibrate your screen gamma and contrast
with this easy tool, which controls xgamma

author: Petr Studeny
version: 0.1
"""
import Tkinter as tk

class mainFrame(object):
    def __init__(self, root, title= "color bars"):
        self.f = tk.Frame(root, padx=5, pady=5)
        root.title(title)
        tk.Grid.rowconfigure(root,0,weight=1)
        tk.Grid.columnconfigure(root,0,weight=1)
        self.f.grid(row=0,column=0,sticky='nesw')
       # self.c = tk.Canvas(self.f, bg="red", width=300, height=50)
       # self.c.grid(row=0, column=0, sticky='nesw')
       # tk.Grid.rowconfigure(self.f,0,weight=1)
       # tk.Grid.columnconfigure(self.f,0,weight=1)

class colorBars(object):
    def __init__(self, root, width, height):
        self.width = width
        self.height = height
        self.bheight = 256/4
        self.bitwidth = 7
        self.w = tk.Canvas(root, width=width, height=height, bg="black")
        self.w.bind("<Configure>",self.redraw)
        self.w.grid(row=0, column=1, sticky='nesw')
        for r in range(4):
            tk.Grid.rowconfigure(root,r,weight=1)
        tk.Grid.columnconfigure(root,1,weight=1)
    def num2col(self, level, color):
        """ returns clean color of given level in form #xxxxxx """
        cval = hex(level).split("x")[1]
        if len(cval) == 1:
            cval = '0'+cval
        colors = {
                'red':'#'+cval+'0000',
                'green':'#00'+cval+'00',
                'blue':'#0000'+cval,
                'grey':'#'+cval+cval+cval
                }
        return colors[color]

    def scale(self, per256, dimension):
        """ returns scaled value per 256 values
            for given dimension """
        if dimension == "h":
            return self.height * per256/256
        else: # dimension == "w":
            return self.width * per256/256
        # There should be some error check
    def drawBars(self):
        """ draws 4 stripes RGB and black from zero to max saturation """
        colors = [ 'red', 'green', 'blue', 'grey' ]
        self.w.grid(rowspan=4,row=0, column=1, sticky='nesw')
        for col in range(256)[::self.bitwidth]:
            for color in colors:
                self.w.create_rectangle(self.scale(col,"w"),\
                               colors.index(color)*self.scale(self.bheight,"h"),\
                               self.scale(col+self.bitwidth,"w"),\
                               (1+colors.index(color))*self.scale(self.bheight,"h"),\
                               fill = self.num2col(col,color),\
                               outline = self.num2col(col,color))
#            w.create_rectangle(col,self.bheight,col+self.bitwidth,2*self.bheight, fill = G, outline = G)
#        self.root.mainloop()
    def redraw(self, event):
        self.width = event.width
        self.height = event.height
        self.drawBars()

class modButtons(object):
    def __init__(self, root):
        rbutmin = tk.Button(root, text = "-")
        rbutmin.grid(column=0, row=0, sticky="nwse")
        rbutplus = tk.Button(root, text = "+")
        rbutplus.grid(column=2, row=0, sticky="nesw")
        gbutmin = tk.Button(root, text = "-")
        gbutmin.grid(column=0, row=1, sticky="nesw")
        gbutplus = tk.Button(root, text = "+")
        gbutplus.grid(column=2, row=1, sticky="nesw")
        bbutmin = tk.Button(root, text = "-")
        bbutmin.grid(column=0, row=2, sticky="nesw")
        bbutplus = tk.Button(root, text = "+")
        bbutplus.grid(column=2, row=2, sticky="nesw")
        cbutmin = tk.Button(root, text = "-")
        cbutmin.grid(column=0, row=3, sticky="nesw")
        cbutplus = tk.Button(root, text = "+")
        cbutplus.grid(column=2, row=3, sticky="nesw")



root = tk.Tk()
app = mainFrame(root)
cb = colorBars(app.f,400,100)
cb.drawBars()
butt = modButtons(app.f)
root.mainloop()

