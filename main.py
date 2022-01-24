#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import Label, Button, Scale, HORIZONTAL, Canvas, LEFT, Frame, Entry, S, END, StringVar

# from tkinter import ttk


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "ColorMishMash"
    
    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.bind("<Escape>", self.quit)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.frameR = Frame(self)
        self.frameR.pack()
        self.frameG = Frame(self)
        self.frameG.pack()
        self.frameB = Frame(self)
        self.frameB.pack()

        self.varR = StringVar()
        self.lblR = tk.Label(self.frameR, text="R:")
        self.lblR.pack(side=LEFT, anchor=S)
        self.varR.trace('w', self.change)
        self.scaleR = Scale(
            self.frameR, from_=0, to=255, orient=HORIZONTAL, length=256, variable=self.varR)
        self.scaleR.pack(side=LEFT, anchor=S)
        self.entryR = Entry(self.frameR, width=4, textvariable=self.varR)
        self.entryR.pack(side=LEFT, anchor=S)

        self.lblG = tk.Label(self.frameG, text="G:")
        self.lblG.pack(side=LEFT, anchor=S)
        self.varG = StringVar()
        self.varG.trace('w', self.change)
        self.scaleG = Scale(
            self.frameG, from_=0, to=255, orient=HORIZONTAL, length=256, variable=self.varG)
        self.scaleG.pack(side=LEFT, anchor=S)
        self.entryG = Entry(self.frameG, width=4, textvariable=self.varG)
        self.entryG.pack(side=LEFT, anchor=S)

        self.lblB = tk.Label(self.frameB, text="B:")
        self.lblB.pack(side=LEFT, anchor=S)
        self.varB = StringVar()
        self.varB.trace('w', self.change)
        self.scaleB = Scale(
            self.frameB, from_=0, to=255, orient=HORIZONTAL, length=256, variable=self.varB)
        self.scaleB.pack(side=LEFT, anchor=S)
        self.entryB = Entry(self.frameB, width=4, textvariable=self.varB)
        self.entryB.pack(side=LEFT, anchor=S)

        self.varR.trace("w", self.change)
        self.varB.trace("w", self.change)
        self.varG.trace("w", self.change)

        

        self.canvasMain = Canvas(width=256, height=100, background="#000000")
        self.canvasMain.bind("<Button-1>", self.clickHandler)
        self.canvasMain.pack()
        self.entryMain = Entry(self,)
        self.entryMain.pack()



        self.btnQuit = tk.Button(self, text="Quit", command=self.quit)
        self.btnQuit.pack()


        self.frameMem = Frame(self)
        self.frameMem.pack()
        self.canvasMem=[]
        for row in range(3):
            for column in range(7):
                canvas = Canvas(self.frameMem, width=50, height=50, background='#abcdef')
                canvas.grid(row=row, column=column)
                canvas.bind("<Button-1>", self.clickHandler)
                self.canvasMem.append(canvas)
        
        self.load()

    def clickHandler(self,event):
        if self.cget('cursor') != 'pencil':
            self.config(cursor='pencil')
            self.color = event.widget.cget('background')
        elif self.cget('cursor') == 'pencil':
            self.config(cursor='')
            event.widget.config(background=self.color)


    def change(self, var, index, mode):

        r = self.scaleR.get()
        g = self.scaleG.get()
        b = self.scaleB.get()
        colorcode = (f"#{r:02x}{g:02x}{b:02x}")
        self.canvasMain.config(background=colorcode)
        self.entryMain.delete(0, END)
        self.entryMain.insert(0, colorcode)

        self.varR.set(r)
        self.varG.set(g)
        self.varB.set(b)

    def canvasMain2Scales(self):
        color = self.canvasMain.cget('background')
        print(color)
        r = int(color[1:3],16)
        g = int(color[3:6],16)
        b = int(color[5:], 16)

    def load(self):
        try: 
            with open("paleta.txt", "r") as f:
                color = f.readline().strip()

                self.canvasMain.config(background=color)
                self.canvasMain2Scales()
                for canvas in self.canvasMem:
                    color = f.readline().strip()
                    canvas.config(background=color)
        except FileNotFoundError:
            print("Nepodařilo se načíst.")
            

    def quit(self, event=None):
        with open('paleta.txt', 'w') as f:
            f.write(self.canvasMain.cget('background') + "\n")
            for canvas in self.canvasMem:
                f.write(canvas.cget('background') + "\n")
        print('Konec')
        super().quit()


app = Application()
app.mainloop()
