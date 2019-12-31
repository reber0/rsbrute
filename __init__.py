#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-24 00:02:57
@LastEditTime: 2019-12-31 16:56:55
'''

"""
usage:

    >>> from Rsbrute import ComHostPortUserPwd
    >>> from Rsbrute import LoadModule
    >>> chpup = ComHostPortUserPwd({"host":"59.108.35.198", "port":22, "service_type":"ssh"})
    >>> hpup = chpup.generate()

    >>> lm = LoadModule({"service_type":"ssh","timeout":10,"thread_num":50})
    >>> result = lm.start_brute(hpup)
"""

import sys
sys.dont_write_bytecode = True  # 不生成pyc文件

from .libs.core import ComHostPortUserPwd
from .libs.module import LoadModule

