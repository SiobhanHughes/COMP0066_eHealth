#template for tkinter home page taken from:
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import logging

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


#============================GP HOME interface======================

log_file = path.dataDir_path('eHealth_output.log', 3)
logging.basicConfig(level=logging.DEBUG,
                    filename=log_file,
                    filemode ='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

class GP(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class GP1(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is GP 1")
       label.pack(side="top", fill="both", expand=True)

class GP2(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is GP 2")
       label.pack(side="top", fill="both", expand=True)

class GP3(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is GP 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        lbl_title = tk.Label(self, text = "GP: eHealth system", font=('arial', 15))
        lbl_title.pack(fill=tk.X)
        p1 = GP1(self)
        p2 = GP2(self)
        p3 = GP3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="GP 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="GP 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="GP 3", command=p3.lift)
        btn_back = tk.Button(buttonframe, text='logout', command=self.logout)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        btn_back.pack(side="right")

        p1.show()
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
    
    def logout(self):
        print('GP logged out. Widgets destroyed')
        logging.info('GP logged out. Widgets destroyed')
        path.delete_from_dataDir('user.pickle', 3) #deleting user.pickle indicates no user is logged in and frees the application for another user to log in
        logging.info('user.pickle deleted - new user can log in')
        self.destroy()

def close(*args):
    print('GP logged out. Window closed')

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("400x400")
    main.bind('<Destroy>', close)
    root.mainloop()