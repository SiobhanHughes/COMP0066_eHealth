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
path.delete_dir()

class Add_medical:
    
    def __init__(self, parent, patient_id=None, *args, **kwargs):
        self.parent = parent
        self.patient_id = patient_id
        self.user = track.load('user.pickle', 3)
        self.details = self.get_patient()

        
              #==============================FRAMES=========================================
        self.Form = tk.Frame(self.parent, height=200)
        self.Form.pack(side=tk.TOP, pady=20)
 
                 #==============================LABELS=========================================
 
        self.lbl_name = tk.Label(self.Form, text = "Patient name, NHS number:", font=('arial', 14), bd=15)
        self.lbl_name.grid(row=0, sticky="w")
        self.lbl_pname = tk.Label(self.Form, text = self.details[0], font=('arial', 14), bd=15, fg='blue')
        self.lbl_pname.grid(row=1, sticky="w")
        self.lbl_text = tk.Label(self.Form) #error messages appear here
        self.lbl_text.grid(row=2, columnspan=2)
 
 
                 #==============================ENTRY WIDGETS==================================
        self.textFrame = scrolledtext.ScrolledText(self.Form, width=50, bd=10, relief="raised")
        self.textFrame.grid(row=3)
 
                 #==============================BUTTON WIDGETS=================================
        self.btn_save = tk.Button(self.Form, text="Save", width=45, command=self.save, fg='green')
        self.btn_save.grid(pady=25, row=4)
         
        
    
    def get_patient(self):
        self.connect_to_db()
        cursor.execute('SELECT fname, lname, NHSno FROM Patients p, Patient_Record pr WHERE p.patientid = pr.patientid AND p.patientid = ?', (self.patient_id,))
        info = cursor.fetchall()
        cursor.close()
        conn.close
        print(info)
        return info
    
    def save(self):
        self.connect_to_db()
        record = self.textFrame.get("1.0", tk.END)
        if self.textFrame.compare("end-1c", "==", "1.0"):
            self.lbl_text.config(text="No Medical History entered", fg="red")
        else:
            medical_history = (self.details[0][2], self.patient_id, self.user['gpid'], dt.datetime.now(), record)
            dbu.insert_medical_history(conn, medical_history)
            cursor.close()
            conn.close()
            self.btn_save.destroy()

    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
        
if __name__ == '__main__':
    root = tk.Tk()

    Add_medical(root, patient_id=1)
    root.mainloop()