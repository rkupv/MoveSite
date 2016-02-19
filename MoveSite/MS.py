MoveSite version for Windows 10

from movesiteutils import MovesiteUtils
import os.path

""" Set environment """

place = os.path.normpath('E:/xampp/htdocs/rkupv')
agurk = 'agurk4.agurk.dk'
agurkuser = 'rkupv'
backupsdir = '/home/rkupv/drush-backups'
keyfile = os.path.normpath('D:/rkupv/Google/Home/Data/peter/Codes/PuTTY/PuTTYprivateForOpenssh.ppk')
mysqluser = 'rkupv'
mysqlpw = 'LarsMarianne'
drush = os.path.normpath('C:/Users/rkupv/AppData/Roaming/Composer/vendor/drush/drush/drush.bat')

# Get desired site name
while True:
    site = input("Please type Web sitename, either lillan or gretel1:\n")
    site=site.strip()
    if site in ('lillan', 'gretel1'):
        break

msu = MovesiteUtils()

# Connect
msu.connect(agurk, agurkuser, keyfile)

# Get filename
shells = "cd drush-backups;ls -t | " + "grep " + site + " | sed 1q | head -c -1"
stdin, stdout, stderr = msu.ssh.exec_command(shells)
output = stdout.read()
archivename = output.decode("utf-8")

# Get file if needed
restoredir = os.path.normpath(place + '/' + archivename)
restoreto = os.path.normpath(place + '/' + site)

if not os.path.exists(restoredir):
    print('Fetching archive ...')
    msu.getremote(backupsdir + '/' + archivename, restoredir)
else:
    print('Archive exists')

#       Assure that MySQL is active
while True:
    (exitcode, stdout, stderr) = msu.localcommand(['tasklist', '/nh', '/fi', "IMAGENAME eq mysqld.exe"])
    s = stdout.decode("utf-8")
    if s[0:5] == "INFO:":
        print('Please start MySQL from XAMPP Control Panel')
        print('Type RETURN when done')
        input()
    else: break

print('Calling Drush ...')
(exitcode, stdout, stderr) = msu.localcommand([drush, "-v",
                 "archive-restore", restoredir,
                 "--destination=" + restoreto,
                 "--overwrite",
                 "--db-su=" + mysqluser,
                 "--db-su-pw=" + mysqlpw])










