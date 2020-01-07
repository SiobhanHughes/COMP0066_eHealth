
#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import logging

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
path.delete_dir()


class Edit_info(tk.Frame):
    """ Get GP or Patient information from the database.
        Allow Admin to edit the information and save to the database """
        
    def __init__(self, parent, titles, user_type, user_id, *args, **kwargs):
        self.parent = parent
        self.titles = titles
        self.user_id = user_id
        self.user_type = user_type
        
        
        #mechanism to test that only one id is entered, it is correct and determine if gp or patient
        #sql queries needed 
        #self.select(self.type, self.id)
        self.info = self.select_gp(user_id)
        self.create_widgets(self.titles, self.info)
    
    def create_widgets(self, titles, info):
        self.entries = []
        for i in range(len(titles)):
            title = titles[i]
            self.labelframe = tk.LabelFrame(self.parent, text='Edit user')
            self.labelframe.pack(fill="both", expand=True)
    
            self.label = tk.Label(self.labelframe, text=title)
            self.label.pack(expand=True, fill='both')
    
            self.entry = tk.Entry(self.labelframe, )
            self.entry.insert(0, info[i])
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
    titles = ['GP first name', 'GP last name', 'GP email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number']
    user_type = 'GP'
    gpid = 1
    Edit_info(root, titles, user_type, gpid)
    root.mainloop()