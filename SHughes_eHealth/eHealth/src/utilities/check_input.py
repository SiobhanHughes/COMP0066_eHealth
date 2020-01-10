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

def check_dates_format(dates):
    """ function to check entered range of dates is in correct format and convert to date object
        Parameter: a string in the form YYYY-MM-DD,YYYY-MM-DD """
        
    date_range = dates.split(',')
    if len(date_range) != 2: #check that only 2 dates entered
        return 'error'
    else: #convert strings to date objects
        nums = {date_range[0]: date_range[0].split('-'), date_range[1]: date_range[1].split('-')}
        print(nums)
        
        try:
            start = dt.date(int(nums[date_range[0]][0]), int(nums[date_range[0]][1]), int(nums[date_range[0]][2]))
            end = dt.date(int(nums[date_range[1]][0]), int(nums[date_range[1]][1]), int(nums[date_range[1]][2]))
        except:
            return 'error'
        
        if start > end or start < dt.date.today():
            return 'error'
        else:
            return start, end
        
def gen_dates(start, end):
    date_range = []
    if start == end:
        date_range.append(start)
    else:
        next = start
        i = 0
        while (next < end):
            next = start + dt.timedelta(days=i)
            date_range.append(next)
            i +=1
    return date_range
    
def check_time_format(time):
    """ function to check entered range of time is in correct format and convert to time object
        Parameter: a string in the form HH:MM-HH:MM,HH:MM-HH:MM (use 24 hour clock)"""
        
    time_blocks = time.split(',')
    print(time_blocks)
    time_spans = {}
    for block in time_blocks:
        time_spans[block] = block.split('-')
    print(time_spans)
    for value in time_spans.values():
        value[0] = value[0].split(':')
        value[1] = value[1].split(':')
    print(time_spans)
    
    for key, value in time_spans.items():
        # print(value[0][0])
        # print(value[0][1])
        # print(value[1][0])
        # print(value[1][1])
        
        try:
            time_spans[key] = [dt.time(int(value[0][0]), int(value[0][1])), dt.time(int(value[1][0]), int(value[1][1]))]
        except:
            return 'error'
    
    return time_spans
    

if __name__ == '__main__':
    x = check_dates_format('2020-01-10,2020-01-15')
    print(x)
    
    y = gen_dates(x[0], x[1])
    print(y)
    for i in y:
        print(i)
    
    x = check_time_format('09:00-12:00,13:00-17:00')
    print('x: ', x)
    