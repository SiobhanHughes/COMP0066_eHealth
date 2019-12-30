import os.path

package_dir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(package_dir, 'ehealth.db')


if __name__ == '__main__':
    print(database_path)