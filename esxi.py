#!/usr/bin/env python3

##python script to pull esxi backups.
##written by Ian Moore for Practichem

from subprocess import call
from subprocess import check_output
from tempfile import mkdtemp
from datetime import date
from os import path
import util

def backup(esxiHostname, outputPath):
    #pull backup configuration from esxi
    
    tmpDir = mkdtemp()
    outputDirectory = outputPath + '/' + esxiHostname + '/'
    downloadedConfig = tmpDir + '/esxi-' + date.today().isoformat() + '-' + util.randomString(5) + '.tgz'
    backupCommands = 'vim-cmd hostsvc/firmware/backup_config'

    #make the backup on esxi
    backupOutput = check_output(['ssh', 'root@' + esxiHostname, backupCommands])
    
    #ESXi makes the backup file available at a URL
    #these operations strip the command's output down to just the URL
    backupOutput = backupOutput.decode('UTF-8').rstrip('\n')
    backupOutput = backupOutput.split(' ').pop().replace('*', esxiHostname)
   
    #download the file to the tmp directory
    call(['wget', '-O', downloadedConfig, backupOutput, '--no-check-certificate'])

    #checks for changes to the configuration and moves the file if there are.
    #get the current backups sorted by date
    if path.isdir(outputDirectory):
        latestConfigFile = check_output(['ls', '-t', outputDirectory], universal_newlines=True).split('\n').pop(0)
    else:
        call(['mkdir', '-p', outputDirectory])
        latestConfigFile = None
    #if there's nothing in the directory, backup the file
    if latestConfigFile is None:
        call(['cp', downloadedConfig, outputDirectory])
    #if there are files in the directory, we need to check and see if there have been any changes to the config
    #by taking a hash of it and comparing it to the current file
    elif not util.areFilesEqual(outputDirectory + latestConfigFile, downloadedConfig):
        call(['cp', downloadedConfig, outputDirectory])
    
    call(['rm', '-rf', tmpDir])
