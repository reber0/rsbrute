#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-26 14:00:25
@LastEditTime: 2019-12-31 16:50:56
'''

import socket
import winrm
from concurrent.futures import ThreadPoolExecutor
from libs.brute import BruteBaseClass


class WinrmBruteForce(BruteBaseClass):
    """WinrmBruteForce"""

    def worker(self,hpup):
        socket.setdefaulttimeout(self.timeout)

        host,port,user,pwd = hpup
        try:
            s = winrm.Session("http://{}:{}/wsman".format(host,port),auth=(user,pwd))
            r = s.run_cmd("whoami")
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            hook_msg((True,host,port,user,pwd))
        finally:
            ssh.close()


bruter = WinrmBruteForce

