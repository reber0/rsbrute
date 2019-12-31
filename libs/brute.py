#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-31 14:34:20
@LastEditTime: 2019-12-31 15:45:04
'''

from concurrent.futures import ThreadPoolExecutor, TimeoutError,as_completed

class BruteBaseClass(object):
    """BruteForce BaseClass"""
    def __init__(self, targets, thread_num, timeout):
        super(BruteBaseClass, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.unauth_result = list()
        self.flag = True

    def check_unauth(self,host,port):
        pass

    def worker(self,hpup):
        pass

    def run(self):
        ip_port_list = set([(x[0],x[1]) for x in self.targets])
        for ip,port in ip_port_list:
            self.check_unauth(ip,port)

        try:
            with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
                for host,port,user,pwd in self.targets:
                    if host not in self.unauth_result:
                        f = executor.submit(self.worker,(host,port,user,pwd))
                        # f.add_done_callback(call_back)
        except KeyboardInterrupt:
            print('user aborted !')
            self.flag = False

