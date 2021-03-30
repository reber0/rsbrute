#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2020-09-23 15:55:43
@LastEditTime : 2021-03-30 11:30:59
'''
import sys
import pathlib
from loguru import logger

from .data import config
from .utils import file_is_exist
from .parse import ParserCmd


def init_logger():
    """
    初始化日志路径、字典路径
    """

    # 设置日志路径
    config.log_file_path = config.src_path.joinpath("log/runtime_{time:YYYY-MM-DD}.log")
    config.err_log_file_path = config.src_path.joinpath("log/err_{time:YYYY-MM-DD}.log")

    # 初始化日志
    logger.remove()
    logger_format1 = "[<green>{time:HH:mm:ss}</green>] <level>{message}</level>"
    logger_format2 = "<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    logger.add(sys.stdout, format=logger_format1, level="INFO")
    logger.add(config.log_file_path, format=logger_format2, level="INFO", rotation="10 MB", enqueue=True, encoding="utf-8", errors="ignore")
    # logger.add(config.log_file_path, format=logger_format2, level="INFO", rotation="00:00", enqueue=True, encoding="utf-8", errors="ignore")
    logger.add(config.err_log_file_path, rotation="10 MB", level="ERROR", enqueue=True, encoding="utf-8", errors="ignore")
    config.pop("log_file_path")
    config.pop("err_log_file_path")
    config.logger = logger

    # 设置字典路径
    config.dict_path = config.code_path.joinpath("dict")

def init_options():
    """
    初始化命令行参数
    检测给的参数是否正常、检查目标文件或字典是否存在
    """
    def check_file(filename):
        if not file_is_exist(filename):
            config.logger.error("No such file \"{}\"".format(filename))
            exit(0) 

    # 解析命令行参数
    args = ParserCmd().init()
    ip            = args.get("ip")
    ip_file       = args.get("ip_file")
    ip_port_file  = args.get("ip_port_file")
    user_file     = args.get("user_file")
    pwd_file      = args.get("pwd_file")
    user_pwd_file = args.get("user_pwd_file")

    if not (ip or ip_file or ip_port_file):
        config.logger.error("the arguments -i or -iL or -ip is required, please provide !")
        exit(0)

    if ip_file:
        check_file(ip_file)
    if ip_port_file:
        check_file(ip_port_file)
    if user_file:
        check_file(user_file)
    if pwd_file:
        check_file(pwd_file)
    if user_pwd_file:
        check_file(user_pwd_file)

    config.update(args)
