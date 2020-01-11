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

import datetime as dt

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
from src.utilities import check_input as check
path.delete_dir()


class Add_time(tk.Frame):
    """ GGP adds availability for apppointments """
        
    def __init__(self, parent, dates, *args, **kwargs):
        self.parent = parent
        self.dates = dates
        self.user = track.load('user.pickle', 3)
        self.create_widgets(self.dates)
    
    def create_widgets(self, dates):
        self.labelframe = tk.LabelFrame(self.parent)
        self.labelframe.pack(fill="both", expand=True)
        self.label = tk.Label(self.labelframe, text='Add time range in the format HH:MM-HH:MM,HH:MM-HH:MM using 24h (separated by comma)')
        self.label.pack(expand=True, fill='both')
        
        self.times = []
        for i in range(len(dates)):
            date = dates[i]
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
    
            self.entered_date = tk.Label(self.labelframe, text=date)
            self.entered_date.pack()
    
            self.enter_time = tk.Entry(self.labelframe)
            self.enter_time.pack()
            self.times.append(self.enter_time)
        
        self.labelframe = tk.LabelFrame(self.parent)
        self.labelframe.pack(fill="both", expand=True)
        self.label = tk.Label(self.labelframe)
        self.label.pack(expand=True, fill='both')
        self.label = tk.Label(self.labelframe, text='Add Appointment availability', fg='blue')
        self.label.pack(expand=True, fill='both')
        self.lbl_text = tk.Label(self.labelframe) #error messages appear here
        self.lbl_text.pack(expand=True, fill='both')
        self.button = tk.Button(self.labelframe, text="Save", command=self.get_input, fg='blue')
        self.button.pack()



    
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()

    
    def get_input(self):
        self.connect_to_db()
        times = self.get_times()
        print('times entered:', times)       
        dates = self.dates
        print('dates entered:', dates)
        if times is not None:
            time_ranges = self.format_times(times)
            print('times: ', time_ranges)
        
        #dates list - pass one date together with time_ranges dictionary to generate appointments for each date (index match)
            if time_ranges is not None:
                for i in range(len(dates)):
                    appointments = check.gen_appointments(dates[i], time_ranges[i])
                    for i in appointments:
                        print(i)
                        date_time = i
                        gpid = self.user['gpid']
                        appoint = (gpid, date_time)
                        print(appoint)
                        dbu.insert_appointment(conn, appoint)
                        self.save()
        conn.close()
    
    def get_times(self):
        entered_time_ranges= []
        for entry in self.times:
            val = entry.get().strip()
            if val != '':
                entered_time_ranges.append(val)
        if len(entered_time_ranges) != len(self.dates):
                self.lbl_text.config(text="Some data is missing", fg="red")
                return None
        else:
            return entered_time_ranges
        
    # def get_dates(self):
    #     date_ranges = []
    #     for entry in self.dates_inserted:
    #         val = entry.get().strip()
    #         if val != '':
    #             date_ranges.append(val)
    #     if len(date_ranges) != len(self.dates):
    #             self.lbl_text.config(text="Some data is missing", fg="red")
    #             return None
    #     else: 
    #         return date_ranges
    
    # def format_dates(self, dates):
    #     format_dates = []
    #     for d in dates:
    #         one_date = check.check_date_format(d)
    #         if one_date == 'error':
    #             self.lbl_text.config(text="Error with date formatt (YYYY-MM-DD)", fg="red")
    #             return None
    #         else:
    #             format_dates.append(one_date)
    #     if len(format_dates) != len(self.dates):
    #         self.lbl_text.config(text="Error: date missing", fg="red")
    #         return None
    #     else:
    #         return format_dates
        
    def format_times(self, times):
        ranges = []
        for t in times:
            time_range = check.check_time_format(t)
            if time_range == 'error':
                self.lbl_text.config(text="Error: time range not correctly formatted", fg="red")
                return None
            else:
                ranges.append(time_range)
        if len(ranges) != len(self.dates):
            self.lbl_text.config(text="Error: times missing", fg="red")
            return None
        else:
            return ranges
    
    def save(self):
        for widget in self.labelframe.winfo_children():
            widget.destroy()
    
        
if __name__ == '__main__':
    root = tk.Tk()
    dates = ('08-01,01-02')
    Add_time(root, dates)
    root.mainloop()