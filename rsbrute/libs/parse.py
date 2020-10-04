#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-26 00:10:17
@LastEditTime : 2020-02-16 18:20:14
'''

import re
import socket
import argparse
from IPy import IP

class ParserCmd(object):
    """ParserCmd"""
    def __init__(self):
        super(ParserCmd, self).__init__()
        self.parser = self.my_parser()
        self.args = self.parser.parse_args().__dict__


    def my_parser(self):
        '''使用说明'''
        service_type_list = [
            "ssh","ftp", #telent,rlogin
            "mysql","mssql","oracle","pgsql","redis","mongodb","memcache",
            "ldap","winrm", #"vnc","rdp","smb","snmp"
            # "smpt","pop",
        ]
        example = """Examples:
                          \r  python3 {shell_name} -s ssh -i 59.108.35.123
                          \r  python3 {shell_name} -s ssh -i 192.168.3.123 -l root -p 123456
                          \r  python3 {shell_name} -s ssh -i 192.168.3.123 -l root -P pwd_dict.txt
                          """

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,#使 example 可以换行
            add_help=True,
            # description = "常见服务口令爆破",
            )
        parser.epilog = example.format(shell_name=parser.prog)
        parser.add_argument("-i", dest="ip", type=str, 
                            help="target ip")
        parser.add_argument("-iL", dest="ip_file", type=str, 
                            help="load target from file, one ip per line")
        parser.add_argument("-ip", dest="ip_port_file", type=str, 
                            help="load target from file, colon separated \"ip:port\" format")
        parser.add_argument("--port", dest="port", type=int, 
                            help="define a non-default port for the service")

        parser.add_argument("-l", dest="user", type=str, 
                            help="specify a user name")
        parser.add_argument("-p", dest="pwd", type=str, 
                            help="specify a password")
        parser.add_argument("-L", dest="user_file", type=str, 
                            help="load several usernames from file")
        parser.add_argument("-P", dest="pwd_file", type=str, 
                            help="load several passwords from file")
        parser.add_argument("-C", dest="user_pwd_file", type=str, 
                            help="colon separated \"login:pass\" format, instead of -L/-P")

        parser.add_argument("-s", dest="service_type", type=str, required=True, 
                            choices=service_type_list, help="the type of service to scan")
        parser.add_argument("-t", dest="thread_num", type=int, default=10, 
                            help="the number of threads, default is 10")
        parser.add_argument("-T", dest="timeout", type=int, default=10, 
                            help="wait time per login attempt over all threads, default is 10s")
        # args = parser.parse_args()
        # parser.print_help()

        return parser

    @staticmethod
    def init():
        parser = ParserCmd()
        return parser.args

class ParseTarget(object):
    """ParseTarget"""
    def __init__(self):
        super(ParseTarget, self).__init__()
        self.ip_list = list()

    def parse_target(self, targets):
        # ["10.17.1.1/24", "10.17.2.30-55", "10.111.22.12"]

        if isinstance(targets, list):
            for target in targets:
                ips = self.parse_ip(target)
                self.ip_list.extend(ips)
        elif isinstance(targets, str):
            ips = self.parse_ip(targets)
            self.ip_list.extend(ips)
        
        return self.ip_list

    def parse_ip(self, target):
        # 10.17.1.1/24 or 10.17.2.30-55 or 10.111.22.12

        ip_list = list()
        #校验target格式是否正确
        m1 = re.match(r'\d{1,3}(\.\d{1,3}){3}/(1[6789]|2\d|3[012])$', target)
        m2 = re.match(r'\d{1,3}(\.\d{1,3}){3}-\d{1,3}$', target)
        m3 = re.match(r'\d{1,3}(\.\d{1,3}){3}$', target)
        if m1:
            ip_list = [str(x) for x in IP(target, make_net=1)]
        elif m2:
            prev = ".".join(target.split('.')[:3])
            st,sp = target.split('.')[-1].split('-')
            for x in range(int(st),int(sp)+1):
                ip_list.append(prev+"."+str(x))
        elif m3:
            ip_list.append(target)
        else:
            error_msg = "IP {} invalid format".format(target)
            raise Exception(error_msg)

        ips = [ip for ip in sorted(set(ip_list),key=socket.inet_aton)]
        return ips

if __name__ == "__main__":
    pt = ParseTarget()
    # print(pt.parse_target("123.123.123.123/29"))
    print(pt.parse_target(["123.123.123.123/30","1.1.1.1-4"]))
