#============================IMPORT============================================

import tkinter as tk

import os
import sys
import inspect

import sqlite3
from sqlite3 import Error

import admin_home
import gp_home
import patient_home
import create_account

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
path.delete_dir()

#============================Open Home Windows======================

class Home:
    
    def Admin_Window(self): #open Admin home window (Toplevel)
        global Admin
        top = tk.Toplevel()
        Admin = admin_home.MainView(top)
        top.title("Welcome to the eHealth system")
        Admin.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    def GP_Window(self): #open GP home window (Toplevel)
        global GP
        top = tk.Toplevel()
        GP = gp_home.MainView(top)
        top.title("Welcome to the eHealth system")
        GP.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
    def Patient_Window(self): #open Pateint home window (Toplevel)
        global Patient
        top = tk.Toplevel()
        Patient = patient_home.MainView(top)
        top.title("Welcome to the eHealth system")
        Patient.pack(side="top", fill="both", expand=True)
        width = 800
        height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        top.geometry("%dx%d+%d+%d" % (width, height, x, y))