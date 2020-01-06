#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-12-14 15:06:54
@LastEditTime: 2019-12-26 14:55:36
'''

import pathlib


root_abspath = pathlib.Path(__file__).parent.resolve()  #绝对路径
module_path = root_abspath.joinpath("modules")
dict_path = root_abspath.joinpath("dict")
log_file_path = root_abspath.joinpath("log")

# log_level = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
log_level = "INFO"
