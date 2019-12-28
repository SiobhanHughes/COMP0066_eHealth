#https://www.sqlitetutorial.net/sqlite-python/creating-database/

import sqlite3
from sqlite3 import Error
 
 
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
    conn = create_connection(r"eHealth.db")
    print(conn)
    print("sqlite version", sqlite3.sqlite_version)
    if conn is not None:
        print("connected")
        
    conn.close()