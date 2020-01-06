#https://www.sqlitetutorial.net/sqlite-python/creating-database/

import sqlite3
from sqlite3 import Error

import os
import sys
import inspect
import pkgutil
import get_path_utilities as get_path

#get the absolute file path to the eHealth database - used to pass the database file to create_connection
def db_path(num):
    current = get_path.get_current_dir()
    package_dir = get_path.getDir(current, num)
    database_path = os.path.join(package_dir, 'data/eHealth.db')
    return (database_path)

db_file = db_path(2)
 
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
    conn = create_connection(db_file)
    print(db_file)
    print(conn)
    print("sqlite version", sqlite3.sqlite_version)
    if conn is not None:
        print("connected")
        
    conn.close()