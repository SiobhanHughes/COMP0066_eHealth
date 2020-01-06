eHealth Patient Management System protptype
Siobhan Hughes
Student number 18122424
COMP0066

# ehealth Patient Management system for GP Practice
----> Details about the features and functions of the application. ADD INFO/DESCRIPTION of application.

**Login**

1. Login window is the root window - controls the application. Closing the Login window will shutdown the application.
2. Three types of users can log in (Home Windows - Toplevel windows will open):
 - Admin: Admin Home window opens, containing features that the admin can use on the eHealth system
 - GP: GP Home window opens, containing features that the GP can use on the eHealth system
 - Patient: Patient Home window opens, containing features that the patient can use on the eHealth system
3. When a user logs in, user.pickle, containing a dictionary storing info about that user, is created and stored in the data directory. This is used to indicate that a user is logged in as well as track info about the user that is required to run sql queries and keep track of which user is currently logged in to the application.
4. When a user logs out, user.pickle is deleted.
5. If the Application is shutdown (Login window closed) while a user is still logged in, user.pickle is deleted to automatically log out the user.
6. System is currently configured to only allow one user to log in at a time
7. When the admin logs in with the default password (admin), a window will open allowing the admin to change the password or continue with the default password. Otherwise, the admin logs is using admin (in the email field) and their chosen password. Using the default password is useful for set up of the system, but chagning the admin password to a more secure one is highly recommended.


**Admin**

1. Admin would likely be the GP practice manager


### CREATE eHealth database with default admin to start application the very first time: Manually run script

1. Create sql database: createdb.py will create the eHealth database (all tables and default admin). 
 - File path: SHughes_eHealth/eHealth/src/database/createdb.py
 - eHealth.db database is stored in the data directory: SHughes_eHealth/eHealth/data/eHealth.db

2. Admin table in eHealth database: conatins 2 columns (administrator, passwd) 
 - default set up when database is first created: adminstrator = 'admin', passwd = 'admin' 
 - Admin table only ever has one row (store username: 'admin' and passwd)
 - When admin logs in to the eHealth application using the default password, they will be asked to change the password to somthing more secure or continue with the default password
 - Admin table is only used to confirm the log in of the admin

3. populate.py (File path: SHughes_eHealth/eHealth/src/database/populate.py). Running this file will autopopulate the GPs, Patients and Patient_Record tables with 2 GPs and 2 patients. GPs and patients are added to the system by the admin, so they have no passwords until they create an acount on the system. This file allows testing and development of the login/create account features. 
 