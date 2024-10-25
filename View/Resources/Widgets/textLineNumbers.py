import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textWidget = None

    def attach(self, textWidget):
        self.textWidget = textWidget
        
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textWidget.index("@0,0")
        while True :
            dline= self.textWidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textWidget.index("%s+1line" % i)
