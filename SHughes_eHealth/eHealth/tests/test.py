import os, sys, inspect
print(sys.path)
print(" ")

def get_parent_dir():

    #Following lines are for assigning parent directory dynamically.

    #dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    print(dir_path)

    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    print(parent_dir_path)

    sys.path.insert(0, parent_dir_path)

get_parent_dir()
print(sys.path)
print(' ')

from src.database import db_path

print("DB file path:", db_path.database_path)