#https://www.sqlitetutorial.net/sqlite-python/create-tables/
#FOREIGN KEY (project_id) REFERENCES projects (id)

import connect
import sqlite3
from sqlite3 import Error
 

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
 
 
def main():
    database = r"eHealth.db"
 
    create_admin_table = """ CREATE TABLE IF NOT EXISTS admin (
                                        administrator text DEFAULT "admin" NOT NULL,
                                        passwd text DEFAULT "admin" NOT NULL
                                    ); """
 
    create_gp_table = """CREATE TABLE IF NOT EXISTS gp (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    fname text NOT NULL,
                                    lname text NOT NULL,
                                    email text NOT NULL,
                                    passwd text,
                                    street text NOT NULL,
                                    city text NOT NULL,
                                    postcode text NOT NULL,
                                    tel text NOT NULL,
                                    active text DEFAULT "yes" NOT NULL
                                );"""
 
    # create a database connection
    conn = connect.create_connection(database)
    print(conn)
 
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, create_admin_table)
 
        # create tasks table
        create_table(conn, create_gp_table)
        
        #save changes
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
        
    
    conn.close()
 
 
if __name__ == '__main__':
    main()