# How to create functions to manipulate sqlite tables taken from: 
# https://www.sqlitetutorial.net/sqlite-python/insert/
#https://www.sqlitetutorial.net/sqlite-python/update/

import sqlite3
from sqlite3 import Error

#==============================INSERT======================================

def insert_gp(conn, gp):
    """
    Add a new gp into the GPs table
    :param conn: Connection object
    :param gp: details to be inserted
    :return: id (gp id as primary key for the table)
    """
    sql = ''' INSERT INTO GPs (fname, lname, email, street, city, postcode, tel, begin_date)
              VALUES(?,?,?,?,?,?,?,?) '''
    get_id = 0
    try:
        cur = conn.cursor()
        cur.execute(sql, gp)
        get_id = cur.lastrowid
        conn.commit()
    except Error as e:
        print(e)
    return get_id

def insert_patient(conn, patient):
    """
    Add a new patient into the Patients table
    :param conn: Connection object
    :param patient: details to be inserted
    :return: id (patient id as primary key for the table)
    """
    sql = ''' INSERT INTO Patients (fname, lname, email, street, city, postcode, tel, begin_date, contact_fname, 
    contact_lname, contact_email, contact_street, contact_city, contact_postcode, contact_tel, contact_relationship)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    get_id = 0
    try:
        cur = conn.cursor()
        cur.execute(sql, patient)
        get_id = cur.lastrowid
        conn.commit()
    except Error as e:
        print(e)
    return get_id

def insert_patient_record(conn, patient_record):
    """
    Add a new patient record to the Patient_Record table when new patient is added/registered with the system
    :param conn: Connection object
    :param patient_record: details to be inserted
    """
    sql = ''' INSERT INTO Patient_Record (NHSno, patientid, DOB, drug_allergies, medical_conditions, disabilities, smoker,
    alcohol_units_per_week, exercise)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, patient_record)
        conn.commit()
    except Error as e:
        print(e)

def insert_vaccine_record(conn, vaccine_record):
    """
    Add a new vaccine record into the Vaccine _Record table
    :param conn: Connection object
    :param vaccine_record: details to be inserted
    """
    sql = ''' INSERT INTO Vaccine_Record (NHSno, patientid, date_v, vaccine)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, vaccine_record)
        conn.commit()
    except Error as e:
        print(e)
    
def insert_medical_history(conn, medical_history):
    """
    Add a new medical history record into the Medical _History table
    :param conn: Connection object
    :param medical_history: details to be inserted
    """
    sql = ''' INSERT INTO Medical_History (NHSno, patientid, gpid, date_mh, record)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, medical_history)
        conn.commit()
    except Error as e:
        print(e)
    
def insert_presciption(conn, prescription):
    """
    Add a new presciption into the Presciptions table
    :param conn: Connection object
    :param presciption: details to be inserted
    """
    sql = ''' INSERT INTO Prescriptions (NHSno, patientid, gpid, medication, dosage, date_p)
              VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, prescription)
        conn.commit()
    except Error as e:
        print(e)

#gp makes thier time slots available      
def insert_appointment(conn, appointment):
    """
    Add a new appointment into the Appointments table
    :param conn: Connection object
    :param appointment: details to be inserted
    """
    sql = ''' INSERT INTO Appointments (gpid, date_time)
              VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, appointment)
        conn.commit()
    except Error as e:
        print(e)


        
#==============================UPDATE======================================

def update_gp(conn, gp):
    """
    Update gp details in the GPs table
    :param conn: Connection object
    :param gp: details to be updated and the gpid
    """
    sql = ''' UPDATE GPs 
              SET fname = ?, lname = ?, street = ?, city = ?, postcode = ?, tel = ?
              WHERE gpid = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, gp)
        conn.commit()
    except Error as e:
        print(e)

def update_patient(conn, patient):
    """
    update patient details in the Patients table
    :param conn: Connection object
    :param patient: details to be updated and patientid
    """
    sql = ''' UPDATE Patients
              SET fname = ?, lname = ?, street = ?, city = ?, postcode = ?, tel = ?, contact_fname = ?, 
              contact_lname = ?, contact_email = ?, contact_street = ?, contact_city = ?, contact_postcode = ?, 
              contact_tel = ?, contact_relationship = ?
              WHERE patientid = ? '''

    try:
        cur = conn.cursor()
        cur.execute(sql, patient)
        conn.commit()
    except Error as e:
        print(e)

def update_patient_record(conn, patient_record):
    """
    Update Patient_Record table
    :param conn: Connection object
    :param patient_record: details to be updated and patientid
    """
    sql = ''' UPDATE Patient_Record
              SET DOB = ?, drug_allergies = ?, medical_conditions = ?, disabilities = ?, smoker = ?,
              alcohol_units_per_week = ?, exercise = ?
              WHERE patientid = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, patient_record)
        conn.commit()
    except Error as e:
        print(e)


#==============================Patient makes appointment======================================
def book_appointment(conn, book):
    """
    update Appointments table - add patientid and set available to 'no'
    :param conn: Connection object
    :params book:
    """
    sql = ''' UPDATE Appointments
              SET patientid = ? , 
                available = "no" 
              WHERE gpid = ?,
              AND date = ?,
              AND time = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, book)
        conn.commit()
    except Error as e:
        print(e)
    
#==============================Patient cancels appointment======================================
def cancel_appointment(conn, cancel):
    """
    update Appointments table - remove patientid and set available to 'yes'
    :param conn: Connection object
    :params cance;:
    """
    sql = ''' UPDATE Appointments
              SET patientid = NULL , 
                available = "yes" 
              WHERE gpid = ?,
              AND date = ?,
              AND time = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, cancel)
        conn.commit()
    except Error as e:
        print(e)
        
        
#==============================Search Patient======================================
def search_patient_fname(conn, fname):
    """
    Search and retrieve patient information using patient first name
    :param conn: Connection object
    :params patient first name:
    return patient information
    """
    sql = ''' SELECT p.patientid, fname, lname, email, DOB, NHSno, street, city, postcode, tel, active
              FROM Patients p, Patient_Record pr
              WHERE p.patientid = pr.patientid
              AND fname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (fname,))
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
        
    return rows

def search_patient_lname(conn, lname):
    """
    Search and retrieve patient information using patient last name
    :param conn: Connection object
    :params patient last name:
    return patient information
    """
    sql = ''' SELECT p.patientid, fname, lname, email, DOB, NHSno, street, city, postcode, tel, active
              FROM Patients p, Patient_Record pr
              WHERE p.patientid = pr.patientid
              AND lname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (lname,))
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    
    return rows

def search_patient_fullname(conn, fullname):
    """
    Search and retrieve patient information using patient full name
    :param conn: Connection object
    :params patient full name:
    return patient information
    """
    sql = ''' SELECT fname, lname, email, street, city, postcode, tel, DOB, NHSno, street, city, postcode, tel, active
              FROM Patients p, Patient_Record pr
              WHERE p.patientid = pr.patientid
              AND fname = ?
              AND lname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, fullname)
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
        
    return rows
        
        
def search_patient_id(conn, patientid):
    """
    Search and retrieve patient information using patient id
    :param conn: Connection object
    :params patientid:
    return patient information
    """
    sql = ''' SELECT fname, lname, email, street, city, postcode, tel,
                    contact_fname, contact_lname, contact_email, contact_street, contact_city, contact_postcode,
                    contact_tel, contact_relationship, NHSno, DOB, drug_allergies, medical_conditions, disabilities,
                    smoker, alcohol_units_per_week, exercise
              FROM Patients p, Patient_Record pr
              WHERE p.patientid = pr.patientid
              AND p.patientid = ? '''

    try:
        cur = conn.cursor()
        cur.execute(sql, (patientid,))
        row = cur.fetchone()
        conn.commit()
    except Error as e:
        print(e)
         
    return row


#==============================Search GP======================================
def search_gp_fname(conn, fname):
    """
    Search and retrieve GP information using GP first name
    :param conn: Connection object
    :params GP first name:
    return GP information
    """
    sql = ''' SELECT gpid, fname, lname, email, street, city, postcode, tel, active
              FROM GPs
              WHERE fname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (fname,))
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
        
    return rows

def search_gp_lname(conn, lname):
    """
    Search and retrieve GP information using GP last name
    :param conn: Connection object
    :params GP last name:
    return GP information
    """
    sql = ''' SELECT gpid, fname, lname, email, street, city, postcode, tel, active
              FROM GPs
              WHERE lname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (lname,))
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    
    return rows
        
        
def search_gp_fullname(conn, fullname):
    """
    Search and retrieve GP information using GP first and last name
    :param conn: Connection object
    :params GP first and last name:
    return GP information
    """
    sql = ''' SELECT gpid, fname, lname, email, street, city, postcode, tel, active
              FROM GPs
              WHERE fname = ?
              AND lname = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, fullname)
        rows = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
        
    return rows

def search_gp_id(conn, gpid):
    """
    Search and retrieve GP information using GP id
    :param conn: Connection object
    :params gpid:
    return GP information
    """
    sql = ''' SELECT fname, lname, email, street, city, postcode, tel
              FROM GPs
              WHERE gpid = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (gpid,))
        row = cur.fetchone()
        conn.commit()
    except Error as e:
        print(e)
        
    return row

#==============================GET NHSno======================================
def get_NHSno(conn, pid):
    """
    Get NHS number using patient id
    :param conn: Connection object
    :params patient id:
    :return NHSno
    """
    
    sql = ''' SELECT NHSno 
              FROM Patient_Record
              WHERE patientid = ? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (pid,))
        NHS_num = cur.fetchone()
        conn.commit()
    except Error as e:
        print(e)
        
    return NHS_num
    