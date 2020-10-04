#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-31 14:34:20
@LastEditTime : 2020-06-01 15:37:12
'''

from rsbrute.libs.data import config

from concurrent.futures import ThreadPoolExecutor


class BruteBaseClass(object):
    """BruteForce BaseClass"""
    def __init__(self, payloads, timeout, thread_num):
        super(BruteBaseClass, self).__init__()
        self.payloads = payloads
        self.timeout = timeout
        self.unauth_result = list()
        self.flag = True
        self._set_thread(thread_num)

    def _set_thread(self, thread_num):
        if len(self.payloads) < thread_num:
            self.thread_num = len(self.payloads)
        else:
            self.thread_num = thread_num

    def check_unauth(self,host,port):
        pass

    def worker(self, payload):
        pass

    def run(self):
        ip_port_list = set([(x[0],x[1]) for x in self.payloads])
        try:
            with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
                for ip,port in ip_port_list:
                    f = executor.submit(self.check_unauth, ip, port)
        except KeyboardInterrupt:
            config.logger.error('user aborted !')
            self.flag = False

        try:
            with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
                for payload in self.payloads:
                    if payload[0] not in self.unauth_result:
                        # print(host,port,user,pwd)
                        f = executor.submit(self.worker, payload)
                        # f.add_done_callback(call_back)
        except KeyboardInterrupt:
            config.logger.error('user aborted !')
            self.flag = False

