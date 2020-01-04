#template for tkinter home page taken from:
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import sqlite3
from sqlite3 import Error

# get file path for eHealth directory and add it to sys.path 
# import my modules
# delete file path for eHealth directory from sys.path
import get_path_utilities as path
current = path.get_current_dir()
eHealth_dir = path.getDir(current, 3)
path.insert_dir(eHealth_dir)
from src.database import db_utilities as dbu
from src.database import connect
from src.utilities import track_user as track
path.delete_dir()


#============================ADMIN HOME interface======================

class Admin(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Admin1(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is Admin 1")
       label.pack(side="top", fill="both", expand=True)

class Admin2(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is Admin 2")
       label.pack(side="top", fill="both", expand=True)

class Admin3(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is Admin 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        lbl_title = tk.Label(self, text = "Admin: eHealth system", font=('arial', 15))
        lbl_title.pack(fill=tk.X)
        p1 = Admin1(self)
        p2 = Admin2(self)
        p3 = Admin3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Admin 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Admin 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Admin 3", command=p3.lift)
        btn_back = tk.Button(buttonframe, text='logout', command=self.logout)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        btn_back.pack(side="right")

        p1.show()
        
    def logout(self):
        print('Home window closed')
        return self.destroy()

def close(*args):
    print('Window closed. User logged out')

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    main.bind('<Destroy>', close) #bind a function call to when the window is closed/destroyed - logout the user and delete user.pickle
    root.mainloop()