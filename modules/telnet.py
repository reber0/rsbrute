#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-09-30 17:07:15
'''

class TelnetBruteForce(object):
    """TelnetBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(TelnetBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.result = list()
        print("TelnetBruteForce...")
    
    def worker(self):
        pass
    
    def run(self):
        pass