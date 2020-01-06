# How to create the database with all the relevant tables using sqlite3 and python taken from this tutorial: 
# https://www.sqlitetutorial.net/sqlite-python/create-tables/

import sqlite3
from sqlite3 import Error
import connect
import db_path


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
 
def create_admin(conn, admin):
    """ create admin in the Admin table
    :param conn: Connection object
    :param admin: details to be inserted into Admin table """
    
    sql = """ INSERT INTO Admin (administrator, passwd) VALUES (? , ?); """
    
    try:
        c = conn.cursor()
        c.execute(sql, admin)
    except Error as e:
        print(e)
 
def main():
    database = db_path.database_path
 
    create_admin_table = """ CREATE TABLE IF NOT EXISTS Admin (
                                    administrator text NOT NULL,
                                    passwd text NOT NULL
                                    ); """
                                    
    admin = ('admin', 'admin')
 
    create_gp_table = """ CREATE TABLE IF NOT EXISTS GPs (
                                    gpid integer PRIMARY KEY AUTOINCREMENT,
                                    fname text NOT NULL,
                                    lname text NOT NULL,
                                    email text NOT NULL,
                                    passwd text,
                                    street text NOT NULL,
                                    city text NOT NULL,
                                    postcode text NOT NULL,
                                    tel text NOT NULL,
                                    begin_date text NOT NULL,
                                    active text DEFAULT "yes" NOT NULL
                                ); """
 
    create_patient_table = """ CREATE TABLE IF NOT EXISTS Patients (
                                    patientid integer PRIMARY KEY AUTOINCREMENT,
                                    fname text NOT NULL,
                                    lname text NOT NULL,
                                    email text NOT NULL,
                                    passwd text,
                                    street text NOT NULL,
                                    city text NOT NULL,
                                    postcode text NOT NULL,
                                    tel text NOT NULL,
                                    begin_date text NOT NULL,
                                    contact_fname text NOT NULL,
                                    contact_lname text NOT NULL,
                                    contact_email text NOT NULL,
                                    contact_street text NOT NULL,
                                    contact_city text NOT NULL,
                                    contact_postcode text NOT NULL,
                                    contact_tel text NOT NULL,
                                    contact_relationship text NOT NULL,
                                    active text DEFAULT "yes" NOT NULL
                                ); """
    
    create_patient_record_table = """ CREATE TABLE IF NOT EXISTS Patient_Record (
                                    NHSno text NOT NULL PRIMARY KEY,
                                    patientid integer NOT NULL,
                                    DOB text NOT NULL,
                                    drug_allergies text NOT NULL,
                                    medical_conditions text NOT NULL,
                                    disabilities text NOT NULL,
                                    smoker text NOT NULL,
                                    alcohol_units_per_week integer NOT NULL,
                                    exercise text NOT NULL,
                                    FOREIGN KEY (patientid) REFERENCES Patients (patientid)
                                ); """
                                
    create_vaccine_record_table = """ CREATE TABLE IF NOT EXISTS Vaccine_Record (
                                    NHSno text NOT NULL,
                                    patientid integer NOT NULL,
                                    date text NOT NULL,
                                    vaccine text NOT NULL,
                                    FOREIGN KEY (patientid) REFERENCES Patients (patientid),
                                    FOREIGN KEY (NHSno) REFERENCES Patient_Record (NHSno),
                                    PRIMARY KEY (NHSno, date, vaccine)
                                ); """
    
    create_medical_history_table = """ CREATE TABLE IF NOT EXISTS Medical_History (
                                    NHSno text NOT NULL,
                                    patientid integer NOT NULL,
                                    gpid integer NOT NULL,
                                    date text NOT NULL,
                                    record text NOT NULL,
                                    FOREIGN KEY (patientid) REFERENCES Patients (patientid),
                                    FOREIGN KEY (gpid) REFERENCES GPs (gpid),
                                    FOREIGN KEY (NHSno) REFERENCES Patient_Record (NHSno),
                                    PRIMARY KEY (NHSno, gpid, date)
                                ); """
    
    create_prescriptions_table = """ CREATE TABLE IF NOT EXISTS Presciptions (
                                    prescriptionid integer PRIMARY KEY AUTOINCREMENT,
                                    NHSno text NOT NULL,
                                    patientid integer NOT NULL,
                                    gpid integer NOT NULL,
                                    medication text NOT NULL,
                                    dosage text NOT NULL,
                                    startDate text NOT NULL,
                                    endDate text NOT NULL,
                                    repeatScript text DEFAULT "no" NOT NULL,
                                    repeatEnd text,
                                    FOREIGN KEY (patientid) REFERENCES Patients (patientid),
                                    FOREIGN KEY (gpid) REFERENCES GPs (gpid),
                                    FOREIGN KEY (NHSno) REFERENCES Patient_Record (NHSno)
                                ); """
                                
    create_appointments_table = """ CREATE TABLE IF NOT EXISTS Appointments (
                                    appointmentid integer PRIMARY KEY AUTOINCREMENT,
                                    gpid integer NOT NULL,
                                    date text NOT NULL,
                                    time text NOT NULL,
                                    patientid integer NULL,
                                    available text DEFAULT "yes" NOT NULL,
                                    FOREIGN KEY (patientid) REFERENCES Patients (id),
                                    FOREIGN KEY (gpid) REFERENCES GPs (id)
                                ); """
    
    
    # create a database connection
    conn = connect.create_connection(database)
    print(conn)
 
    # create tables
    if conn is not None:
        # create admin table
        create_table(conn, create_admin_table)
        
        #insert admin details
        create_admin(conn, admin)
 
        # create gp table
        create_table(conn, create_gp_table)
        
        # create patient table
        create_table(conn, create_patient_table)
        
        # create patient record table
        create_table(conn, create_patient_record_table)
        
        # create vaccine record table
        create_table(conn, create_vaccine_record_table)
        
        # create medical history table
        create_table(conn, create_medical_history_table)
        
        # create precriptions table
        create_table(conn, create_prescriptions_table)
        
        # create apointments table
        create_table(conn, create_appointments_table)
        
        #commit changes
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
        
    
    conn.close()
 
 
if __name__ == '__main__':
    main()