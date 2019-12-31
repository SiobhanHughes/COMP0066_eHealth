import os
import sys
import inspect
import pkgutil
import get_path

current = get_path.get_current_dir()
package_dir = get_path.getDir(current, 2)
database_path = os.path.join(package_dir, 'data/eHealth.db')


if __name__ == '__main__':
    print("DB file path:", database_path)