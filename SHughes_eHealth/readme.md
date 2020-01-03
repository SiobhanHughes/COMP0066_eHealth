eHealth Patient Management System protptype
Siobhan Hughes
Student number 18122424
COMP0066

----> Details about the features and functions of the application. ADD INFO/DESCRIPTION of application.

CREATE eHealth database with default admin to start application the very first time:

1. Create sql database: createdb.py will create the eHealth database (all tables and default admin). 
 - File path: SHughes_eHealth/eHealth/src/database/createdb.py
 - eHealth.db database is stored in the data directory: SHughes_eHealth/eHealth/data/eHealth.db
 - db_path.py is used to get the absoulte file path of eHealth.db (SHughes_eHealth/eHealth/src/database/db_path.py)

2. Admin table in eHealth database: conatins 2 columns (administrator, passwd) 
 - default set up when database is first created: adminstrator = 'admin', passwd = 'admin' 
 - Admin table only ever has one row (store username: 'admin' and passwd)
 - The very first time the admin logs in to the eHealth application, they will be asked to change the password to somthing more secure
 - Admin table is only used to confirm the log in of the admin (no other access or update to the table when running the application)

 3. populate.py (File path: SHughes_eHealth/eHealth/src/database/populate.py). Running this file will autopopulate the GPs and Patients tables with 2 GPs and 2 patients. GPs and patients are added to the system by the admin, so they have no passwords until they create an acount on the system. This file allows testing and development of the login/create account features. 
 