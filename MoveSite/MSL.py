from movesiteutils import MovesiteUtils
import os.path

""" Set environment """

place = os.path.normpath('/var/www/html')
agurk = 'agurk4.agurk.dk'
agurkuser = 'rkupv'
backupsdir = '/home/rkupv/drush-backups'
keyfile = os.path.normpath('/home/rkupv/.ssh/id_rsa')
mysqluser = 'rkupv'
mysqlpw = 'LarsMarianne'
drush = os.path.normpath('/home/rkupv/.composer/vendor/bin/drush')
usergroup = 'rkupv:www-data'

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

print('Calling Drush ...')

msu.localcommand([drush,\
'archive-restore', restoredir,\
'--destination=' + restoreto,\
'--overwrite',\
'--db-su=' + mysqluser,\
'--db-su-pw=' + mysqlpw])

# Set owner and mode
msu.localcommand(['sudo','chown','-R', usergroup, place])
msu.localcommand(['sudo','chmod','-R','0770',place])









