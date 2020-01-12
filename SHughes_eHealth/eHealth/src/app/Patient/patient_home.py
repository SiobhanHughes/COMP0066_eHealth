#template for tkinter home page taken from:
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

#============================IMPORT============================================

import tkinter as tk
from tkinter import scrolledtext

import os
import sys
import inspect

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
from src.app.GUI import view_records
path.delete_dir()



#============================PATIENT HOME interface======================

class Patient(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    
    def show(self):
        self.lift()
        
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

class Cancel(Patient):
   def __init__(self, *args, **kwargs):
       Patient.__init__(self, *args, **kwargs)
       self.user = track.load('user.pickle', 3)


            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)

                #==============================LABELS=========================================
       self.lbl_dates_title = tk.Label(self.Form, text = "View Your Appointments", font=('arial', 18), bd=15)
       self.lbl_dates_title.grid(row=0, sticky="w")
       self.lbl_dates_format = tk.Label(self.Form, text = "To cancel an appointment, click the numbered button next to that appointment", font=('arial', 14), bd=15)
       self.lbl_dates_format.grid(row=1, sticky="w")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=2, columnspan=2)

                #==============================BUTTON WIDGETS=================================
       self.btn_view = tk.Button(self.Form, text="View/Cancel", width=45, command=self.view, fg='blue')
       self.btn_view.grid(pady=25, row=3, columnspan=2)


   def view(self):
       titles = ['Appointment date', 'Appointment time', 'GP first name', 'GP last name', 'Cancel']
       self.connect_to_db()
       pid = self.user['patientid']
       sql = '''SELECT date(date_time), time(date_time), g.fname, g.lname, appointmentid
                FROM Appointments a, GPs g WHERE a.gpid = g.gpid AND available = 'no' AND patientid = ?'''
       cursor.execute(sql, (pid,))
       rows = cursor.fetchall()
       if rows != []:
            self.apppointment_search_result(titles, rows)
       elif rows == []:
            self.lbl_text.config(text="You do not have any appointments booked", fg="red")
       cursor.close()
       conn.close()

       
   def apppointment_search_result(self, titles, rows):
       top = tk.Toplevel()
       appoint_win = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       info = search_results_window.Search_results(appoint_win.inner, titles, rows)
       top.title("You Appointments")
       appoint_win.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
               



class Book(Patient):
   def __init__(self, *args, **kwargs):
       Patient.__init__(self, *args, **kwargs)
       self.user = track.load('user.pickle', 3)
       
        #==============================VARIABLES======================================
       self.date_range = tk.StringVar()

            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)

                #==============================LABELS=========================================
       self.lbl_dates_title = tk.Label(self.Form, text = "Enter a range of dates to book an appointment:", font=('arial', 18), bd=15)
       self.lbl_dates_title.grid(row=0, sticky="w")
       self.lbl_dates_format = tk.Label(self.Form, text = "Format: YYYY-MM-DD,YYYY-MM-DD (Dates separated by comma)", font=('arial', 14), bd=15)
       self.lbl_dates_format.grid(row=1, sticky="w")
       self.lbl_dates_format2 = tk.Label(self.Form, text = "For one day, use the same start and end date", font=('arial', 12), bd=15)
       self.lbl_dates_format2.grid(row=2, sticky="w")
       self.lbl_dates_format2 = tk.Label(self.Form, text = "A new window will open for each date you enter if appointments are available", font=('arial', 12), bd=15)
       self.lbl_dates_format2.grid(row=3, sticky="w")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=4, columnspan=2)

                #==============================ENTRY WIDGETS==================================
       self.enter_dates = tk.Entry(self.Form, textvariable=self.date_range, font=(14))
       self.enter_dates.grid(row=5)

                #==============================BUTTON WIDGETS=================================
       self.btn_view = tk.Button(self.Form, text="Book an appointment", width=45, command=self.enter, fg='blue')
       self.btn_view.grid(pady=25, row=6, columnspan=2)
       


   def enter(self):
       dates_entered = self.date_range.get().strip()
       self.connect_to_db()
       if check.check_dates_format(dates_entered) == 'error':
            self.lbl_text.config(text="Error: dates not correctly formatted", fg="red")
       else:
           start, end = check.check_dates_format(dates_entered)
           if start < dt.date.today():
               self.lbl_text.config(text="Error: date has past", fg="red")
           else:
               self.lbl_text.config(text=" ")
               date_range = check.gen_dates(start, end)
               titles = ['Appointment date', 'Appointment time', 'GP first name', 'GP last name', 'Book']
               now = dt.datetime.now() + dt.timedelta(hours=2)
               print(now)
               sql = '''SELECT date(date_time), time(date_time), g.fname, g.lname, appointmentid
                    FROM Appointments a, GPs g WHERE a.gpid = g.gpid AND available = 'yes' AND date_time > ? AND date(date_time) = ?'''
               for d in date_range:
                   cursor.execute(sql, (now, d))
                   rows = cursor.fetchall()
                   if rows == []:
                       self.lbl_text.config(text="No appointments available for some or all of your chosen dates", fg="red")
                   else:
                       self.book(titles, rows)
               cursor.close()
               conn.close()

                       
   def book(self, titles, rows):
       top = tk.Toplevel()
       appoint_book = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       info = search_results_window.Search_results(appoint_book.inner, titles, rows, pid=self.user['patientid'])
       top.title("Book an appointment")
       appoint_book.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
               




class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        lbl_title = tk.Label(self, text = "Patient: eHealth system", font=('arial', 15))
        lbl_title.pack(fill=tk.X)
        c = Cancel(self)
        b = Book(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        c.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        b.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        btn_c = tk.Button(buttonframe, text="View/Cancel Appointment", command=c.lift)
        btn_b = tk.Button(buttonframe, text="Book Appointment", command=b.lift)
        btn_logout = tk.Button(buttonframe, text='logout', command=self.logout)

        btn_c.pack(side="left")
        btn_b.pack(side="left")
        btn_logout.pack(side="right")

        c.show()
        
    
    
    def logout(self):
        print('Patient logged out. Widgets destroyed')
        path.delete_from_dataDir('user.pickle', 3) #deleting user.pickle indicates no user is logged in and frees the application for another user to log in
        self.destroy()

def close(*args):
    print('Patient logged out. Window closed')

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Welcome to the eHealth system")
    root.wm_geometry("900x900")
    main.bind('<Destroy>', close)
    root.mainloop()