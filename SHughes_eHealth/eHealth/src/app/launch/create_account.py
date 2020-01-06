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
from src.app.GP import gp_home
from src.app.Patient import patient_home
path.delete_dir()


#============================CREATE ACCOUNT interface======================


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

        #==============================ENTRY WIDGETS==================================
        self.email = tk.Entry(self.Form, textvariable=self.EMAIL, font=(14))
        self.email.grid(row=0, column=1)
        self.password1 = tk.Entry(self.Form, textvariable=self.PASSWORD1, show="*", font=(14))
        self.password1.grid(row=3, column=1)
        self.password2 = tk.Entry(self.Form, textvariable=self.PASSWORD2, show="*", font=(14))
        self.password2.grid(row=4, column=1)

        #==============================BUTTON WIDGETS=================================
        self.btn_login = tk.Button(self.Form, text="Create", width=45, command=self.create)
        self.btn_login.grid(pady=25, row=6, columnspan=2)
        self.btn_login.bind('<Return>', self.create)
        
        #==============================METHODS=================================
        
    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
    
    def create(self):
        self.connect_to_db()
        email = self.EMAIL.get().strip()
        cursor.execute(' SELECT email FROM GPs WHERE email = ? ', (email,))
        gp = cursor.fetchone()
        print(gp)
        cursor.execute(' SELECT email FROM Patients WHERE email = ? ', (email,))
        patient = cursor.fetchone()
        print(patient)
        conn.commit()
        cursor.close()
        conn.close()
        if gp is not None:
            user = 'GP'
            self.passwd(user, email)
        elif patient is not None:
            user = 'Patient'
            self.passwd(user, email)
        else:
            self.lbl_text.config(text="Incorrect email", fg="red")
            self.EMAIL.set("")
            self.PASSWORD1.set("")
            self.PASSWORD2.set("") 
            
    
        
    def passwd(self, user, email):
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
            if user == 'GP':
                cursor.execute(' UPDATE GPs SET passwd = ? WHERE email = ? ', (pwd, email))
                conn.commit()
                cursor.close()
                conn.close()
                self.message_box()
                self.destroy()
            elif user == 'Patient':
                cursor.execute(' UPDATE Patients SET passwd = ? WHERE email = ? ', (pwd, email))
                conn.commit()
                cursor.close()
                conn.close()
                self.message_box()
                self.destroy()
     
    def message_box(self):
        global message
        message = tk.Toplevel()
        message.title("Welcome to the eHealth system")
        width = 500
        height = 500
        message.geometry("%dx%d" % (width, height))
        display = tk.Label(message, text="You successfully created an account! Now you can log in.", font=('arial', 14)).pack()
        
        
        
        
def close(*args):
    print('Window closed')
         
if __name__ == "__main__":
    root = tk.Tk()
    main = Create_account(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("600x600")
    main.bind('<Destroy>', close) #bind a function call to when the window is closed/destroyed - logout the user and delete user.pickle
    root.mainloop()