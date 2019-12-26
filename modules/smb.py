#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-23 21:28:37
'''

class SmbBruteForce(object):
    """SmbBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(SmbBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.result = list()
        print("SmbBruteForce...")
    
    def worker(self):
        pass
    
    def run(self):
        logger.info("Module SmbBruteForce is Developing...")
        pass


bruter = SmbBruteForce
