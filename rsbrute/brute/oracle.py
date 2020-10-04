#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-02-16 18:38:16
'''

import socket
import cx_Oracle

from .baseclass import BruteBaseClass

class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self, payload):
        if self.flag:
            socket.setdefaulttimeout(self.timeout)
            host,port,user,pwd,sid = payload

            dsn = cx_Oracle.makedsn(host=host, port=port, sid=sid)
            try:
                conn = cx_Oracle.connect(user, pwd, dsn, encoding="UTF-8", threaded = True)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd),sid)
                conn.close()
