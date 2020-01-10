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
    try:    
        dob = DOB.split('-')
    except:
        return 'error'
    nums = []
    for i in dob:
        try:
            num = int(i)
            nums.append(num)
        except ValueError:
            return 'error'
    else:
        try:
            date_of_birth = dt.date(nums[0], nums[1], nums[2])
        except:
            return 'error'
    return date_of_birth


def check_dates_format(dates):
    """ function to check entered range of dates is in correct format and convert to date object
        Parameter: a string in the form YYYY-MM-DD,YYYY-MM-DD """
    
    try:  
        date_range = dates.split(',')
    except:
        return 'error'
    if len(date_range) != 2: #check that only 2 dates entered
        return 'error'
    else: #convert strings to date objects
        nums = {}
        try:
            nums[date_range[0]] = date_range[0].split('-')
            nums[date_range[1]] = date_range[1].split('-')
        except:
            return 'error'
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
    
    try:    
        time_blocks = time.split(',')
    except:
        return 'error'
    time_spans = {}
    for block in time_blocks:
        try:
            time_spans[block] = block.split('-')
        except:
            return 'error'
    for block in time_blocks:
        if len(time_spans[block]) != 2:
            return 'error'

    for value in time_spans.values():
        try:
            value[0] = value[0].split(':')
            value[1] = value[1].split(':')
        except:
            return 'error'
    for key, value in time_spans.items():
        try:
            time_spans[key] = [dt.time(int(value[0][0]), int(value[0][1])), dt.time(int(value[1][0]), int(value[1][1]))]
        except:
            return 'error'
        
    for value in time_spans.values():
        if value[0] >= value[1]:
            return 'error'
    
    return time_spans
    
def gen_appointments(one_date, time_ranges):
    for key, value in time_ranges.items():
        time_ranges[key].append(one_date)
        #print(time_ranges)
    
    datetime_ranges = {}
    for key, value in time_ranges.items():
        datetime_ranges[key] = [dt.datetime.combine(value[2], value[0]), dt.datetime.combine(value[2], value[1])]
        #print(datetime_ranges)
    
    appointments = []
    for key, value in datetime_ranges.items():
        next = value[0]
        while next <= value[1]:
            appointments.append(next)
            next += dt.timedelta(minutes=15)
    return appointments

def check_date_format(one_date):
    """ function to check single date is in correct format and convert to date object
        Parameter: a string in the form YYYY-MM-DD """

    try:
       nums = one_date.split('-')
    except:
        return 'error'

    if len(nums)!= 3:
        return 'error'
    
    try:
        one_date = dt.date(int(nums[0]), int(nums[1]), int(nums[2]))
    except:
        return 'error'
    else:
        return one_date
        
        

if __name__ == '__main__':
    
    #check dates
    d, e = check_dates_format('2020-01-10,2020-01-12')
    print(d, e)
    
    #generate list of dates
    y = gen_dates(d, e)
    print("y: ", y)
    for i in y:
        print(i)
    
    #check time range
    z = check_time_format('09:00-12:00, 13:00-17:00')
    print('z: ', z)
    
    # #generate appointments for one date only (need to save foe each date) - get date and time
    test = gen_appointments(dt.date(2020,1,10), z)
    for i in test:
        print(i)
        only_date, only_time =  i.date(), i.time()
        print(only_date)
        print(only_time)
        
    print(check_date_format('2020-01-11'))
        


    