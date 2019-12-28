#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-13 16:36:14
'''

import socket
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

class MongoDBBruteForce(object):
    """MongoDBBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(MongoDBBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.unauth_result = list()

    def check_unauth(self,host,port):
        try:
            mongo = MongoClient(host=host,port=port,serverSelectionTimeoutMS=self.timeout)
            dblist = mongo.list_database_names()
        except Exception as e:
            hook_msg((False,host,port,"Anonymous",""))
            # print(str(e))
        else:
            hook_msg((True,host,port,"Anonymous",""))
            self.unauth_result.append(host)
        finally:
            mongo.close()

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            mongo = MongoClient(host=host,port=port,username=user,password=pwd,
                                authSource='admin',serverSelectionTimeoutMS=self.timeout)
            dblist = mongo.list_database_names()
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            hook_msg((True,host,port,user,pwd))
        finally:
            mongo.close()
    
    def run(self):
        socket.setdefaulttimeout(self.timeout)

        ip_port_list = set([(x[0],x[1]) for x in self.targets])
        for ip,port in ip_port_list:
            self.check_unauth(ip,port)

        with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
            for host,port,user,pwd in self.targets:
                if host not in self.unauth_result:
                    f = executor.submit(self.worker,(host,port,user,pwd))
                # f.add_done_callback(call_back)


bruter = MongoDBBruteForce

