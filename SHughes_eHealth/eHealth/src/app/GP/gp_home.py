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

import datetime as dt
import re

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
from src.utilities import check_input as check
from src.app.GUI import outter_scroll_frame
from src.app.GUI import search_results_window
from src.app.GUI import user_info
from src.app.GP import add_availability
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
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

class Search(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is GP 1")
       label.pack(side="top", fill="both", expand=True)

class Appointments(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       self.user = track.load('user.pickle', 3)
       print(self.user)
       
        #==============================VARIABLES======================================
       self.date_range = tk.StringVar()

            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)

                #==============================LABELS=========================================
       self.lbl_dates_title = tk.Label(self.Form, text = "Enter a range of dates:", font=('arial', 18), bd=15)
       self.lbl_dates_title.grid(row=0, sticky="w")
       self.lbl_dates_format = tk.Label(self.Form, text = "Format: YYYY-MM-DD,YYYY-MM-DD (Dates separated by comma)", font=('arial', 14), bd=15)
       self.lbl_dates_format.grid(row=1, sticky="w")
       self.lbl_dates_format2 = tk.Label(self.Form, text = "For one day, use the same start and end date", font=('arial', 12), bd=15)
       self.lbl_dates_format2.grid(row=2, sticky="w")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=3, columnspan=2)

                #==============================ENTRY WIDGETS==================================
       self.enter_dates = tk.Entry(self.Form, textvariable=self.date_range, font=(14))
       self.enter_dates.grid(row=5)

                #==============================BUTTON WIDGETS=================================
       self.btn_view = tk.Button(self.Form, text="View", width=45, command=self.view, fg='blue')
       self.btn_view.grid(pady=25, row=6, columnspan=2)
       self.btn_enter = tk.Button(self.Form, text="Enter Appointment times", width=45, command=self.enter, fg='green')
       self.btn_enter.grid(pady=25, row=7, columnspan=2)

   def view(self):
       dates_entered = self.date_range.get().strip()
       self.connect_to_db()
       if check.check_dates_format(dates_entered) == 'error':
            self.lbl_text.config(text="Error: dates not correctly formatted", fg="red")
       else:
           start, end = check.check_dates_format(dates_entered)
           date_range = check.gen_dates(start, end)
           gpid = self.user['gpid']
           titles = ['Appointment date', 'Appointment time', 'Patient first name', 'Patient last name', 'Appointment Available']
           sql = '''SELECT date(date_time), time(date_time), fname, lname, available
                FROM Appointments a LEFT JOIN Patients p ON a.patientid = p.patientid WHERE date(date_time) = ? AND gpid = ?'''
           for d in date_range:
                info = (d, gpid)
                cursor.execute(sql, info)
                rows = cursor.fetchall()
                if rows != []:
                    self.apppointment_search_result(titles, rows)
                elif rows == []:
                    self.lbl_text.config(text="No Appointments for one or all of the entered dates", fg="red")
       cursor.close()
       conn.close()


   def enter(self):
       dates_entered = self.date_range.get().strip()
       self.connect_to_db()
       if check.check_dates_format(dates_entered) == 'error':
            self.lbl_text.config(text="Error: dates not correctly formatted", fg="red")
       else:
           start, end = check.check_dates_format(dates_entered)
           if start <= dt.date.today():
               self.lbl_text.config(text="Error: to add appointments you need to enter a date in the furture", fg="red")
           else:
               date_range = check.gen_dates(start, end)
               for d in date_range:
                   cursor.execute('SELECT date(date_time) FROM Appointments WHERE date(date_time) = ?', (d,))
                   row = cursor.fetchall()
                   if row != []:
                       self.lbl_text.config(text="Error: You already added availability for some of these dates", fg="red")
                       break
               else:
                   self.lbl_text.config(text=" ")
                   self.add_availability(date_range)
       cursor.close()
       conn.close()

                       
   def add_availability(self, date_range):
       top = tk.Toplevel()
       add_times = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       available = add_availability.Add_time(add_times.inner, date_range)
       top.title("Add available times for appointments")
       add_times.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
       
   def apppointment_search_result(self, titles, rows):
       top = tk.Toplevel()
       appoint_win = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       info = search_results_window.Search_results(appoint_win.inner, titles, rows)
       top.title("Appointments")
       appoint_win.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
               

class Patient_Record(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is GP 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        lbl_title = tk.Label(self, text = "GP: eHealth system", font=('arial', 15))
        lbl_title.pack(fill=tk.X)
        search = Search(self)
        appointments = Appointments(self)
        patient = Patient_Record(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        search.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        appointments.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        patient.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        search_btn = tk.Button(buttonframe, text="Search", command=search.lift)
        appointments_btn = tk.Button(buttonframe, text="Appointments", command=appointments.lift)
        patient_btn = tk.Button(buttonframe, text="Patient Records", command=patient.lift)
        btn_logout = tk.Button(buttonframe, text='logout', command=self.logout)

        search_btn.pack(side="left")
        appointments_btn.pack(side="left")
        patient_btn.pack(side="left")
        btn_logout.pack(side="right")

        search.show()
    
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
    root.wm_geometry("900x900")
    main.bind('<Destroy>', close)
    root.mainloop()