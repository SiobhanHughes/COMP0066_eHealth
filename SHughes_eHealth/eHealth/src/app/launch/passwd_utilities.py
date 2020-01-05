import re
import os
import hashlib
import binascii

def strong_passwd(passwd):
    if len(passwd) < 8:
        #print('too short)
        return 'weak'
    elif not re.match(r'.*[0-9].*', passwd):
        #print('no number')
        return 'weak' 
    elif not re.match(r'.*[A-Z].*', passwd):
        #print('no capital')
        return 'weak'
    elif not re.match(r'.*[!@£$%^&*()_+={}?:~+\[\]].*', passwd):
        #print('no special character')
        return 'weak'
    else:
        #print('good password')
        return 'strong'

# To hash protect password, code was used from: https://www.vitoshacademy.com/hashing-passwords-in-python/
  
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
   


if __name__ == '__main__':
    password = input('Enter password to test: ')
    print(strong_passwd(password))