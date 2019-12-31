#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-31 15:55:43
'''

import socket
import cx_Oracle
from concurrent.futures import ThreadPoolExecutor
from libs.brute import BruteBaseClass

class OracleBruteForce(BruteBaseClass):
    """OracleBruteForce"""

    def worker(self,hpup):
        socket.setdefaulttimeout(self.timeout)

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


bruter = OracleBruteForce
