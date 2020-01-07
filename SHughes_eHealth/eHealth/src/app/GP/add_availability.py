#Help with loop to create multiple widgets
#https://stackoverflow.com/questions/22916622/how-to-store-values-from-an-entry-widget-for-loop-in-tkinter


#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import logging

import sqlite3
from sqlite3 import Error

import datetime

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


class Add_time(tk.Frame):
    """ GGP adds availability for apppointments """
        
    def __init__(self, parent, dates, *args, **kwargs):
        self.parent = parent
        self.dates = self.get_dates(dates)
        #get dates for which GP wants to enter availability
        self.create_widgets(self.dates)
    
    def create_widgets(self, dates):
        self.entries = []
        for i in range(len(dates)):
            date = dates[i]
            self.labelframe = tk.LabelFrame(self.parent, text='Add Availability')
            self.labelframe.pack(fill="both", expand=True)
    
            self.label = tk.Label(self.labelframe, text=date)
            self.label.pack(expand=True, fill='both')
    
            self.entry = tk.Entry(self.labelframe, )
            self.entry.pack()
            self.entries.append(self.entry)
        
        self.label = tk.Label(self.labelframe)
        self.label.pack(expand=True, fill='both')
        self.label = tk.Label(self.labelframe, text='Save all details', fg='blue')
        self.label.pack(expand=True, fill='both')
        self.lbl_text = tk.Label(self.labelframe) #error messages appear here
        self.lbl_text.pack(expand=True, fill='both')
        self.button = tk.Button(self.labelframe, text="Save", command=self.get_input, fg='blue')
        self.button.pack()

    @staticmethod
    def get_dates(dates):
        #get all dates between start date and end date as a list
        #need to check dates correcty entered!! Separate utitlites for this as need to check all date formats entered - see lab sheets
        d = dates.split(',') #'DD-MM,DD-MM' string - need to check this entry!!!
        start = d[0].split('-')
        end = d[1].split('-')
        now = datetime.datetime.now()
        
        start_date = datetime.date(now.year, int(start[1]), int(start[0]))
        end_date = datetime.date(now.year, int(end[1]), int(end[0]))
        
        date_range = Add_time.genDate(start_date, end_date)
        dates = []
        for i in date_range:
            dates.append(i)
        print(dates)
        for i in dates:
            print(i)
        return dates
            
            
        
    @staticmethod   
    def genDate(start, end):
        next = start
        i = 0
        while (next < end):
            next = start + datetime.timedelta(days=i)
            yield next
            i +=1
        
        
    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
        
    def select_gp(self, user_id):
        self.connect_to_db()
        sql = "SELECT fname, lname, email, street, city, postcode, tel  FROM GPs WHERE gpid = ?"
        cursor.execute(sql, (user_id,))
        gp = cursor.fetchone()
        print(gp)
        cursor.close()
        conn.close()
        return gp
    
    def get_input(self):
        info = []
        for entry in self.entries:
            val = entry.get().strip()
            if val != '':
                info.append(val)
        print(info)
        #call tests - if not errors, then save
        if len(info) != len(self.titles):
            self.lbl_text.config(text="Some data is missing", fg="red")
        else:
            self.save()
    
    def save(self):
        #send automatic email to GP or Patient
        for widget in self.labelframe.winfo_children():
            widget.destroy()
    
        
if __name__ == '__main__':
    root = tk.Tk()
    dates = ('08-01,01-02')
    Add_time(root, dates)
    root.mainloop()