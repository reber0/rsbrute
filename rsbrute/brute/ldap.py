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
from ldap3 import Server, Connection, ALL

from .baseclass import BruteBaseClass

class BruteForce(BruteBaseClass):
    """BruteForce"""

    def check_unauth(self, host, port):
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
                print(str(e))
            else:
                if "invalid" in str(result):
                    hook_msg((True,host,port,"Anonymous",""))
                    self.unauth_result.append(host)
            finally:
                s.close()

    def worker(self, payload):
        if self.flag:
            host, port, user, pwd = payload
            try:
                # 123.123.123.123 389 domain\\user password
                server = Server(host=host, port=port, use_ssl=False, connect_timeout=self.timeout, get_info='ALL')
                conn = Connection(server, user=user, password=pwd, check_names=True, lazy=False,
                              auto_bind=True, receive_timeout=self.timeout, authentication="NTLM")
                # whoami = conn.extend.standard.who_am_i()
                # print(whoami)
            except Exception as e:
                hook_msg((False,host,port,user,pwd))
            else:
                hook_msg((True,host,port,user,pwd))
            finally:
                conn.unbind()
                server.close()

#python3 rsbrute.py -s ldap -i 10.11.11.5 -l 'reber.com\administrator' -p Aa123456.
