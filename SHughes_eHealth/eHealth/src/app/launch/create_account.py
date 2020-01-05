#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import sqlite3
from sqlite3 import Error

import admin_home
import gp_home
import patient_home
import open_home

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


class Create_account(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        #==============================VARIABLES======================================
        self.EMAIL = tk.StringVar()
        self.PASSWORD1 = tk.StringVar()
        self.PASSWORD2 = tk.StringVar()
        
        #set up the layout for the login interface
        #==============================FRAMES=========================================
        self.Top = tk.Frame(self, bd=2,  relief=tk.RIDGE)
        self.Top.pack(side=tk.TOP, fill=tk.X)
        self.Form = tk.Frame(self, height=200)
        self.Form.pack(side=tk.TOP, pady=20)
        
        #==============================LABELS=========================================
        self.lbl_title = tk.Label(self.Top, text = "Create an account for the eHealth system", font=('arial', 15))
        self.lbl_title.pack(fill=tk.X)
        self.lbl_email = tk.Label(self.Form, text = "email:", font=('arial', 14), bd=15)
        self.lbl_email.grid(row=0, sticky="e")
        self.lbl_password1 = tk.Label(self.Form, text = "Password:", font=('arial', 14), bd=15)
        self.lbl_password1.grid(row=1, sticky="e")
        self.lbl_password2 = tk.Label(self.Form, text = "Re-enter Password:", font=('arial', 14), bd=15)
        self.lbl_password2.grid(row=2, sticky="e")
        self.lbl_text = tk.Label(self.Form)
        self.lbl_text.grid(row=3, columnspan=2)

        #==============================ENTRY WIDGETS==================================
        self.email = tk.Entry(self.Form, textvariable=self.EMAIL, font=(14))
        self.email.grid(row=0, column=1)
        self.password1 = tk.Entry(self.Form, textvariable=self.PASSWORD1, show="*", font=(14))
        self.password1.grid(row=1, column=1)
        self.password2 = tk.Entry(self.Form, textvariable=self.PASSWORD2, show="*", font=(14))
        self.password2.grid(row=2, column=1)

        #==============================BUTTON WIDGETS=================================
        self.btn_login = tk.Button(self.Form, text="Create", width=45, command=self.create)
        self.btn_login.grid(pady=25, row=3, columnspan=2)
        self.btn_login.bind('<Return>', self.create)
        
    def create(self):
        pass
    
    def Admin_Window(self): #open Admin home window (Toplevel)
        open_home.Home.Admin_Window(self)
        
    def GP_Window(self): #open GP home window (Toplevel)
        open_home.Home.GP_Window(self)
        
    def Patient_Window(self): #open Pateint home window (Toplevel)
        open_home.Home.Patient_Window(self)
        
        
        
def close(*args):
    print('Window closed')
         
if __name__ == "__main__":
    root = tk.Tk()
    main = Create_account(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("400x400")
    main.bind('<Destroy>', close) #bind a function call to when the window is closed/destroyed - logout the user and delete user.pickle
    root.mainloop()