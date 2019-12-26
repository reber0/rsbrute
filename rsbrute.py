#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:10:49
@LastEditTime: 2019-12-24 00:33:40
'''

import sys
sys.dont_write_bytecode = True  # 不生成pyc文件

from libs.parse import Parser
from libs.parse import CheckParames
from libs.core import ComHostPortUserPwd
from libs.module import LoadModule



def run():
    args = Parser().init()
    # print(args)

    ch = CheckParames(args)
    if ch.parames_is_right():
        #得到 payload [(ip,port,user,pwd), (ip,port,user,pwd)]
        chpup = ComHostPortUserPwd(args)
        hpup = chpup.generate()
        # print(hpup)

        # load 模块开始爆破
        lm = LoadModule(args)
        result = lm.start_brute(hpup)
        print(result)


if __name__ == "__main__":
    run()

        # target = {"host":'59.108.35.198',"service_type":'ssh',""}
        # chpup = ComHostPortUserPwd(args=target)