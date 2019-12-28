#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-26 21:48:38
@LastEditTime: 2019-12-13 16:36:11
'''

from pymemcache.client.base import Client
from concurrent.futures import ThreadPoolExecutor


class MemcacheBruteForce(object):
    """MemcacheBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(MemcacheBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.unauth_result = list()

    def check_unauth(self,host,port):
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

    def run(self):
        ip_port_list = set([(x[0],x[1]) for x in self.targets])
        for ip,port in ip_port_list:
            self.check_unauth(ip,port)

        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                if host not in self.unauth_result:
                    f = executor.submit(self.worker,(host,port,user,pwd))
                # f.add_done_callback(call_back)



bruter = MemcacheBruteForce

