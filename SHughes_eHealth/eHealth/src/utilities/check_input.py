""" Functions to check user input for eHealth System"""
#============================IMPORT============================================

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
eHealth_dir = path.getDir(current, 2)
path.insert_dir(eHealth_dir)
from src.database import db_utilities as dbu
from src.database import connect
path.delete_dir()

#============================CHECK USER INPUT FUNCTIONS============================================

#helper function for use in this module only
# def connect_to_db():
#     global conn, cursor
#     db_file = connect.db_path(2)
#     conn = connect.create_connection(db_file)
#     cursor = conn.cursor()
    
def email_format(email):
    """ function checks that entered email matches the correct format using regular expressions """
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(email_regex, email)):
        return 'match'
    else:
        return 'not correct'
    
def email_unique(cursor, user_type, email):
    """ function checks that email is unique with the eHealth database as it is used for login.
        param: cursor - global variable created when call function to connect to database
        param: user_type, email """
    if user_type == 'GP':
        cursor.execute('SELECT * from GPs WHERE email = ?', (email,))
        gp_email = cursor.fetchall()
        print(gp_email)
        if gp_email != []:
            return 'exists'
        else:
            return 'unique'
    if user_type == 'Patient':
        cursor.execute('SELECT * from Patients WHERE email = ?', (email,))
        patient_email = cursor.fetchall()
        if patient_email != []:
            return 'exists'
        else:
            return 'unique'
    
def NHSno_unique(cursor, NHSno):
    """ function checks that entered NHS number is unique as it is the primary key for the Patient Record table
        in the eHealth database
        param: cursor - global variable created when call function to connect to database
        param: NHSno"""
    cursor.execute('SELECT * from Patient_Record WHERE NHSno = ?', (NHSno,))
    patient_num = cursor.fetchall()
    if patient_num != []:
        return 'exists'
    else:
        return 'unique'
    
def tel_format(tel):
    """ Telephone number accpeted when is consists of up to 11 digits
        Entered string is checked to ensure each character is an integer"""
    if len(tel) > 11:
        return 'not tel'
    else:
        for num in tel:
            try:
                int(num)
            except ValueError:
                return 'not num'
        else:
            return 'tel'
    
    
def check_dob(DOB):
    """ function to format entered date of birth into date object.
        Parameter: a string in the form YYYY-MM-DD """
        
    dob = DOB.split('-')
    nums = []
    for i in dob:
        try:
            num = int(i)
            nums.append(num)
        except ValueError:
            return 'not num'
    else:
        try:
            date_of_birth = dt.date(nums[0], nums[1], nums[2])
        except:
            return 'not date'
    return date_of_birth
        
        
    
    
    
    
    
if __name__ == '__main__':
    connect_to_db()
    
    if email_unique(cursor, 'GP', 'jane_allen1@gmail.com') == 'unique':
        print('yes')
    else: print('no')
    
    if NHSno_unique(cursor, 'NHS001') == 'unique':
        print('yes')
    else:
        print('no')
        
    print(tel_format('0798697235'))
    
    conn.close()
    
    print(check_dob('1950/02/04'))
    