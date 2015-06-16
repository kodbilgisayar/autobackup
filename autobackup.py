#!/usr/bin/env python3

import pfsense
import freenas
import esxi

###
# Set the host names of your machines here 
# Make sure the machine running this script has passwordless access to each of them.
###
PFSENSE_HOSTNAMES = ['pfsense.example.org', 'firewall.example.org']
FREENAS_HOSTNAMES = ['freenas.example.org', 'backup.example.org']
ESXI_HOSTNAMES = ['esxi.example.org']
#MUST BE AN ABSOLUTE PATH
OUTPUT_PATH = '/home/backup/'

def backup():
    for host in PFSENSE_HOSTNAMES:
        pfsense.backup(host, OUTPUT_PATH)
	
    for host in FREENAS_HOSTNAMES:
        freenas.backup(host, OUTPUT_PATH)
	
    for host in ESXI_HOSTNAMES:
        esxi.backup(host, OUTPUT_PATH)

if __name__ == '__main__':
    backup()
