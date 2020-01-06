#============================LAUNCH eHealth Application======================

#Used the following tutorial to help make the login feature
#https://www.sourcecodester.com/tutorials/python/11351/python-simple-login-application.html

#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect
import re
import hashlib
import binascii
import logging

import sqlite3
from sqlite3 import Error

import create_account
import open_home
import change_admin_passwd
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
from src.app.GP import gp_home
from src.app.Patient import patient_home
path.delete_dir()


#============================Interface for LOGIN to open main/root window======================

log_file = path.dataDir_path('eHealth_output.log', 3)
logging.basicConfig(level=logging.DEBUG,
                    filename=log_file,
                    filemode ='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

class Login(tk.Frame):
    
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master = master
        
        #==============================VARIABLES======================================
        self.EMAIL = tk.StringVar()
        self.PASSWORD = tk.StringVar()
        
        #set up the layout for the login interface
        #==============================FRAMES=========================================
        self.Top = tk.Frame(self.master, bd=2,  relief=tk.RIDGE)
        self.Top.pack(side=tk.TOP, fill=tk.X)
        self.Form = tk.Frame(self.master, height=200)
        self.Form.pack(side=tk.TOP, pady=20)

        #==============================LABELS=========================================
        self.lbl_title = tk.Label(self.Top, text = "Log in to the eHealth system", font=('arial', 15))
        self.lbl_title.pack(fill=tk.X)
        self.lbl_email = tk.Label(self.Form, text = "email:", font=('arial', 14), bd=15)
        self.lbl_email.grid(row=0, sticky="e")
        self.lbl_password = tk.Label(self.Form, text = "Password:", font=('arial', 14), bd=15)
        self.lbl_password.grid(row=1, sticky="e")
        self.lbl_text = tk.Label(self.Form)
        self.lbl_text.grid(row=2, columnspan=2)
        self.lbl_create = tk.Label(self.Form, text = "New user? Create an account.")
        self.lbl_create.grid(row=4, columnspan=2)

        #==============================ENTRY WIDGETS==================================
        self.email = tk.Entry(self.Form, textvariable=self.EMAIL, font=(14))
        self.email.grid(row=0, column=1)
        self.password = tk.Entry(self.Form, textvariable=self.PASSWORD, show="*", font=(14))
        self.password.grid(row=1, column=1)

        #==============================BUTTON WIDGETS=================================
        self.btn_login = tk.Button(self.Form, text="Login", width=45, command=self.Login)
        self.btn_login.grid(pady=25, row=3, columnspan=2)
        self.btn_login.bind('<Return>', self.Login)
        self.btn_create = tk.Button(self.Form, text="Create", width=45, command=self.createAC_Window)
        self.btn_create.grid(pady=25, row=5, columnspan=2)


    #==============================METHODS========================================
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
            
            
    def Login(self, event=None):
        self.connect_to_db()
        user_logged_in = path.dataDir_path('user.pickle', 3)
        entered_passwd = self.PASSWORD.get().strip()
        entered_email = self.EMAIL.get().strip()
        if entered_email == "" or entered_passwd == "":
            self.lbl_text.config(text="Please complete the required field!", fg="red")
        elif os.path.exists(user_logged_in):
            self.lbl_text.config(text="Another user is currently logged in!", fg="red")
            self.EMAIL.set("")
            self.PASSWORD.set("") 
        elif entered_email == "admin":
            cursor.execute("SELECT passwd FROM Admin")
            row = cursor.fetchone()
            print(row[0])
            if row[0] == 'admin':
                user = {'type': 'admin'}
                print(user)
                track.store(user, 3)
                self.admin_passwd()
                self.EMAIL.set("")
                self.PASSWORD.set("")
            elif row[0] != 'admin':
                storedpasswd = row[0]
                if pwdu.verify_password(storedpasswd, entered_passwd):
                    user = {'type': 'admin'}
                    print(user)
                    track.store(user, 3)
                    self.EMAIL.set("")
                    self.PASSWORD.set("") 
                    self.Admin_Window()
                else:
                    self.lbl_text.config(text="Admin entered incorrect password", fg="red")
                    self.EMAIL.set("")
                    self.PASSWORD.set("") 
        elif entered_email != "admin":
            cursor.execute(self.gp_login_query(), (entered_email,))
            gp_login = cursor.fetchone()
            print(gp_login)
            cursor.execute(self.patient_login_query(),(entered_email,))
            patient_login = cursor.fetchone()
            print(patient_login)
            if gp_login is not None and gp_login[4] is None:
                self.lbl_text.config(text="Please create an account", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")
            elif gp_login is not None and gp_login[5] == 'no':
                self.lbl_text.config(text="Your account has been deactivated. Please contact the Admin.", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")
            elif patient_login is not None and patient_login[4] is None:
                self.lbl_text.config(text="Please create an account", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")
            elif patient_login is not None and patient_login[6] == 'no':
                self.lbl_text.config(text="Your account has been deactivated. Please contact the Admin.", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")
            elif gp_login is not None and gp_login[4] is None:
                storedpasswd = gp_login[4]
                if pwdu.verify_password(storedpasswd, entered_passwd):
                    user = {'type': 'gp', 'id': gp_login[0], 'fname': gp_login[1], 'lname': gp_login[2], 'email': gp_login[3]}
                    print(user)
                    track.store(user, 3)
                    self.EMAIL.set("")
                    self.PASSWORD.set("") 
                    self.GP_Window()
                else:
                    self.lbl_text.config(text="GP entered incorrect password", fg="red")
                    self.EMAIL.set("")
                    self.PASSWORD.set("")
            elif patient_login is not None and patient_login[4] is None:
                storedpasswd = patient_login[4]
                if pwdu.verify_password(storedpasswd, entered_passwd):
                    user = {'type': 'patient', 'id': patient_login[0],
                            'fname': patient_login[1], 'lname': patient_login[2],
                            'email': patient_login[3], 'NHSno': patient_login[5]}
                    print(user)
                    track.store(user, 3)
                    self.EMAIL.set("")
                    self.PASSWORD.set("") 
                    self.Patient_Window()
                else:
                    self.lbl_text.config(text="Patient entered incorrect password", fg="red")
                    self.EMAIL.set("")
            else:
                self.lbl_text.config(text="Invalid username or password", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")
        else:
            self.lbl_text.config(text="Error trying to login", fg="red")
            self.EMAIL.set("")
            self.PASSWORD.set("")  
        cursor.close()
        conn.close()
    
    @staticmethod
    def gp_login_query():
        gp_sql = "SELECT gpid, fname, lname, email, passwd, active FROM GPs WHERE email = ?"
        return gp_sql
    
    @staticmethod
    def patient_login_query():
        patient_sql = '''SELECT p.patientid, fname, lname, email, passwd, NHSno, active
                        FROM Patients p, Patient_Record r
                        WHERE p.patientid = r.patientid AND email = ?'''
        return patient_sql
    
    def admin_passwd(self): #open Change Admin Password window(Toplevel)
        global change
        top = tk.Toplevel()
        change = change_admin_passwd.Change_admin_passwd(top)
        top.title("Welcome to the eHealth system")
        change.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
    
    def createAC_Window(self): #open Create account window (Toplevel)
        global create
        top = tk.Toplevel()
        create = create_account.Create_account(top)
        top.title("Welcome to the eHealth system")
        create.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    
    def Admin_Window(self): #open Admin home window (Toplevel)
        open_home.Home.Admin_Window(self)
        
    def GP_Window(self): #open GP home window (Toplevel)
        open_home.Home.GP_Window(self)
        
    def Patient_Window(self): #open Pateint home window (Toplevel)
        open_home.Home.Patient_Window(self)

    def shutdown(self):
        path.delete_from_dataDir('user.pickle', 3) #deleting user.pickle indicates no user is logged in and frees the application for another user to log in
        #if user.pickle file exists (user forgot to log out), it is deleted when application shuts down
        logging.info('Application closed')
        print('Application closed')


def main():
    root = tk.Tk()
    login = Login(root)
    root.title("Welcome to the eHealth system")
    width = 500
    height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    login.bind('<Destroy>', Login.shutdown)
    root.mainloop() #Starts the event loop for the main window
    


if __name__ == '__main__':
    main()
    
    # db_file = connect.db_path(3)
    # conn = connect.create_connection(db_file)
    # cursor = conn.cursor()
    # email1 = 'jane_allen@gmail.com'
    # print(email1)
    # sql1 = Login.gp_login_query()
    # print(sql1)
    # cursor.execute(sql1, (email1,))
    # gp_login = cursor.fetchone()
    # print(gp_login)
    # email2 = 'nhughes@gmail.com'
    # sql2 = Login.patient_login_query(email2)
    #cursor.execute(sql2)
    #patient_login = cursor.fetchone()
    #print(patient_login)
    
    
    # db_file = connect.db_path(3)
    # conn = connect.create_connection(db_file)
    # print(db_file)
    # print(conn)
    # print("sqlite version", sqlite3.sqlite_version)
    # if conn is not None:
    #     print("connected")  
    # conn.close()

    # emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
    # track.store(emp, 3)
    # emp = track.load(emp, 3)
    # print(emp)
    # path.delete_from_dataDir("user.pickle", 3)
    