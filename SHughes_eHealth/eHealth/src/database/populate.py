import sqlite3
from sqlite3 import Error

import datetime as dt
from dateutil.relativedelta import relativedelta

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


def main():
    
    """ Autopopulate the databse with 2 GPs and 3 Patients """
    
    gp1 = ('Jane', 'Allen', 'jane_allen@gmail.com', 'Claire Lane', 'London', 'N1', '07912378346', dt.date.today())

    gp2_date = dt.date.today() + relativedelta(months=-6)
    gp2 = ('Theresa', 'Chng', 'theresa_chng@gmail.com', 'Orion street', 'London', 'N1', '07658911937', gp2_date)

    patient1 = ('Nicola', 'Hughes', 'nhughes@gmail.com', 'Berkeley street', 'London', 'N1', '07878842306', dt.date.today(),
                'Charlie', 'Guo', 'cguo@gamil.com', 'Berkeley street', 'London', 'N1', '07869229113', 'husband')

    patient2_date = dt.date.today() + relativedelta(months=-4)
    patient2 = ('Norman', 'Smith', 'nsmith@gmail.com', 'Packington street', 'London', 'N1', '07988504379', patient2_date,
                'Damien', 'Smith', 'damien_smith@gamil.com', 'Canary street', 'London', 'NW1', '07604482117', 'son')
    
    patient3 = ('Nicola', 'Jones', 'njones@gmail.com', 'Wells street', 'London', 'N1', '07878842458', dt.date.today(),
                'Mary', 'Jones', 'maryjones@gamil.com', 'Barker street', 'London', 'E1', '07869227801', 'sister')
    
    database = connect.db_path(2)
    conn = connect.create_connection(database)
    
    if conn is not None:
        #add gps to database
        dbu.insert_gp(conn, gp1)
        dbu.insert_gp(conn, gp2)
        
        #add patient info and record to database
        insert_patient1 = dbu.insert_patient(conn, patient1)
        print(insert_patient1)
        patient1_record = ('NHS001', insert_patient1, dt.date(1984,12,14), 'penecillin', 'none', 'none', 'no', 5, 'gym classes three time a week')
        dbu.insert_patient_record(conn, patient1_record)
        
        insert_patient2 = dbu.insert_patient(conn, patient2)
        patient2_record = ('NHS002', insert_patient2, dt.date(1950,8,23), 'none', 'diabetes', 'none', 'yes', 0, 'moderate activity level, mainly walking')
        dbu.insert_patient_record(conn, patient2_record)
        
        insert_patient3 = dbu.insert_patient(conn, patient3)
        patient3_record = ('NHS003', insert_patient3, dt.date(1984,12,14), 'aspirin', 'ventricular septum defect', 'none', 'no', 2, 'yoga')
        dbu.insert_patient_record(conn, patient3_record)
    
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
        
    
    conn.close()
 
 
if __name__ == '__main__':
    main()
