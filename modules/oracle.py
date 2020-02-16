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
from concurrent.futures import ThreadPoolExecutor

try:
    from config import dict_path
    from libs.utils import get_content
    from libs.brute import BruteBaseClass
except ModuleNotFoundError:
    from Rsbrute.config import dict_path
    from Rsbrute.libs.utils import get_content
    from Rsbrute.libs.brute import BruteBaseClass


class OracleBruteForce(BruteBaseClass):
    """OracleBruteForce"""

    def guess_sid(self,host,port):
        """
        ORA-01017 用户名或密码不对
        ORA-12505 sid不正确
        """

        sid_filename = dict_path.joinpath("sid.txt")
        sid_list = get_content(sid_filename)
        for sid in sid_list:
            dsn = cx_Oracle.makedsn(host=host, port=port, sid=sid)
            try:
                connection = cx_Oracle.connect("sys", "123", dsn, encoding="UTF-8")
            except cx_Oracle.DatabaseError as e:
                code = e.args[0].code
                message = e.args[0].message
                if code == 1017:
                    return sid

    def worker(self,hpup):
        if self.flag:
            socket.setdefaulttimeout(self.timeout)
            host,port,user,pwd = hpup

            sid = self.guess_sid(host,port)
            if sid:
                dsn = cx_Oracle.makedsn(host=host, port=port, sid=sid)
                try:
                    conn = cx_Oracle.connect(user, pwd, dsn, encoding="UTF-8", threaded = True)
                except Exception as e:
                    hook_msg((False,host,port,user,pwd))
                else:
                    hook_msg((True,host,port,user,pwd))
                    conn.close()


bruter = OracleBruteForce
