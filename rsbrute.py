#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:10:49
@LastEditTime : 2021-03-30 11:26:55
'''

import sys
sys.dont_write_bytecode = True  # 不生成pyc文件
import pathlib

def main():
    # 将 rsbrute 添加到 sys.path 里
    root_abspath = pathlib.Path(__file__).resolve()
    src_path = root_abspath.parent
    code_path = src_path.joinpath("rsbrute")
    # src_path = pathlib.Path("/Users/reber/Pentest/tools/Rsbrute")
    # code_path = src_path.joinpath("rsbrute")
    sys.path.insert(0, str(src_path))

    from rsbrute.libs.data import config
    config.src_path = src_path
    config.code_path = code_path

    from rsbrute.libs.initialize import init_logger
    from rsbrute.libs.initialize import init_options
    init_logger()
    init_options()

    config.logger.info("Start brute {} ...".format(config.service_type))

    from rsbrute import GeneratePayload
    gen_payload = GeneratePayload()
    gen_payload.run()
    payloads = gen_payload.payloads

    from rsbrute import MainBrute
    main_brute = MainBrute(payloads)
    main_brute.start_brute()
    result = main_brute.result

    print(result)

if __name__ == '__main__':
    main()
