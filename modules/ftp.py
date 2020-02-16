#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-02-16 18:37:07
'''

from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor

try:
    from libs.brute import BruteBaseClass
except ModuleNotFoundError:
    from Rsbrute.libs.brute import BruteBaseClass

class FtpBruteForce(BruteBaseClass):
    """FtpBruteForce"""

    def check_unauth(self,host,port):
        if self.flag:
            try:
                ftp = FTP()
                ftp.connect(host, port, timeout=self.timeout)
                ftp.login()
            except Exception as e:
                hook_msg((False,host,port, "Anonymous", ""))
                # print(str(e))
            else:
                hook_msg((True,host,port,"Anonymous",""))
                self.unauth_result.append(host)
            finally:
                ftp.close()

    def worker(self,hpup):
        host,port,user,pwd = hpup
        if self.flag:
            try:
                ftp = FTP()
                ftp.connect(host, port, timeout=self.timeout)
                ftp.login(user=user, passwd=pwd)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                ftp.close()


bruter = FtpBruteForce

