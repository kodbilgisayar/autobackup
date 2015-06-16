# Autobackup
Automated backup scripts for pfSense, ESXi and FreeNAS

pfSense, FreeNAS and ESXi all have methods of backing up and restoring configuration files. These scripts make it easy to pull and store them in a central location. If you tell the script to download the files to a directory that already contains backups, it will only add a new file if the configuration has changed.

To run the script, enter the hostnames of your machines and the path where you want to store the backups in autobackup.py. Then execute autobackup.py. The machine running the script must have passwordless access to all the machines you are backing up.

## dependencies
python3
