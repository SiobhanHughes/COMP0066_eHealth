import os
import sys
import inspect

def get_current_dir():
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    current_path = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    return current_path

def get_parent_dir(current_path):
    parent_dir_path = os.path.abspath(os.path.join(current_path, os.pardir))
    return parent_dir_path

#get absolute file path any number of levels up from current file path
#pass absolute current file path and levels up as args
def getDir(path, level=1):
  return os.path.normpath( os.path.join(path, *([".."] * level)) )

#insert absolute file path into sys.path - python will search here (position 0 in path list) first to import packages and modules
def insert_dir(dir_path):
    sys.path.insert(0, dir_path)

#delete file path once after imports from eHealth (revert to original file path lists for sys.path)
def delete_dir():
    del sys.path[0]

if __name__ == '__main__':
    print(sys.path)
    print(" ")
    current_path = get_current_dir()
    print(current_path)
    parent_path = get_parent_dir(current_path)
    print(parent_path)
    insert_dir(parent_path)
    print(" ")
    print(sys.path)
    print(" ")
    delete_dir()
    print(sys.path)
    print(" ")
    get_dir_2up = getDir(current_path, 2)
    print(get_dir_2up)
    insert_dir(get_dir_2up)
    print(" ")
    print(sys.path)