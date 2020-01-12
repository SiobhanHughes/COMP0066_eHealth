#============================IMPORT============================================

import tkinter as tk

import datetime as dt

import get_path_utilities as path
current = path.get_current_dir()
eHealth_dir = path.getDir(current, 3)
path.insert_dir(eHealth_dir)
from src.database import db_utilities as dbu
from src.database import connect
from src.utilities import track_user as track
from src.utilities import check_input as check
path.delete_dir()


#============================Search results interface======================

class Search_results:
    def __init__(self, parent, titles, rows, pid=0, *args, **kwargs):
        self.parent = parent
        self.titles = titles
        self.rows = rows
        self.pid = pid
        self.display_result(self.titles, self.rows)
        
    def display_result(self, titles, rows):
        for x in range(len(rows)):
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
            for i in range(len(titles)):
                if titles[i] == 'Cancel':
                    tk.Button(self.labelframe, text='cancel', width=20, command=lambda c=rows[x][i]: self.cancel_appoint(c), fg='red').grid(row=0, column=i)
                elif titles[i] == 'Book':
                    tk.Button(self.labelframe, text='book', width=20, command=lambda b=rows[x][i]: self.book_appoint(b), fg='blue').grid(row=0, column=i)
                else:
                    tk.Label(self.labelframe, text=titles[i]).grid(row=0, column=i)
                for j in range(len(titles)):
                    tk.Label(self.labelframe, text=rows[x][j]).grid(row=1, column=j)
    
    def cancel_appoint(self, c):
        appointmentid = c
        print(appointmentid)
        self.connect_to_db()
        sql = ''' UPDATE Appointments SET patientid = ?, available = ? WHERE appointmentid = ?'''
        info = (None, 'yes', appointmentid)
        cursor.execute(sql, info)
        conn.commit()
        cursor.close()
        conn.close()
        self.parent.destroy()
        
    def book_appoint(self, b):
        appointmentid = b
        print(appointmentid)
        self.connect_to_db()
        sql = ''' UPDATE Appointments SET patientid = ?, available = ? WHERE appointmentid = ?'''
        info = (self.pid, 'no', appointmentid)
        cursor.execute(sql, info)
        conn.commit()
        cursor.close()
        conn.close()
        self.parent.destroy()
        
            
    def connect_to_db(self):
        global conn, cursor
        db_file = connect.db_path(3)
        conn = connect.create_connection(db_file)
        cursor = conn.cursor()
                
if __name__ == '__main__':
    root = tk.Tk()
    titles = ['Appointment date', 'Appointment time', 'GP first name', 'GP last name', 'Cancel']
    rows = [(1, 2, 3, 4, 5), (1, 2, 3, 4, 6)]
    # titles = ['Patient id','Patient first name', 'Patient last name', 'email', 'DOB', 'NHSno', 'active' ]
    # rows = [(1,'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes'), (3, 'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes')]
    Search_results(root, titles, rows)   
    root.mainloop()     
        
        
        
    