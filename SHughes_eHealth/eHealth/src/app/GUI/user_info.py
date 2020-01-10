#Help with loop to create multiple widgets
#https://stackoverflow.com/questions/22916622/how-to-store-values-from-an-entry-widget-for-loop-in-tkinter


import tkinter as tk

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
path.delete_dir()

class Info_form:
    """ Generate form (inner widgets for scrollable window/frame - see outter_scroll_frame.py) 
        for adding, viewing or editing a GP or Patient.
        Add info: Admin can enter all detales in the required fields and save the information to the database
        View info: Admin can view patient for GP info. GP can view patient info
        Edit info: Admin can edit patient for GP info."""
    
    def __init__(self, parent, user_type=None, mode='add', user_id=None, *args, **kwargs):
        self.parent = parent
        self.user_type = user_type
        self.mode = mode
        self.user_id = user_id
        self.titles = self.create_titles()
        
        if self.user_id is not None:
            self.details = self.get_info()
        else:
            self.details = []

        self.create_widgets()
    
    def create_titles(self):
        if self.user_type == 'GP':
            titles = ['GP first name', 'GP last name', 'email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number']
        elif self.user_type == 'Patient':
            titles = ['Patient first name', 'Patient last name', 'email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number',
                 'Emergency contact first name', 'Emergency contact last name', 'Emergency contact email', 'Emergency contact -  Address: street',
                 'Emergency contact -  Address: city', 'Emergency contact -  Address: postcode', 'Emergency contact -  Telephone number', 'Emergency contact -  Relationship',
                 'NHS number', 'DOB (YYYY-MM-DD)', 'Drug allgergies', 'Medical Conditions', 'Disabilities', 'Smoker',
                 'Alcohol - Units per week', 'Exercise']
        return titles
    
    def get_info(self):
        self.connect_to_db()
        if self.user_type == 'GP':
            info = dbu.search_gp_id(conn, self.user_id)
        elif self.user_type == 'Patient':
            info = dbu.search_patient_id(conn, self.user_id)
        conn.close()
        return info
    
    def create_widgets(self):
        self.entries = []
        for i in range(len(self.titles)):
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
    
            self.label = tk.Label(self.labelframe, text=self.titles[i])
            self.label.grid(row=0)
            if self.mode == 'add':
                self.entry = tk.Entry(self.labelframe)
                self.entry.grid(row=1)
                self.entries.append(self.entry)
            elif self.mode == 'edit':
                self.entry = tk.Entry(self.labelframe)
                if self.titles[i] == 'email':
                    self.show_email = tk.Label(self.labelframe, text=self.details[i]) #can not edit email as this is used to login
                    self.show_email.grid(row=1)
                elif self.titles[i] == 'NHS number':
                    self.show_num = tk.Label(self.labelframe, text=self.details[i]) #can not edit email as this is used to login
                    self.show_num.grid(row=1)
                else:
                    self.entry.insert(0, self.details[i])
                    self.entry.grid(row=1)
                    self.entries.append(self.entry)
            elif self.mode == 'view':
                self.show_details = tk.Label(self.labelframe, text=self.details[i])
                self.show_details.grid(row=1)
                
                

        if self.mode == 'add' or self.mode == 'edit':
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
            self.label = tk.Label(self.labelframe)
            self.label.pack(expand=True, fill='both')
            self.label = tk.Label(self.labelframe, text='Save all details', fg='blue')
            self.label.pack(expand=True, fill='both')
            self.lbl_text = tk.Label(self.labelframe) #error messages appear here
            self.lbl_text.pack(expand=True, fill='both')
            self.button = tk.Button(self.labelframe, text="Save", command=self.get_input, fg='blue')
            self.button.pack()

    def get_input(self):
        entered = []
        for entry in self.entries:
            val = entry.get().strip()
            if val != '':
                entered.append(val)
        #call tests
        if self.mode == 'add' and self.user_type == 'GP':
            if len(entered) != len(self.titles):
                self.lbl_text.config(text="Some data is missing", fg="red")
            else:
                self.check_gp(entered)
        elif self.mode == 'edit' and self.user_type == 'GP':
            if (len(entered) + 1) != len(self.titles):
                self.lbl_text.config(text="Some data is missing", fg="red")
            else:
                self.check_gp(entered)
        if self.mode == 'add' and self.user_type == 'Patient':
            if len(entered) != len(self.titles):
                self.lbl_text.config(text="Some data is missing", fg="red")
            else:
                self.check_patient(entered)
        elif self.mode == 'edit' and self.user_type == 'Patient':
            if (len(entered) + 2) != len(self.titles):
                self.lbl_text.config(text="Some data is missing", fg="red")
            else:
                self.check_patient(entered)

    
    def check_gp(self, entered):
        self.connect_to_db()
        if self.mode == 'add':
            email = entered[2]
            if check.email_format(email) == 'not correct':
                self.lbl_text.config(text="Email is not correctly formatted", fg="red")
            elif check.email_unique(cursor, self.user_type, email) == 'exists':
                    self.lbl_text.config(text="Email is not unique", fg="red")
            elif check.tel_format(entered[6]) != 'tel':
                self.lbl_text.config(text="Error entering telephone number", fg="red")
            else:
                entered.append(dt.date.today())
                gp = tuple(entered)
                dbu.insert_gp(conn, gp)
                self.save()
        elif self.mode == 'edit':
            if check.tel_format(entered[5]) != 'tel':
                self.lbl_text.config(text="Error entering telephone number", fg="red")
            else:
                entered.append(self.user_id)
                gp = tuple(entered)
                print(gp)
                dbu.update_gp(conn, gp)
                self.save()
        cursor.close()
        conn.close()
        
    def check_patient(self, entered):
        self.connect_to_db()
        if self.mode == 'add':
            email = entered[2]
            if check.email_format(email) == 'not correct':
                self.lbl_text.config(text="Email is not correctly formatted", fg="red")
            elif check.email_unique(cursor, self.user_type, email) == 'exists':
                    self.lbl_text.config(text="Email is not unique", fg="red")
            elif check.tel_format(entered[6]) != 'tel':
                self.lbl_text.config(text="Error entering telephone number", fg="red")
            elif check.email_format(entered[9]) == 'not correct':
                self.lbl_text.config(text="Emergency contact email is not correctly formatted", fg="red")
            elif check.tel_format(entered[13]) != 'tel':
                self.lbl_text.config(text="Error entering emergency contact telephone number", fg="red")
            elif check.NHSno_unique(cursor, entered[15]) == 'exists':
                self.lbl_text.config(text="Error: NHS number is not unique", fg="red")
            elif check.check_dob(entered[16]) == 'error':
                self.lbl_text.config(text="Error: DOB not correctly formattted", fg="red")
            else:
                date_birth = check.check_dob(entered[16])
                begin = dt.date.today()
                patient = (entered[0], entered[1], entered[2], entered[3], entered[4], entered[5], entered[6], begin,
                           entered[7], entered[8], entered[9], entered[10], entered[11], entered[12], entered[13], entered[14])
                patient_id = dbu.insert_patient(conn, patient)
                patient_record = (entered[15], patient_id, date_birth, entered[17], entered[18], entered[19],
                                  entered[20], entered[21], entered[22])
                dbu.insert_patient_record(conn, patient_record)
                self.save()
        elif self.mode == 'edit':
            if check.tel_format(entered[5]) != 'tel':
                self.lbl_text.config(text="Error entering telephone number", fg="red")
            elif check.email_format(entered[8]) == 'not correct':
                self.lbl_text.config(text="Emergency contact email is not correctly formatted", fg="red")
            elif check.tel_format(entered[12]) != 'tel':
                self.lbl_text.config(text="Error entering emergency contact telephone number", fg="red")
            elif check.check_dob(entered[14]) == 'error':
                self.lbl_text.config(text="Error: DOB not correctly formattted", fg="red")
            else:
                date_birth = check.check_dob(entered[14])
                patient = (entered[0], entered[1], entered[2], entered[3], entered[4], entered[5], entered[6],
                              entered[7], entered[8], entered[9], entered[10], entered[11], entered[12], entered[13], self.user_id)
                dbu.update_patient(conn, patient)
                patient_record = (date_birth, entered[15], entered[16], entered[17], entered[18], entered[19], entered[20], self.user_id)
                dbu.update_patient_record(conn, patient_record)
                self.save()
        cursor.close()
        conn.close()
                
            
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

    
    def save(self):
        #send automatic email to GP or Patient
        for widget in self.labelframe.winfo_children():
            widget.destroy()
    
        
if __name__ == '__main__':
    root = tk.Tk()

    Info_form(root, user_type='Patient', mode='edit', user_id=1)
    root.mainloop()
    
    