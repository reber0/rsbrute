#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-27 15:57:41
@LastEditTime : 2020-02-16 18:18:26
'''

try:
    from libs.utils import get_content
    from libs.parse import ParseTarget
    from config import dict_path
except ModuleNotFoundError:
    from Rsbrute.libs.utils import get_content
    from Rsbrute.libs.parse import ParseTarget
    from Rsbrute.config import dict_path

class ComHostPortUserPwd(object):
    """生成目标列表:[(host,port,user,pwd),(host,port,user,pwd)]"""
    def __init__(self, args):
        super(ComHostPortUserPwd, self).__init__()
        self.service_type   = args.get("service_type")
        self.host           = args.get("host")
        self.host_file      = args.get("host_file")
        self.port           = args.get("port")
        self.user_pwd_file  = args.get("user_pwd_file")
        self.user_file      = args.get("user_file")
        self.pwd_file       = args.get("pwd_file")
        self.user           = args.get("user")
        self.pwd            = args.get("pwd")

        self.default_user_filename = dict_path.joinpath("{}_user.txt".format(self.service_type))
        self.default_pwd_filename = dict_path.joinpath("{}_pwd.txt".format(self.service_type))

        self.hpup = list()
        self.p_s = {
            "ssh":22,"ftp":21,"telnet":23,"rlogin":513,
            "mysql":3306,"mssql":1433,"oracle":1521,"pgsql":5432,"redis":6379,"mongodb":27017,"memcache":11211,
            "ldap":389,"winrm":5985,"vnc":5901,"rdp":3389,"smb":445,"snmp":161,
            "smtp":25,"pop":110,
        }

    def generate(self):
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
            user_pwd_list = self.com_users_pwds_from_dict()

        for user,pwd in user_pwd_list:
            for host,port in self.com_host_port():
                self.hpup.append((host,port,user,pwd))

        return self.hpup

    def com_host_port(self):
        """得到host、port列表，返回格式: [(host1,<port>),(host2,<port>)]"""
        host_port_list = list()

        #确定 port
        if self.port:
            port = self.port
        else:
            port = self.p_s.get(self.service_type)

        #得到 hosts
        pt = ParseTarget()
        if self.host_file:
            target_list = get_content(self.host_file)
            host_list = pt.parse_target(target_list)
        elif self.host:
            host_list = pt.parse_target(self.host)

        for host in host_list:
            host_port_list.append((host,port))

        return host_port_list

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

    def com_users_pwds_from_dict(self):
        user_pwd_list = list()
        user_list = get_content(self.default_user_filename)
        pwd_list = get_content(self.default_pwd_filename)
        for user in user_list:
            for pwd in pwd_list:
                pwd = pwd.replace("<user>",user)
                pwd = pwd.replace("<null>","")
                user_pwd_list.append((user,pwd))
        return user_pwd_list
