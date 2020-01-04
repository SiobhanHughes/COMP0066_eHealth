#============================LAUNCH eHealth Application======================

#Used the following tutorial to help make the login feature
#https://www.sourcecodester.com/tutorials/python/11351/python-simple-login-application.html

#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import sqlite3
from sqlite3 import Error

import admin_home

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


#============================Interface for login to open main window======================

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

        #==============================ENTRY WIDGETS==================================
        self.email = tk.Entry(self.Form, textvariable=self.EMAIL, font=(14))
        self.email.grid(row=0, column=1)
        self.password = tk.Entry(self.Form, textvariable=self.PASSWORD, show="*", font=(14))
        self.password.grid(row=1, column=1)

        #==============================BUTTON WIDGETS=================================
        self.btn_login = tk.Button(self.Form, text="Login", width=45, command=self.Login)
        self.btn_login.grid(pady=25, row=3, columnspan=2)
        self.btn_login.bind('<Return>', self.Login)


    #==============================METHODS========================================
    def Database(self):
        global conn, cursor
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, email TEXT, password TEXT)")       
        cursor.execute("SELECT * FROM `member` WHERE `email` = 'admin' AND `password` = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `member` (email, password) VALUES('admin', 'admin')")
            conn.commit()
            
            
    def Login(self, event=None):
        self.Database()
        if self.EMAIL.get() == "" or self.PASSWORD.get() == "":
            self.lbl_text.config(text="Please complete the required field!", fg="red")
        else:
            cursor.execute("SELECT * FROM `member` WHERE `email` = ? AND `password` = ?", (self.EMAIL.get(), self.PASSWORD.get())) #.get will get what user enters in the window
            if cursor.fetchone() is not None:
                self.AdminWindow() #call the next window! This is how you jump around!!
                self.EMAIL.set("")
                self.PASSWORD.set("")
                self.lbl_text.config(text="")
            else:
                self.lbl_text.config(text="Invalid username or password", fg="red")
                self.EMAIL.set("")
                self.PASSWORD.set("")   
        cursor.close()
        conn.close()
        
    
    def AdminWindow(self): #next window
        global Admin
        top = tk.Toplevel()
        Admin = admin_home.MainView(top)
        Admin.pack(side="top", fill="both", expand=True)
        
    
    def HomeWindow(self): #next window
        global Home
        self.master.withdraw()
        Home = tk.Toplevel()
        Home.title("Welcome to the eHealth system")
        width = 600
        height = 500
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.master.resizable(0, 0)
        Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
        lbl_home = tk.Label(Home, text="Successfully Login!", font=('arial', 20)).pack()
        btn_back = tk.Button(Home, text='Back', command=self.Back).pack(pady=20, fill=tk.X)
    
    def Back(self):
        Home.destroy()
        self.master.deiconify()
    
    @staticmethod   
    def shutdown(self):
        print('Application closed')


def main():
    root = tk.Tk()
    login = Login(root)
    root.title("Welcome to the eHealth system")
    width = 400
    height = 280
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    login.bind('<Destroy>', Login.shutdown)
    root.mainloop() #Starts the event loop for the main window
    


if __name__ == '__main__':
    db_file = connect.db_path(3)
    conn = connect.create_connection(db_file)
    print(db_file)
    print(conn)
    print("sqlite version", sqlite3.sqlite_version)
    if conn is not None:
        print("connected")  
    conn.close()

    emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
    track.store(emp, 3)
    emp = track.load(emp, 3)
    print(emp)
    path.delete_from_dataDir("user.pickle", 3)
    
    main()
    