#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect
import re
import hashlib
import binascii

import sqlite3
from sqlite3 import Error

import open_home
import passwd_utilities as pwdu

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
from src.app.Admin import admin_home
path.delete_dir()


#============================ADMIN HOME interface======================


class Change_admin_passwd(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        #==============================VARIABLES======================================
        self.PASSWORD1 = tk.StringVar()
        self.PASSWORD2 = tk.StringVar()
        
        #set up the layout for the login interface
        #==============================FRAMES=========================================
        self.Top = tk.Frame(self, bd=2,  relief=tk.RIDGE)
        self.Top.pack(side=tk.TOP, fill=tk.X)
        self.Form = tk.Frame(self, height=200)
        self.Form.pack(side=tk.TOP, pady=20)
        
        #==============================LABELS=========================================
        self.lbl_title = tk.Label(self.Top, text = "Change Admin default password", font=('arial', 15))
        self.lbl_title.pack(fill=tk.X)
        self.lbl_admin = tk.Label(self.Form, text = "Username: admin", font=('arial', 14), bd=15)
        self.lbl_admin.grid(row=0, sticky="e")
        self.lbl_admin = tk.Label(self.Form, text = "Password requirements: ", font=('arial', 12), bd=15)
        self.lbl_admin.grid(row=1, sticky="e")
        self.lbl_admin = tk.Label(self.Form, text = "At least 8 characters, A capital letter, one number, one special characrter. ", font=('arial', 12), bd=15)
        self.lbl_admin.grid(row=2, sticky="e")
        self.lbl_password1 = tk.Label(self.Form, text = "Password:", font=('arial', 14), bd=15)
        self.lbl_password1.grid(row=3, sticky="e")
        self.lbl_password2 = tk.Label(self.Form, text = "Re-enter Password:", font=('arial', 14), bd=15)
        self.lbl_password2.grid(row=4, sticky="e")
        self.lbl_text = tk.Label(self.Form)
        self.lbl_text.grid(row=5, columnspan=2)
        self.lbl_create = tk.Label(self.Form, text = "If you want to keep the default password, click No.")
        self.lbl_create.grid(row=7, columnspan=2)

        #==============================ENTRY WIDGETS==================================
        self.password1 = tk.Entry(self.Form, textvariable=self.PASSWORD1, show="*", font=(14))
        self.password1.grid(row=3, column=1)
        self.password2 = tk.Entry(self.Form, textvariable=self.PASSWORD2, show="*", font=(14))
        self.password2.grid(row=4, column=1)

        #==============================BUTTON WIDGETS=================================
        self.btn_login = tk.Button(self.Form, text="Yes", width=45, command=self.change_passwd)
        self.btn_login.grid(pady=25, row=6, columnspan=2)
        self.btn_login.bind('<Return>', self.change_passwd)
        self.btn_create = tk.Button(self.Form, text="No", width=45, command=self.no)
        self.btn_create.grid(pady=25, row=8, columnspan=2)
        
        #==============================METHODS=================================
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
    
    def change_passwd(self):
        passwd1 = self.PASSWORD1.get().strip()
        passwd2 = self.PASSWORD2.get().strip()
        if passwd1 == "" or passwd2 == "":
            self.lbl_text.config(text="Please complete the required field!", fg="red")
        elif passwd1 != passwd2:
            self.lbl_text.config(text="Error: re-entered password does not match", fg="red")
            self.PASSWORD1.set("")
            self.PASSWORD2.set("") 
        elif pwdu.strong_passwd(passwd1) == 'weak':
            self.lbl_text.config(text="Error: password does not match the requirements", fg="red")
            self.PASSWORD1.set("")
            self.PASSWORD2.set("") 
        else:
            self.connect_to_db()
            pwd = pwdu.hash_password(passwd1)
            print(pwd)
            cursor.execute(' UPDATE Admin SET passwd = ? WHERE administrator = "admin" ', (pwd,))
            conn.commit()
            cursor.close()
            conn.close()
            self.Admin_Window()
            self.destroy()
        
        
    
    def no(self):
        self.Admin_Window()
        print('Admin logged in without changing password')
        self.destroy()
        
    def Admin_Window(self): #open Admin home window (Toplevel)
        open_home.Home.Admin_Window(self)
        
        
        
def close(*args):
    print('Window closed')
         
if __name__ == "__main__":
    root = tk.Tk()
    main = Change_admin_passwd(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("800x800")
    main.bind('<Destroy>', close) #bind a function call to when the window is closed/destroyed - logout the user and delete user.pickle
    root.mainloop()