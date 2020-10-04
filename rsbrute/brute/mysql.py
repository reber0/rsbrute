#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-31 15:38:54
'''

import pymysql

from .baseclass import BruteBaseClass

class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self, payload):
        host,port,user,pwd = payload
        if self.flag:
            try:
                conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd,
                                    connect_timeout=self.timeout, charset="utf8")
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                conn.close()
