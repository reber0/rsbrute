#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-10-28 16:02:07
'''

class RloginBruteForce(object):
    """RloginBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(RloginBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.result = list()
        print("RloginBruteForce...")
    
    def worker(self):
        pass
    
    def run(self):
        logger.info("Module RloginBruteForce is Developing...")
        pass

bruter = RloginBruteForce
