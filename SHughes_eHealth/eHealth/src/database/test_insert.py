import sqlite3
from sqlite3 import Error

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import connect
import db_utilities as db


only_date = date.today()
time = datetime.now()
only_time = time.time()
appoint = (1, only_date, only_time)

print(appoint)
database = connect.db_path(2)
conn = connect.create_connection(database)
db.insert_appointment(conn, appoint)