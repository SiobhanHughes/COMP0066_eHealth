import os
import sys
import inspect

#get the full file path of the current directory
def get_current_dir():
    current_path = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    return current_path

#get the parent directory (one path up)
def get_parent_dir(current_path):
    parent_dir_path = os.path.abspath(os.path.join(current_path, os.pardir))
    return parent_dir_path

#get absolute file path any number of levels up from current file path
#pass absolute current file path (get_current_dir) and levels up as args
def getDir(path, level=1):
  return os.path.normpath( os.path.join(path, *([".."] * level)) )

#insert absolute file path into sys.path - python will search here (position 0 in path list) first to import packages and modules
#insert path to eHealth directory (then can import any package or module)
def insert_dir(dir_path):
    sys.path.insert(0, dir_path)

#delete file path after imports from eHealth (revert to original file path lists for sys.path)
def delete_dir():
    del sys.path[0]

#get the absolute file path to the data directory. 
#Pass interger (num) to indicate the levels up to eHealth directory
#used to store user.pickle in data directory - track current user (logged in)
def dataDir_path(file_name, num):
    current = get_current_dir()
    package_dir = getDir(current, num)
    data_path = os.path.join(package_dir, 'data/' + file_name)
    return data_path

#delete a file from the data directory
#get the absolute file path to the data directory. 
#Pass interger (num) to indicate the levels up to eHealth directory
#used to delet user.pickle in data directory - track current user (logged out)
def delete_from_dataDir(file_name, num):
    file = dataDir_path(file_name, num)
    if os.path.exists(file):
      os.remove(file)
    else:
        print("The file does not exist")

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
    print(dataDir_path('test.py', 2))
    delete_from_dataDir('test.py', 2)
    