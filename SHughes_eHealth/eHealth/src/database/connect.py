#https://www.sqlitetutorial.net/sqlite-python/creating-database/

import sqlite3
from sqlite3 import Error
import db_path

 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn
 
 
if __name__ == '__main__':
    db_file = db_path.database_path
    conn = create_connection("db_file")
    print(conn)
    print("sqlite version", sqlite3.sqlite_version)
    if conn is not None:
        print("connected")
        
    conn.close()