import os.path
import sys, inspect
import pkgutil

package_dir = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
#os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(package_dir, 'eHealth.db')


if __name__ == '__main__':
    print("DB file path:", database_path)
    print(sys.path)
    print(' ')
    

    search_path = ['.'] # set to None to see all modules importable from sys.path
    all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
    print("Modules in search path to import")
    print(all_modules)