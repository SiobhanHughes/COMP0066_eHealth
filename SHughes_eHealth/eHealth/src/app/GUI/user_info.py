#Help with loop to create multiple widgets
#https://stackoverflow.com/questions/22916622/how-to-store-values-from-an-entry-widget-for-loop-in-tkinter


import tkinter as tk

import os
import sys
import inspect

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
        self.titles = self.create_titles(self.user_type)
        
        if self.user_id is not None:
            details = self.get_info(self.user_type, self.user_id)
        else:
            details = []

        
        self.create_widgets(self.titles, self.mode, details)
    
    def create_titles(self, user_type):
        if user_type == 'GP':
            titles = ['GP first name', 'GP last name', 'GP email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number']
        elif user_type == 'Patient':
            titles = ['Patient first name', 'Patient last name', 'Patient email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number'
                 'Emergency contact first name', 'Emergency contact last name', 'Emergency contact email', 'Emergency contact -  Address: street'
                 'Emergency contact -  Address: city', 'Emergency contact -  Address: postcode', 'Emergency contact -  Telephone number', 'Emergency contact -  Relationship',
                 'NHS number', 'DOB (YYYY-MM-DD)', 'Drug allgergies', 'Medical Conditions', 'Disabilities', 'Smoker',
                 'Alcohol - Units per week', 'Exercise']
        return titles
    
    def get_info(self, user_type, user_id):
        self.connect_to_db()
        if user_type == 'GP':
            info = dbu.search_gp_id(conn, user_id)
        elif user_type == 'Patient':
            info = dbu.search_patient_id(conn, user_id)
        conn.close()
        return info
    
    def create_widgets(self, titles, mode, details):
        self.entries = []
        for i in range(len(titles)):
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
    
            self.label = tk.Label(self.labelframe, text=titles[i])
            self.label.grid(row=0)
            if mode == 'add':
                self.entry = tk.Entry(self.labelframe)
                self.entry.grid(row=1)
                self.entries.append(self.entry)
            elif mode == 'edit':
                self.entry = tk.Entry(self.labelframe)
                self.entry.insert(0, details[i])
                self.entry.grid(row=1)
                self.entries.append(self.entry)
            elif mode == 'view':
                self.details = tk.Label(self.labelframe, text=details[i])
                self.details.grid(row=1)
                
                

        if mode == 'add' or mode == 'edit':
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
        print(entered)
        #call tests - if not errors, then save
        if len(entered) != len(self.titles):
            self.lbl_text.config(text="Some data is missing", fg="red")
        else:
            self.save()
            
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

    Info_form(root, user_type='GP', mode='edit', user_id=1)
    root.mainloop()
    
    