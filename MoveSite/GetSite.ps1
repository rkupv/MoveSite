#
# Get Site from agurk4 and install under xampp
# Parameter is site, default peter
#
$site = $args[0]
if (! $site) {$site = "gretel1"}
$pv = Get-Credential -UserName rkupv -Message NoPassword
$keyfile = "D:\rkupv\Google\Home\Data\peter\Codes\PuTTY\PuTTYprivateForOpenssh.ppk"
$localfile = "E:\xampp\htdocs\rkupv\DrushBackups\$site.gz"
$sitedir =   "E:\xampp\htdocs\rkupv"
$s = New-SSHSession -ComputerName agurk4.agurk.dk -Credential $pv -KeyFile $keyfile -verbose -debug
$grepcmd = "grep $site"
$file = invoke-sshcommand -command "cd drush-backups;ls -t|$grepcmd | sed 1q | head -c -1" -index $s.index
$remotefile = "/home/rkupv/drush-backups/" + $file.output
#
# Initialise htdocs
#
rm  -ErrorAction:SilentlyContinue $localfile 
rm  -ErrorAction:SilentlyContinue -Recurse $sitedir/$site
mkdir $sitedir/$site
#
# Get the drush backup from agurk4
#
Get-SCPFile -LocalFile $localfile -RemoteFile $remotefile -ComputerName "agurk4.agurk.dk" -Credential $pv -KeyFile $keyfile 
#
# Close connection
#
Remove-SSHSession -index $s.index 
#
# Start MySQL
start-job {cd "E:\xampp\mysql\bin"; mysqld.exe}
#
# Install Site
#
cd $sitedir; 
#
drush -v archive-restore $localfile --overwrite --db-su=rkupv --db-su-pw=LarsMarianne
cd C:\Users\rkupv\OneDrive\Documents\WindowsPowerShell
