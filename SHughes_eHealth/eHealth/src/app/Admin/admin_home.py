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

import add_user
import edit_user

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
from src.app.GUI import search_results_window
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
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

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
       self.lbl_remind = tk.Label(self.Form, text = "Send 24h appointment reminder email", font=('arial', 14), bd=15, fg='blue')
       self.lbl_remind.grid(row=0, sticky="e")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=2, columnspan=2)
       self.lbl_search = tk.Label(self.Form, text = "SEARCH", font=('arial', 14), bd=15, fg='green')
       self.lbl_search.grid(row=3, sticky="e")
       self.lbl_pfname = tk.Label(self.Form, text = "Patient First Name:", font=('arial', 14), bd=15)
       self.lbl_pfname.grid(row=4, sticky="e")
       self.lbl_plname = tk.Label(self.Form, text = "Patient Last Name:", font=('arial', 14), bd=15)
       self.lbl_plname.grid(row=4, column= 1,sticky="e")
       self.lbl_gpfname = tk.Label(self.Form, text = "GP First Name:", font=('arial', 14), bd=15)
       self.lbl_gpfname.grid(row=7, sticky="e")
       self.lbl_gplname = tk.Label(self.Form, text = "GP Last Name:", font=('arial', 14), bd=15)
       self.lbl_gplname.grid(row=7, column= 1,sticky="e")


                #==============================ENTRY WIDGETS==================================
       self.enter_patient_fname = tk.Entry(self.Form, textvariable=self.patient_fname, font=(14))
       self.enter_patient_fname.grid(row=5)
       self.enter_patient_lname = tk.Entry(self.Form, textvariable=self.patient_lname, font=(14))
       self.enter_patient_lname.grid(row=5, column=1)
       self.enter_gp_fname = tk.Entry(self.Form, textvariable=self.gp_fname, font=(14))
       self.enter_gp_fname.grid(row=8)
       self.enter_gp_lname = tk.Entry(self.Form, textvariable=self.gp_lname, font=(14))
       self.enter_gp_lname.grid(row=8, column=1)

                #==============================BUTTON WIDGETS=================================
       self.btn_email = tk.Button(self.Form, text="email", width=45, command=self.reminder_email, fg='blue')
       self.btn_email.grid(pady=25, row=1, columnspan=2)
       self.btn_search_p = tk.Button(self.Form, text="Search Patients", width=45, command=self.search_patient, fg='green')
       self.btn_search_p.grid(pady=25, row=6, columnspan=2)
       self.btn_search_gp = tk.Button(self.Form, text="Search GPs", width=45, command=self.search_gp, fg='green')
       self.btn_search_gp.grid(pady=25, row=9, columnspan=2)
       self.btn_clear = tk.Button(self.Form, text="Clear all fields", width=45, command=self.clear)
       self.btn_clear.grid(pady=25, row=10, columnspan=2)
       
   def reminder_email(self):  #complete this!!!
       pass
   
   def search_patient(self):
       first = self.patient_fname.get().strip()
       last = self.patient_lname.get().strip()
       titles = ['Patient id','Patient first name', 'Patient last name', 'email', 'DOB', 'NHSno', 'street', 'city', 'postcode', 'tel', 'active' ]
       if first == '' and last == '':
           self.lbl_text.config(text="No Patient name to search!", fg="red")
       else:
        self.connect_to_db()
        if first != '' and last == '':
            p1 = dbu.search_patient_fname(conn, first)
            if p1 != []:
                self.patient_search_result(titles, p1)
                print(p1)
            else:
                self.lbl_text.config(text="Error: No such Patient found", fg="red")
        elif first == '' and last != '':
            p2 = dbu.search_patient_lname(conn, last)
            if p2 != []:
                self.patient_search_result(titles, p2)
            else:
                self.lbl_text.config(text="Error: No such Patient found", fg="red")
        else:
            p3 = dbu.search_patient_fullname(conn, (first, last))
            if p3 != []:
                self.patient_search_result(titles, p3)
            else:
                self.lbl_text.config(text="Error: No such Patient found", fg="red")
        conn.close()

   
   def search_gp(self):
       first = self.gp_fname.get().strip()
       last = self.gp_lname.get().strip()
       titles = ['GP id','GP first name', 'GP last name', 'email', 'street', 'city', 'postcode', 'tel', 'active' ]
       if first == '' and last == '':
           self.lbl_text.config(text="No GP name to search!", fg="red")
       else:
           self.connect_to_db()
       if first != '' and last == '':
           gp1 = dbu.search_gp_fname(conn, first)
           if gp1 != []:
               self.gp_search_result(titles, gp1)
               print(gp1)
           else:
               self.lbl_text.config(text="Error: No such GP found", fg="red")
       elif first == '' and last != '':
           gp2 = dbu.search_gp_lname(conn, last)
           if gp2 != []:
               self.gp_search_result(titles, gp2)
           else:
               self.lbl_text.config(text="Error: No such GP found", fg="red")
       else:
           gp3 = dbu.search_patient_fullname(conn, (first, last))
           if gp3 != []:
               self.patient_search_result(titles, gp3)
           else:
               self.lbl_text.config(text="Error: No such GP found", fg="red")
       conn.close()
   
   def clear(self):
       self.patient_fname.set("")
       self.patient_lname.set("")
       self.gp_fname.set("")
       self.gp_lname.set("")
   
   def patient_search_result(self, titles, patient):
       top = tk.Toplevel()
       search_results_window.Search_results(top, titles, patient)
       top.title("Patient Search Results")
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
       
   def gp_search_result(self, titles, gp):
       top = tk.Toplevel()
       search_results_window.Search_results(top, titles, gp)
       top.title("GP Search Results")
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
        

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
        self.lbl_edit = tk.Label(self.Form, text = "EDIT: enter a Patient or GP id number (use the search function)", font=('arial', 14), bd=15, fg='green')
        self.lbl_edit.grid(row=0, sticky="e")
        self.lbl_text = tk.Label(self.Form) #error messages appear here
        self.lbl_text.grid(row=1, columnspan=2)
        self.lbl_pid = tk.Label(self.Form, text = "Patient id:", font=('arial', 14), bd=15)
        self.lbl_pid.grid(row=2, sticky="w")
        self.lbl_gpid = tk.Label(self.Form, text = "GP id:", font=('arial', 14), bd=15)
        self.lbl_gpid.grid(row=4, sticky="w")


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
        global edit_info_win
        top = tk.Toplevel()
        edit_info_win = outter_scroll_frame.ScrolledFrame(top)
        top.title("Edit Information")
        edit_info_win.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
    
    def delete(self):
        pass
    
    def deactivate(self):
        pass
       

class Add(Admin):
   def __init__(self, *args, **kwargs):
       Admin.__init__(self, *args, **kwargs)

            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)
       
                #==============================LABELS=========================================
       self.lbl_add = tk.Label(self.Form, text = "Add a new Patient or GP to the eHealth system", font=('arial', 14), bd=15)
       self.lbl_add.grid(row=0, sticky="e")
       
                #==============================BUTTON WIDGETS=================================
       self.btn_add_patient = tk.Button(self.Form, text="Add Patient", width=45, command=self.add_patient_info, fg='blue')
       self.btn_add_patient.grid(pady=25, row=1, columnspan=2)
       self.btn_add_gp = tk.Button(self.Form, text="Add GP", width=45, command=self.add_gp_info, fg='green')
       self.btn_add_gp.grid(pady=25, row=2, columnspan=2)
   
   def add_patient_info(self):
       top = tk.Toplevel()
       patient_info = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       
       titles = ['Patient first name', 'Patient last name', 'Patient email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number'
                 'Emergency contact first name', 'Emergency contact last name', 'Emergency contact email', 'Emergency contact -  Address: street'
                 'Emergency contact -  Address: city', 'Emergency contact -  Address: postcode', 'Emergency contact -  Telephone number', 'Emergency contact -  Relationship',
                 'NHS number', 'DOB (YYYY-MM-DD)', 'Drug allgergies', 'Medical Conditions', 'Disabilities', 'Smoker',
                 'Alcohol - Units per week', 'Exercise']
       add_user.Add_info(patient_info.inner, titles) #add entry widgets for details in the list above
        
       top.title("Add a new Patient to the eHealth system")
       patient_info.pack(side="top", fill="both", expand=True)
       width = 800
       height = 700
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))

   
   def add_gp_info(self):
       top = tk.Toplevel()
       gp_info = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       
       titles = ['GP first name', 'GP last name', 'GP email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number']
       add_user.Add_info(gp_info.inner, titles)#add entry widgets for details in the list above
        
       top.title("Add a new GP to the eHealth system")
       gp_info.pack(side="top", fill="both", expand=True)
       width = 800
       height = 700
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))



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
        add_to_system = Add(self)
        edit = Edit(self)
    
        home.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        add_to_system.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        edit.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        btn_home = tk.Button(buttonframe, text="Home", command=home.lift)
        btn_add_to_system = tk.Button(buttonframe, text="Add", command=add_to_system.lift)
        btn_edit = tk.Button(buttonframe, text="Edit", command=edit.lift)
        
        btn_logout = tk.Button(buttonframe, text='logout', command=self.logout, fg='red')

        btn_home.pack(side="left")
        btn_add_to_system.pack(side="left")
        btn_edit.pack(side="left")

        btn_logout.pack(side="right")

        home.show()
        
    
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