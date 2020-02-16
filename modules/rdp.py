#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-31 15:54:41
'''

from subprocess import Popen, PIPE, STDOUT
from concurrent.futures import ThreadPoolExecutor

try:
    from libs.brute import BruteBaseClass
except ModuleNotFoundError:
    from Rsbrute.libs.brute import BruteBaseClass

class RdpBruteForce(BruteBaseClass):
    """RdpBruteForce"""

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            command = "xfreerdp /sec:nla /p:{} /u:{} /port:{} /v:{} /cert-ignore "
            p = Popen(command, shell=True)
            p.communicate()
        except Exception as e:
            logger.error(str(e))
        else:
            logger.info("[OK] {} {} {} {}".format(host, port, user, pwd))
            self.result.append((host, port, user, pwd))
        finally:
            conn.close()

    def run(self):
        logger.info("Module RdpBruteForce is Developing...")


bruter = RdpBruteForce
