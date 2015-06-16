#!/usr/bin/env python3

from subprocess import call
from subprocess import check_output
from tempfile import mkdtemp
from os import path

def backup(pfSenseHostname, outputPath):
    #pull backup configuration from pfsense
    remotePath = 'root@' + pfSenseHostname + ':/cf/conf/backup/config-*'
    tmpDir = mkdtemp() + '/'
    outputDirectory = outputPath + '/' + pfSenseHostname + '/'

    call(['scp', remotePath, tmpDir])

    #determines whether there are new configuration files, and if so, adds them to the output directory.
    #this is done so that in the event that the configuration files are corrupted, the old files remain.
    
    #check which files are in each folder
    contentsOfTmpDir = check_output(['ls', tmpDir], universal_newlines=True)
    if path.isdir(outputDirectory):
        oldConfFiles = check_output(['ls', outputDirectory], universal_newlines=True)

        #we need an iterable set of the files in the current output folder and the ones we just downloaded
        setOfTmpFiles = set(contentsOfTmpDir.split('\n'))
        setOfOldConfFiles = set(oldConfFiles.split('\n'))
        
        #now we take the difference of those files to see if we have any newly downloaded files.
        setOfTmpFiles.difference_update(setOfOldConfFiles)
    else:
        #if no files exist in the output directory, move them all over
        setOfTmpFiles = set(contentsOfTmpDir.split('\n'))
        call(['mkdir', '-p', outputDirectory])
    #move the new files over
    for i in setOfTmpFiles:
        call(['cp', tmpDir + i, outputDirectory])

    call(['rm', '-rf', tmpDir])
