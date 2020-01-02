#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2020-01-02 12:52:50
'''

import pymssql
from concurrent.futures import ThreadPoolExecutor
from libs.brute import BruteBaseClass

class MsSQLBruteForce(BruteBaseClass):
    """MsSQLBruteForce"""

    def worker(self,hpup):
        if self.flag:
            host,port,user,pwd = hpup
            try:
                conn = pymssql.connect(host=host,port=port,user=user,password=pwd,
                                    database="master",timeout=self.timeout,charset="utf8")
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
                # logger.error(str(e))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                conn.close()

bruter = MsSQLBruteForce

