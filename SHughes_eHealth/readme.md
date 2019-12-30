eHealth Patient Management System protptype
Siobhan Hughes
student number 18122424
COMP0066

Python 3.7.5
sqlite3 version 3.30.1
GUI: Tkinter

1. Create sql database: createdb.py will create the eHealth database (all tables and default admin) using the following file path /SHughes_eHealth/eHealth/src/database/eHealth.db. Using db_path.py gives the file path required to access the eHealth.db database in the eHealth/src/database directory.
2. Admin table in eHealth database: this table conatins 2 columns (administrator, passwd) which has the default settings 'admin', 'admin' already saved in the database. This table is used to store the administrator username (admin) and password (admin). When admin first logs in using the password 'admin', the system will ask the admin to change the password to a more secure one. The admin will log in using the username 'admin' and the chosen password from then on.
3. Very first log in to the eHealth application as administrator (admind): username = 'admin', password = 'admin'