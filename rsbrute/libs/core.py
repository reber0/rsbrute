#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-27 15:57:41
@LastEditTime : 2021-03-16 15:27:25
'''

import importlib
import cx_Oracle

from .data import config
from .utils import get_content
from .parse import ParseTarget

service_port_dict = {
    "ssh":22, "ftp":21, "telnet":23, "rlogin":513,
    "mysql":3306, "mssql":1433, "oracle":1521, "pgsql":5432, "redis":6379, "mongodb":27017, "memcache":11211,
    "ldap":389, "winrm":5985, "vnc":5901, "rdp":3389, "smb":445, "snmp":161,
    "smtp":25, "pop":110,
    "tomcat":443,
}

def guess_sid(host, port):
    """
    ORA-01017 用户名或密码不对
    ORA-12505 sid不正确
    """
    config.logger.info("Start enum oracle sid...")
    sid_filename = config.dict_path.joinpath("oracle_sid.txt")
    sid_list = get_content(sid_filename)

    for sid in sid_list:
        dsn = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        try:
            connection = cx_Oracle.connect("sys", "123", dsn, encoding="UTF-8")
        except cx_Oracle.DatabaseError as e:
            code = e.args[0].code
            message = e.args[0].message
            if code == 1017:
                config.logger.error("[*] {}:{} sid: {} right.".format(host,port,sid))
                return sid
            else:
                config.logger.info("[-] {}:{} sid: {} error.".format(host,port,sid))

class GeneratePayload(object):
    """生成目标列表:[(host,port,user,pwd),(host,port,user,pwd)]"""
    def __init__(self):
        super(GeneratePayload, self).__init__()
        self.service_type  = config.get("service_type")
        self.ip            = config.get("ip")
        self.ip_file       = config.get("ip_file")
        self.ip_port_file  = config.get("ip_port_file")
        self.port          = config.get("port")
        self.user_pwd_file = config.get("user_pwd_file")
        self.user_file     = config.get("user_file")
        self.pwd_file      = config.get("pwd_file")
        self.user          = config.get("user")
        self.pwd           = config.get("pwd")

        self.default_user_filename = config.dict_path.joinpath("{}_user.txt".format(self.service_type))
        self.default_pwd_filename = config.dict_path.joinpath("{}_pwd.txt".format(self.service_type))

        self.payloads = list()

    def run(self):
        #得到 payload [(ip,port,user,pwd), (ip,port,user,pwd)]
        user_pwd_list = None

        if self.user and self.pwd:
            user_pwd_list = [(self.user,self.pwd)]
        elif self.user_pwd_file:
            user_pwd_list = self.com_user_pwd(self.user_pwd_file)
        elif self.user_file and self.pwd_file:
            user_pwd_list = self.com_users_pwds(self.user_file, self.pwd_file)
        elif self.user_file and self.pwd:
            user_pwd_list = self.com_users_pwd(self.user_file, self.pwd)
        elif self.user and self.pwd_file:
            user_pwd_list = self.com_user_pwds(self.user, self.pwd_file)
        elif self.user:
            user_pwd_list = self.com_user_pwdfile(self.user)
        elif self.pwd:
            user_pwd_list = self.com_userfile_pwd(self.pwd)
        else:
            user_pwd_list = self.com_users_pwds_from_file()

        ip_port_list = self.com_ip_port()
        for user,pwd in user_pwd_list:
            if self.service_type == "oracle":
                for ip,port,sid in ip_port_list:
                    self.payloads.append((ip, port, user, pwd, sid))
            else:
                for ip,port in ip_port_list:
                    self.payloads.append((ip, port, user, pwd))

        config.logger.info("Generate {} payload (host_port_list:{}, user_pwd_list:{})".format(
            len(self.payloads), len(ip_port_list), len(user_pwd_list)))

    def com_ip_port(self):
        """得到host、port列表，返回格式: [(host1,<port1>),(host2,<port2>)]"""
        if self.ip_port_file:
            ip_port_line = get_content(self.ip_port_file)
            return [(ip_port.split(":")) for ip_port in ip_port_line]

        #确定 port
        if self.port:
            port = self.port
        else:
            port = service_port_dict.get(self.service_type)

        # 解析目标资产
        pt = ParseTarget()
        if self.ip:
            ip_list = pt.parse_target(self.ip)
        elif self.ip_file:
            target_list = get_content(self.ip_file)
            ip_list = pt.parse_target(target_list)

        ip_port_list = list()
        for ip in ip_list:
            if self.service_type == "oracle":
                sid = guess_sid(ip, port)
                if sid:
                    ip_port_list.append((ip,port,sid))
                else:
                    config.logger.error("{}:{} Can not guess the sid.".format(ip,port))
            else:
                ip_port_list.append((ip,port))

        return ip_port_list

    def com_user_pwd(self, user_pwd_file):
        """解析类似: admin:123456 这种格式的用户名密码文件，返回格式: [(<user1>,<pwd1>),(<user2>,<pwd2>)]"""
        user_pwd_list = list()
        content = get_content(user_pwd_file)
        for user_pwd in content:
            user,pwd = user_pwd.split(":")
            user_pwd_list.append((user,pwd))
        return user_pwd_list

    def com_users_pwds(self, user_file, pwd_file):
        """得到user、pwd列表，返回格式: [(<user1>,<pwd1>),(<user2>,<pwd1>)]"""
        user_pwd_list = list()
        user_list = get_content(user_file)
        pwd_list = get_content(pwd_file)
        for user in user_list:
            for pwd in pwd_list:
                pwd = pwd.replace("<user>",user)
                pwd = pwd.replace("<null>","")
                user_pwd_list.append((user,pwd))
        return user_pwd_list

    def com_users_pwd(self, user_file, pwd):
        """得到user、pwd列表，返回格式: [(<user1>,<pwd>),(<user2>,<pwd>)]"""
        user_pwd_list = list()
        user_list = get_content(user_file)
        for user in user_list:
            user_pwd_list.append((user,pwd))
        return user_pwd_list

    def com_user_pwds(self, user, pwd_file):
        """得到user、pwd列表，返回格式: [(<user>,<pwd1>),(<user>,<pwd2>)]"""
        user_pwd_list = list()
        pwd_list = get_content(pwd_file)
        for pwd in pwd_list:
            pwd = pwd.replace("<user>",user)
            pwd = pwd.replace("<null>","")
            user_pwd_list.append((user,pwd))
        # print(user_pwd_list)
        return user_pwd_list

    def com_user_pwdfile(self, user):
        """[(<user>,<pwd1>),(<user>,<pwd2>)]"""
        user_pwd_list = list()
        pwd_list = get_content(self.default_pwd_filename)
        for pwd in pwd_list:
            pwd = pwd.replace("<user>",user)
            pwd = pwd.replace("<null>","")
            user_pwd_list.append((user,pwd))
        return user_pwd_list

    def com_userfile_pwd(self, pwd):
        """[(<user1>,<pwd>),(<user2>,<pwd>)]"""
        user_pwd_list = list()
        user_list = get_content(self.default_user_filename)
        for user in user_list:
            user_pwd_list.append((user,pwd))
        return user_pwd_list

    def com_users_pwds_from_file(self):
        user_pwd_list = list()
        user_list = get_content(self.default_user_filename)
        pwd_list = get_content(self.default_pwd_filename)
        for user in user_list:
            for pwd in pwd_list:
                pwd = pwd.replace("<user>",user)
                pwd = pwd.replace("<null>","")
                user_pwd_list.append((user,pwd))
        return user_pwd_list

class MainBrute(object):
    """MainBrute"""
    def __init__(self, payloads):
        super(MainBrute, self).__init__()
        self.payloads = payloads
        self.timeout = config.timeout
        self.thread_num = config.thread_num
        self.service_type = config.service_type
        self.result = list()

    def hook_msg(self, msg, sid=""):
        try:
            status, host, port, user, pwd = msg
            if status:
                config.logger.error("[*] {}:{} {} {}".format(host, port, user, pwd))
                if self.service_type == "oracle":
                    self.result.append((host, port, user, pwd, sid))
                else:
                    self.result.append((host, port, user, pwd))
            else:
                config.logger.info("[-] {}:{} {} {}".format(host, port, user, pwd))
        except Exception as e:
            raise e
        else:
            pass

    def start_brute(self):
        "根据 service_type 加载对应的模块"
        # print(self.payloads)
        fname = self.service_type
        module = importlib.import_module("."+fname, package="rsbrute.brute")
        module.hook_msg = self.hook_msg

        brute = module.BruteForce(self.payloads, self.thread_num, self.timeout)
        brute.run()
