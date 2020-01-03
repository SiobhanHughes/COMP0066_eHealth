import pickle
import get_path_utilities as path



def store(user):
    file = path.dataDir_path("user.pickle")
    pickling_on = open(file,"wb")
    pickle.dump(user, pickling_on)
    pickling_on.close()

def load(user):
    file = path.dataDir_path("user.pickle")
    pickle_off = open(file,"rb")
    user = pickle.load(pickle_off)
    return user


if __name__ == "__main__":
    emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
    store(emp)
    emp = load(emp)
    print(emp)
    path.delete_from_dataDir("user.pickle")