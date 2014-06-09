#!/usr/bin/env python
"""
Calibrate your screen gamma and contrast
with this easy tool, which controls xgamma

author: Petr Studeny
version: 0.1
"""
import Tkinter as tk
import ttk
import subprocess as subp
from pyxrandr import pyxrandr

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

class dashBoard(object):
    def __init__(self, root):
        board = tk.Frame(root)
        board.grid(row=0, column=0, columnspan=3, sticky="nwse")
        tk.Grid.rowconfigure(board,0,weight=1)
        tk.Grid.columnconfigure(board,0,weight=1)

        label = tk.Label(board,text="Set gamma for your monitor using xgamma or xrandr")
        label.grid(row=0, column=0, columnspan=3, sticky="nwse")
        xrandr = pyxrandr()
        self.devs = ttk.Combobox(board, state = 'disable')
        self.devs['values'] = xrandr.getConnectedDevices()
        self.devs.set( xrandr.getConnectedDevices()[0] )
        self.devs.grid(row=1, column=0, sticky="nws")
        self.method = tk.StringVar()
        self.method.set('xgamma')
        metxrandr = tk.Radiobutton(board,text='xrandr', variable = self.method, value = 'xrandr', command=self.togglemethod)
        metxgamma = tk.Radiobutton(board,text='xgamma', variable = self.method, value = 'xgamma', command=self.togglemethod)
        metxrandr.grid(row=1, column=1, sticky="nse")
        metxgamma.grid(row=1, column=2, sticky="nse")
    def togglemethod(self):
        if self.method.get() == 'xrandr':
            self.devs.configure(state='readonly')
        else:
            self.devs.configure(state='disable')


class colorBars(object):
    def __init__(self, root, width, height):
        self.width = width
        self.height = height
        self.bheight = 256/4
        self.bitwidth = 7
        self.w = tk.Canvas(root, width=width, height=height, bg="black")
        self.w.bind("<Configure>",self.redraw)
        self.w.grid(row=0, column=1, sticky='nesw')
        for r in range(5):
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
        self.w.grid(rowspan=4,row=1, column=1, sticky='nesw')
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
        rbutmin =   tk.Button(root, text = "-", command=self.rmin)
        rbutmin.grid(column=0, row=1, sticky="nesw")
        rbutplus =  tk.Button(root, text = "+", command=self.rplus)
        rbutplus.grid(column=2, row=1, sticky="nesw")
        gbutmin =   tk.Button(root, text = "-", command=self.gmin)
        gbutmin.grid(column=0, row=2, sticky="nesw")
        gbutplus =  tk.Button(root, text = "+", command=self.gplus)
        gbutplus.grid(column=2, row=2, sticky="nesw")
        bbutmin =   tk.Button(root, text = "-", command=self.bmin)
        bbutmin.grid(column=0, row=3, sticky="nesw")
        bbutplus =  tk.Button(root, text = "+", command=self.bplus)
        bbutplus.grid(column=2, row=3, sticky="nesw")
        cbutmin =   tk.Button(root, text = "-", command=self.cmin)
        cbutmin.grid(column=0, row=4, sticky="nesw")
        cbutplus =  tk.Button(root, text = "+", command=self.cplus)
        cbutplus.grid(column=2, row=4, sticky="nesw")

    def rmin(self):
        self.changegamma('r','-')
    def rplus(self):
        self.changegamma('r','+')
    def gmin(self):
        self.changegamma('g','-')
    def gplus(self):
        self.changegamma('g','+')
    def bmin(self):
        self.changegamma('b','-')
    def bplus(self):
        self.changegamma('b','+')
    def cmin(self):
        self.changegamma('c','-')
    def cplus(self):
        self.changegamma('c','+')

    def changegamma(self,color,plusmin):
        step = 0.1
        print lableandsetting.devs.get()
        oldgamma = self.getgamma()
        if not color == 'c':
            newgamma = oldgamma[color]+step if plusmin == '+' else oldgamma[color]-step
            cmdline = 'xgamma -'+color+'gamma '+str(newgamma)
            subp.Popen(cmdline.split()).communicate()
        else:
            for citem in oldgamma.keys():
                newgamma = oldgamma[citem]+step if plusmin == '+' else oldgamma[citem]-step
                cmdline = 'xgamma -'+citem+'gamma '+str(newgamma)
                subp.Popen(cmdline.split()).communicate()


    def getgamma(self):
        proc = subp.Popen(['xgamma'], stderr=subp.PIPE)
        (out, err) = proc.communicate()
#-> Red  1.000, Green  1.000, Blue  1.000
        gamma = []
        err = err.strip()
        for bit in err.split(','):
            gamma.append(float(bit[-5:]))
        print gamma
        gammadict = {
                'r':gamma[0],
                'g':gamma[1],
                'b':gamma[2]
                }
        print gammadict
        return gammadict



root = tk.Tk()
app = mainFrame(root)
lableandsetting = dashBoard(app.f)
cb = colorBars(app.f,400,100)
cb.drawBars()
butt = modButtons(app.f)
root.mainloop()

