#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""

def execute(self, command):
    ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
    return ssh_stdin, ssh_stdout, ssh_stderr

def runsas(self):
    return self.execute(self.runsas)
