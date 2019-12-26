#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime: 2019-10-14 15:24:54
'''

class OracleBruteForce(object):
    """OracleBruteForce"""
    def __init__(self, targets, thread_num, timeout):
        super(OracleBruteForce, self).__init__()
        self.targets = targets
        self.thread_num = thread_num
        self.timeout = timeout

    def worker(self,hpup):
        host,port,user,pwd = hpup
        try:
            conn = pymysql.connect(host=host,port=port,user=user,passwd=pwd,
                                connect_timeout=self.timeout,charset="utf8")
        except Exception as e:
            hook_msg((False,host,port,user,pwd))
            # logger.error(str(e))
        else:
            hook_msg((True,host,port,user,pwd))
        finally:
            conn.close()

    def run(self):
        print("Module OracleBruteForce is Developing...")
        # ip_list = [x[0] for x in self.result]
        # with ThreadPoolExecutor(max_workers = self.thread_num) as executor:
        #     for host,port,user,pwd in self.targets:
        #         f = executor.submit(self.worker,(host,port,user,pwd))


bruter = OracleBruteForce
