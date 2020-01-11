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
from src.app.GP import view_records
from src.app.GP import add_medical
from src.app.GP import add_prescription
from src.app.GP import add_vaccine
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
       self.user = track.load('user.pickle', 3)
       
        #==============================VARIABLES======================================
       self.patient_fname = tk.StringVar()
       self.patient_lname = tk.StringVar()

            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)

                #==============================LABELS=========================================

       self.lbl_search = tk.Label(self.Form, text = "SEARCH", font=('arial', 18), bd=15)
       self.lbl_search.grid(row=0, sticky="e")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=1, columnspan=2)
       self.lbl_pfname = tk.Label(self.Form, text = "Patient First Name:", font=('arial', 14), bd=15)
       self.lbl_pfname.grid(row=2, sticky="e")
       self.lbl_plname = tk.Label(self.Form, text = "Patient Last Name:", font=('arial', 14), bd=15)
       self.lbl_plname.grid(row=2, column= 1,sticky="e")


                #==============================ENTRY WIDGETS==================================
       self.enter_patient_fname = tk.Entry(self.Form, textvariable=self.patient_fname, font=(14))
       self.enter_patient_fname.grid(row=3)
       self.enter_patient_lname = tk.Entry(self.Form, textvariable=self.patient_lname, font=(14))
       self.enter_patient_lname.grid(row=3, column=1)

                #==============================BUTTON WIDGETS=================================
       self.btn_search_p = tk.Button(self.Form, text="Search Patients", width=45, command=self.search_patient, fg='green')
       self.btn_search_p.grid(pady=25, row=4, columnspan=2)
       self.btn_clear = tk.Button(self.Form, text="Clear", width=45, command=self.clear)
       self.btn_clear.grid(pady=25, row=5, columnspan=2)
       
   
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


   
   def clear(self):
       self.patient_fname.set("")
       self.patient_lname.set("")

   
   def patient_search_result(self, titles, patient):
       top = tk.Toplevel()
       patient_win = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       patient_info = search_results_window.Search_results(patient_win.inner, titles, patient)
       top.title("Patient Search Results")
       patient_win.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 400
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))

        


class Appointments(GP):
   def __init__(self, *args, **kwargs):
       GP.__init__(self, *args, **kwargs)
       self.user = track.load('user.pickle', 3)
       
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
       self.user = track.load('user.pickle', 3)
       
        #==============================VARIABLES======================================
       self.patient_id = tk.StringVar()
            
            #==============================FRAMES=========================================
       self.Form = tk.Frame(self, height=200)
       self.Form.pack(side=tk.TOP, pady=20)   
           #==============================LABELS=========================================
       self.lbl_enter = tk.Label(self.Form, text = "Enter a Patient id number (use the search function)", font=('arial', 18), bd=15)
       self.lbl_enter.grid(row=0, sticky="e")
       self.lbl_text = tk.Label(self.Form) #error messages appear here
       self.lbl_text.grid(row=1, columnspan=2)
       self.lbl_pid = tk.Label(self.Form, text = "Patient id:", font=('arial', 14), bd=15)
       self.lbl_pid.grid(row=2, sticky="w") 
                #==============================ENTRY WIDGETS==================================
       self.patient_id = tk.Entry(self.Form, textvariable=self.patient_id, font=(14))
       self.patient_id.grid(row=3)
  
                #==============================BUTTON WIDGETS=================================
       self.btn_view = tk.Button(self.Form, text="View Patient Records", width=45, command=self.view, fg='green')
       self.btn_view.grid(pady=25, row=4, columnspan=2)
       self.btn_edit = tk.Button(self.Form, text="Edit Patient info", width=45, command=self.edit)
       self.btn_edit.grid(pady=25, row=5, columnspan=2)
       self.btn_medical = tk.Button(self.Form, text="Add Medical Record", width=45, command=self.medical, fg='blue')
       self.btn_medical.grid(pady=25, row=6, columnspan=2)
       self.btn_presciption = tk.Button(self.Form, text="Add Prescription", width=45, command=self.prescription, fg='blue')
       self.btn_presciption.grid(pady=25, row=7, columnspan=2)  
       self.btn_vaccine = tk.Button(self.Form, text="Add Vaccine Record", width=45, command=self.vaccine, fg='blue')
       self.btn_vaccine.grid(pady=25, row=8, columnspan=2)  
   
   def get_input(self):
       type_id = []
       pid = self.patient_id.get().strip()
       
       if pid == '':
           self.lbl_text.config(text="Please enter a Patient id number", fg="red")
       else:
           type_id = self.get_id('Patient', pid)
       return type_id
       
   
   def get_id(self, user_type, user_id):
       type_id = [user_type]
       self.connect_to_db()
       try:
           user_id = int(user_id)
       except ValueError:
           self.lbl_text.config(text="Error: Please enter a number", fg="red")
       else:
           if user_type == 'Patient':
               cursor.execute('SELECT * from Patients WHERE patientid = ?', (user_id,))
               patient = cursor.fetchall()
               if patient == []:
                   self.lbl_text.config(text="Error: Patient does not exist - check id number", fg="red")
               else:
                   type_id.append(user_id)
       return type_id
   
   def view(self):
      patient_details = self.get_input()
      if len(patient_details) == 2:
        #open multiple windows!! Patient info, medical record, presciption, vaccine
        self.view_info(patient_details)
        self.view_medical(patient_details[1])
        self.view_vaccine(patient_details[1])
        self.view_prescriptions(patient_details[1])
      else:
        self.lbl_text.config(text="Error getting patient information", fg="red") #maybe remove this....
        
   def view_medical(self, patient_id_num):
       top = tk.Toplevel()
       view_medical = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       get_info = view_records.Patient_records(view_medical.inner, patient_id=patient_id_num) #add entry widgets for details in the list above
       top.title("Patient Medical History")
       view_medical.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 700
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))

   
   def view_vaccine(self, patient_id_num):
       top = tk.Toplevel()
       view_vaccine = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       get_info = view_records.Patient_records(view_vaccine.inner, patient_id=patient_id_num, record_type='vaccine') #add entry widgets for details in the list above
       top.title("Patient Vaccine Record")
       view_vaccine.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 700
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))
   
   def view_prescriptions(self, patient_id_num):
       top = tk.Toplevel()
       view_prescription = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
       get_info = view_records.Patient_records(view_prescription.inner, patient_id=patient_id_num, record_type='prescription') #add entry widgets for details in the list above
       top.title("Patient Presciptions")
       view_prescription.pack(side="top", fill="both", expand=True)
       width = 1100
       height = 700
       screen_width = self.master.winfo_screenwidth()
       screen_height = self.master.winfo_screenheight()
       x = (screen_width/2) - (width/2)
       y = (screen_height/2) - (height/2)
       top.geometry("%dx%d+%d+%d" % (width, height, x, y))


        
    
   def view_info(self, patient_details):
        top = tk.Toplevel()
        view_info = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
        get_info = user_info.Info_form(view_info.inner, user_type=patient_details[0], user_id=patient_details[1], mode='view') #add entry widgets for details in the list above
    
        if patient_details[0] == 'Patient':
            top.title("View Patient information")
    
        view_info.pack(side="top", fill="both", expand=True)
        width = 1100
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
        cursor.close()
        conn.close()
   
   def edit(self):
      patient_details = self.get_input()
      if len(patient_details) == 2:
          top = tk.Toplevel()
          edit_info = outter_scroll_frame.ScrolledFrame(top) #open window that can scroll
          get_info = user_info.Info_form(edit_info.inner, user_type=patient_details[0], user_id=patient_details[1], mode='edit') #add entry widgets for details in the list above
          
          if patient_details[0] == 'Patient':
              top.title("Edit Patient information")
          
          edit_info.pack(side="top", fill="both", expand=True)
          width = 1100
          height = 700
          screen_width = self.master.winfo_screenwidth()
          screen_height = self.master.winfo_screenheight()
          x = (screen_width/2) - (width/2)
          y = (screen_height/2) - (height/2)
          top.geometry("%dx%d+%d+%d" % (width, height, x, y))
          cursor.close()
          conn.close()
 
   
   def medical(self):
       patient_details = self.get_input()
       if len(patient_details) == 2:
           top = tk.Toplevel()
           add_medical_history = add_medical.Add_medical(top, patient_details[1])
           top.title("Add Patient Medical History")
           width = 500
           height = 600
           screen_width = self.master.winfo_screenwidth()
           screen_height = self.master.winfo_screenheight()
           x = (screen_width/2) - (width/2)
           y = (screen_height/2) - (height/2)
           top.geometry("%dx%d+%d+%d" % (width, height, x, y))

   
   def prescription(self):
       patient_details = self.get_input()
       if len(patient_details) == 2:
           top = tk.Toplevel()
           add_script = add_prescription.Add_prescription(top, patient_details[1])
           top.title("Add Prescription")
           width = 500
           height = 600
           screen_width = self.master.winfo_screenwidth()
           screen_height = self.master.winfo_screenheight()
           x = (screen_width/2) - (width/2)
           y = (screen_height/2) - (height/2)
           top.geometry("%dx%d+%d+%d" % (width, height, x, y))

   
   def vaccine(self):
       patient_details = self.get_input()
       if len(patient_details) == 2:
           top = tk.Toplevel()
           add_vaccine_record = add_vaccine.Add_vaccine(top, patient_details[1])
           top.title("Add Vaccine Record")
           width = 500
           height = 600
           screen_width = self.master.winfo_screenwidth()
           screen_height = self.master.winfo_screenheight()
           x = (screen_width/2) - (width/2)
           y = (screen_height/2) - (height/2)
           top.geometry("%dx%d+%d+%d" % (width, height, x, y))
   
 
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