import tkinter, sys
from tkinter import scrolledtext

root = tkinter.Tk()

class saveProject:
    def __init__(self, master):
        self.master = master
        self.textFrame = scrolledtext.ScrolledText(self.master, width=100, bd=10, relief="raised")
        self.textFrame.pack()
        self.saveb = tkinter.Button(self.master, text="Save", command= lambda : self.save())
        self.saveb.pack()

    def save(self):
        cur_inp = self.textFrame.get("1.0", tkinter.END)
        print(cur_inp)
        #fl = open("output.txt", "w")
        #fl.write(cur_inp)

project = saveProject(root)
root.mainloop()
