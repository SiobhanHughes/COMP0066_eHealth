import sqlite3
from sqlite3 import Error

from datetime import date
from dateutil.relativedelta import relativedelta

import connect
import db_path
import db_utilities as db

def main():
    gp1 = ('Jane', 'Allen', 'jane_allen@gmail.com', 'Claire Lane', 'London', 'N1', '07912378346', date.today())

    gp2_date = date.today() + relativedelta(months=-6)
    gp2 = ('Theresa', 'Chng', 'theresa_chng@gmail.com', 'Orion street', 'London', 'N1', '07658911937', gp2_date)

    patient1 = ('Nicola', 'Hughes', 'nhughes@gmail.com', 'Berkeley street', 'London', 'N1', '07878842306', date.today(),
                'Chalrie', 'Guo', 'cguo@gamil.com', 'Berkeley street', 'London', 'N1', '07869229113', 'husband')

    patient2_date = date.today() + relativedelta(months=-4)
    patient2 = ('Norman', 'Smith', 'nsmith@gmail.com', 'Packington street', 'London', 'N1', '07988504379', patient2_date,
                'Damien', 'Smith', 'damien_smith@gamil.com', 'Canary street', 'London', 'N1', '07604482117', 'son')
    
    database = db_path.database_path
    conn = connect.create_connection(database)
    
    if conn is not None:
        #add gps to database
        db.insert_gp(conn, gp1)
        db.insert_gp(conn, gp2)
        
        #add patient info and record to database
        insert_patient1 = db.insert_patient(conn, patient1)
        print(insert_patient1)
        patient1_record = ('NHS001', insert_patient1, date(1984,12,14), 'penecillin', 'none', 'none', 'no', 3, 'gym classes three time a week')
        db.insert_patient_record(conn, patient1_record)
        
        insert_patient2 = db.insert_patient(conn, patient2)
        patient2_record = ('NHS002', insert_patient2, date(1950,8,23), 'none', 'diabetes', 'none', 'no', 0, 'moderate activity level, mainly walking')
        db.insert_patient_record(conn, patient2_record)
    
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
        
    
    conn.close()
 
 
if __name__ == '__main__':
    main()
