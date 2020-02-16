#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-02-16 18:38:26
'''

import psycopg2
from concurrent.futures import ThreadPoolExecutor

try:
    from libs.brute import BruteBaseClass
except ModuleNotFoundError:
    from Rsbrute.libs.brute import BruteBaseClass

class PgSQLBruteForce(BruteBaseClass):
    """PgSQLBruteForce"""

    def worker(self,hpup):
        if self.flag:
            host,port,user,pwd = hpup
            try:
                conn = psycopg2.connect(host=host,port=port,user=user,password=pwd,
                                        connect_timeout=self.timeout)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
                # logger.error(str(e))
            else:
                hook_msg((True,host,port,user,pwd))
                # self.result.append((host, port, user, pwd))
            finally:
                conn.close()

bruter = PgSQLBruteForce

