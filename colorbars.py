import Tkinter as tk

class colorBars(object):
    def __init__(self, width, height, title= "color bars"):
        self.root = tk.Tk()
        self.root.title(title)
        self.w = tk.Canvas(self.root, width=width, height=height)
        self.w.pack()
        self.width = width
        self.height = height
        self.bheight = 256/4
        self.bitwidth = 7
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
        for col in range(256)[::self.bitwidth]:
            for color in colors:
                self.w.create_rectangle(self.scale(col,"w"),\
                               colors.index(color)*self.scale(self.bheight,"h"),\
                               self.scale(col+self.bitwidth,"w"),\
                               (1+colors.index(color))*self.scale(self.bheight,"h"),\
                               fill = self.num2col(col,color),\
                               outline = self.num2col(col,color))
#            w.create_rectangle(col,self.bheight,col+self.bitwidth,2*self.bheight, fill = G, outline = G)
        self.root.mainloop()

cb = colorBars(400,100)
cb.drawBars()




