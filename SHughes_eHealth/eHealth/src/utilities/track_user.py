import pickle
import get_path_utilities as path

""" This module is used to track the current user that is logged in.
    Details of the user are stored in a dictionary - used to manipulate data from the eHealth.db database
    The dictionary (user.pickle) is stored in the data directory while the user is logged in.
    When the user logs out, user.pickle is deleted."""

#store dictionary in data directory
def store(user, num):
    file = path.dataDir_path("user.pickle", num)
    pickling_on = open(file,"wb")
    pickle.dump(user, pickling_on)
    pickling_on.close()

#load dictionary into current module
def load(user, num):
    file = path.dataDir_path("user.pickle", num)
    pickle_off = open(file,"rb")
    user = pickle.load(pickle_off)
    return user


if __name__ == "__main__":
    emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
    store(emp, 2)
    emp = load(emp, 2)
    print(emp)
    path.delete_from_dataDir("user.pickle", 2)