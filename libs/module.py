#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 23:57:35
@LastEditTime : 2020-02-16 18:30:36
'''

import time
import importlib

try:
    from libs.mylog import MyLog
    from config import log_file_path
    from config import log_level
except ModuleNotFoundError:
    from Rsbrute.libs.mylog import MyLog
    from Rsbrute.config import log_file_path
    from Rsbrute.config import log_level

log_file = log_file_path.joinpath("{}.log".format(time.strftime("%Y-%m-%d", time.localtime())))

class LoadModule(object):
    """LoadModule"""
    def __init__(self, args):
        super(LoadModule, self).__init__()
        self.service_type = args.get("service_type")
        self.thread_num   = args.get("thread_num")
        self.timeout      = args.get("timeout")
        self.logger = MyLog(loglevel=log_level, logger_name=self.service_type, logfile=log_file)

        self.result = list()
        self.modules = list()

    def hook_msg(self, msg):
        status,host,port,user,pwd = msg
        if status:
            self.logger.error("[*] {} {} {} {}".format(host, port, user, pwd))
            self.result.append((host, port, user, pwd))
        else:
            self.logger.info("[-] {} {} {} {}".format(host, port, user, pwd))

    def load_module(self):
        "根据 service_type 加载对应的模块"
        fname = self.service_type
        self.logger.info("Start brute {} ...".format(fname))
        try:
            module = importlib.import_module("."+fname, package="modules")
        except ModuleNotFoundError:
            module = importlib.import_module(".modules."+fname, package="Rsbrute")
        module.hook_msg = self.hook_msg

        return module.bruter
    
    def start_brute(self,hpup):
        bruter = self.load_module()
        bruter(hpup, self.thread_num, self.timeout).run()

        return self.result
