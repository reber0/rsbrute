#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-05-22 15:30:07
@LastEditTime : 2020-02-16 18:34:28
'''

import paramiko

from .baseclass import BruteBaseClass

# from rsbrute.libs.data import config
# paramiko.util.log_to_file(config.code_path.joinpath("log/paramiko.log"))

class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self, payload):
        if self.flag:
            host,port,user,pwd = payload
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
