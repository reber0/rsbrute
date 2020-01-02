#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-26 21:48:38
@LastEditTime: 2020-01-02 12:52:11
'''

from pymemcache.client.base import Client
from concurrent.futures import ThreadPoolExecutor
from libs.brute import BruteBaseClass


class MemcacheBruteForce(BruteBaseClass):
    """MemcacheBruteForce"""

    def check_unauth(self,host,port):
        if self.flag:
            try:
                memcache = Client(server=(host,port), connect_timeout=self.timeout, timeout=self.timeout)
                version = memcache.version()
            except Exception as e:
                hook_msg((False,host,port, "Anonymous", ""))
                # print(str(e))
            else:
                if version:
                    hook_msg((True,host,port, "Anonymous", ""))
                    self.unauth_result.append(host)
            finally:
                memcache.close()

    def worker(self,hpup):
        if self.flag:
            host,port,user,pwd = hpup
            try:
                memcache = Client(server=(host,port), connect_timeout=self.timeout, timeout=self.timeout)
                version = memcache.version()
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
                logger.error(str(e))
            else:
                hook_msg((True,host,port, "Anonymous", ""))
                self.result.append((host, port, user, pwd))
            finally:
                memcache.close()


bruter = MemcacheBruteForce

