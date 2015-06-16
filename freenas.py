#!/usr/bin/env python3

from subprocess import call
from subprocess import check_output
from datetime import date
from tempfile import mkdtemp
from os import path
import util

def backup(freenasHostname, outputPath):
    #pull backup configuration from pfsense
    remotePath = 'root@' + freenasHostname + ':/data/freenas-v1.db'
    outputDirectory = outputPath + '/' + freenasHostname + '/'
    tmpDir = mkdtemp()
    downloadedConfig = tmpDir + '/freenas-' + date.today().isoformat() + '-' + util.randomString(5) + '.db'

    call(['rsync', remotePath, downloadedConfig])

    #checks for changes to the configuration and moves the file if there are.
    if path.isdir(outputDirectory):
        #this returns the newest config file so it can be compared to the one just downloaded
        latestConfigFile = check_output(['ls', '-t', outputDirectory], universal_newlines=True).split('\n').pop(0)
    else:
        #if there's no directory, make it.
        latestConfigFile = None
        call(['mkdir', '-p', outputDirectory])
    
    #if there's nothing in the directory, backup the file
    if latestConfigFile is None:
        call(['cp', downloadedConfig, outputDirectory])
    #if there are files in the directory, we need to check and see if there have been any changes to the config
    #by taking a hash of it and comparing it to the current file
    elif not util.areFilesEqual(outputDirectory + latestConfigFile, downloadedConfig):
        call(['cp', downloadedConfig, outputDirectory])
    
    #remove the tmp directory
    call(['rm', '-rf', tmpDir])
