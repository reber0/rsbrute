#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-02-16 18:38:26
'''

import psycopg2

from .baseclass import BruteBaseClass

class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self, payload):
        if self.flag:
            host,port,user,pwd = payload
            try:
                # conn = psycopg2.connect(database="rscan", host=host, port=port, user=user, password=pwd,
                #                         connect_timeout=self.timeout)
                conn = psycopg2.connect(host=host, port=port, user=user, password=pwd,
                                        connect_timeout=self.timeout)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                conn.close()
