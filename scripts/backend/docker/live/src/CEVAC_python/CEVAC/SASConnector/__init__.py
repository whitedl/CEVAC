#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
from CEVAC.config import config as cf
import paramiko
import os

class SASConnector:
    from ._execute import execute, runsas
    from ._upload import upload
    def __init__(self, username=cf['SASConnector']['username'], password=cf['SASConnector']['password'],
            host=cf['SASConnector']['host'], port=cf['SASConnector']['port']):
        self.host = host
        self.runsas = cf['SASConnector']['runsas']
        self.autoload = cf['SASConnector']['autoload']
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if not os.path.isfile(os.path.expanduser('~/.ssh/id_rsa')):
            os.system('ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa')
        k = paramiko.RSAKey.from_private_key_file(os.path.expanduser('~/.ssh/id_rsa'))
        try:
            print('Attempting to connect with private key...')
            self.ssh.connect(self.host, port=port, username=username, pkey=k)
        except:
            print('Failed to connect with private key. Connecting with password and deploying key')
            self.ssh.connect(self.host, port=port, username=username, password=password)
            self.deploy_key()
        else:
            print('Successfully logged in')
    
    def deploy_key(self):
        key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
        self.ssh.exec_command('mkdir -p ~/.ssh/')
        self.ssh.exec_command(f'echo "{key}" >> ~/.ssh/authorized_keys')
        self.ssh.exec_command('chmod 644 ~/.ssh/authorized_keys')
        self.ssh.exec_command('chmod 700 ~/.ssh/')

