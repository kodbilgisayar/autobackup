#!/usr/bin/env python3

from random import SystemRandom
import string
from hashlib import md5
from os import path

def hashFile(filename):
    BUFFER_SIZE = 65536
    #hashes a file
    #code mostly taken from stackoverflow because I don't know that much about hashing
    File = open(filename, 'rb')
    filehash = md5()

    while True:
            data = File.read(BUFFER_SIZE)
            if not data:
                break
            filehash.update(data)
    
    File.close()
    
    return filehash.hexdigest()

def areFilesEqual(file1, file2):
   return hashFile(file1) == hashFile(file2)

def randomString(digits):
    return ''.join(SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(digits))
