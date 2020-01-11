import tkinter as tk
import tkinter.scrolledtext as scrolledtext

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

class Add_prescription:
    def __init__(self, parent, patient_id=None, *args, **kwargs):
        self.parent = parent
        self.patient_id = patient_id
        self.name = self.get_patient()
        
         #==============================VARIABLES======================================
        self.patient_fname = tk.StringVar()
        self.patient_lname = tk.StringVar()
        
              #==============================FRAMES=========================================
        self.Form = tk.Frame(self.parent, height=200)
        self.Form.pack(side=tk.TOP, pady=20)
 
                 #==============================LABELS=========================================
 
        self.lbl_search = tk.Label(self.Form, text = "Patient name:", font=('arial', 14), bd=15)
        self.lbl_search.grid(row=0, sticky="w")
        self.lbl_pfname = tk.Label(self.Form, text = self.name[0], font=('arial', 14), bd=15, fg='blue')
        self.lbl_pfname.grid(row=0, column=1, sticky="w")
        self.lbl_text = tk.Label(self.Form) #error messages appear here
        self.lbl_text.grid(row=2, columnspan=2)
 
 
                 #==============================ENTRY WIDGETS==================================
        self.enter_patient_fname = tk.Entry(self.Form, textvariable=self.patient_fname, font=(14))
        self.enter_patient_fname.grid(row=3)
        self.enter_patient_lname = tk.Entry(self.Form, textvariable=self.patient_lname, font=(14))
        self.enter_patient_lname.grid(row=3, column=1)
 
                 #==============================BUTTON WIDGETS=================================
        self.btn_search_p = tk.Button(self.Form, text="Save", width=45, command=self.save, fg='green')
        self.btn_search_p.grid(pady=25, row=4, columnspan=2)
         
        
    
    def get_patient(self):
        self.connect_to_db()
        cursor.execute('SELECT fname, lname FROM Patients WHERE patientid = ?', (self.patient_id,))
        info = cursor.fetchall()
        return info
    
    def save(self):
        pass

    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
        
if __name__ == '__main__':
    root = tk.Tk()

    Add_medical(root, patient_id=1)
    root.mainloop()