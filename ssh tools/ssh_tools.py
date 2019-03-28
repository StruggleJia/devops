#!/usr/bin/env python
# coding:utf-8
# code by struggle

import threadpool
import paramiko
import os
import sys
import logging

sshlogs = 'ssh_tools.log'
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(filename=sshlogs, format=log_format, datefmt='%Y-%m-%d %H:%M:%S %p', logmode='a', level=logging.INFO)


class SSH(object):
    def __init__(self, serinfo):
        self.ip = serinfo[0]
        self.port = serinfo[1] 
        self.user = serinfo[2]
        self.pw = serinfo[3]
        self.cmd = serinfo[4]
        try:
            self.sshclient = paramiko.SSHClient()
            self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.sshclient.connect(self.ip, int(self.port), username=self.user, password=self.pw,allow_agent=False, look_for_keys=False)
        except Exception as e:
            logging.error('ssh_connect failed,err is %s' % e)
    
    def __del__(self):
        pass

    def command(self):
        try:
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            try:
            	outputerror = stderr.readlines()[0]
            except:
                outputerror = ''

            if outputerror:
                return outputerror
            else:
                output = ''.join(str(i) for i in stdout.readlines())
		if output:
		    return output
                else:
                    return 'command not output\n'
        except Exception as e:
            logging.error('ssh_command failed,err is %s' % e)


    def sftp(self, localfile, remotefile):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.sshclient.get_transport())
            sftp = self.sshclient.open_sftp()
            sftp.put(localfile, remotefile)
        except Exception as e:
            logging.error('ssh_sftp failed,err is %s' % e)


def f(file):
    all_server = []
    try:
        ff = open(file).readlines()
        for i in ff:
            i = i.replace('\n', '')
            serverinfo = i.split(" ")[:4]
            commandinfo = i.split(" ")[4:]
            serverinfo.append(" ".join(commandinfo))
            all_server.append(serverinfo)
        return all_server
    except Exception as e:
        logging.error('openfile failed,err is %s' % e)

if __name__ == '__main__':
    pass

'''
example
import ssh_tools as t
serverinfo = t.f('aaa.txt') 
for i in serverinfo:
    i[4] = "uname -a"
    conn = t.SSH(i)
    print i[0] + "\n " + conn.command()


'''

