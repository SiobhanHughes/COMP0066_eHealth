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

class Patient_records:
    
    def __init__(self, parent, record_type='medical', patient_id=None, *args, **kwargs):
        self.parent = parent
        self.record_type = record_type
        self.patient_id = patient_id
        self.titles = self.create_titles()
        self.details = self.get_info()
        self.create_widgets()
        
    
    def create_titles(self):
        if self.record_type == 'medical':
            titles = ['Date','Patient first name', 'Patient last name', 'GP first name', 'GP last name',  'NHS number', 'Record']
        elif self.record_type == 'prescription':
            titles = ['Date','Patient first name', 'Patient last name', 'GP first name', 'GP last name', 'NHS number', 'Medication', 'Dosage']
        elif self.record_type == 'vaccine':
            titles = ['Date','Patient first name', 'Patient last name', 'NHS number', 'Vaccine']
        return titles
    
    def create_widgets(self):
        if self.details == []:
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
            tk.Label(self.labelframe, text="There are currently no %s records for this patient."  %self.record_type, font=('arial', 14)).pack()
        else:
            for row in self.details:
                for i in range(len(self.titles)):
                    self.labelframe = tk.LabelFrame(self.parent)
                    self.labelframe.pack(fill="both", expand=True)

                    self.label = tk.Label(self.labelframe, text=self.titles[i])
                    self.label.grid(row=0)

                    self.show_details = tk.Label(self.labelframe, text=row[i])
                    self.show_details.grid(row=1)
                

    def get_info(self):
        self.connect_to_db()
        if self.record_type == 'medical':
            info = dbu.search_medical(conn, self.patient_id)
            print(info)
        elif self.record_type == 'prescription':
            info = dbu.search_prescription(conn, self.patient_id)
        elif self.record_type == 'vaccine':
            info = dbu.search_vaccine(conn, self.patient_id)
        conn.close()
        return info
    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

    
if __name__ == '__main__':
    root = tk.Tk()

    Patient_records(root, patient_id=1, record_type='vaccine')
    root.mainloop()
    