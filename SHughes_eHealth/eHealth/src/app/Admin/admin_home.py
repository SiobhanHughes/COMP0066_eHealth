#template for tkinter home page taken from:
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

#============================IMPORT============================================

import tkinter as tk
from tkinter import ttk

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
from src.app.GUI import outter_scroll_frame
path.delete_dir()


#============================ADMIN HOME interface======================

log_file = path.dataDir_path('eHealth_output.log', 3)
logging.basicConfig(level=logging.DEBUG,
                    filename=log_file,
                    filemode ='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')


class Admin(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Homepage(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       
        #==============================VARIABLES======================================
       self.patient_fname = tk.StringVar()
       self.patient_lname = tk.StringVar()
       self.gp_fname = tk.StringVar()
       self.gp_lname = tk.StringVar()

            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)

                #==============================LABELS=========================================
       self.lbl_email = tk.Label(self.Form, text = "Send 24h appointment reminder email", font=('arial', 14), bd=15, fg='blue')
       self.lbl_email.grid(row=0, sticky="e")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=2, columnspan=2)
       self.lbl_password = tk.Label(self.Form, text = "SEARCH", font=('arial', 14), bd=15, fg='green')
       self.lbl_password.grid(row=3, sticky="e")
       self.lbl_password = tk.Label(self.Form, text = "Patient First Name:", font=('arial', 14), bd=15)
       self.lbl_password.grid(row=4, sticky="e")
       self.lbl_password = tk.Label(self.Form, text = "Patient Last Name:", font=('arial', 14), bd=15)
       self.lbl_password.grid(row=4, column= 1,sticky="e")
       self.lbl_password = tk.Label(self.Form, text = "GP First Name:", font=('arial', 14), bd=15)
       self.lbl_password.grid(row=6, sticky="e")
       self.lbl_password = tk.Label(self.Form, text = "GP Last Name:", font=('arial', 14), bd=15)
       self.lbl_password.grid(row=6, column= 1,sticky="e")


                #==============================ENTRY WIDGETS==================================
       self.patient_fname = tk.Entry(self.Form, textvariable=self.patient_fname, font=(14))
       self.patient_fname.grid(row=5)
       self.patient_lname = tk.Entry(self.Form, textvariable=self.patient_lname, font=(14))
       self.patient_lname.grid(row=5, column=1)
       self.gp_fname = tk.Entry(self.Form, textvariable=self.gp_fname, font=(14))
       self.gp_fname.grid(row=7)
       self.gp_lname = tk.Entry(self.Form, textvariable=self.gp_lname, font=(14))
       self.gp_lname.grid(row=7, column=1)

                #==============================BUTTON WIDGETS=================================
       self.btn_email = tk.Button(self.Form, text="email", width=45, command=self.reminder_email, fg='blue')
       self.btn_email.grid(pady=25, row=1, columnspan=2)
       self.btn_search = tk.Button(self.Form, text="Search", width=45, command=self.search, fg='green')
       self.btn_search.grid(pady=25, row=8, columnspan=2)
       self.btn_clear = tk.Button(self.Form, text="Clear all fields", width=45, command=self.search, fg='green')
       self.btn_clear.grid(pady=25, row=9, columnspan=2)
       
   def reminder_email(self):
       pass
   
   def search(self):
       pass
   
   def clear(self):
       pass

class Edit(Admin):
    def __init__(self, *args, **kwargs):
        Admin.__init__(self, *args, **kwargs)
       
         #==============================VARIABLES======================================
        self.patient_id = tk.StringVar()
        self.gp_id = tk.StringVar()
             
             #==============================FRAMES=========================================
        self.Form = tk.Frame(self, height=200)
        self.Form.pack(side=tk.TOP, pady=20)

                 #==============================LABELS=========================================
        self.lbl_password = tk.Label(self.Form, text = "EDIT: enter a Patient or GP id number (use the search function)", font=('arial', 14), bd=15, fg='green')
        self.lbl_password.grid(row=0, sticky="e")
        self.lbl_text = tk.Label(self.Form) #error messages appear here
        self.lbl_text.grid(row=1, columnspan=2)
        self.lbl_password = tk.Label(self.Form, text = "Patient id:", font=('arial', 14), bd=15)
        self.lbl_password.grid(row=2, sticky="w")
        self.lbl_password = tk.Label(self.Form, text = "GP id:", font=('arial', 14), bd=15)
        self.lbl_password.grid(row=4, sticky="w")


                 #==============================ENTRY WIDGETS==================================
        self.patient_id = tk.Entry(self.Form, textvariable=self.patient_id, font=(14))
        self.patient_id.grid(row=3)
        self.gp_id = tk.Entry(self.Form, textvariable=self.gp_id, font=(14))
        self.gp_id.grid(row=5)

                 #==============================BUTTON WIDGETS=================================
        self.btn_edit = tk.Button(self.Form, text="Edit", width=45, command=self.edit, fg='green')
        self.btn_edit.grid(pady=25, row=6, columnspan=2)
        self.btn_delete = tk.Button(self.Form, text="Delete", width=45, command=self.delete, fg='red')
        self.btn_delete.grid(pady=25, row=7, columnspan=2)
        self.btn_deactivate = tk.Button(self.Form, text="Deactivate", width=45, command=self.deactivate, fg='blue')
        self.btn_deactivate.grid(pady=25, row=8, columnspan=2)

    
    def edit(self):
        pass
    
    def delete(self):
        pass
    
    def deactivate(self):
        pass
       

class Register_Patient(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       scroll_win = outter_scroll_frame.ScrolledFrame(self)
       label = tk.Label(self, text="This is Admin 2")
       label.pack(side="top", fill="both", expand=True)

class Add_GP(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is Admin 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        Top = tk.Frame(bd=2,  relief=tk.RIDGE)
        Top.pack(side=tk.TOP, fill=tk.X)
        lbl_title = tk.Label(Top, text = "Admin: eHealth", font=('arial', 15))
        lbl_title.pack(fill=tk.X)
        
        buttonframe = tk.Frame(self, Top)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        home = Homepage(self)
        edit = Edit(self)
        new_patient = Register_Patient(self)
        new_gp = Add_GP(self)
    
        home.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        edit.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        new_patient.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        new_gp.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        btn_home = tk.Button(buttonframe, text="Home", command=home.lift)
        btn_edit = tk.Button(buttonframe, text="Edit", command=edit.lift)
        btn_patient = tk.Button(buttonframe, text="Register Patient", command=new_patient.lift)
        btn_gp = tk.Button(buttonframe, text="Add GP", command=new_gp.lift)
        
        btn_logout = tk.Button(buttonframe, text='logout', command=self.logout, fg='red')

        btn_home.pack(side="left")
        btn_edit.pack(side="left")
        btn_patient.pack(side="left")
        btn_gp.pack(side="left")

        btn_logout.pack(side="right")

        home.show()
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
    
    def logout(self):
        print('Admin logged out. Widgets destroyed')
        logging.info('Admin logged out. Widgets destroyed')
        path.delete_from_dataDir('user.pickle', 3) #deleting user.pickle indicates no user is logged in and frees the application for another user to log in
        logging.info('user.pickle deleted - new user can log in')
        self.destroy()

def close(*args):
    print('Admin logged out. Window closed')

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("900x900")
    main.bind('<Destroy>', close)
    root.mainloop()