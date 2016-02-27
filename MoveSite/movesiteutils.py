#! /usr/bin/env python3

import subprocess
import paramiko

class MovesiteUtils:

    def connect(self, node, user, keyfile):
        """ set up a connection """
        self.ssh = paramiko.client.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(node, username=user, key_filename=keyfile)

    def remotecommand(self, command):
        """ Execute on remote """
        self.ssh.exec_command(command)

    def getremote(self, file, store):
        """ Get file from remote """
        ftp = self.ssh.open_sftp()
        ftp.get(file, store)
        ftp.close()

    def localcommand(self, command):
        """  Execute on local """
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        exitcode = process.wait()
        return (exitcode, stdout, stderr)


